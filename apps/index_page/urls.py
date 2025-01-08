from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from index_page import views as index_views
from index_page.views import DevicesInfo, BannerInfo, MessageInfo, TaskInfo

app_name = 'index_page'
router = DefaultRouter()
router.register(r'devices', DevicesInfo)
router.register(r'banner', BannerInfo)
router.register(r'message_info', MessageInfo)
router.register(r'task_info', TaskInfo)
urlpatterns = [
    path('', include(router.urls)),
    path('login/', index_views.Login.as_view(), name='login'),
    path('pic_position/', index_views.PicInfo.as_view(), name='pic'),
    path('pic_person/', index_views.PicCacheInfo.as_view(), name='pic_person'),
    path('pic_rubbish/', index_views.RubbishCacheInfo.as_view(), name='pic_person'),
    path('task_update/', index_views.TaskUpdate.as_view(), name='task_update'),
]