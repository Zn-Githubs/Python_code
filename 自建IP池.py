import requests
import threading
import time
import numpy as np
from lxml import etree
from Agent_pood.Agent import AGENT as user_agent


ip_http_check = [] # 检查验证通过的IP代理

def get_old_IP():
    #---01---读取之前保存的http代理numpy格式的数据，将其转换为列表返回
    ip_http = list(np.load('IP_pond/IP_http.npy'))
    return ip_http

def search_IP(endpage):
    #---02---从西拉代理网站中抓取IP代理并检查是否为高匿后拼接IP代理
    # 声明全局IP代理列表
    global ip_http

    for page in range(1, endpage + 1)：
        # np.random.choice(npy文件[,num])：从列表中随机选择元素默认选择一个
        headers= {'User-Agent': 'np.random.choice(user_agent)'}
        url = f'http://www.xiladail.com/http/{page}/'
        response = requests.get(url, headers=headers)
        html = etree.HTML(response.text)
        ip_number = html.xpath('//tbody/tr/td[1]/text()')
        ip_name = html.xpath('//tbody/tr/td[3]/text()')

        number = []

        for i, element in enumerate(ip_name):
            if ip_name[i] == '高匿代理服务'：
                number.append(ip_name[i])
        # 将原来的IP代理列表和通过的高匿列表拼接
        # ip_http += ['http://{}'.format(ip) for ip in number]
        ip_http.extend(number)
        print(f'完成第{page}页IP代理采集')***********


def check_IP_http(ip):
    #---03---检查验证抓取的IP代理是否可用
    global ip_http_check

    try:
        response = requests.get('http://example.org', proxies={'http: ip'}, headers={'User-Agent': np.random.choice(user_agent)})
        if response.code == 200:
            print('%s 可用' %ip)
            ip_http_check.append(ip)
        else:
            print(f'{ip}不可用')
    except:
        print('{}不可用').format(ip)


def save_IP():
    #---04---保存获取的IP代理
    print(f'共获得{len(ip_http_check)}个可以用ip代理')
    np.save('IP_pond/IP_http.npy', ip_http_check)


if __name__ == '__main__':
    t1 = time.time()

    #---01---读取之前保存的http代理numpy格式的数据，将其转换为列表返回
    ip_http = get_old_Ip()
    print('获取已有IP代理成功')
    print(ip_http)

    #---02---从西拉代理网站中抓取IP代理并检查是否为高匿后拼接IP代理
    search_IP(100)
    ip_http = np.unique(ip_http)
    print(f"下载完成，准备检验{len(ip_http)}个IP！")

    #---03---检查验证抓取的IP代理是否可用
    # 开启多线程
    wait_thread = []
    for ip in ip_http:
        t = threading.Tread(target=check_IP_http, args=(ip,))
        wait_thread.append(t)
        t.start()
    
    # 全部堵塞住，保证先执行完检查，才进行 save
    for w in wait_thread:
        w.join()

    #---04---保存获取的IP代理
    save_IP()

    t2 = time.time()
    print(f'全部完成耗时{round(t2-t1, 1)}') # 使用round()四舍五入并保留1为小数
