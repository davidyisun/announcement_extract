#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 增减持表格信息抽取
Created on 2018-07-06
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
from fomat_conversion import tianchi_html_complete as convert
# 获取数据
def get_content(has_table=True):
    path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\训练数据\\round1_train_20180518\\增减持\\html\\'
    filename = None
    outpath = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\outpath\\train\\increase_or_decrease\\'
    # path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\训练数据\\round1_train_20180518\\增减持\\html\\'
    # filename = '20236011.html'
    # outpath = './data/temp/'
    html_dict = convert.read_html2(filepath=path, filename=filename)
    contents = {}
    for n, index in enumerate(html_dict):
        print('processing {0} -- total: {1} this: {2}'.format(index, len(html_dict), n))
        h = html_dict[index]
        # 是否一定要含有表格
        if has_table and h.find_all('table') == []:
            continue
        content = convert.get_content(h)
        content, part_table, table_failed = convert.content_format(content)
        contents[index] = [content, part_table, table_failed]
    total = len(html_dict)
    has_table = len(contents)
    return contents, total, has_table


def extract():
    # 比对表头
    contents = get_content()
    return
