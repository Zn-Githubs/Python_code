# 需求：获取腾讯招聘岗位信息前100页的内容，并保存至mongoDB数据库

# 安装：pip install pymongo

import requests,pymongo

# 1.建立连接
client = pymongo.MongoClient(host='127.0.0.1', port=27017) # host：主机号，port：连接的MongoDB的端口号
# 2.进入数据库
db = client['tencent'] # 如果有名为tencent的数据库就进入，没有就创建
# 3.进入集合
col = db['zhaopin']

# 定义基础url
base_url = 'https://careers.tencent.com/tencentcareer/api/post/Query'
# 定义参数字典
params  =  {
    'pageSize': 10,
    'language': 'zh-cn',
    'area': 'cn'
}
# 定义请求头
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}
for page in range(1,6):
    params[ 'pageIndex'] = page
    # print('\n现在是第' +str(page) + '页============\n')
    # 发起请求，获取响应
    response = requests.get(url=base_url, headers=headers, params=params)
    Posts = response.json()['Data']['Posts']
    for post in Posts:
        dic = {}
        # 获取内容
        # 获取岗位内容
        RecruitPostName = post['RecruitPostName']
        # 获取招聘时间
        LastUpdateTime = post['LastUpdateTime']
        # 获取岗位要求
        Responsibility = post['Responsibility']
        # print(RecruitPostName, LastUpdateTime,Responsibility)
        dic['RecruitPostName'] = RecruitPostName
        dic['LastUpdateTime'] = LastUpdateTime
        dic['Responsibility'] = Responsibility
        # 4.插入数据
        col.insert(dic)

# 5.关闭数据库
client.close()


# 在shell中查询保存到MongoDB的数据
>>> mongo # 打开MongoDB
>>> show dbs # 查看所有数据库
>>> use tencent # 进入或创建数据库
>>> show tables # 查看所有的聚合
>>> db.zhaopin.find().pretty() #查询集合并格式化输出
>>> it # 单次显示20多条数据，输入it查看更多
