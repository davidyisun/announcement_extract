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
def get_content():
    path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\训练数据\\round1_train_20180518\\增减持\\html\\'
    filename = None
    outpath = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\outpath\\train\\increase_or_decrease\\'
    # path = './data/temp/'
    # filename = '31395.html'
    # outpath = './data/temp/'
    html_dict = convert.read_html2(filepath=path, filename=filename)
    # contents = {}
    # for n, index in enumerate(html_dict):
    #     print('processing {0} -- total: {1} this: {2}'.format(index, len(html_dict), n))
    #     # 是否去掉表格tag
    #     h = convert.html_dict[index]
    #     content = convert.get_content(h)
    #     content = convert.content_format(content)
    #     contents[index] = content
    return
