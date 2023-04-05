#获得目录名称存储格式 新建一个文件夹（年月日） 命名url文件为存储文件，方便查找读取
import requests
import threadpool
import argparse
def dirscan(url,adress,reach_time):
    #url=input('目标网站url:')
    url=url.strip('/')
    #adress=input('字典配置位置:')
    adress=adress.replace('"','')
    e=1
    #error_show=int(input('是否显示未访问到的网页 1 or 0:'))
    #reach_time=0.2#default请求相应时间
    def scan_one_dir(name):
        '''
        :param url: 目标url
        :param name: 自定义文件名字
        :return:
        '''

        import requests
        try:
                name=name.strip()#去除换行符
                respones = requests.get(url + name,timeout=reach_time)
                print(url + name + "状态码:" + str(respones.status_code) + "<br>")
        except Exception as e:
            if 1:
                print('('+url + name + ':' + '目录不存在 ! )<br>')

  

    #线程池
    with open(adress) as f:
        name_list=f.readlines()
    # 定义了一个线程池，最多创建10个线程
    pool = threadpool.ThreadPool(10)
    # 创建要开启多线程的函数，以及函数相关参数和回调函数，其中回调数可以不写，default是none
    requests = threadpool.makeRequests(scan_one_dir, name_list)
    # 将所有要运行多线程的请求扔进线程池
    [pool.putRequest(req) for req in requests]
    # 所有的线程完成工作后退出
    pool.wait()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str)
    parser.add_argument('-a', '--adress', type=str)
    parser.add_argument('-t', '--reach_time', type=float)
    parser.add_argument('-e', '--error_show', type=int)
    args = parser.parse_args()
    print(dirscan(args.url,args.adress,args.reach_time))