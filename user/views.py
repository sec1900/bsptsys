from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from index.models import *
from .models import *
import os
import re
import random
# Create your views here.

# 使用装饰器检查用户是否登录,若未登录则强制跳转到登录界面
@login_required(login_url='/user/login.html')
# 用户中心视图
def userView(request):
    # 顶部导航栏
    nav_list = Navigation.objects.all()
    # 左侧导航栏脚本分类列表
    label_list = Label.objects.all()
    # 左侧导航栏脚本列表
    script_list = Script.objects.select_related('script_label').all()  # 获取所有脚本名称
    return render(request, "usercenter.html", locals())  # locals() 函数会以字典类型返回当前位置的全部局部变量。

# 使用装饰器检查用户是否登录,若未登录则强制跳转到登录界面
@login_required(login_url='/user/login.html')
# 用户任务列表视图
def usertaskView(request):
    # 顶部导航栏
    nav_list = Navigation.objects.all()
    # 左侧导航栏脚本分类列表
    label_list = Label.objects.all()
    # 左侧导航栏脚本列表
    script_list = Script.objects.select_related('script_label').all()
    return render(request, "usertask.html", locals())


# 任务结果查询视图
def taskresultView(request):
    try:
        task_id = request.GET.get('task_id')
        # 获取任务开始时间，用来进行拼接获取任务结果文件路径
        task_result_time = str(UserTask.objects.select_related('userTask_task').get(userTask_task__task_id=task_id).date_start).split(" ")[0]
        # 进行拼接获取任务结果文件路径
        task_result_file_path = os.getcwd() + '/result/' + request.user.username + "/" + task_result_time + "/" + task_id
        task_result = ''
        with open(task_result_file_path, mode='r') as f:
            task_result = f.read()
        # 把\n换成<br/>再进行输出
        return HttpResponse(task_result.replace('\n', '<br>'))
    except:
        return HttpResponse()


# 用户任务视图的数据接口
def usertaskapiView(request):
    try:
        data_list = []
        # 当前请求的页数
        page = request.GET.get("page")
        # 当前页数请求的数量
        limit = request.GET.get("limit")
        # 获取数据并分页
        query_data = UserTask.objects.filter(userTask_user_id=request.user.id).order_by('-date_start')[
            (int(page)-1)*int(limit):int(page)*int(limit)]
        # 以JSON格式组织数据
        for i in query_data:
            dic = {'date_start': i.date_start, 'task_id': i.userTask_task.task_id,
                   'username': i.userTask_user.username, 'date_done': i.userTask_task.date_done,
                   'status': i.userTask_task.status, 'task_args': re.split(r"['](.*?)[']", i.userTask_task.task_args)[3]}
            data_list.append(dic)
        # 构造JSON数据
        json_data = {
            "code": 0,
            "msg": "",
            "count": UserTask.objects.filter(userTask_user_id=request.user.id).count(),
            "data": data_list
        }
        return JsonResponse(json_data)
    except:
        return HttpResponse('')

# 用户注册视图
def registerView(request):
    # 返回提示的类型(success,info,warning,danger)
    alertType = ""
    # 返回提示的内容
    tips = ""
    # 使用POST方法处理用户的注册请求
    if request.method == "POST":
        # 获取表单的账号、密码、邮箱信息
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        confirmpassword = request.POST.get('confirmpassword', '')
        email = request.POST.get('email', '')
        # 检查表单信息内容是否为空
        if (not username.strip()) or \
        (not password.strip()) or \
        (not confirmpassword.strip()) or \
        (not email.strip()):
            alertType = "danger"
            tips = "表单信息有误,请重试"
        else:
            if User.objects.filter(username=username):
                # 用户名存在则返回提示信息
                alertType = "danger"
                tips = "用户已经存在,请重新输入"
            else:
                if password != confirmpassword:
                # 两次输入的密码不一样,返回提示信息
                    alertType = "danger"
                    tips = "两次密码不同,请重新确认密码"
                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()
                    # 注册成功返回提示信息
                    alertType = "success"
                    tips = "注册成功!"
    return render(request, "register.html", locals())

