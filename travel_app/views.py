from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
import json
import os
from.forms import load_country_data,ContactForm
from dotenv import load_dotenv
import openai
import markdown2
from xhtml2pdf import pisa
import io
load_dotenv()


MODEL_GPT = 'gpt-4o-mini'
api_key=os.getenv('OPENAI_API_KEY')

# Create your views here.
def home(request):
    return render(request,'home.html')


def find_more_page(request):
    name = load_country_data()
    vacation_time_span = [
        '1 day',
        'weekend',
        '1-3 days',
        '4-6 days',
        '1 week',
        '2 weeks'
    ]
    system_prompt = ' '
    rendered_result_html = ' '
    selected_country = request.POST.get('country')
    selected_city = request.POST.get('city')
    selected_time_span = request.POST.get('time_span')


    if request.method == "POST":
        system_prompt += 'You are a professional trip planner'
        system_prompt += f"You are given this city, country and time span"
        system_prompt += 'make a professional visit plan for this destination. '
        system_prompt += 'Plan needs to include breaks for food(recommend restaurants), mandatory places to see and hotels to rest'
        system_prompt += 'estimate whole price for the trip in $'
        system_prompt += 'provide all links for all offers'

        response = openai.chat.completions.create(
            model=MODEL_GPT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{selected_city}, {selected_country}, {selected_time_span}"}
            ],
        )

        raw_result_markdown = response.choices[0].message.content
        rendered_result_html = markdown2.markdown(raw_result_markdown)


        if request.method=="POST":
            if 'save_pdf' in request.POST:

                rendered_html = request.POST.get('rendered_result_html', '')
                print("SAVE PDF CLICKED")

                # Tworzymy HttpResponse z PDF
                response = HttpResponse(content_type="application/pdf")
                response['Content-Disposition'] = 'attachment; filename="travel_plan.pdf"'

                # Konwersja HTML do PDF
                pisa_status = pisa.CreatePDF(io.StringIO(rendered_html), dest=response)

                # Sprawdzenie błędów
                if pisa_status.err:
                    return HttpResponse("Coś poszło nie tak podczas generowania PDF", status=500)

                return response
                

        # Wykrywaj AJAX i zwróć tylko część szablonu
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Zmieniamy to, aby renderować cały fragment HTML, który chcesz wstawić do stopki
            # W tym celu, najlepiej stworzyć osobny, mały szablon, np. 'plan_content.html'
            return render(request, 'plan_content.html', {
                'rendered_result_html': rendered_result_html
            })
        
        
                

    return render(request, 'find_more.html', {
        'name': name,
        'vacation_time_span': vacation_time_span,
        'selected_country': selected_country,
        'selected_city': selected_city,
        'selected_time_span': selected_time_span,
        "rendered_result_html": rendered_result_html,
    })

def about_page(request):

    return render(request, 'about.html')

def contact_page(request):
    form=ContactForm
    if request.method=="POST":
        if 'send_email' in request.POST:
            form=ContactForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data["name"]
                email = form.cleaned_data["email"]
                subject = form.cleaned_data["subject"]
                message = form.cleaned_data["message"]

                full_message = f"Message from {name} ({email}):\n\n{message}"

                send_mail(
                    subject,
                    full_message,
                    email,
                    ["supporttravelai@gmail.com"],
                )
                messages.success(request, "Your message has been sent successfully!")
                return redirect('contact.html')
    system_prompt = ' '
    raw_result_markdown = ''   
    question_chat = request.POST.get('question_chat')

    if request.method=="POST":
        if 'send_message' in request.POST:

            system_prompt += 'You are a professional worker in support center'
            system_prompt += "Answer on every given question, be helpfull"


            response = openai.chat.completions.create(
                model=MODEL_GPT,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"{question_chat}"}
                ],
            )

            raw_result_markdown = response.choices[0].message.content

    # Sprawdzenie, czy żądanie jest z HTMX
    if request.headers.get('HX-Request') == 'true':
        # Jeśli tak, zwracamy tylko fragment czatu.
        # WAŻNE: W tym przypadku widok ZAWSZE zwraca cały blok <div id="chat-container">...</div>
        # Używamy szablonu chatbox_only.html, który zawiera tylko ten fragment.
        return render(request, 'chatbox_only.html',
                      {'form':form,
                    'answer_chat':raw_result_markdown,
                    'question_chat':question_chat,
                                          
                    })
     
        

    return render(request,'contact.html'
                  ,{'form':form,
                    'answer_chat':raw_result_markdown,
                                          
                    })

