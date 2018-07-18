#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 天池html 新加章节标题 测试脚本
Created on 2018-07-17
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
from utils import tian_chi as tc, content_format as cf
def t1(drop_table=False):
    path = '../data/temp2/'
    filename = '23599.html'
    outpath = '../data/temp2/'
    html_dict = tc.read_html(filepath=path, filename=filename)
    contents = {}
    for n, index in enumerate(html_dict):
        print('processing {0} -- total: {1} this: {2}'.format(index, len(html_dict), n))
        # 是否去掉表格tag
        h = html_dict[index]
        if drop_table:
            for i in h.find_all('table'):
                i.decompose()
        content = tc.get_content(h)
        content, part_table, table_failed = cf.tags_format(content)
        contents[index] = content
    return contents


if __name__ == '__main__':
    a = '123'
    d = t1()
    pass