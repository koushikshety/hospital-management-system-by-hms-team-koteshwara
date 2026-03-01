
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url
from .views import *
from . import views
from django.urls import path
from django.views.generic.base import TemplateView


urlpatterns = [
    # here are basic and important urls
    path("",TemplateView.as_view(template_name='index.html'), name='index'),
    # path("",TemplateView.as_view(template_name='ok.html'), name='index'),
    path('admin/', admin.site.urls),
    path('main', views.main, name='main'),
    path('base', views.BASE, name='base'),
    # here comes the login,sing up and logout urls
    path("accounts/",include("django.contrib.auth.urls")),
    path('accounts/sign_up', views.signup_view, name='signup_view'),
    path('logout/', views.logout_view, name='logout'),
    # here comes indivisual urls
    path('terms', views.TERMS, name='terms'),
    path('about', views.ABOUT, name='about'),
    path('profile', views.profile, name='profile'),
    # here comes the patients urls
    path('Patient/add', views.ADD_PATIENT, name='add_patient'),
    path('Patient/all', views.ALL_PATIENT, name='all_patients'),
    path('Patient/about', views.about, name='Patient_detail1'),
    path('p_update/<int:id>/', views.p_update, name='p_update'),
    # here comes the doctor urls
    path('Doctors/add', views.ADD_DOCTOR, name='add_doctor'),
    path('Doctors/all', views.all_doctor, name='all_doctor'),
    path('Doctors/about', views.about_doctor, name='doctor_detail1'),
    path('edit_doctor/<int:id>/', views.edit_doctor, name='edit_doctor'),

    # here comes appointment urls 
    path('Appointments/add', views.add_appoint, name='add_appointment'),
    path('Appointments/all', views.all_appoint, name='all_appointment'),
    path('Appointments/about', views.about_appoint, name='appointment_details1'),
    path('edit_appoint/<int:id>', views.edit_appoint, name='edit_appoint'),

    # name here latter
    path('p_about/<int:id>', views.PATIENT_DETAILS, name='p_about'),
    path('d_about/<int:id>', views.DOCTOR_DETAILS, name='d_about'),
    path('a_about/<int:id>', views.APPOINT_DETAILS, name='a_about'),


    #write it after 
    path('delete/<int:id>', views.delete, name='delete1'),
    path('delete2/<int:id>',views.delete2,name='delete02'),
    path('deleteappoint/<int:id>', views.deleteapp, name='deleteapp'),
    path('deletepay/<int:id>', views.deletepay, name='deletepay'),
    path('deleteroom/<int:id>',views.deleteroom,name='deleteroom'),
    
    #payments urls
    path('Payments/add', views.add_payment, name='add_payment'),
    path('Payments/all', views.all_payment, name='all_payment'),
    path('edit_Payments/<int:id>', views.edit_payment, name='edit_payment'),
    # path('Payment/invoice/<str:pp_id>', views.invoice, name='invoice'),
    path('Payment/invoice2/<int:id>', views.invoice2, name='invoice2'),



    #Room urls
    path('Room/add', views.add_room, name='add_room'),
    path('Room/all', views.all_room, name='all_room'),
    path('edit_Room/<int:id>', views.edit_room, name='edit_room'),

    # Resource pages
    path('Resource/map', views.map, name='map'),
    # path('Resource/typo', views.typography, name='typo'),
    path('Resource/form',views.form, name='form'),
    path('new_doctor_application/', views.new_doctor_application, name='new_doctor_application'),
    path('application/', views.application, name='application'),
    path('contract-form/', views.contract_form, name='contract_form'),



    #other pages
    path('Other-pages/faq', views.faq, name='faq'),
    path('Other-pages/subscription', views.sub, name='sub'),
    path('Other-pages/BloodDonner', views.bd, name='blooddonner'),
    path('Other-pages/schedule',views.schedule,name='schedule'),
    

]

