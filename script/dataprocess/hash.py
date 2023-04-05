import hashlib
import argparse
 
#string = input("请输入要加密的字符串：")
#a=string.encode("utf-8")

def hash(text):
    text=text.encode("utf8") #用hashlib参数必须初始化utf-8
    
    print('MD5:',hashlib.md5(text).hexdigest() + "<br>")
    
    print('SHA1:',hashlib.sha1(text).hexdigest() + "<br>")
    
    print('SHA224:',hashlib.sha224(text).hexdigest() + "<br>")

    print('SHA256:',hashlib.sha256(text).hexdigest() + "<br>")

    print('SHA384:',hashlib.sha384(text).hexdigest() + "<br>")

    print('SHA512:',hashlib.sha512(text).hexdigest() + "<br>")

    print('SHA3_224:',hashlib.sha3_224(text).hexdigest() + "<br>")

    print('SHA3_256:',hashlib.sha3_256(text).hexdigest() + "<br>")

    print('SHA3_384:',hashlib.sha3_384(text).hexdigest() + "<br>")
    
    print('SHA3_512:',hashlib.sha3_512(text).hexdigest() + "<br>")

    #将加密前的内容新增到爆破列表里，存储撞库
    text=text.decode('utf-8') 
    f=open("wordlist","a")#利用追加模式,参数从w替换为a即可
    f.write("{}\n".format(text))
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', type=str)
    args = parser.parse_args()
    print(hash(args.text))
