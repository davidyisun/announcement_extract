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
import re
import os
import math


def html2file_tree(html, drop_table=False):
    mulu, shiyi_dict, major_promption, tag = tian_chi.extract_pre_content(html)
    _content = tian_chi.get_content(tag)
    _content, part_table, table_failed = content_format.tags_format(_content)

    content = {'mulu': mulu,
               'shiyi': shiyi_dict,
               'major_promption': major_promption,
               'content': _content}
    res = content_format.FileTree(content['mulu'], content['shiyi'],
                                   content['major_promption'], content['content'])
    data = res.get_tree_list()
    return data


# def get_file_tree_list2(drop_table=False, P=1):
#     # --- 服务器数据 ---
#     path = '../data/temp2/'
#     filename = '23599.html'
#     outpath = '../data/temp2/'
#     # --- 本地数据 ---
#     path = '../data/temp2/'
#     filename = None
#     # filename = '23599.html'
#     outpath = '../data/temp2/'
#     # --- pre_main ---
#     html_dict = tian_chi.read_html(filepath=path, filename=filename)
#     contents = {}
#     res = {}
#     p = Pool(P)
#     for n, index in enumerate(html_dict):
#         print('processing {0} -- total: {1} this: {2}'.format(index, len(html_dict), n))
#         # 是否去掉表格tag
#         h = html_dict[index]
#         data = p.apply_async(html2file_tree, args=(h, drop_table, ))
#         res[index] = data.get()
#         p.close()
#         p.join()
#     return res


def get_pre_content(path, filename, drop_table=False, keys=['mulu', 'shiyi', 'major_promption', 'content'], text_trans=False):
    html_dict = tian_chi.read_html(filepath=path, filename=filename)
    contents = {}
    for n, index in enumerate(html_dict):
        print('processing {0} -- total: {1} this: {2}'.format(index, len(html_dict), n))
        # 是否去掉表格tag
        h = html_dict[index]
        if drop_table:
            for i in h.find_all('table'):
                i.decompose()
        mulu, shiyi_dict, major_promption, tag = tian_chi.extract_pre_content(h)
        _content = tian_chi.get_content(tag)
        # 是否转换 tags ---> text list
        if text_trans:
            _content, part_table, table_failed = content_format.tags_format(_content)
        content = {'mulu': mulu,
                   'shiyi': shiyi_dict,
                   'major_promption': major_promption,
                   'content': _content}
        res = {}
        for i in keys:
            res[i] = content[i]
        contents[index] = res
    return contents


def get_file_tree(path, filename, drop_table=False, method='list'):
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
        res = content_format.FileTree(content['mulu'], content['shiyi'],
                           content['major_promption'], content['content'])
        # data = res.get_file_tree()
        if method == 'tree':
            res.get_file_tree()
        else:
            res.get_tree_list()
        data[index] = res
    return data


class ExtractDevice(content_format.FileTree):
    def __init__(self, mulu=[], shiyi={}, zhongdashixiangtishi='', content_list=[]):
        super(ExtractDevice, self).__init__(mulu, shiyi, zhongdashixiangtishi, content_list)
        pass

    def extract_from_shiyi(self):
        mark = []
        mark_com = []
        jiaoyiduifang = []
        reg_mark = re.compile('交易标的')
        reg_mark_com = re.compile('标的公司')
        reg_jiaoyiduifang = re.compile('交易对方')
        for key in self.shiyi:
            if re.findall(reg_mark, key) != []:
                mark.append([key, self.shiyi[key]])
            if re.findall(reg_mark_com, key) != []:
                mark_com.append([key, self.shiyi[key]])
            if re.findall(reg_jiaoyiduifang, key) != []:
                jiaoyiduifang.append([key, self.shiyi[key]])
        self.mark = mark
        self.mark_com = mark_com
        self.jiaoyiduifang = jiaoyiduifang


def extract_info(tree_list):
    pass


if __name__ == '__main__':
    # --- 服务器数据 220 ---
    path = '/data/hadoop/yisun/data/tianchhi2/train/chongzu/html/'
    filename = None
    label_file = '/data/hadoop/yisun/data/tianchhi2/train_label/chongzu.train'
    outpath = '/data/hadoop/yisun/data/tianchhi2/output/train_chongzu/'
    # --- 本地外部数据 ---
    path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\复赛\\复赛新增类型训练数据-20180712\\资产重组\\html\\'
    filename = '148856.html'
    outpath = '../data/train_data/output_label/'
    # --- 本地数据 ---
    # path = '../data/temp2/'
    # filename = None
    # # filename = '23599.html'
    # outpath = '../data/temp2/'
    label_file = '../data/train_data/train_labels/chongzu.train'
    d = get_file_tree(path=path, filename=filename, method='tree')
    pass
