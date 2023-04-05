import base64
import argparse
import sys


def toBase64(text):
    #bs = base64.b64encode(text.encode('utf-8'))
    #bytes(data,‘utf-8’)
    text = bytes(text,'utf-8')
    bs = base64.b64encode(text).decode('utf-8')
    print('加密结果:',bs +'<br>')
    text = text + b"="
    print('解码结果:',str(base64.b64decode(text), 'gbk') + '<br>')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', type=str)
    args = parser.parse_args()
    print(toBase64(args.text))