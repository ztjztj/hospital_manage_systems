from django.shortcuts import render, redirect, HttpResponse
from django import views
from registration.models import *
from xlwt import *
from io import BytesIO
import os

from django.core.paginator import Paginator


def medicine_house_index(request):
    return render(request, 'medicine_house/index.html')


def medicine_insert(request, mid):
    if request.method == 'GET':
        med1 = Medicine.objects.get(pk=mid)
        return render(request, 'medicine_house/medicine_insert.html', {'med1': med1})
    else:
        medicine_number = request.POST.get('medicine_number')
        s = Medicine.objects.get(pk=mid)
        s.medicine_number = int(s.medicine_number) + int(medicine_number)
        s.save()
        return redirect('medicine_house')


# 药品详情
def medicine_detail(request, mid):
    med2 = Medicine.objects.get(pk=mid)

    if med2.medicine_number <= 0:
        return render(request, 'medicine_house/medicine_detail.html', {'med2': med2, 'med3': "补货中···"})
    else:
        return render(request, 'medicine_house/medicine_detail.html', {'med2': med2})


# 更该药品信息
def medicine_update(request, mid):
    if request.method == 'GET':
        med3 = Medicine.objects.get(pk=mid)
        return render(request, 'medicine_house/medicine_update.html', {'med3': med3})
    else:
        medicine_enter_price = request.POST.get('medicine_enter_price')
        medicine_outer_price = request.POST.get('medicine_outer_price')
        medicine_message = request.POST.get('medicine_message1')
        medicine_name = request.POST.get('medicine_name')
        medicine_number = request.POST.get('medicine_number')
        s = Medicine.objects.get(pk=mid)
        s.medicine_enter_price = medicine_enter_price
        s.medicine_outer_price = medicine_outer_price
        s.medicine_number = medicine_number
        s.medicine_name = medicine_name
        s.medicine_message = medicine_message

        s.save()
        return redirect('medicine_house')


# 药品查询页面
class medicine_house1(views.View):
    def get(self, request):

        return redirect('medicine_house')

    def post(self, request):

        medicine_name = self.request.POST.get('mecidine_name')
        selectmed = self.request.POST.get('selectmed')

        s = Department.objects.get(depart_name=selectmed)

        if Medicine.objects.filter(medicine_name=medicine_name, fk_medicine_type_department_id=s.id).exists():
            selects = Medicine.objects.get(medicine_name=medicine_name)

            return render(request, 'medicine_house/medicine_select.html', {'selects': selects})

        else:
            return render(request, 'medicine_house/medicine_select.html')



# 药品首页
def medicine_house(request):
    if request.method == 'GET':
        # if
        meds = Medicine.objects.all()
        count = meds.count()

        limit = 3
        paginator = Paginator(meds, limit)  # 按每页10条分页
        page = request.GET.get('page', '1')  # 默认跳转到第一页
        result = paginator.page(page)
        return render(request, 'medicine_house/medicine_index.html', {'meds': result, 'count': count})
    else:
        # return render(request, 'medicine_house/medicine_index.html', {'meds': result})
        medicine_name = request.POST.get('mecidine_name')
        selectmed = request.POST.get('selectmed')

        s = Department.objects.get(depart_name=selectmed)

        if Medicine.objects.filter(medicine_name=medicine_name, fk_medicine_type_department_id=s.id).exists():
            selects = Medicine.objects.get(medicine_name=medicine_name)

            return render(request, 'medicine_house/medicine_index.html', {'selects': selects})
        else:
            return render(request, 'medicine_house/medicine_index.html', {'noselect': '暂无此药'})


# 添加新药
class new_medicine(views.View):
    def get(self, request):
        # meds1 = Medicine.objects.order_by('-id')[0].id

        meds2 = Department.objects.all()
        return render(self.request, 'medicine_house/new_medicine.html', {'meds2': meds2})
        # return render(self.request, 'medicine_house/new_medicine.html')
        # return render(self.request,'medicine_house/new_medicine.html')

    def post(self, request):
        new_enter_medicine = request.POST.get('new_enter_medicine')
        new_outer_medicine = request.POST.get('new_outer_medicine')
        new_name_medicine = request.POST.get('new_name_medicine')
        new_dpartment_medicine = request.POST.get('new_department_medicine')

        dpartment = Department.objects.get(depart_name=new_dpartment_medicine)
        new_message_medicine = request.POST.get('new_message_medicine')
        new_number_medicine = request.POST.get('new_number_medicine')
        if Medicine.objects.filter(medicine_name=new_name_medicine).exists():
            return HttpResponse('此药已有')

        else:
            Medicine.objects.create(fk_medicine_type_department_id=dpartment.id, medicine_name=new_name_medicine,
                                    medicine_enter_price=new_enter_medicine, medicine_outer_price=new_outer_medicine,
                                    medicine_message=new_message_medicine,
                                    medicine_number=new_number_medicine)
            return redirect('medicine_house')


