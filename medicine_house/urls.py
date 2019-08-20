from django.contrib import admin
from django.urls import path, include
from medicine_house import views

urlpatterns = [
    path("", views.medicine_house_index, name="medicine_house_index"),
    path("medicine_house_index/", views.medicine_house, name="medicine_house"),
    path("export_excel/", views.export_excel, name="export_excel"),
    path("select_excel/<int:eid>", views.select_excel, name="select_excel"),
    path("medicine_house1/", views.medicine_house1.as_view(), name="medicine_house1"),
    path("new_medicine/", views.new_medicine.as_view(), name="new_medicine"),
    path("medicine_update/<int:mid>", views.medicine_update, name="medicine_update"),
    path("medicine_detail/<int:mid>", views.medicine_detail, name="medicine_detail"),
    path("medicine_house_password/", views.medicine_house_password, name="medicine_house_password"),
    path("medicine_insert/<int:mid>", views.medicine_insert, name="medicine_insert"),
    path("medicine_delete/", views.medicine_delete, name="medicine_delete"),
    path("medicine_delete1/", views.medicine_delete1, name="medicine_delete1"),
]
