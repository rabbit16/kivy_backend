import json
import os
import time

import cv2
from channels.auth import logout
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from rest_framework import viewsets
from rest_framework.response import Response
import requests
from index_page.models import Devices, User, Banner, MessageRecord, Task
from index_page.schemas import DeviceDetail, BannerDetail, MessageDetail, TaskDetail
from kivy_backend.settings import FASTAPI_URL
from utils.calcute_dis import get_closest_bin
from utils.res_code import to_json_data, Code, error_map
from verification.forms import LoginForm
from django.core.cache import cache
import numpy as np


# Create your views here.
class Login(View):

    def post(self, request):
        json_data = json.loads(request.body)
        if not json_data:
            return to_json_data(errno=Code.PARAMERR, errmsg='参数错误')

        else:
            loginForm = LoginForm(data=json_data, request=request)
            try:
                if loginForm.is_valid():
                    return to_json_data(errmsg="登录成功", data=User.objects.get(
                        employee_number=loginForm.cleaned_data['employee_number']).to_dict())
                else:
                    err_m_l = []
                    for i in loginForm.errors.values():
                        err_m_l.append(i[0])
                    err_msg_str = '/'.join(err_m_l)
                    return to_json_data(errno=Code.PARAMERR, errmsg=err_msg_str)
            except:
                return to_json_data(errno=Code.PARAMERR, errmsg='参数错误')


class LoginOut(View):
    def get(self, request):
        logout(request)


class DevicesInfo(viewsets.ModelViewSet):
    queryset = Devices.objects.all()
    serializer_class = DeviceDetail

    def get_queryset(self):
        user_phone = self.request.query_params.get('employee_number', None)

        # 先查找用户
        try:
            user = User.objects.get(employee_number=user_phone)  # 假设User模型有phone字段
        except User.DoesNotExist:
            return Devices.objects.none()  # 如果用户不存在，返回一个空的QuerySet

        # 查询与该用户相关联的所有设备
        devices = Devices.objects.filter(access_user=user)
        return devices

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user_phone = self.request.query_params.get('user_phone')
        user_address = User.objects.get(employee_number=user_phone).address
        request.data["device_addr"] = user_address
        if Devices.objects.filter(device_name=user_phone, children=request.data["children"]).exists():
            Devices.objects.filter(device_name=user_phone, children=request.data["children"]).update(**request.data)
            return to_json_data(errmsg="数据已更新")
        else:
            return super().create(request, *args, **kwargs)


