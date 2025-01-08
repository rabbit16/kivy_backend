from django.db import models
# from utils import ModelBase
from django.contrib.auth.models import UserManager as _UserManager, AbstractUser
from django.utils import timezone


# Create your models here.


class UserManager(_UserManager):
    def create_superuser(self, username, email, password=None, **extra_fields):
        super().create_superuser(username=username, email=email, password=password, **extra_fields)


class User(AbstractUser):
    """用户表单"""
    objects = UserManager()
    REQUIRED_FIELDS = ['email', 'mobile', 'employee_number', "address"]
    mobile = models.CharField(max_length=11, verbose_name='手机号', help_text="手机号", unique=True,
                              error_messages={'unique': "改手机号已注册"})
    email_ac = models.BooleanField(default=False, verbose_name="邮箱状态")
    is_delete = models.BooleanField(default=False)
    update_time = models.DateTimeField('更新日期', default=timezone.now)
    salary = models.FloatField('用户工资', default=0)
    employee_number = models.CharField(max_length=200, verbose_name='工号', help_text="工号", unique=True,
                              error_messages={'unique': "该工号已存在"})
    address = models.CharField(max_length=200, verbose_name='地址', help_text="地址", unique=False,
                              error_messages={'unique': "该地址格式不正确"}, default='')

    def to_dict(self):
        return {
            'id': self.id,
            'mobile': self.mobile,
            'email_ac': self.email_ac,
            'update_time': self.update_time,
            'employee_number': self.employee_number,
        }
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'

    def __str__(self):
        return self.username

