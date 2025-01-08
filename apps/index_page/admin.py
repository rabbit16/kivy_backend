from datetime import datetime

from django.contrib import admin
import pickle

from django.http import HttpResponse
from openpyxl.workbook import Workbook

from index_page.models import User, Task, Devices, UserDevicePri, FunctionCode, Alarms, MessageRecord, Community, \
    UserCommunityRecord, Settings, Banner

# Register your models here.
# admin.site.register(User)
admin.site.register(FunctionCode)
admin.site.register(Alarms)
admin.site.register(Settings)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "mobile",
        "email",
        "update_time",
        "salary",
        "employee_number",
        "address",
    ]

@admin.action(description="下载指标数据(excel)")
def make_published(modeladmin, request, queryset):
    # 创建一个工作簿和一个工作表
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "指标数据"
    now = datetime.now().strftime('%Y-%m-%d--%H:%M:%S')
    # 写入表头
    columns = [field.name for field in queryset.model._meta.fields]
    worksheet.append(columns)

    # 写入数据
    for item in queryset.values_list(*columns):
        worksheet.append(item)
    workbook.save(f'static/excel_tmp/{now}-executor({request.user}).xlsx')
    # 创建 HTTP 响应
    response = HttpResponse(
        content=open(f'static/excel_tmp/{now}-executor({request.user}).xlsx', 'rb').read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{now}.xlsx"'

    return response


# 关于垃圾指标的展示
@admin.register(MessageRecord)
class MessageRecordAdmin(admin.ModelAdmin):
    list_display = ["id", "dry_daily_weight", "wet_daily_weight", "hazardous_daily_weight",
                    "recyclable_daily_weight", "dry_daily_visits", "wet_daily_visits", "hazardous_daily_visits",
                    "recyclable_daily_visits", "uncivilized_behavior", "daily_time", "update_time"]
    actions = [make_published]


@admin.register(Devices)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "device_name",
        "device_type",
        "add_time",
        "update_time",
        "device_addr",
        "children",
        "status",
    ]

@admin.register(UserDevicePri)
class UserDevicePriAdmin(admin.ModelAdmin):
    list_display = [
    "devices",
    "user",
    "access_reason",
]

@admin.register(Community)
class CommunityCharAdmin(admin.ModelAdmin):
    list_display = [
    "id",
    "add_time",
    "update_time",
    "name",
    "address",
    "describe",
    ]

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "create_time",
        "update_time",
        "community",
        "filename",
        "url",
    ]

@admin.register(UserCommunityRecord)
class UserCommunityRecordAdmin(admin.ModelAdmin):
    list_display = [
        "community",
        "user",
        "access_reason",
    ]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'level',
        'status',
        'is_delete',
        'name',
        'add_time',
        'update_time',
        'user',
        'pic_url'
    ]