class BannerInfo(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerDetail

    def get_queryset(self):
        employee_number = self.request.query_params.get('employee_number', None)
        # 查找对应的轮播图
        try:
            banner = Banner.objects.filter(community__access_user__employee_number=employee_number)  # 假设User模型有phone字段
            return banner
        except User.DoesNotExist:
            return Devices.objects.none()  # 如果用户不存在，返回一个空的QuerySet

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PicInfo(View):
    def get(self, request):
        employee_num = request.query_params.get('employee_number', None)
        if employee_num is None:
            return to_json_data(errno=Code.PARAMERR, errmsg="数据不存在，先初始化")
        return to_json_data(errmsg=Code.OK, data={
            "pic_position": json.loads(cache.get(employee_num)),
        })

    def post(self, request):
        """
        这个是设置每个特定垃圾桶缓存的
        {
            "employee_number": request.data['employee_number'],
            "position": request.data['position'],
        }
        """
        json_data = json.loads(request.body)
        if not json_data:
            return to_json_data(errno=Code.PARAMERR)
        employee_number = json_data.get('employee_number')
        value = json_data.get("position", None)
        if employee_number is None:
            return to_json_data(errno=Code.SESSIONERR, errmsg=f"{error_map[Code.SESSIONERR]}")
        cache.set(str(employee_number), json.dumps(value))
        return to_json_data(errno=Code.OK, data=json.loads(cache.get(str(employee_number))))


class PicCacheInfo(View):
    def get(self, request):
        """
        0_person -> [...] 用户的像素数据
        """
        employee_num = request.query_params.get('employee_number', None)
        get_key = f"{employee_num}_person"
        if employee_num is None:
            return to_json_data(errno=Code.PARAMERR)
        return to_json_data(errno=Code.OK, data=cache.get(str(get_key)))

    def post(self, request):
        """
        发送图片数据进行分析和请求，并记录数据
        这里有两个缓存消息，一个是 垃圾桶的坐标位置，一个是任务的特征列表。这两个联合来统计每日的投放人数。
        employee_number -> 垃圾桶的坐标位置
        employee_number_person -> 人的特征记录
        """
        json_data = json.loads(request.body)
        get_key = f"{json_data['employee_number']}_person"  # 缓存人物数据的库键
        cache_list = cache.get(get_key) if cache.get(get_key) else '[]'  # 这里开始获取人物数据缓存库
        if json_data['employee_number'] is None:
            return to_json_data(errno=Code.PARAMERR)
        else:
            try:
                r = requests.post(f"{FASTAPI_URL}/gpu_apps/people_monitor/", json={
                    "employee_number": json_data['employee_number'],
                    "image_data": json_data['image_data'],
                    "cache_list": cache_list,
                }, verify=False)  # 做一层中转，发送给计算集群计算人物信息
                # print(r.json())
                cache_list_json = json.loads(cache_list)
            except Exception as e:
                # print(e, cache_list)
                cache_list_json = []
                r = requests.post(f"{FASTAPI_URL}/gpu_apps/people_monitor/", json={
                    "employee_number": json_data['employee_number'],
                    "image_data": json_data['image_data'],
                    "cache_list": '[]',
                }, verify=False)  # 做一层中转，发送给计算集群计算人物信息
                # FIXME  这里开始决定是否记录数据
            if r.json()["data"]:  # 记录新的人物记录
                cache_list_json = r.json()["data"]
                cache.set(get_key, json.dumps(cache_list_json), timeout=60)
                # FIXME 这里开始计算坐标并统计个数。 左中右分别是 干垃圾 湿垃圾 有害垃圾
                # pic_detect_position = cache.get(json_data['employee_number'])
                # if pic_detect_position:
                #     pic_detect_position = json.loads(pic_detect_position)
                today = timezone.now().date()
                obj, created = MessageRecord.objects.get_or_create(
                    daily_time=today,
                    defaults={"daily_time": today},
                    author_id=User.objects.filter(employee_number=json_data['employee_number']).first().id,
                )  # 搜索或者创建一个记录对象
                for p in r.json()["new_people"]:  # 开始写入数据库
                    obj.execute_person += 1
                    # bin = get_closest_bin(p, pic_detect_position)  # FIXME 这里需要加上人物的坐标才好判断
                    # # choose_dict = {
                    # #     0: "dry_daily_visits",
                    # #     1: "wet_daily_visits",
                    # #     2: "hazardous_daily_visits",
                    # #     3: "recyclable_daily_visits"
                    # # }
                    # if bin == 0:
                    #     obj.dry_daily_visits += 1
                    # elif bin == 1:
                    #     obj.wet_daily_visits += 1
                    # elif bin == 2:
                    #     obj.hazardous_daily_visits += 1
                    # else:
                    #     obj.recyclable_daily_visits += 1
                    obj.save()

            return to_json_data(errno=Code.OK, data=r.json())


class RubbishCacheInfo(View):
    def get(self, request):
        """
        0_person -> [...] 用户的像素数据
        """
        employee_num = request.query_params.get('employee_number', None)
        get_key = f"{employee_num}_person"
        if employee_num is None:
            return to_json_data(errno=Code.PARAMERR)
        return to_json_data(errno=Code.OK, data=cache.get(str(get_key)))

    def post(self, request):
        """
        发送图片数据进行分析和请求，并记录数据
        这里有两个缓存消息，一个是 垃圾桶的坐标位置，一个是任务的特征列表。这两个联合来统计每日的投放人数。
        employee_number -> 垃圾桶的坐标位置
        employee_number_person -> 人的特征记录
        """
        json_data = json.loads(request.body)
        get_key = f"{json_data['employee_number']}_rubbish"  # 缓存人物数据的库键
        cache_list = cache.get(get_key) if cache.get(get_key) else '[]'  # 这里开始获取人物数据缓存库
        if json_data['employee_number'] is None:
            return to_json_data(errno=Code.PARAMERR)
        else:
            try:
                r = requests.post(f"{FASTAPI_URL}/gpu_apps/rubbish_monitor/", json={
                    "employee_number": json_data['employee_number'],
                    "image_data": json_data['image_data'],
                    "cache_list": cache_list,
                }, verify=False)  # 做一层中转，发送给计算集群计算人物信息
            except Exception as e:
                # print(e, cache_list)
                r = requests.post(f"{FASTAPI_URL}/gpu_apps/rubbish_monitor/", json={
                    "employee_number": json_data['employee_number'],
                    "image_data": json_data['image_data'],
                    "cache_list": '[]',
                }, verify=False)  # 做一层中转，发送给计算集群计算人物信息
                # FIXME  这里开始决定是否记录数据
            if r.json()["new_rubbish_pic"]:  # 记录新的人物记录
                cache_list_json = r.json()["data"]
                cache.set(get_key, json.dumps(cache_list_json), timeout=60)
                today = timezone.now().date()
                current_directory = os.path.dirname(os.path.abspath(__file__))
                main_dir = f'{os.path.abspath(os.path.join(current_directory, "../../"))}'
                user = User.objects.filter(employee_number=json_data['employee_number']).first()
                for r in r.json()["new_rubbish_pic"]:
                    tmp_path = f"{main_dir}/static/pic_rubbish/{json_data['employee_number']}_{int(time.time())}.jpg"
                    cv2.imwrite(tmp_path, np.array(r))
                    Task.objects.create(
                        name="小包垃圾",
                        user=user,
                        pic_url=tmp_path,
                    )  # 开始创建任务

                # obj, created = MessageRecord.objects.get_or_create(
                #     daily_time=today,
                #     defaults={"daily_time": today},
                #     author_id=User.objects.filter(employee_number=json_data['employee_number']).first().id,
                # )  # 搜索或者创建一个记录对象
                # for p in r.json()["rubbish_people"]:  # 开始写入数据库
                #     obj.execute_person += 1
                #     # bin = get_closest_bin(p, pic_detect_position)  # FIXME 这里需要加上人物的坐标才好判断
                #     # # choose_dict = {
                #     # #     0: "dry_daily_visits",
                #     # #     1: "wet_daily_visits",
                #     # #     2: "hazardous_daily_visits",
                #     # #     3: "recyclable_daily_visits"
                #     # # }
                #     # if bin == 0:
                #     #     obj.dry_daily_visits += 1
                #     # elif bin == 1:
                #     #     obj.wet_daily_visits += 1
                #     # elif bin == 2:
                #     #     obj.hazardous_daily_visits += 1
                #     # else:
                #     #     obj.recyclable_daily_visits += 1
                #     obj.save()

            return to_json_data(errno=Code.OK, data="", errmsg="创建任务成功")

class MessageInfo(viewsets.ModelViewSet):
    queryset = MessageRecord.objects.all()
    serializer_class = MessageDetail

    def get_queryset(self):
        employee_number = self.request.query_params.get('employee_number', None)

        # 先查找用户
        try:
            user = User.objects.get(employee_number=employee_number)  # 假设User模型有phone字段
        except User.DoesNotExist:
            return MessageRecord.objects.none()  # 如果用户不存在，返回一个空的QuerySet

        # 查询与该用户相关联的所有设备
        message_record = MessageRecord.objects.filter(author=user, daily_time__gte=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
        return message_record

class TaskInfo(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskDetail
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    def get_queryset(self):
        employee_number = self.request.query_params.get('employee_number', None)
        # 先查找用户
        try:
            user = User.objects.get(employee_number=employee_number)  # 假设User模型有phone字段
        except User.DoesNotExist:
            return Task.objects.none()  # 如果用户不存在，返回一个空的QuerySet

        # 查询与该用户相关联的所有设备
        task_record = Task.objects.filter(user=user,
                                          is_delete=False,
                                          status=False
                                          ).order_by('add_time')
        return task_record

class TaskUpdate(View):

    def get(self, request):
        employee_num = request.GET["employee_number"]
        if employee_num is None:
            return to_json_data(errno=Code.PARAMERR)
        user = User.objects.filter(employee_number=employee_num).first()
        task_all = Task.objects.filter(user=user, is_delete=False).count()
        task_deal = Task.objects.filter(user=user, is_delete=False, status=True).count()
        return to_json_data(errno=Code.OK, data={
            "待办工单": task_all - task_deal,
            "结束工单": task_deal,
        })
    def post(self, request):
        json_data = json.loads(request.body)  # 获取具体信息
        task_id = json_data['task_id']
        task = Task.objects.filter(pk=task_id)
        update_fields = json_data['update_fields']
        task.update(**update_fields)
        return to_json_data(errno=Code.OK, data="更新成功", errmsg=f"更新字段为{json_data['update_fields']}")