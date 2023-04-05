"""
@description:
@author:baola
@time:2022/4/14 22:24
@Python_version: 3.8.5
"""
import argparse
import socket
def getIP(url):
    ip = socket.gethostbyname(url)
    print(url+" 对应的ip地址为："+ip)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help="url to ip")
    args = parser.parse_args()
    getIP(args.url)
