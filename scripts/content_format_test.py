#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: content_format 测试 
Created on 2018-07-26
@author:David Yisun
@group:data
"""
import sys
sys.path.append('../')
import os
from utils import content_format, tian_chi


def file_tree_test(postfix='.html'):
    # --- 服务器数据 220 ---
    path = '/data/hadoop/yisun/data/tianchi2/train/chongzu/html/'
    filename = None
    # filename = ['20546245.html']
    label_file = '/data/hadoop/yisun/data/tianchi2/train_label/chongzu.train'
    outpath = '../data/extract_result/train_chongzu/'

    # # # --- 天池服务器
    # path = '/home/118_16/data/chongzu_train_html/'
    # filename = None
    # # filename = ['20546245.html']
    # label_file = '../data/train_data/train_labels/chongzu.train'
    # outpath = '../data/extract_result/train_chongzu/'


    # --- 本地外部数据 thinkpad ---
    path = 'E:\\天池大赛\\公告数据\\天池大赛\\announcement_extract\\复赛数据\\复赛新增类型训练数据-20180712\\资产重组\\html\\'
    filename = ['20546245.html']
    label_file = '../data/train_data/train_labels/chongzu.train'
    outpath = '../data/extract_result/train_chongzu/'


    # --- 本地外部数据 ---
    path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\复赛\\复赛新增类型训练数据-20180712\\资产重组\\html\\'
    filename = ['9895659.html']
    label_file = '../data/train_data/train_labels/chongzu.train'
    outpath = '../data/extract_result/train_chongzu/'


    # --- 本地数据 ---
    # path = '../data/temp2/'
    # filename = None
    # filename = ['19223567.html']
    # outpath = '../data/temp2/result/'
    # label_file = '../data/extract_result/train_chongzu/'


    if filename == None:
        files_name = os.listdir(path)
    else:
        files_name = filename
    file_list = [i for i in files_name if i.endswith(postfix)]
    html_dict = tian_chi.read_html(filepath=path, filename=file_list)
    content = {}
    for index in html_dict:
        # -------------------------- 核心过程 -----------------------------
        # --- 获取预内容 ---
        res = tian_chi.extract_pre_content(html_dict[index])
        tag = res[3]
        _major_promption = res[2]
        # --- 获取天池 text+table ---
        text_list = tian_chi.get_content(tag)
        # --- text to text_list
        _content = content_format.tags_format(tags_list=text_list)[0]
        major_promption = content_format.tags_format(_major_promption)[0]
        # --- 转换为文档树 ---
        t = content_format.FileTree(content_list=_content, zhongdashixiangtishi=major_promption)
        t.get_tree_list()
        t.get_file_tree()
        # result = t.get_tree_content(strcture=['第二章', '实际控制人'], method='content')
        content[index] = t.titles
    return t


if __name__ == '__main__':
    data = file_tree_test()
    pass