# #excel表格
def export_excel(request):
    """导出表格"""
    list_obj = Medicine.objects.all().order_by("id")
    if list_obj:
        ws = Workbook(encoding="utf-8")
        # ws = Workbook()
        w = ws.add_sheet(u"数据报表第一页")
        # w.write(0,0,"id")
        w.write(0, 0, u"药品编号")
        w.write(0, 1, u"药品名称")
        w.write(0, 2, u"药品类型")
        w.write(0, 3, u"简单描述")
        # w.write(0,5,u"状态")
        w.write(0, 4, u"剩余量")
        excel_row = 1
        for obj in list_obj:
            data_id = obj.id
            data_name = obj.medicine_name
            data_type = obj.fk_medicine_type_department.depart_name
            data_des = obj.medicine_message
            data_num = obj.medicine_number
            w.write(excel_row, 0, data_id)
            w.write(excel_row, 1, data_name)
            w.write(excel_row, 2, data_type)
            w.write(excel_row, 3, data_des)
            w.write(excel_row, 4, data_num)
            excel_row += 1
        exits_file = os.path.exists('test.xls')
        if exits_file:
            os.remove(r"test.xls")
        ws.save('test.xls')
        sio = BytesIO()
        ws.save(sio)
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='pplication/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=test.xls'
        response.write(sio.getvalue())
        return response


# 查询页面的excel表
def select_excel(request, eid):
    obj = Medicine.objects.get(id=eid)
    if obj:
        ws = Workbook(encoding="utf-8")
        w = ws.add_sheet(u"数据报表第一页")
        # w.write(0,0,"id")
        w.write(0, 0, u"药品编号")
        w.write(0, 1, u"药品名称")
        w.write(0, 2, u"药品类型")
        w.write(0, 3, u"简单描述")
        # w.write(0,5,u"状态")
        w.write(0, 4, u"剩余量")
        excel_row = 1
        # for obj in list_obj:
        data_id = obj.id
        data_name = obj.medicine_name
        data_type = obj.fk_medicine_type_department.depart_name
        data_des = obj.medicine_message
        data_num = obj.medicine_number
        w.write(excel_row, 0, data_id)
        w.write(excel_row, 1, data_name)
        w.write(excel_row, 2, data_type)
        w.write(excel_row, 3, data_des)
        w.write(excel_row, 4, data_num)
        # excel_row += 1
        exits_file = os.path.exists('test.xls')
        if exits_file:
            os.remove(r"test.xls")
        ws.save('test.xls')
        sio = BytesIO()
        ws.save(sio)
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=test.xls'
        response.write(sio.getvalue())
        return response


# 密码管理
def medicine_house_password(request):
    return render(request, 'medicine_house/medicine_house_password.html')


# 药品首页的删除
def medicine_delete(request):
    try:
        del_med = request.POST.getlist('check1')[0]

        dell = Medicine.objects.filter(id=del_med)

        dell.delete()
        return redirect('medicine_house')
    except IndexError:

        return redirect('medicine_house')


def medicine_delete1(request):
    try:

        del_med = request.POST.getlist('check')[0]

        dell = Medicine.objects.filter(id=del_med)

        dell.delete()
        return redirect('medicine_house')
    except IndexError:

        return redirect('medicine_house')


# 列表导出所选的药品
def obj2(request):
    obj1 = request.POST.getlist('check1')[0]
    obj5 = obj1.split(',')
    obj3 = []
    for obj in obj5:
        obj3.append(int(obj))
    one = []
    for i in range(len(obj5)):

        for obj0 in obj3:
            obj2 = Medicine.objects.filter(id=obj0)

            one.append(obj2)

        return one

