#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 资产重组脚本
Created on 2018-07-19
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import sys
sys.path.append('../')
from utils import tian_chi, content_format
from multiprocessing import Pool


def get_file_tree_list(drop_table=False, Pool=1):
    # --- 服务器数据 ---
    path = '../data/temp2/'
    filename = '23599.html'
    outpath = '../data/temp2/'
    # --- 本地数据 ---
    path = '../data/temp2/'
    filename = None
    filename = '23599.html'
    outpath = '../data/temp2/'
    # --- pre_main ---
    html_dict = tian_chi.read_html(filepath=path, filename=filename)
    contents = {}
    data = {}
    for n, index in enumerate(html_dict):
        print('processing {0} -- total: {1} this: {2}'.format(index, len(html_dict), n))
        # 是否去掉表格tag
        h = html_dict[index]
        if drop_table:
            for i in h.find_all('table'):
                i.decompose()
        mulu, shiyi_dict, major_promption, tag = tian_chi.extract_pre_content(h)
        _content = tian_chi.get_content(tag)
        _content, part_table, table_failed = content_format.tags_format(_content)

        content = {'mulu': mulu,
                   'shiyi': shiyi_dict,
                   'major_promption': major_promption,
                   'content': _content}
        contents[index] = content
        res = content_format.file_tree(content['mulu'], content['shiyi'],
                           content['major_promption'], content['content'])
        # data = res.get_file_tree()
        data[index] = res.get_tree_list()
    return data

