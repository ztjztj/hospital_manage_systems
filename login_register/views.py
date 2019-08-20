from django.shortcuts import render, redirect, HttpResponse, reverse
from django import views, forms
from django.views.decorators.csrf import csrf_exempt
from login_register.forms import *
import time, random
from django.http import JsonResponse


def Login(request):
    if request.method == "GET":
        return render(request, 'login_register/login.html', {'wzp': id})
    else:
        # 获取用户输入的验证码
        vcode_input = request.POST.get('vcode')
        # 获取session中存储的验证码
        vcode_session = request.session.get('verifycode')
        # 进行验证码的校验
        if vcode_input != vcode_session:
            # 验证码错误
            return render(request, 'login_register/login.html', {'code_error': '验证码错误'})
        name = request.POST.get('user_number')
        pwd = request.POST.get('user_pwd')
        try:
            user_one = UserInfo.objects.get(user_number=name, user_password=pwd)
        except UserInfo.DoesNotExist:
            return render(request, "login_register/login.html", {"cuo_wu": "该账号不存在"})
        if user_one.user_status == "禁用":
            return render(request, "login_register/login.html", {"cuo_wu": "该账号未启用"})
        if user_one.user_password == pwd:
            request.session['u_id'] = user_one.user_name
            request.session.set_expiry(0)
            a = request.session.get("u_id")
            if user_one.user_role_id == 1:
                return redirect(reverse("medicine_house_index"))
            elif user_one.user_role_id == 2:
                return redirect(reverse('regist_index'))
            elif user_one.user_role_id == 3:
                return redirect(reverse('pay_money_place_index'))
            elif user_one.user_role_id == 4:
                doctor_id = Doctor.objects.get(fk_doctor_user_id=user_one.id)
                request.session['doctor_id'] = doctor_id.id
                return redirect(reverse('doctor_index'))
            elif user_one.user_role_id == 5:
                return redirect(reverse('administrator_index'))
            else:
                return render(request, "login_register/login.html", {"cuo_wu": "请确认是否入职"})
        else:
            return render(request, 'login_register/login.html')


class Register(views.View):

    def get(self, request):
        depart = Department.objects.all()
        role = Role.objects.all()
        return render(request, 'login_register/register.html', {"depart": depart, "role": role})

    def post(self, request):
        nickname = request.POST.get('nickName')
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        education = request.POST.get('education')
        identity = request.POST.get('identity')
        phone = request.POST.get('phone')
        pwd = request.POST.get('pwd')
        nicknum = request.POST.get('nicknum')
        user_role = request.POST.get('user_role')
        doctor_belong = request.POST.get('doctor_belong')
        if user_role == '4':
            info = UserInfo.objects.create(user_number=nicknum, user_name=nickname, user_age=age, user_gender=sex,
                                           user_level=education,
                                           user_card=identity, user_phone=phone, user_password=pwd,
                                           user_role_id=user_role,
                                           doctor_belong_id=doctor_belong)
            Doctor.objects.create(fk_doctor_user_id=info.id)
        else:
            UserInfo.objects.create(user_number=nicknum, user_name=nickname, user_age=age, user_gender=sex,
                                    user_level=education,
                                    user_card=identity, user_phone=phone, user_password=pwd, user_role_id=user_role)
        return render(request, 'login_register/login.html')


# 图片验证码
from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO


def generate_code(request):
    """
    生成验证码
    :param request:
    :return:
    """
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100  # 验证码图片的宽度
    height = 25  # 验证码图片的高度
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)  # 实例化图片对象并指定宽高和背景颜色
    # 创建画笔对象
    draw = ImageDraw.Draw(im)  # 基于im对象得到画笔对象
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        # (2,5)
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)  # 使用画笔画噪点并指定噪点的颜色

    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    # 得到四位验证码
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]

    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('login_register/FreeMono.ttf', 23)
    # 构造字体颜色.
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


# 手机验证码
from login_register.phone_sys.phone_sys import *
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt  # 使用ajax发送post请求时必须使用的装饰器
def get_phone_code(request):
    """
    获取手机验证码
    :param request:
    :return:
    """
    phone = request.POST.get('phone')  # 得到手机号码
    # 1.得到生成的验证码
    phone_code = get_code(alpha=False)
    print('phone_code_sys=' + str(phone_code))

    # 2.向指定手机号码发送验证码
    result = send_sms(phone, phone_code)
    request.session['phone_code'] = phone_code
    return HttpResponse(result)


# 定义装饰器
def login_required(view_func):
    # 定义闭包函数
    def wrapper(request, *args, **kwargs):
        if not request.session.has_kry(''):
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return wrapper


# 职业
def profession(request):
    role_id = request.POST.getlist('select')[0]
    if role_id == '1':
        return JsonResponse({'status': 1})
    elif role_id == '2':
        return JsonResponse({'status': 2})
    elif role_id == '3':
        return JsonResponse({'status': 3})
    elif role_id == '4':
        return JsonResponse({'status': 4})
    elif role_id == '5':
        return JsonResponse({'status': 5})
    else:
        return JsonResponse({'status': 0})


# 判断用户名是否可用
@csrf_exempt
def username_is(request):
    nickName = request.POST.get('username')
    successes = 0
    try:
        UserInfo.objects.get(user_name=nickName)
    except UserInfo.DoesNotExist:
        successes = 1
    except UserInfo.MultipleObjectsReturned:
        successes = 0
    return JsonResponse({'successes': successes})


# 判断账号是否可用
@csrf_exempt
def usernum_is(request):
    nicknum = request.POST.get('nicknum')
    successes = 0
    try:
        UserInfo.objects.get(user_number=nicknum)
    except UserInfo.DoesNotExist:
        successes = 1
    except UserInfo.MultipleObjectsReturned:
        successes = 0
    return JsonResponse({'successes': successes})


# 判断身份证是否可用
@csrf_exempt
def identity_is(request):
    identity = request.POST.get('identity')
    successes = 0
    try:
        UserInfo.objects.get(user_card=identity)
    except UserInfo.DoesNotExist:
        successes = 1
    return JsonResponse({'successes': successes})


# 判断手机号是否可用
@csrf_exempt
def phone_is(request):
    identity = request.POST.get('phone')
    successes = 0
    try:
        UserInfo.objects.get(user_phone=identity)
    except UserInfo.DoesNotExist:
        successes = 1
    except UserInfo.MultipleObjectsReturned:
        successes = 0
    return JsonResponse({'successes': successes})


# 判断验证码是否正确
@csrf_exempt
def yzm_is(request):
    identity = request.POST.get('identity')
    successes = 0
    try:
        UserInfo.objects.get(user_card=identity)
    except UserInfo.DoesNotExist:
        successes = 1
    return JsonResponse({'successes': successes})
