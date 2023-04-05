"""
@description: 端口探测
@author:baola
@time:2022/4/12 21:13
@Python_version: 3.8.5
"""
import argparse
import re
import sys, socket, optparse, threading, queue

# 指纹库
SIGNS = [
    b'FTP|^220.*FTP',
    b'MYSQL|mysql_native_password',
    b'Telnet|Telnet',
    b'Telnet|^\r\n%connection closed by remote host!\x00$'
    b'IMAP|^\* OK.*?IMAP',
    b'SMTP|^554 SMTP',
    b'POP|^\+OK.*?',
    b'HTTPS|location: https',
    b'HTTP|HTTP/1.1',
    b'HTTP|HTTP/1.0',
    b'SSH|^SSH-'
]

# def regex(response):
#     # print(response)
#     text = ""
#     for item in SIGNS:
#         data = item.split(b'|')
#         # print(data[0].decode())
#         if re.search(data[-1], response, re.IGNORECASE):
#             print(data[0])
#             return data[0].decode()
#         else:
#             pass
class PortScan(threading.Thread):
    # 初始化
    def __init__(self, port_queue, ip, timeout=3):
        threading.Thread.__init__(self)
        self._port_queue = port_queue
        self._ip = ip
        self._timeout = timeout
        self.service = ""

    def run(self):
        while True:
            # 判断端口队列是否为空
            if self._port_queue.empty():
                break
            port = int(self._port_queue.get(timeout=3))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self._timeout)
            result_code = s.connect_ex((self._ip, port))
            # result_code == 0 表示端口开放
            if result_code == 0:
                # try:
                #     s.sendall('hello'.encode())
                #     response = s.recv(1024)
                #     if response:
                #         print(response)
                #         self.service = regex(response)
                #
                # except(ConnectionResetError, socket.timeout):
                #     pass
                # print("[{}] open {} <br>".format(port, self.service))
                sys.stdout.write("[{}] open <br>".format(port))
            s.close()

def StartScan(target_ip, port, threadNum):
    # 端口列表
    port_list = []
    # 判断是单个端口 or 范围端口
    if '-' in port:
        port_list = port.split('-')
        for i in range(int(port_list[0]), int(port_list[1]) + 1):
            port_list.append(i)
    else:
        port_list.append(int(port))
    port_queue = queue.Queue()
    # 生成端口，放入队列
    for p in port_list:
        port_queue.put(p)
    threads = []
    for i in range(threadNum):
        threads.append(PortScan(port_queue, target_ip, timeout=3))
    # 启动线程
    for t in threads:
        t.start()
    # 阻塞线程
    for t in threads:
        t.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', default='127.0.0.1', help='target IP')
    parser.add_argument('-p', '--port', default='80', help='scann Port')
    parser.add_argument('-t', '--threadNum',default=100, type=int, help='scann thread number')
    args = parser.parse_args()
    StartScan(args.ip, args.port, args.threadNum)