# 用户登录视图
def loginView(request):
    # 返回提示的类型(success,info,warning,danger)，用于前端样式显示
    alertType = ""
    # 返回提示的内容
    tips = ""
    # GET方法来处理用户的访问操作
    if request.method == 'GET':
        # 判断用户是否验证过,若验证过则跳回首页,防止用户重复登录
        if request.user.is_authenticated:
            return redirect('/')
    # POST方法用来处理用户的登录请求
    if request.method == 'POST':
        # 获取表单的账号和密码
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # 根据用户名进行查询，判断用户是否存在
        if User.objects.filter(username=username):
            # 对用户的账号和密码进行验证
            user = authenticate(username=username, password=password)
            # 若user存在则表示验证成功，若不存在则表示验证失败
            if user:
                # 若验证成功，再判断账号是否处于激活状态
                if user.is_active:
                    # 若账号处于激活状态，则对改用户进行登录
                    login(request, user)
                    # 在session中写入is_login(用来判断是否登录)
                    # 用is_authenticated函数，在注册账号时也会验证通过
                    request.session['is_login'] = 1
                    # 登录成功重定向到网站首页
                    return redirect('/')
            # 若验证失败则返回提示信息
            else:
                alertType = "danger"
                tips = "用户名/密码错误,请重新输入"
        # 若数据库不存在相应的用户则返回提示信息
        else:
            alertType = "danger"
            tips = "用户名/密码错误,请重新输入"
    return render(request, "login.html", locals())

# 用户注销视图
def logoutView(request):
    logout(request)
    # 注销后重定向到登录页面
    return redirect("login.html")

# 使用装饰器检查用户是否登录,若未登录则强制跳转到登录界面
@login_required(login_url='/user/login.html')
# 用户重置密码视图
def setpasswordView(request):
    try:
        username = request.user.username
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        rep_password = request.POST.get('rep_password', '')
        # 检查数据库是否存在当前用户
        if User.objects.filter(username=username):
            # 对用户的旧密码进行验证
            user = authenticate(username=username, password=old_password)
            # 对新密码进行验证
            if user and new_password == rep_password and new_password != '' and rep_password != '':
                user.set_password(new_password)
                user.save()
                return redirect('/')
            else:
                # 出错触发异常
                raise
    except:
        # 顶部导航栏
        nav_list = Navigation.objects.all()
        # 左侧导航栏脚本分类列表
        label_list = Label.objects.all()
        # 左侧导航栏脚本列表
        script_list = Script.objects.select_related('script_label').all()
        tips = 'error'
        return render(request, "usercenter.html", locals())

# 用户忘记密码视图
def resetpasswordView(request):
    try:
        # 获取参数
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        button = '获取验证码'
        new_password_flag = False
        new_password = request.POST.get('new_password', '')
        VerificationCode = request.POST.get('VerificationCode', '')
        # GET请求为网页显示，POST请求为密码重置
        if request.method == 'POST':
            user = User.objects.filter(username=username)
            # 判断用户是否存在，且邮箱填写是否正确
            if user and user[0].email == email:
                # 判断验证码是否发送
                if not request.session.get('VerificationCode', ''):
                    # 发送验证码并写入session，进行缓存
                    button = '重置密码'
                    tips = '验证码已经发送到您的邮箱!'
                    alertType = 'success'
                    new_password_flag = True
                    VerificationCode = str(random.randint(1000,9999))
                    request.session['VerificationCode'] = VerificationCode
                    user[0].email_user('web渗透测试工具集找回密码', '您的验证码为: %s' % VerificationCode)  # 发送验证码，参考 https://www.jianshu.com/p/12fe10466e79
                elif VerificationCode == request.session.get('VerificationCode'):
                    # 密码加密处理并保存到数据库
                    dj_ps = make_password(new_password, None, 'pbkdf2_sha256')  # make_password的使用方法：https://blog.csdn.net/q3102885/article/details/83303415
                    user[0].password = dj_ps
                    user[0].save()
                    tips = '密码重置成功'
                    alertType = 'success'
                    # 重置完毕后把username,email字段清空防止再次出现在页面上
                    username = ''
                    email = ''
                    del request.session['VerificationCode']
            else:
                alertType = "danger"
                new_password_flag = False
                username = ''
                email = ''
                tips = '信息有误！请重试'
            return render(request, "resetpassword.html", locals())
        else:
            return render(request, "resetpassword.html", locals())
    except:
        return HttpResponse('')
    
