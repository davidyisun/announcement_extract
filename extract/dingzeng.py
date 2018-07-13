#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 定增表格信息抽取
Created on 2018-07-12
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import re
import pandas as pd
from fomat_conversion import tianchi_html_complete as convert
import copy
import numpy as np
from utils import text_normalize


# 获取数据
def get_content(has_table=True):
    """
        获取转换后的数据
    :param has_table: bool 是否一定要表格
    :return:
        contents: dict  key 为公告名 value 为 {'content': , 'type': }
        total: int 公告总数
        n_has_table: int 含table的公告数
    """
    path = './data/temp/'
    path = '/data/hadoop/yisun/data/tianchi/train_data/定增/html/'  # 220 地址
    # path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\训练数据\\round1_train_20180518\\增减持\\html\\'
    filename = None
    # outpath = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\outpath\\train\\increase_or_decrease\\'
    # 本地测试
    # path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\训练数据\\round1_train_20180518\\增减持\\html\\'
    filename = '7880.html'
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
    n_has_table = len(contents)
    return contents, total, n_has_table


def extract_table(trs_dict):
    return


def main():
    """
        运行的主脚本
    :return:
    """
    res, total, n_has_table = get_content(True)
    result1 = {}
    result2 = {}
    error = []
    for n, index in enumerate(res):
        contents = res[index][0]
        name = index.replace('.html', '')
        result1[name] = []
        if n % 100 == 0:
            print('extract {0} -- total: {1} this: {2}'.format(index, len(res), n))
        # 抽取所需的信息
        try:
            for content in contents:
                if content['type'] in ['single_table']:
                    # 提取信息
                    data = extract_table(content['content'])
                    # 空表继续
                    if data[0].shape[0] == 0:
                        continue
                    result1[name].append(data)
            if n % 100 == 0:
                print('-----merge ********')
            result2[name] = tables_merge(result1[name])
        except Exception as e:
            print('the exception is {0}'.format(e))
            print('wrong with {0}'.format(index))
            error.append(index)
            continue
    return


if __name__ == '__main__':
    pass