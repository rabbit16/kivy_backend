from rest_framework import serializers

from index_page.models import Devices, Banner, MessageRecord, Task


class DeviceDetail(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = '__all__'

class BannerDetail(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class MessageDetail(serializers.ModelSerializer):
    class Meta:
        model = MessageRecord
        fields = '__all__'

class TaskDetail(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'