from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from registration.models import *
from django.db.models import Q
import re
import openpyxl
from django.core.paginator import Paginator


# 首页
def index(request):
    return render(request, 'registration/index.html')


# 挂号的首页（包含医生与病人）
def registration_index(request):
    patients = PatientOne.objects.all()
    doctors = Doctor.objects.all()
    departs = Department.objects.all()
    limit = 5
    paginator = Paginator(patients, limit)
    page = request.GET.get("page", "1")
    patients = paginator.page(page)
    return render(request, 'registration/registration_index.html',
                  {"doctors": doctors, 'patients': patients, "departs": departs})


def to_excel(request):
    patients = PatientOne.objects.all()
    content = [["病人编号", "病人姓名", "病人性别", "挂号科室", "主治医生", "挂号时间"]]
    for patient in patients:
        content.append([patient.id, patient.patient_name, patient.patient_sex, patient.fk_patient_depart.depart_name,
                        patient.fk_patient_doctor.fk_doctor_user.user_name, patient.patient_registed_time])
    print(content)
    f = openpyxl.Workbook()
    d = f.active
    d.title = '挂号情况'
    for i in range(0, len(content)):
        for j in range(0, len(content[i])):
            d.cell(i + 1, j + 1, str(content[i][j]))
    f.save(r'a.xlsx')
    f = open(r'a.xlsx', 'rb')
    h = HttpResponse()
    h.content = f
    h['Content-TYpe'] = "application/octet-stream"
    h['Content-Disposition'] = 'attachment;filename="a.xlsx"'
    return h


# 添加挂号
def registration_add(request):
    if request.method == "GET":
        departs = Department.objects.all()
        doctors = UserInfo.objects.filter(doctor_belong__depart_name='外科')
        return render(request, 'registration/registration_add.html', {"departs": departs, "doctors": doctors})
    else:
        n_type = request.POST.get("type")
        if n_type == "姓名":
            n = request.POST.get("n")
            if n == "":
                msg = "<p>用户名不能为空</p>"
                return JsonResponse({"status": 0, "msg": msg})
            else:
                return JsonResponse({"status": 1})

        elif n_type == "年龄":
            n = request.POST.get("n")
            if n == "":
                msg = "<p>年龄不能为空</p>"
                return JsonResponse({"status": 0, "msg": msg})
            elif 0 < int(n) < 150 or not int(n):
                return JsonResponse({"status": 1})
            else:
                msg = "<p>年龄不合法</p>"
                return JsonResponse({"status": 0, "msg": msg})

        elif n_type == "性别":
            n = request.POST.get("n")
            if n:
                return JsonResponse({"status": 1})
            else:
                msg = "<p>性别不合法</p>"
                return JsonResponse({"status": 0, "msg": msg})

        elif n_type == "身份证号":
            n = request.POST.get("n")
            if n == "":
                msg = "<p>身份证号不能为空</p>"
                return JsonResponse({"status": 0, "msg": msg})
            elif PatientOne.objects.filter(patient_card=n).exists():
                msg = "<p>该身份证号已挂号</p>"
                return JsonResponse({"status": 0, "msg": msg})
            elif len(n) != 18 or not int(n):
                msg = "<p>身份证号不合法</p>"
                return JsonResponse({"status": 0, "msg": msg})
            else:
                return JsonResponse({"status": 1})

        elif n_type == "手机号":
            n = request.POST.get("n")
            if n == "":
                msg = "<p>手机号不能为空</p>"
                return JsonResponse({"status": 0, "msg": msg})
            elif PatientOne.objects.filter(patient_phone=n).exists():
                msg = "<p>该手机号已挂号</p>"
                return JsonResponse({"status": 0, "msg": msg})
            elif len(n) != 11:
                msg = "<p>手机号长度为11位</p>"
                return JsonResponse({"status": 0, "msg": msg})
            elif not re.match(r'1[34578]\d{9}', n) or not int(n):
                msg = "<p>手机号不合法</p>"
                return JsonResponse({"status": 0, "msg": msg})
            else:
                return JsonResponse({"status": 1})

        elif n_type == "症状":
            n = request.POST.get("n")
            if n == "":
                msg = "<p>症状不能为空</p>"
                return JsonResponse({"status": 0, "msg": msg})
            else:
                return JsonResponse({"status": 1})

        elif n_type == "过敏史":
            n = request.POST.get("n")
            if n == "":
                msg = "<p>过敏史不能为空</p>"
                return JsonResponse({"status": 0, "msg": msg})
            else:
                return JsonResponse({"status": 1})

        elif n_type == "科室":
            depart_id = request.POST.getlist("n")[0]
            doctors = list(UserInfo.objects.filter(doctor_belong__id=depart_id).values_list('user_name', flat=True))
            return JsonResponse({"status": 2, "depart_id": depart_id, "doctors": doctors})

        else:
            patient_name = request.POST.get("patient_name")
            patient_age = request.POST.get("patient_age")
            patient_sex = request.POST.get("patient_sex")
            patient_phone = request.POST.get("patient_phone")
            patient_card = request.POST.get("patient_card")
            patient_status = request.POST.get("patient_status")
            patient_history = request.POST.get("patient_history")
            patient_depart = request.POST.getlist("patient_depart")[0]
            patient_depart = Department.objects.get(id=patient_depart).id
            patient_main_doctor = request.POST.getlist("patient_main_doctor")[0]
            patient_main_doctor = UserInfo.objects.get(user_name=patient_main_doctor).id
            patient_main_doctor = Doctor.objects.get(fk_doctor_user_id=patient_main_doctor).id

            PatientOne.objects.create(patient_name=patient_name,
                                      patient_age=patient_age,
                                      patient_card=patient_card,
                                      patient_history=patient_history,
                                      patient_status=patient_status,
                                      patient_sex=patient_sex,
                                      patient_phone=patient_phone,
                                      fk_patient_doctor_id=patient_main_doctor,
                                      fk_patient_depart_id=patient_depart)
            doctor = Doctor.objects.get(id=patient_main_doctor)
            if doctor.doctor_status == "空闲中":
                doctor.doctor_status = "挂号中"
                doctor.waiting_number = doctor.waiting_number + 1
                doctor.save()
            else:
                doctor.waiting_number = doctor.waiting_number + 1
                doctor.save()
            return redirect('registration_index')


