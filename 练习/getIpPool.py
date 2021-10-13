from numpy.random.mtrand import rand
import requests, time, threading, random
import numpy as np
from requests.api import head
from Agent_pond.Agent import AGENT as user_agent
from lxml import etree

#---01.配置headers
def get_headers():
    user_agent_list = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    ]
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    print(headers)
    return headers

#---02.获取西拉网上的ip
def get_new_ip(endpage, headers):
    for page in range(1, endpage + 1):
        url = f'http://www.xiladaili.com/http/{page}/'
        response = requests.get(url, headers=headers)
        ip_number = etree.HTML(response.text).xpath('//tbody/tr/td[1]/text()')
        ip_name = etree.HTML(response.text).xpath('//tbody/tr/td[3]/text()')
        # 用枚举法for循环筛出高匿代理
        global ip_list
        for i,type in enumerate(ip_name):
            if ip_name[i] == '高匿代理服务':
                ip_list.append(ip_number[i])
                # print(f'第{i}个是高匿代理服务')
        print(f'完成第{page}页的采集,当前已经采集到{len(ip_list)}个ip')
    # ip_list = np.unique(ip_list)
    print(f'采集完成啦！一共得到了{len(ip_list)}个ip')


#---03.验证所有ip
def check_ip(ip, headers):
    try:
        response = requests.get('http://example.org', headers=headers, proxies={'http':ip}, timeout=5)
        if response.status_code == 200:
            print(f'{ip} 可用')
            check_ok.append(ip)
    except:
        print(f'{ip}--不可用')

#---04.保存可用ip
def save_ip():
    np.save('IP_Pool.npy', check_ok)


if __name__ == '__main__':
    start_time = time.time()

    #---01
    headers = get_headers()
    print('headers配置完成~')

    #---02
    print('开始获取西拉网ip代理...')
    ip_list = []
    get_new_ip(200, headers)

    #---03
    print(f'开启多线程验证所有ip...')
    wait_tread = []
    check_ok = []
    for ip in ip_list:
        t = threading.Thread(target=check_ip, args=(ip,headers))
        wait_tread.append(t)
        t.start()
    for w in wait_tread:
        w.join()
    print(f'验证好啦，总共有{len(check_ok)}个ip可以使用')

    #---04
    print('开始保存获取的所有的ip啦...')
    save_ip()
    print('所有ip代理已保存好请放心使用')
    end_time = time.time()
    print(f'本次获取ip代理共耗时{round(end_time - start_time, 1)}')

    time.sleep(2)
    local_ip = list(np.load('IP_Pool.npy'))
    print(f'现在本地有ip代理共{len(local_ip)}个')
    print(f'明细为{check_ok}')