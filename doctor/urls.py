from django.contrib import admin
from django.urls import path, include
from doctor import views

urlpatterns = [
    path("", views.index, name="doctor_index"),  # 主页
    path("find_0/", views.find_0, name="find_0"),  # 查询信息植入sission
    path("query/", views.query, name="query"),  # 查询页
    path("patient_list/", views.patient_list, name="patient_list"),  # 所有 病例打印，并分页
    path("patient_list_1/<str:ids>", views.patient_list_1, name="patient_list_1"),  # 指定病例的打印并分页
    path("detail/<int:ids>", views.detail, name="detail"),  # 病例详情页
    path("dispensing/<int:ids>", views.dispensing, name="dispensing"),  # 开药界面
    path("medicine_one_add/<int:ids>", views.Medicine_one_add, name="medicine_one_add"),  # 药方加药
    path("delete_yaofang/<str:ids>", views.delete_yaofan, name="delete_yaofang"),  # 药方删药
    path("hospital/<str:ids>", views.hospital, name="hospital"),  # 住院办理
    path("save_excle/<int:ids>", views.save_excle, name="save_excle"),  # 药方输出save_excle
    path("submit/<int:ids>", views.submit, name="submit"),  # 开药结束并提交
    path("doctor_password/", views.doctor_password, name="doctor_password"),  # 密码管理
]
