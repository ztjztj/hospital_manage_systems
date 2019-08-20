from django.contrib import admin
from django.urls import path,include
from pay_money_place import views

urlpatterns = [
    path("", views.index, name="pay_money_place_index"),
    path("enter_index/", views.enter_index, name="enter_index"),
    path("outer_index/", views.outer_index, name="outer_index"),
    path("give_medicine_index/", views.give_medicine_index, name="give_medicine_index"),
    path("password/", views.pay_money_place_password, name="pay_money_place_password"),
    path("enter_add/", views.enter_add, name="enter_add"),
    path("outer_detail/<int:o_id>", views.outer_detail, name="outer_detail"),
    path("give_detail/<int:m_id>", views.give_detail, name="give_detail"),
    path("medicine_look/<int:m_id>", views.medicine_look, name="medicine_look"),
    path("give_medicine/<int:m_id>", views.give_medicine, name='give_medicine'),
    path('inquire/', views.inquire, name='inquire'),
    path('look/<int:l_id>', views.enter_look, name='look'),
    path('edit/<int:l_id>', views.enter_edit, name='edit'),
    path('add_many/<int:l_id>', views.enter_add_many, name='add_many'),
    path('updata_info/<int:l_id>', views.updata_info, name='updata_info'),
    path('cash_pledge/<int:l_id>', views.cash_pledge, name='cash_pledge'),
    path('close/<int:o_id>', views.close, name='close'),
    path('export_excel/', views.export_excel, name='export_excel'),
    path('export_excel_patient/', views.export_excel_patient, name='export_excel_patient'),
    path('query/', views.query, name='query'),
    path('export_detail/<int:o_id>', views.export_detail, name='export_detail'),
    path('hospitalization/', views.hospitalization, name='hospitalization'),
    path('del_patient/', views.del_patient, name='del_patient'),
    path('enter_del/', views.enter_del, name='enter_del'),
    path('outer_del/', views.outer_del, name='outer_del'),
]