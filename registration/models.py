from django.db import models


class UserInfo(models.Model):  # 用户表
    user_number = models.CharField(max_length=11, default=0)
    user_password = models.CharField(max_length=10, default=0)  # 用户密码
    user_name = models.CharField(max_length=20, default=0)  # 用户名
    user_email = models.EmailField(default=0)  # 用户邮箱
    user_card = models.CharField(max_length=18, default=0)  # 用户身份证号
    user_age = models.CharField(max_length=3, default=0)  # 用户年龄
    user_gender = models.CharField(max_length=2, default='男')  # 用户性别
    user_level = models.CharField(max_length=10, default=0)  # 用户学历
    user_phone = models.CharField(max_length=16, default=0)  # 用户电话号码
    user_status = models.CharField(max_length=20, default='禁用')  # 用户状态：启用，禁用
    user_role = models.ForeignKey('Role', on_delete=models.CASCADE, null=True)
    doctor_belong = models.ForeignKey('Department', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'UserInfo'


# 在院发药
class Main_details(models.Model):
    mediacal_redord_NO = models.IntegerField(default=0)  # 病历号

    patient_name = models.CharField(max_length=10)  # 病人姓名

    doctor = models.CharField(max_length=10)  # 医生姓名

    drug_name = models.CharField(max_length=30)  # 药品名称

    drug_number = models.IntegerField(default=0)  # 药品数量

    drug_status = models.BooleanField(default=False)  # 是否发药

    class Meta:
        db_table = 'Main_details'


# 药库
class Medicine(models.Model):  # 药
    medicine_name = models.CharField(max_length=20)  # 名称
    medicine_number = models.IntegerField()  # 数量
    medicine_outer_price = models.FloatField()  # 售价
    medicine_enter_price = models.FloatField()  # 进价
    medicine_message = models.CharField(max_length=200)  # 详细描述
    fk_medicine_type_department = models.ForeignKey('Department', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Medicine'
    # 药品类型和科室表关联


class PatientOne(models.Model):  # 病人表(第1次住院)
    patient_name = models.CharField(max_length=6)  # 病人姓名
    patient_age = models.IntegerField()  # 病人年龄
    patient_sex = models.CharField(max_length=50)  # 病人性别
    patient_phone = models.CharField(max_length=11)  # 病人电话
    patient_card = models.CharField(max_length=18)  # 病人的身份证号
    patient_status = models.CharField(max_length=200)  # 病人的症状
    patient_history = models.CharField(default=None, max_length=600)  # 病人的过敏史
    patient_registed_time = models.DateTimeField(auto_now=True)  # 病人的挂号时间
    patient_is_live = models.CharField(default=None, max_length=200, null=True)  # 病人是否住院
    patient_live_day = models.CharField(default=None, max_length=300, null=True)  # 病人住院的天数
    patient_condition = models.CharField(default=None, max_length=600, null=True)  # 病人的病情
    patient_message = models.CharField(default=None, max_length=600, null=True)  # 病人的备注
    patient_one_enter_time = models.DateTimeField(auto_now_add=True, null=True)  # 病人住院的时间
    patient_one_outer_time = models.DateTimeField(auto_now_add=True, null=True)  # 病人出院的时间
    patient_over_look_doctor = models.CharField(default=0, max_length=20, null=True)  # 是否已开药
    patient_take_medicine_time = models.DateTimeField(auto_now_add=True, null=True)  # 病人领药的时间
    fk_patient_doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, null=True)  # 关联医生表
    fk_patient_depart = models.ForeignKey('Department', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'PatientOne'
    # 关联科室表


class Department(models.Model):  # 科室
    depart_name = models.CharField(max_length=10)

    def __str__(self):
        return self.depart_name

    class Meta:
        db_table = 'Department'


class Money(models.Model):
    profit = models.FloatField(default=0)  # 盈利

    source = models.CharField(max_length=200)  # 收入钱的来源

    collect_money = models.FloatField(default=0)  # 收入的钱

    collect_time = models.DateTimeField()  # 收钱时间

    is_hospital = models.BooleanField(default=True)  # 状态

    fk_patientone = models.ForeignKey('PatientOne', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Money'


class PatientTwo(models.Model):  # 病人表(用户要续院)
    patient_two_enter_time = models.DateTimeField(auto_now_add=True)  # 病人住院的时间
    patient_two_outer_time = models.DateTimeField(auto_now_add=True)  # 病人出院的时间
    continue_live_day = models.CharField(default=None, max_length=200)  # 病人继续住院的天数

    class Meta:
        db_table = 'PatientTwo'


class Medicine_one(models.Model):
    medicine_one_name = models.CharField(max_length=20)  # 名称
    medicine_one_number = models.IntegerField()  # 数量
    medicine_one_outer_price = models.FloatField()  # 售价
    medicine_one_yes_no = models.CharField(default=0, max_length=20)  # 药方是否已提交
    fk_patient_medicine_one = models.ForeignKey('PatientOne', on_delete=models.CASCADE)  # 关联药方表

    class Meta:
        db_table = 'Medicine_one'


class DoctorMessage(models.Model):  # 医生详细信息表
    doctor_belong = models.CharField(max_length=10)  # 所属科室
    fk_doctor_message_user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)

    class Meta:
        db_table = 'DoctorMessage'


class Doctor(models.Model):  # 医生
    doctor_status = models.CharField(max_length=20, default='空闲中')  # 医生状态（是否挂号，空闲）
    waiting_number = models.IntegerField(default=0)  # 等的人数
    fk_doctor_user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)  # 用户表的外键

    class Meta:
        db_table = 'Doctor'


class Role(models.Model):
    role_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'Role'
