from django.contrib import admin
from django.urls import path, include
from registration import views

urlpatterns = [
    path("", views.index, name="regist_index"),
    path("registration_index/", views.registration_index, name="registration_index"),
    path("registration_add/", views.registration_add, name="registration_add"),
    path("patient_look/<int:patient_id>", views.patient_look, name="patient_look"),
    path("doctor_look/<int:doctor_id>", views.doctor_look, name="doctor_look"),
    path("patient_exit/", views.patient_exit, name="patient_exit"),
    path("patients_exit/", views.patients_exit, name="patients_exit"),
    path("patient_keyword/", views.patient_keyword, name="patient_keyword"),
    path("doctor_keyword/", views.doctor_keyword, name="doctor_keyword"),
    path("registration_password/", views.registration_password, name="registration_password"),
    path("to_excel/", views.to_excel, name="to_excel")
]
