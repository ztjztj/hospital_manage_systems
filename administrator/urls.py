from django.contrib import admin
from django.urls import path, include
from administrator import views

urlpatterns = [
    path('', views.administrator_index, name="administrator_index"),
    path("doctor_manage/", views.doctor_manage, name="doctor_manage"),
    path("user_manage/", views.user_manage, name="user_manage"),
    path("password/", views.administrator_password, name="administrator_password"),
    path("user_manage_add/", views.user_manage_add, name="user_manage_add"),
    path("doctor_manage_add/", views.doctor_manage_add, name="doctor_manage_add"),
    path("doctor_manage_edit/<int:user_id>", views.doctor_manage_edit, name="doctor_manage_edit"),
    path("doctor_manage_look/<int:user_id>", views.doctor_manage_look, name="doctor_manage_look"),
    path('doctor_manage_type_look/<int:id>',views.doctor_manage_type_look,name='doctor_manage_type_look'), #医生分科室显示信息
    # 自己添加
    path('user_start_use/<int:user_id>', views.user_start_use, name='user_start_use'),  # 启用用户
    path('user_stop_use/<int:user_id>', views.user_stop_use, name='user_stop_use'),  # 禁用用户
    path('doctor_start_use/<int:user_id>', views.doctor_start_use, name='doctor_start_use'),  # 启用医生
    path('doctor_stop_use/<int:user_id>', views.doctor_stop_use, name='doctor_stop_use'),  # 禁用医生
    path('start_and_stop/', views.start_and_stop, name='start_and_stop'),  # 用户的启用与禁用
    path('start_and_stop_detail/<int:num>', views.start_and_stop_detail, name='start_and_stop_detail'),  # 用户的启用与禁用

    path('doctor_manage_look_excel/<int:user_id>', views.doctor_manage_look_excel, name='doctor_manage_look_excel'),
    # 门诊医生管理：导出Excel

    path('doctor_manage_del/<int:user_id>', views.doctor_manage_del, name='doctor_manage_del'),  # 门诊医生管理：删除
    path('doctor_manage_del_box/', views.doctor_manage_del_box, name='doctor_manage_del_box'),  # 当选中用户时，删除用户
    # path('doctor_manage_search_save/', views.doctor_manage_search_save, name='doctor_manage_search_save'),  # 门诊医生管理：搜索(保存用户输入的内容)
    path('doctor_manage_search/', views.doctor_manage_search, name='doctor_manage_search'),  # 门诊医生管理：搜索

    path('user_manage_search/', views.user_manage_search, name='user_manage_search'),  # 门诊医生管理：搜索

    path('user_manage_look_excel/<int:user_id>', views.user_manage_look_excel, name='user_manage_look_excel'),
    # 门诊医生管理：导出Excel
    path('user_manage_type_look/<int:id>',views.user_manage_type_look,name='user_manage_type_look'), #医生分科室显示信息

    path('user_manage_look/<int:user_id>', views.user_manage_look, name='user_manage_look'),  # 用户管理:查看

    path('user_manage_edit/<int:user_id>', views.user_manage_edit, name='user_manage_edit'),  # 用户管理:修改
    path('user_manage_del/<int:user_id>', views.user_manage_del, name='user_manage_del'),  # 用户管理:删除

]
