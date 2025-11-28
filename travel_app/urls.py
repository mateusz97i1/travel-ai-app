from django.urls import path
from . import views

app_name= 'travel_app'

urlpatterns = [
    path('',views.home, name='home'),
    path('findmore',views.find_more_page,name='find_more'),
    path('aboutpage',views.about_page,name='about'),
    path('privacypolicy',views.privacy_policy,name='privacy_policy'),
    path('contactpage',views.contact_page,name='contact')

]