# 病人详情
def patient_look(request, patient_id):
    patient = PatientOne.objects.get(id=patient_id)
    return render(request, 'registration/patient_look.html', {"patient": patient})


# 医生详情
def doctor_look(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'registration/doctor_look.html', {"doctor": doctor})


# 病人退号
def patient_exit(request):
    patient_id = request.POST.get("patient_id")
    patient = PatientOne.objects.get(id=patient_id)
    patient.delete()
    doctor_id = UserInfo.objects.get(id=patient.fk_patient_doctor_id).id
    doctor = Doctor.objects.get(fk_doctor_user_id=doctor_id)
    doctor.waiting_number -= 1
    doctor.save()
    return JsonResponse({"patient_id": patient_id})


# 病人关键字查询
def patient_keyword(request):
    keyword = request.GET.get("patient_keyword")
    print(keyword)
    if keyword == "":
        msg = "不能为空!"
        patients = PatientOne.objects.all()
        doctors = Doctor.objects.all()
        departs = Department.objects.all()
        limit = 5
        paginator = Paginator(patients, limit)
        page = request.GET.get("page", "1")
        patients = paginator.page(page)
        return render(request, 'registration/registration_index.html',
                      {"patient_msg": msg, "patients": patients, "doctors": doctors, "departs": departs,
                       "keyword": keyword})
    elif PatientOne.objects.filter(Q(patient_name=keyword) | Q(id__contains=keyword)).exists():
        patients = PatientOne.objects.filter(Q(patient_name=keyword) | Q(id__iexact=keyword))
        doctors = Doctor.objects.all()
        departs = Department.objects.all()
        limit = 5
        paginator = Paginator(patients, limit)
        page = request.GET.get("page", "1")
        patients = paginator.page(page)
        return render(request, 'registration/registration_index.html',
                      {"patients": patients, "doctors": doctors, "departs": departs})
    else:
        msg = "数据不符合查询条件!"
        patients = PatientOne.objects.all()
        doctors = Doctor.objects.all()
        departs = Department.objects.all()
        limit = 5
        paginator = Paginator(patients, limit)
        page = request.GET.get("page", "1")
        patients = paginator.page(page)
        return render(request, 'registration/registration_index.html',
                      {"patient_msg": msg, "patients": patients, "doctors": doctors, "departs": departs})


# 医生关键字查询
def doctor_keyword(request):
    keyword = request.POST.get("doctor_keyword")
    if keyword == "":
        msg = "不能为空!"
        patients = PatientOne.objects.all()
        doctors = Doctor.objects.all()
        departs = Department.objects.all()
        return render(request, 'registration/registration_index.html',
                      {"doctor_msg": msg, "patients": patients, "doctors": doctors, "departs": departs})
    elif UserInfo.objects.filter(
            Q(user_name=keyword) | Q(id__contains=keyword) | Q(doctor_belong__depart_name=keyword) | Q(
                doctor__doctor_status=keyword)):
        doctors = Doctor.objects.filter(
            Q(fk_doctor_user__user_name=keyword) | Q(fk_doctor_user__id__contains=keyword) | Q(
                fk_doctor_user__doctor_belong__depart_name=keyword) | Q(doctor_status=keyword))
        departs = doctors.values_list('fk_doctor_user__doctor_belong__depart_name').distinct()
        departs = [i[0] for i in list(departs)]
        count = len(departs) + 1
        patients = PatientOne.objects.all()
        return render(request, 'registration/registration_index2.html',
                      {"patients": patients, "doctors": doctors, "departs": departs, "count": count})
    else:
        msg = "数据不符合查询条件!"
        patients = PatientOne.objects.all()
        doctors = Doctor.objects.all()
        departs = Department.objects.all()
        return render(request, 'registration/registration_index.html',
                      {"doctor_msg": msg, "patients": patients, "doctors": doctors, "departs": departs})


def patients_exit(request):
    id_list = request.POST.getlist("id_list")
    id_list = id_list[0].split(",")
    PatientOne.objects.filter(id__in=id_list).delete()
    return JsonResponse({"id_list": id_list})


# 修改密码
def registration_password(request):
    u = request.session.get("u_id")
    if request.method == "GET":
        return render(request, 'registration/registration_password.html')
    else:
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password2 = request.POST.get("new_password2")
        if UserInfo.objects.get(id=u.id).user_password == old_password:
            user = UserInfo.objects.get(id=u.id)
            if new_password == new_password2:
                user.user_password = new_password2
                user.save()
                login_msg = "请重新登录"
                return JsonResponse({"status": "success", "login_msg": login_msg})
            else:
                password_msg = "密码输入不不正确"
                return JsonResponse({"status": "error_msg", "password_msg": password_msg})
        else:
            error_msg = "密码错误"
            return JsonResponse({"status": "not_exits", "error_msg": error_msg})
