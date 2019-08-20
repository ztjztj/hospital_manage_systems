from django import forms
from registration.models import *
from django.core import validators
import re


class UserForm(forms.ModelForm):
    # user_number = forms.CharField(validators=[validators.MaxLengthValidator(16,message='最大长度为16'),validators.MinLengthValidator(11,'最小长度为11'),validators.RegexValidator('^[a-zA-Z][a-zA-Z0-9_]{10,15}$')])
    # user_number = forms.IntegerField(max_value=16,min_value=11,error_messages={"max_value":"最大长度16","min_value":"最小长度11"})
    # user_password = forms.CharField(validators=[validators.MaxLengthValidator(18,message='最大长度18'),validators.MinLengthValidator(6,message='最小长度为6'),validators.RegexValidator('^[a-zA-Z]\w{5,17}$')])
    user_password2 = forms.CharField(max_length=18, min_length=6)

    # user_card = forms.CharField(validators=[validators.MaxLengthValidator(18,),validators.MinLengthValidator(18,),validators.RegexValidator('^\d{18}$')])
    # user_role = forms.CharField(validators=[validators.MaxLengthValidator(4,),validators.MinLengthValidator(2,),validators.RegexValidator('^[\u4e00-\u9fa5]{0,}$')])
    # doctor_belong = forms.CharField(validators=[validators.MaxLengthValidator(6, ), validators.MinLengthValidator(2, ),validators.RegexValidator('^[\u4e00-\u9fa5]{0,}$')])

    class Meta:

        model = UserInfo
        fields = ['user_number', 'user_card', 'user_password', 'user_phone']

    def clean_user_password(self):
        password = self.cleaned_data.get("user_password")
        if re.match('^[a-zA-Z]\w{5,17}$', password):
            return password

    def clean_user_number(self):
        number = self.cleaned_data.get('user_number')
        if re.match('^[a-zA-Z][a-zA-Z0-9_]{,10}$', number):
            if UserInfo.objects.filter(user_name=number).exists():
                raise forms.ValidationError('该用户名已存在')
            else:
                return number

    def clean(self):
        pwd = self.cleaned_data.get('user_password')
        pwd2 = self.cleaned_data.get('user_password2')
        if pwd != pwd2:
            raise forms.ValidationError('两次输入的密码不一致')

    def clean_user_card(self):
        card = self.cleaned_data.get('user_card')
        if re.match('^\d{18}$', card):
            if UserInfo.objects.filter(user_card=card).exists():
                raise forms.ValidationError('此身份证已存在')
            else:
                return card

    def clean_user_phone(self):
        phone = self.cleaned_data.get('user_phone')
        if re.match('1[345678]\d{9}', phone):
            if UserInfo.objects.filter(user_phone=phone).exists():
                raise forms.ValidationError('该手机号已存在')
            else:
                return phone


class UsertwoForm(forms.ModelForm):
    # user_name = forms.CharField(validators=[validators.MaxLengthValidator(10,message='最大长度为10'),validators.MinLengthValidator(2,message='最小长度为2'),validators.RegexValidator("\w+")])
    # user_age = forms.CharField(validators=[validators.MaxValueValidator(60,message='最大年龄为60'),validators.MinValueValidator(18,message='最小年龄为18'),validators.RegexValidator('^[0-9]*$')])
    # user_gender = forms.CharField(validators=[validators.MaxLengthValidator(1,),validators.MinLengthValidator(1,),validators.RegexValidator('^[\u4e00-\u9fa5]{0,}$')])  # 用户性别
    # user_level = forms.CharField(validators=[validators.MaxLengthValidator(5,),validators.MinLengthValidator(2,),validators.RegexValidator('^[\u4e00-\u9fa5]{0,}$')])  # 用户学历
    # user_phone = forms.IntegerField(validators=[validators.RegexValidator("1[345678]\d{9}",message='请输入正确格式的手机号码')])
    # user_email = forms.EmailField(validators=[validators.EmailValidator(message='请输入正确的邮箱格式')])

    class Meta:

        model = UserInfo
        exclude = ['user_number', 'user_card', 'user_password', 'user_role', 'doctor_belong', 'user_phone','user_status']

    def clean_user_name(self):
        name = self.cleaned_data.get('user_name')
        if re.match('^[\u4e00-\u9fa5]{0,}$', name):
            return name

        else:
                raise forms.ValidationError('只能注册汉字')



    def clean_user_age(self):
        age = self.cleaned_data.get('user_age')
        if re.match('^[0-9]*$', age):
            return age
        else:
            raise forms.ValidationError('年龄只能填写数字')

    def clean_user_gender(self):
        gender = self.cleaned_data.get('user_gender')
        if gender == "男":
            return gender
        elif gender == "女":
            return gender
        else:
            raise forms.ValidationError('填写内容不合法，只能输入男或女！')

    def clean_user_level(self):
        level = self.cleaned_data.get('user_level')
        if re.match('^[\u4e00-\u9fa5]{0,5}$', level):

                return level
        else:
            raise forms.ValidationError('填写内容不符合格式')


    def clean_user_email(self):
        email = self.cleaned_data.get('user_email')
        if re.match('^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', email):
            if UserInfo.objects.filter(user_email=email).exists():
                raise forms.ValidationError('邮箱格式不正确')
            else:
                return email




