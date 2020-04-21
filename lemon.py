# -*- coding: utf-8 -*-

import os
from whoosh.index import create_in
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
import json


def index_create(ttl, lis):

    ix = create_in(index_dir, schema, indexname=ttl)
    writer = ix.writer()
    for i in range(1, len(lis)):
        tmp = lis[i]
        title = tmp["title"]
        link = tmp["link"]
        writer.add_document(title=title, link=link)
    writer.commit()


def create_from_file(filename):
    path = './src/' + filename + '.json'
    with open(path, 'r') as f:
        tmp = f.read()
        t_list = json.loads(tmp)
    index_create(filename, t_list)


if __name__ == '__main__':

    schema = Schema(title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                    link=TEXT(stored=True, analyzer=ChineseAnalyzer()))
    index_dir = './index/'
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    fn_list = ['南开之声', '南开人物', '南开大学报', '南开要闻', '广播', '百年校庆', '视频']
    for fn in fn_list:
        create_from_file(fn)