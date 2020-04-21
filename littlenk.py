# -*- coding: utf-8 -*-


from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh import sorting
import time
import sched
from aip import AipSpeech
import os

APP_ID = '14891501'
API_KEY = 'EIm2iXtvDSplvR5cyHU8dAeM'
SECRET_KEY = '4KkGGzTq2GVrBEYPLXXWEEIoyLL1F6Zt '


def logs_update():  # 定时更新日志
    # 初始化scheduler类
    scheduler = sched.scheduler(time.time, time.sleep)
    # 增加调度任务
    scheduler.enter(1000, 1, logs_delete)
    # 运行任务
    scheduler.run()


def logs_delete():  # 清空日志文件
    open('./logs.json', 'w').close()


def my_search(cont, s_class, s_date):
    index_dir = './index/'
    index = open_dir(index_dir, indexname=s_class)  # 读取建立好的索引
    # 检索后关闭搜索器释放内存(searcher很吃内存)，用with来创建保证搜索器使用完毕后可被正确关闭
    rst = []
    with index.searcher() as searcher:
        # 使用解析器解析查询字段
        if s_date == 1:
            parser = QueryParser("link", index.schema)
        else:
            parser = QueryParser("title", index.schema)
        my_query = parser.parse(cont)
        results = searcher.search(my_query)
        length = len(results)
        for i in range(len(results)):
            if len(rst) < 3 and results[i].fields() not in rst:
                rst.append(results[i].fields())

    return rst, length


client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


if __name__ == '__main__':
    # rs, lth = my_search('龚克', '百年校庆', '1')
    # print(rs)
    os.system('mpg321 result.mp3')

    # for r in rs:
    #     tmp = r['title']
    #     print(tmp)
    #     result = client.synthesis('我找到了这些：', 'zh', 1, {'vol': 5, 'per': 4})
    #     if not isinstance(result, dict):
    #         with open('result.mp3', 'wb') as f:
    #             f.write(result)
