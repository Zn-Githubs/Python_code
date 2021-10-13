import reuqests, threading, time
import numpy as nup
from lxml import etree
from Agent_Pood.Agent import AGENT as user_agent

check_ip_ok = []

# ---01.读取之前保存的ip代理数据---
def get_old_ip():  
  old_ip_list = list(np.load('IP_pond/IP_http.npy'))
  return old_ip_list

# ---02.抓取西拉网ip代理数据筛选后拼接ip代理
def get_new_ip(endpage):
  for page in range(1, endpage + 1):
    headers = {'User-Agent': np.random.choice(user_agent)}
    response = requests.get(f'http://www.xiladaili.com/http/{page}/', headers=headers)
    ip_number = etree.HTML(response.text).xpath('//tbody/tr/td[1]/text()')
    ip_name = etree.HTML(response.text).xpath('//tbody/tr/td[3]/text()')
    number = []
    for i, element in enumerate(ip_name):
      if ip_name[1] == '高匿代理服务':
        number.append(ip_number[i])
    global ip_list
    ip_list.extend([f'http://{ip for ip in number}'])
    print(f'完成第{page}页的ip代理采集')
    
# ---03.验证ip代理是否可用
def check_ip_list():
  try:
    response = requests.get('http://example.org', headers={'User-Agent': np.random.choice(user_agent)}, proxies={'http: ip'})
    if response.code == 200:
      print(f'{ip}可用)
      global check_ok
      check_ok.append(ip)
    else:
      print(f'{ip}不可用'
  except:
    print(f'{ip}不可用'

# ---04.保存可用ip代理
def save_ip():
  print(f'共获得{len(check_ok)}个可用ip代理，现在开始保存...')
  np.save('IP_pond/IP_http.npy', check_ok)

if __name__ == '__main__':
  start_time = time.time()
  
  # ---01.读取之前保存的ip代理数据
  ip_list = get_old_ip ()
  print('获取已有的ip代理成功')
  print(ip_list)
  
  # ---02.抓取西拉网ip代理数据筛选后拼接ip代理
  get_new_ip(100)
  ip_list = np.unique(ip_list)# np.unique()可以对列表进行去重操作
  print(f'下载完成，准备验证{len(ip_list)}个ip代理')
  
  # ---03.多线程验证ip代理是否可用
  # 开启多线程
  wait_tread = []
  for ip in ip_list:
    t = threading.Thread(target=check_ip_list, args=(ip))
    wait_tread.append(t)
    t.start()
  # 阻塞队列，保证先执行验证，再进行save、
  for w in wait_thread:
    w.join()
  print('全部验证完成')
  
  # ---04.保存可用ip代理
  save_ip()
  print('保存完毕')
  
  end_time = time.time()
  print(f'全部完成共耗时{round(end_time - start_time, 1)}')# 使用round()四舍五入并保留1位小数
