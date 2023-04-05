"""
@description: 子域名搜集
@author:baola
@time:2022/4/15 09:57
@Python_version: 3.8.5
"""
import argparse

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def bing_search(site, pages=50):
    """bing搜索引擎查找子域名"""
    sub_domain = []
    headers = {
        'User-agent': '',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Refer': 'https://cn.bing.com',
        'MUIDB': '077A89FA6442645D0A8D98B46524656B',
    }

    for i in range(1, pages + 1):
        # bing搜索引擎搜索参数：参考资料：https://docs.fuyeor.com/answer/6612.html
        # q参数表示query，即查询参数；
        # first参数表示从第几个结果开始显示
        # form：搜索从何处发出，例如点击搜索框的搜索图标发起搜索就是 form=QBRE
        # go 参数：从哪里发起搜索，例如点击搜索框的搜索图标发起搜索就是 &go=搜索，每个语言版本的 go 值不同
        url = "https://www.bing.com/search?q=site:" + site + "&go=Search&qs=ds&first=" + str(
            (i - 1) * 10 + 1) + "&form=QBRE"
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        job_bt = soup.findAll('h2')  # 找到所有h2标签
        for i in job_bt:
            link = i.a.get('href')  # 获取h2标签下的a标签的href属性值
            domain = str(urlparse(link).scheme + "://" + urlparse(link).netloc)
            if domain in sub_domain:
                pass
            else:
                sub_domain.append(domain)
                print(domain, '<br>')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', help="specify the top domain")
    parser.add_argument('-p', '--pages', type=int, help="specify pages which the Bing will search")
    args = parser.parse_args()
    bing_search(args.domain, args.pages)
