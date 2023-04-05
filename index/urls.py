from django.urls import path
from . import views

urlpatterns = [
    # index路由
    path('', views.indexView, name='indexIndex'),
    # 脚本显示路由
    path('scriptdisplay/<scriptId>',views.scriptdisplayView, name='scriptDisplay'),
    # 脚本调用路由
    path('scriptcall', views.scriptcallView, name='scriptCall'),
    # 返回当前时间路由(测试用)
    path('datetime.html', views.datetimeView, name='indexDatetime'),
    # 任务队列路由
    path('tasksqueue', views.tasksqueueView, name="tasksQueue")
]
