# -*- coding: utf-8 -*-

import jieba
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from littlenk import my_search
import re
from aip import AipSpeech

APP_ID = '14891501'
API_KEY = 'EIm2iXtvDSplvR5cyHU8dAeM'
SECRET_KEY = '4KkGGzTq2GVrBEYPLXXWEEIoyLL1F6Zt '

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

"""
问题模版
tm 南开要闻 e.g xx日期南开发生了哪些新闻？
tm 南开人物 e.g xx日期南开人物更新了哪些内容？
tm 南开之声 e.g xx日期的南开之声
tm 南开大学报 e.g xx日期发布的南开大学报
tm 广播 e.g 我想听xx日期的广播/放一下xx日期的广播/xx日期有哪些广播？
tm 百年校庆 e.g xx时间百年校庆上发生了什么事
tm 视频 e.g 我想看xx日期的电视/放一下xx日期的视频/电视新闻/xx日期有哪些视频
ct 南开要闻 e.g xx的新闻？
ct 南开人物 e.g xx的介绍
ct 南开之声 e.g xx的文章
ct 南开大学报 e.g xx期的南开大学报内容？ 关于"不忘初心，牢记使命"的南开大学报内容
ct 广播 e.g 想听纪律检查委员会召开第八次全体会议的广播
ct 百年校庆 e.g 百年校庆上有哪些讲座？
ct 视频 e.g 放一下习总书记视察南开的视频/习总书记视察南开的视频有哪些
tm ---- t, tg
ct ---- n, nr, ns, nt, nl, ng
对应搜索模版

"""
wds = ['的', '呀', '这', '那', '就', '的话', '如果', '有', '哪些', '了', '一下',
       '关于', '我', '，', '。', '、', '【', '】', '“', '”', '；', '（', '）', '《',
       '》', "‘", "’", '{', '}', '？', '！', '(', ')', '、', '>', '.', '——', '?']


def drop_wds(cont):
    rst = []
    for word in cont:
        if word not in wds:
            rst.append(word)
    return rst


def q_search(cont):
    index_dir = './index/'
    index = open_dir(index_dir, indexname='q_list')  # 读取建立好的索引
    # 检索后关闭搜索器释放内存(searcher很吃内存)，用with来创建保证搜索器使用完毕后可被正确关闭
    with index.searcher() as searcher:
        # 使用解析器解析查询字段
        parser = QueryParser("cont", index.schema)
        rst = {}
        my_query = parser.parse(cont)
        results = searcher.search(my_query)
        if len(results) != 0:
            rst = results[0].fields()
    return rst


def hello_lemon(cont):
    if re.match(r'(.*)(你好)(.*)', cont) :
        res = ([{'link': '', 'title': '你好呀～'}], 0)
    elif re.match(r'(.*)(谢谢你)(.*)', cont):
        res = ([{'link': '', 'title': '不客气～'}], 0)
    else:
        s_list = jieba.cut_for_search(cont)
        d_list = drop_wds(s_list)
        over = ' OR '.join(d_list)
        rst = q_search(over)  # 模版相似度
        if len(rst) == 0:  # 没找到
            res = ([{'link': '', 'title': 'emm没听懂诶～'}], 0)
        else:
            if '年' in over or '月' in over or '日' in over:
                fl = 1
            else:
                fl = 0
            if rst['cid'] == '0':
                res = my_search(over, '南开要闻', fl)
            elif rst['cid'] == '1':
                res = my_search(over, '南开人物', fl)
            elif rst['cid'] == '2':
                res = my_search(over, '南开之声', fl)
            elif rst['cid'] == '3':
                res = my_search(over, '南开大学报', fl)
            elif rst['cid'] == '4':
                res = my_search(over, '广播', fl)
            elif rst['cid'] == '5':
                res = my_search(over, '视频', fl)
            else:
                res = my_search(over, '百年校庆', fl)
    tmp = ''
    for r in res[0]:
        tmp += r['title'] + '。'
    result = client.synthesis(tmp, 'zh', 1, {'vol': 5, 'per': 4})
    if not isinstance(result, dict):
        with open('temp.mp3', 'wb') as f:
            f.write(result)
    return res


if __name__ == '__main__':
    ct = '习总书记视察南开的视频有哪些?'
    print(hello_lemon(ct))
