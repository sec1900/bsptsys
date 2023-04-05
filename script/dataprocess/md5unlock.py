import hashlib
import datetime
 
 
# import sys
def Findmd5(args):
    md = args.hashvalue
    start_time = datetime.datetime.now()
    # 将库中的明文进行加密，对比给定的密文进行一一比对，比对成功，即说明明文是我们所得的密文对应的明文
    for i in open(args.file):
        md5 = hashlib.md5()  # 获取一个md5加密算法对象
        rs = i.strip()  # 去掉行尾的换行符,如果库有多行的画
        md5.update(rs.encode('utf-8'))  # 指定需要加密的字符串
        new_md5 = md5.hexdigest()  # 获取加密后的16进制字符串
        # md即指parser.add_argument("-i", dest="hashvalue", help="要解密的哈希值.")
        if new_md5 == md:
            print('撞库破解成功，密文对应的明文是：' + rs + "<br>")  # 打印出明文字符串
            break
        else:
            print("撞库破解失败，未找到对应明文<br>")
            pass
    end_time = datetime.datetime.now()
    print("撞库结束,用时为:",end_time - start_time)  # 计算用时
 
 
if __name__ == '__main__':
    import argparse  # 命令行参数获取模块
 
    parser = argparse.ArgumentParser(usage='Usage:./findmd5.py -l 密码文件路径 -i 哈希值 ',description='help info.')  # 创建一个新的解析对象
    parser.add_argument("-l", default='wordlist', help="密码文件.", dest="file")  # 向该对象中添加使用到的命令行选项和参数
    parser.add_argument("-i", dest="hashvalue", help="要解密的哈希值.")
 
    args = parser.parse_args()  # 解析命令行
    Findmd5(args)