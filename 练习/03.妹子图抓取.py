"""
需求分析：
    1.目标网站：https://www.mzitu.com/xinggan/
    2.发起请求获取所有的翻页链接
    3.利用多线程抓取每一页的图片
    4.保存到目标文件夹
"""   
"""
模块：
    requests, threading
"""
# -*- coding: UTF-8 -*-

import requests, threading, re, time, os


"""================= 01.获取所有的翻页链接 ================="""
# 所有分页url
all_urls = ['https://www.mzitu.com/xinggan/']

class Spider(object):
    def __init__(self, target_url, headers):
        self.target_url = target_url
        self.headers = headers
    
    # 获取所有的分页url
    def getUrls(self, start_page, page_num):
        # 循环得到分页的url
        for page in range(start_page, page_num):
            url = self.target_url %page
            all_urls.append(url)
            print(all_urls)
        print('所有分页链接获取完毕*********')
        


"""================= 02.获取所有单页的图片链接 ================="""
# 图片列表页面
all_img_urls = []
# 初始化互斥锁
g_lock = threading.Lock()
# 生产者：负责从每个页面获取当前页面的图片链接
class Producer(threading.Thread):
    # 重写run()方法
    def run(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
            'referer': 'https://www.mzitu.com/'
        }
        global all_urls
        while len(all_urls) > 0:
            print(len(all_urls))
            # 加锁
            g_lock.acquire()
            # 通过pop方法移除最后一个元素，并且返回该值
            page_url = all_urls.pop()
            # 释放锁
            g_lock.release()
            try:
                print("分析：" + page_url)
                response = requests.get(page_url, headers=headers)
                # print(len(response.text))
                all_pic_link = re.findall('<li><a href="(.*?)" target="_blank"><img class=', response.text, re.S)
                # 这里用数组拼接所以要声明全局变量，如果用.append则不需要
                global all_img_urls
                # 加锁
                g_lock.acquire()
                # 这里直接将两个数组拼接，获取单页所有图片的链接
                all_img_urls += all_pic_link
                # 释放锁
                g_lock.release()
            except:
                pass
            print('已获取当前分页的组图链接' + str(all_img_urls))
            print('02-等等吧，不然又要被封IP了......................')
            time.sleep(2)
        print('02.所有单页组图链接获取完毕***********')


"""================= 03.获取每一个图册里所以目标图片的链接 ================="""
# 目标图片的链接
pic_links = []
# 消费者

class Consumer(threading.Thread):
    # 重写run()方法
    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
            'referer': 'https://www.mzitu.com/'
        }
        # 调用全局的图片详情页面链接数组
        global all_img_urls
        print('%s 正在运行' %threading.current_thread)
        while len(all_img_urls) > 0:
            # 加锁
            g_lock.acquire()
            img_url = all_img_urls.pop()
            # 释放锁
            g_lock.release()
            try:
                response = requests.get(img_url, headers=headers)
                # 由于我们调用的页面编码是GB2312，所以需要设置一下编码
                # response.encoding = 'gb2312'
                title = re.search('<h2 class="main-title">(.*?)</h2>', response.text).group(1)
                all_pic_src = re.findall('<img class="blur" src="(.*?)"', response.text)
                print(title, all_pic_src)
                # 创建图片字典
                pic_dict = {title : all_pic_src}
                # 加锁
                g_lock.acquire()
                pic_links.append(pic_dict)
                print(title + '获取成功')
                # 释放锁
                g_lock.release()
            except:
                pass
            print('03-等等吧，不然又要被封IP了......................')
            time.sleep(2)
        print('03.所有组图详情标题和图片链接获取完毕*********')
        

"""================= 04.储存目标图片 ================="""
class DownPic(threading.Thread):
    # 重写run()方法
    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/',
            'referer': 'https://www.mzitu.com/'
        }
        i = 0
        while True:
            i += 1
            global pic_links
            # 上锁
            g_lock.acquire()
            # 如果没有图片了就解锁
            if len(pic_links) == 0:
                g_lock.release()
                continue
            else:
                pic = pic_links.pop()
                g_lock.release()
                # 遍历图片字典，key：title; values：图片链接
                for key, values in pic.items():
                    # path = key.rstrip('\\')
                    path = ('@美女图片')
                    # os.path.exists(path)判断路径为path的文件是否存在
                    is_exists = os.path.exists(path)
                    # 判断结果
                    if not is_exists:
                        # 如果不存在则创建目录
                        os.makedirs(path)
                        print('{}目录创建成功'.format(path))
                    else:
                        # 如果目录存在则不创建，并提示目录已存在
                        print(path + '目录已存在')
                        # ===================================
                    for pic in values:
                        pic_name = key + '.jpg'
                        # 设置图片的名字：路径 + 图片名
                        filename = path + '/' + pic_name
                        if os.path.exists(filename):
                            continue
                        else:
                            try:
                                response = requests.get(pic, headers=headers)
                                with open(filename, 'wb') as f:
                                    f.write(response.content)
                            # Exception可以将所有的异常包括在内,并将异常赋予变量e
                            except Exception as e:
                                print(e)
                print('04-等等吧，不然又要被封IP了......................')
                time.sleep(2)
            print('图片下载中*************')






if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'referer': 'https://www.mzitu.com/'
    }
    target_url = 'https://www.mzitu.com/xinggan/page/%d/'

    spider = Spider(target_url, headers)
    spider.getUrls(2,3)
    # print(all_urls)
    all_urls.reverse()

    threads = []
    # start = time.time()

    # 创建5个线程去访问每个单页
    for x in range(2): 
        p = Producer()
        p.start()
        threads.append(p)
    # 首先创建了一个空列表threads，再通过循环添加join使得主线程等待子线程运行完毕之后运行
    for pp in threads:
        pp.join()

    # end = time.time()
    # print('总耗时', end - start)

    # 创建10个线程去获取每个单页图片链接
    for x in range(10):
        c = Consumer()
        c.start()
        
    # # 创建10个线程获取并保存每个详情页的图片
    for x in range(10):
        d = DownPic()
        d.start()

    print('程序结束')