class Community(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID", unique=True)
    is_delete = models.BooleanField(verbose_name="软删除", default=False, db_index=True)
    add_time = models.DateTimeField('添加时间', default=timezone.now)
    update_time = models.DateTimeField('更新时间', default=timezone.now, db_index=True)
    name = models.CharField(verbose_name='小区名字', max_length=100, unique=True, db_index=True)
    address = models.TextField(verbose_name='小区地址')
    describe = models.TextField(verbose_name='小区介绍')
    access_user = models.ManyToManyField(
        User,
        through="UserCommunityRecord",
        through_fields=("community", "user"),
    )
    class Meta:
        db_table = 'tb_community'
        verbose_name = "小区记录表单"
    def __str__(self):
        return self.name
class UserCommunityRecord(models.Model):
    """该表单记录用户和设备之间的关系"""
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_reason = models.CharField(verbose_name='访问原因', max_length=300)
    class Meta:
        db_table = 'tb_user_community'
        verbose_name = "用户小区记录表单"

class Devices(models.Model):
    """设备表单"""
    id = models.AutoField(primary_key=True, verbose_name="ID", unique=True)
    is_delete = models.BooleanField(verbose_name="软删除", default=False, db_index=True)
    device_type = models.IntegerField(verbose_name="设备类型", default=0, db_index=True)
    add_time = models.DateTimeField('添加时间', default=timezone.now)
    update_time = models.DateTimeField('更新时间', default=timezone.now, db_index=True)
    device_name = models.CharField(verbose_name='设备名', max_length=100, unique=False, db_index=True)
    device_addr = models.CharField(verbose_name='设备地址', max_length=100, unique=False, db_index=True)
    access_user = models.ManyToManyField(
        User,
        through="UserDevicePri",
        through_fields=("devices", "user"),
    )
    children = models.IntegerField(verbose_name="设备子编号", default=0, db_index=True)
    status = models.IntegerField(verbose_name="设备状态", default=0, db_index=False)
    class Meta:
        db_table = 'tb_devices'
        verbose_name = "设备表单"
    def __str__(self):
        return self.device_name

class UserDevicePri(models.Model):
    """该表单记录用户和设备之间的关系"""
    devices = models.ForeignKey(Devices, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_reason = models.CharField(verbose_name='访问原因', max_length=300)
    class Meta:
        db_table = 'tb_user_device_pri'
        verbose_name = "设备权限控制表单"
    def __str__(self):
        return self.devices.device_name
class Task(models.Model):
    """任务表单"""
    id = models.AutoField(primary_key=True, verbose_name="ID", unique=True)
    level = models.IntegerField(verbose_name='任务等级', db_index=True, default=0)
    status = models.IntegerField(verbose_name='任务状态', db_index=True, default=0)
    is_delete = models.BooleanField(verbose_name='软删除', default=False, db_index=True)
    name = models.CharField(verbose_name='任务名', max_length=100, db_index=True)
    add_time = models.DateTimeField('创建时间', default=timezone.now)
    update_time = models.DateTimeField('更新时间', default=timezone.now, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, verbose_name="拥有人")
    pic_url = models.CharField(verbose_name="图片路径", max_length=200)
    class Meta:
        db_table = 'tb_task'
        verbose_name = "任务状态表单"

class Alarms(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID", unique=True)
    name = models.CharField(verbose_name='报警场景名', max_length=100, db_index=True)
    level = models.IntegerField(verbose_name="报警等级", db_index=True, default=0)
    access_user = models.ManyToManyField(
        User,
        through="UserAlarmsRecord",
        through_fields=("alarm", "user"),
    )
    class Meta:
        db_table = 'tb_alarms'
        verbose_name = '报警场景'

class UserAlarmsRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    alarm = models.ForeignKey(Alarms, on_delete=models.CASCADE, db_index=True)
    add_time = models.DateTimeField('创建时间', default=timezone.now, db_index=True)
    deal_time = models.DateTimeField('解决时间', default=None, db_index=True)
    class Meta:
        db_table = 'tb_user_alarmsrecord'
        verbose_name = '报警关联表单'

class FunctionCode(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID", unique=True)
    name = models.CharField(verbose_name='功能名称', max_length=100, db_index=True)
    desc = models.CharField(verbose_name='简介', max_length=500)
    add_time = models.DateTimeField('创建时间', default=timezone.now, db_index=True)
    update_time = models.DateTimeField('修改时间', default=timezone.now, db_index=True)
    class Meta:
        db_table = 'tb_function_code'
        verbose_name = '功能分类表'

class MessageRecord(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID", unique=True)
    dry_daily_weight = models.FloatField(verbose_name='干垃圾当日重量', db_index=True, default=0)
    wet_daily_weight = models.FloatField(verbose_name='湿垃圾当日重量', db_index=True, default=0)
    hazardous_daily_weight = models.FloatField(verbose_name='有害垃圾当日重量', db_index=True, default=0)
    recyclable_daily_weight = models.FloatField(verbose_name='可回收垃圾当日重量', db_index=True, default=0)
    dry_daily_visits = models.IntegerField(verbose_name='干垃圾当日投放次数', db_index=True, default=0)
    wet_daily_visits = models.IntegerField(verbose_name='湿垃圾当日投放次数', db_index=True, default=0)
    hazardous_daily_visits = models.IntegerField(verbose_name='有害垃圾当日投放次数', db_index=True, default=0)
    recyclable_daily_visits = models.IntegerField(verbose_name='可回收垃圾当日投放次数', db_index=True, default=0)
    uncivilized_behavior = models.IntegerField(verbose_name='当日不文明行为', db_index=True, default=0)
    execute_person = models.IntegerField(verbose_name='当日不文明行为', db_index=True, default=0)
    daily_time = models.DateTimeField('创建时间', default=timezone.now, db_index=True)
    update_time = models.DateTimeField('修改时间', default=timezone.now, db_index=True)
    is_delete = models.BooleanField(verbose_name="软删除", default=False, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    class Meta:
        db_table = 'tb_message_record'
        verbose_name = "垃圾相关指标数据记录表"

class Settings(models.Model):

    id = models.AutoField(primary_key=True, verbose_name="ID", unique=True)
    name = models.CharField(verbose_name='配置名称', max_length=100, db_index=True)
    value = models.CharField(verbose_name='配置值', max_length=500, db_index=True)
    belong = models.CharField(verbose_name='所属对象', max_length=100, db_index=True)
    create_time = models.DateTimeField('创建时间', default=timezone.now, db_index=True)
    update_time = models.DateTimeField('修改时间', default=timezone.now, db_index=True)
    is_delete = models.BooleanField(verbose_name="软删除", default=False, db_index=True)
    class Meta:
        db_table = 'tb_proj_settings'
        verbose_name = "项目配置信息"

class Banner(models.Model):
    """
    这个是存放轮播图的配置表单
    """
    id = models.AutoField(primary_key=True, verbose_name="ID", unique=True)
    url = models.CharField(verbose_name="url地址", max_length=10638)
    create_time = models.DateTimeField('创建时间', default=timezone.now, db_index=True)
    update_time = models.DateTimeField('修改时间', default=timezone.now, db_index=True)
    is_delete = models.BooleanField(verbose_name="软删除", default=False, db_index=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, db_index=True)
    filename = models.CharField(verbose_name="文件名", max_length=200)
    class Meta:
        db_table = 'tb_banner'
        verbose_name = "轮播图（广告）配置信息表"



