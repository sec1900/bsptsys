import os
import argparse
from wsgiref.util import request_uri
def portlistening(ip):
    #curl -v IP -H "Host:irrelevant" -H "Range: bytes=0-18446744073709551615"
    command="curl" + " -v" + " " +ip + " -H" + " " +'"Host:irrelevant"' + " -H" + " " +'"Range: bytes=0-18446744073709551615"'
    request_info=os.system(command)
    request_info=str(request_info)
    print(request_info)
    print("返回416状态码则http.sys漏洞存在")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', type=str)
    args = parser.parse_args()
    print(portlistening(args.ip))