from django.urls import path
from . import views

urlpatterns = [
    # 用户中心首页
    path('', views.userView, name='userIndex'),  # name属性指定url标签做跳转的地址
    # 用户注册页面
    path('register.html', views.registerView, name='register'),
    # 用户登录页面
    path('login.html', views.loginView, name='login'),
    # 用户注销页面
    path('logout.html', views.logoutView, name='logout'),
    # 用户重置密码页面
    path('setpassword.html', views.setpasswordView, name='setPassword'),
    # 用户忘记密码页码
    path('resetpassword.html', views.resetpasswordView, name='resetPassword'),
    # 用户任务列表
    path('usertask.html', views.usertaskView, name='userTask'),
    # 用户任务列表接口
    path('usertaskapi.json', views.usertaskapiView, name='userTaskApi'),
    # 任务结果查询
    path('taskresult.html', views.taskresultView, name='taskResult'),
]
