from django.contrib import admin
from django.urls import path, include
from login_register import views

urlpatterns = [
    path('', views.Login, name="login"),
    path('register/', views.Register.as_view(), name='register'),
    path('generate_code/', views.generate_code, name='vcode'),
    path('get_phone_code/', views.get_phone_code, name="get_phone_code"),
    path("profession/", views.profession, name="profession"),
    path("username_is/", views.username_is, name="username_is"),
    path("usernum_is/", views.usernum_is, name="usernum_is"),
    path("identity_is/", views.identity_is, name="identity_is"),
    path("phone_is/", views.phone_is, name="phone_is"),
    path("yzm_is/", views.yzm_is, name="yzm_is"),
]
