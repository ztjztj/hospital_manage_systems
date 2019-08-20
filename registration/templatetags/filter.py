from django import template
from registration.models import UserInfo, Doctor

register = template.Library()


def doctors(depart_id):
    doctors = UserInfo.objects.filter(doctor_belong_id=depart_id)
    print(doctors)
    return doctors


register.filter("doctors", doctors)


def depart_doctors(depart_id):
    depart_doctors = Doctor.objects.filter(fk_doctor_user__doctor_belong_id=depart_id)
    return depart_doctors


register.filter("depart_doctors", depart_doctors)


def doctors_count(depart_id):
    doctors_count = UserInfo.objects.filter(doctor_belong_id=depart_id).count() + 1
    return doctors_count


register.filter("doctors_count", doctors_count)


