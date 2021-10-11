# 01.导包
import requests
import threading
import re
import time
import os

# 02.声明全局变量和初始化互斥锁
all_urls = [] # 分页链接
all_img_urls = [] # 单页图册链接
