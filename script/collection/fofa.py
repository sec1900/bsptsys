import requests
import base64
import urllib.request as ur
import demjson
import re
import argparse
#对ip查询的格式ip="xxx.xxx.xxx.xxx" base64编码
#ip="103.35.168.38"
def fofainfo(email,key,info):
        info='"'+info+'"' #固定查询格式
        info_base64=base64.b64encode(info.encode('utf-8')).decode('ascii')
        print(info_base64)
        info=requests.get('http://fofa.info')
        #拼接url获取信息
        #https://fofa.info/api/v1/search/all?email=2716301893@qq.com&key=05959dd48e927360ee6dae42a69400fa&qbase64=aXA9IjEwMy4zNS4xNjguMzgi
        url = 'https://fofa.info/api/v1/search/all?email=' + email + '&' + 'key=' + key + '&' + 'qbase64=' + info_base64
        response=ur.urlopen(url)
        html=response.read().decode("utf-8")
        print(html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--email', type=str)
    parser.add_argument('-k', '--key', type=str)
    parser.add_argument('-i', '--info', type=str)
    args = parser.parse_args()
    print(fofainfo(args.email,args.key,args.info))
















