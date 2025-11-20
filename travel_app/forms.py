from django import forms
import json
import os
from django.conf import settings

def load_country_data():
    path = os.path.join(settings.BASE_DIR, 'static','json_city', 'countries.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
    

class ContactForm(forms.Form):

    name=forms.CharField(max_length=100,required=True)
    email=forms.EmailField(required=True)
    subject=forms.CharField(max_length=150,required=True)
    message=forms.CharField(widget=forms.Textarea(attrs={"class":"resize-none",}),required=True)