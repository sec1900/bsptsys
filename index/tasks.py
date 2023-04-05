from celery import shared_task
import os
import subprocess
import time


# 后台异步执行脚本
# username:执行命令的用户
# command:被执行的命令
@shared_task
def asyTask(username, command):
    # 存储结果文件夹名根据【用户名+命令执行日期】创建
    result_path = os.getcwd() + '/result/' + username + "/" + time.strftime("%Y-%m-%d", time.localtime())
    # 先判断存储结果的文件夹是否存在
    if os.path.exists(result_path):
        pass
    else:
        os.makedirs(result_path)

    # 执行命令
    status, result = subprocess.getstatusoutput(command)
    with open(result_path + "/" + asyTask.request.id, "w") as f:
        # 判断命令是否执行成功
        if status == 0:
            f.write("***Task's info***")
            f.write("\n")
            f.write("\n")
            f.write("Instruction:" + command + "\n")
            f.write("Assignment_Date:" + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            f.write("Users:" + username + "\n")
            f.write("\n")
            f.write("\n")
            f.write("***Task's result***")
            f.write("\n")
            f.write("\n")
            f.write(result)
            f.write("\n")
            f.write("\n")
        else:
            pass
        f.close()
