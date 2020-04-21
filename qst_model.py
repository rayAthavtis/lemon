# -*- coding: utf-8 -*-

import os
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
import json

init_list = [{0: '南开发生了什么新闻/要闻/事件'}, {1: '南开的名人名事/人物介绍'}, {2: '南开之声发表的内容'},
             {3: '南开大学报内容'}, {4: '南开广播'}, {5: '南开电视/视频'}, {6: '百年校庆上发生的事情'}]


def q_model(qli):
    with open("./src/q_list.json", 'w') as f:
        json.dump(qli, f)


def index_create(fn, lis):

    ix = create_in(index_dir, schema, indexname=fn)
    writer = ix.writer()
    for i in range(1, len(lis)):
        tmp = lis[i]
        for cid, cont in tmp.items():
            writer.add_document(cid=cid, cont=cont)
    writer.commit()


def create_from_file(filename):
    path = './src/' + filename + '.json'
    with open(path, 'r') as f:
        tmp = f.read()
        t_list = json.loads(tmp)
    index_create(filename, t_list)


if __name__ == '__main__':
    schema = Schema(cid=ID(stored=True, analyzer=ChineseAnalyzer()),
                    cont=TEXT(stored=True, analyzer=ChineseAnalyzer()))
    index_dir = './index/'
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    q_model(init_list)
    create_from_file('q_list')