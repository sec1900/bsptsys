from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from .models import *
from user.models import *
from .tasks import asyTask
import os, copy, subprocess

# 网站目录路径
parent_path = os.getcwd()


# 使用装饰器检查用户是否登录,若未登录则强制跳转到登录界面
@login_required(login_url='/user/login.html')
def indexView(request):
    # 顶部导航栏
    nav_list = Navigation.objects.all()
    # 左侧导航栏脚本分类列表
    label_list = Label.objects.all()
    # 左侧导航栏脚本列表
    script_list = Script.objects.select_related('script_label').all()
    # 对banner模板提前进行渲染再传递显示到index.html   问题：如果不提前渲染呢？直接包含行不行
    banner = loader.get_template(os.path.join(os.getcwd(), 'index/templates/banner.html'))
    display = banner.render()
    return render(request, "index.html", locals())


# 返回当前时间
import datetime


def datetimeView(request):
    return HttpResponse(datetime.datetime.now())


# 使用装饰器检查用户是否登录,若未登录则强制跳转到登录界面
@login_required(login_url='/user/login.html')
# 脚本工具模板渲染函数
# 这个函数主要用于脚本工具界面的显示
def scriptdisplayView(request, scriptId):
    # 顶部导航栏
    nav_list = Navigation.objects.all()
    # 左侧导航栏脚本分类列表
    label_list = Label.objects.all()
    # 左侧导航栏脚本列表
    script_list = Script.objects.select_related('script_label').all()

    # 获取指定参数脚本的信息
    script = Script.objects.select_related('script_label').filter(script_id=scriptId)

    if request.method == 'GET':
        # 渲染脚本的模板
        # 默认脚本的模板名称与脚本名称一致
        # 渲染完成后传递到index.html显示
        scriptTemplate = loader.get_template(os.path.join(os.getcwd(), 'script', script[0].script_label.label_path,
                                                          script[0].script_file.split('.')[0] + ".html"))
        # 把脚本的ID传入到渲染的模板中，让调用脚本时候能够识别是调用哪个脚本
        # 不传脚本名称的原因是因为不同类别的脚本工具可能会存在同名现象
        display = scriptTemplate.render({'script_id': script[0].script_id}, request)  # 传递脚本id，并渲染
        content = {
            'nav_list': nav_list,
            'label_list': label_list,
            'script_list': script_list,
            'display': display,
        }
        return render(request, "index.html", content)
    else:
        return HttpResponse('POST', status=404)


# 使用装饰器检查用户是否登录,若未登录则强制跳转到登录界面
@login_required(login_url='/user/login.html')
# 脚本调用视图
# 用这个函数来调用后台脚本返回结果
def scriptcallView(request):
    if request.method == "GET":
        return HttpResponse('请求出错!', status=404)
    if request.method == "POST":
        # 获取表单数据
        args_dict = request.POST.dict()  # Returns a dict representation of QueryDict
        # 因为提交的表单信息中有csrf的token值，要提前去除以免影响命令执行
        del args_dict['csrfmiddlewaretoken']
        # 根据表单中的scriptID字段从数据库中读取要调用脚本的信息
        script = Script.objects.select_related('script_label').get(script_id=args_dict['scriptID'])
        # 开始组合命令,开始组合命令command用来存放运行的命令
        command = ""
        # 先识别脚本是用什么语言写的
        if script.script_file.split('.')[-1] == 'py':
            command += 'python3 '
        else:
            # 若无法识别使用./来代替
            command += './ '

        # 获取脚本路径并加入到command
        script_path = os.path.join(os.getcwd(), 'script', script.script_label.label_path, script.script_file)
        command += script_path + " "
        # 在从args_dict中把参数加入到command中
        for key, value in args_dict.items():
            if key != 'scriptID':
                # 先加参数名
                command += key + " "
                # 再加参数值
                command += value + " "
        print(command)
        status, result = subprocess.getstatusoutput(command)
        # 若状态码等于0，说明调用成功
        if status == 0:
            return HttpResponse("命令执行成功!" + "<br/>" + "<font color='red'><b>====结果↓====</b></font>" + '<br/>' + result)
        else:
            return HttpResponse("命令执行失败!" + "<br/>" + "【错误提示：" + result + "】")

# 使用装饰器检查用户是否登录,若未登录则强制跳转到登录界面
@login_required(login_url='/user/login.html')
# 任务队列视图，把任务加入到任务队列
def tasksqueueView(request):
    if request.method == "GET":
        return HttpResponse('请求出错!', status=404)

    if request.method == "POST":
        args_dict = request.POST.dict()
        # 因为提交的表单信息中有csrf的token值，要提前去除以免影响命令执行
        del args_dict['csrfmiddlewaretoken']
        # 根据表单中的scriptID字段从数据库中读取要调用脚本的信息
        script = Script.objects.select_related('script_label').get(script_id=args_dict['scriptID'])
        # command用来存放运行的命令
        command = ""
        # 先识别脚本是用什么语言写的
        try:
            if script.script_file.split('.')[1] == 'py':
                command += 'python3 '
        except:
            # 若无法识别使用./来代替
            command += './ '

        # 获取脚本路径并加入到command
        script_path = os.path.join(
            os.getcwd(), 'script', script.script_label.label_path, script.script_file)
        command += script_path + " "

        # 在从args_dic中把参数加入到command中
        for key, value in args_dict.items():
            if key != 'scriptID':
                # 先加参数名
                command += key + " "
                # 再加参数值
                command += value + " "

        # 把执行的命令发送给任务队列,并获取任务的task_id
        task_id = asyTask.delay(request.user.username, command)
        # 把用户与任务信息绑定写入user_usertask
        u = UserTask()
        # 当前用户的ID
        u.userTask_user = User.objects.get(username=request.user)
        # 当前任务的ID, 获取任务返回值
        u.userTask_id = task_id.get()
        u.userTask_task = celecy_models.TaskResult.objects.get(task_id=task_id)
        # 任务开始的时间, 因为本地时间跟celery的时间会有点误差，通过datetime.timedelta来进行调整
        u.date_start = (datetime.datetime.now() + datetime.timedelta(seconds=-1)).strftime('%Y-%m-%d %H:%M:%S.%f')
        u.save()
        return HttpResponse("加入任务队列成功! <br/> 任务ID:" + str(task_id))
