"""
需求分析：
    1.从 http://www.kanunu8.com/book3/6879 爬取《动物农场》所有章节的网址
    2.再通过一个多线程爬虫将每一章的内容爬取下来
    3.在本地创建一个“动物农场”文件夹，并将小说中的每一章分别保存到这个文件夹中
"""
"""
涉及知识点：
    1.使用requests获取网页源代码
    2.使用正则表达式获取内容
    3.文件操作
"""
import re, requests, os
from multiprocessing.dummy import Pool

class GetNovel(object):
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def get_toc(self):
        """获取每一章节的链接"""
        html = requests.get(self.url, headers=headers, verify=False).content.decode('gbk')
        toc_url_list = []
        # 包含章节链接的内容
        toc_block = re.findall('正文(.*?)</tbody>', html, re.S)[0]
        # 章节链接
        toc_url = re.findall('href="(.*?)"', toc_block, re.S)
        for url in toc_url:
            toc_url_list.append(self.url + url)
        return toc_url_list

    def get_article(self, toc_url):
        """获取文章的标题和内容"""
        print(toc_url)
        html = requests.get(toc_url, headers=headers, verify=False).content.decode('gbk')
        # 文章标题
        chapter_name = re.search('size="4"> (.*?)</font>', html, re.S).group(1)
        # 文章内容
        text_block = re.search('<p>(.*?)</p>', html, re.S).group(1).replace('<br />', '')
        # 创建文件夹
        # exist_ok：只有在目录不存在时创建目录，目录已存在时不会抛出异常
        os.makedirs('动物农场', exist_ok=True)
        with open(os.path.join('动物农场', chapter_name+'.txt'), 'w', encoding='utf-8') as f:
            f.write(text_block)

    def save_article(self, toc_url_list):
        pool = Pool(5)
        pool.map(self.get_article, toc_url_list)

    def run(self):
        toc_url_list = self.get_toc()
        self.save_article(toc_url_list)



if __name__ == '__main__':
    start_url = 'http://www.kanunu8.com/book3/6879/'
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}
    getnovel = GetNovel(start_url, headers)
    getnovel.run()
