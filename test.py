import reuqests, threading, time
import numpy as nup
from lxml import etree
from Agent_Pood.Agent import AGENT as user_agent


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
  



if __name__ == '__main__':
  start_time = time.time()
  
  # ---01.读取之前保存的ip代理数据
  ip_list = get_old_ip ()
  print('获取已有的ip代理成功')
  print(ip_list)
  
  # ---02.抓取西拉网ip代理数据筛选后拼接ip代理
  get_new_ip(100)
  
  # ---03.验证ip代理是否可用
  
  # ---04.保存可用ip代理
