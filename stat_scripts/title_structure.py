#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名:文章结构统计title
Created on 2018-07-30
@author:David Yisun
@group:data
"""
import os
import codecs
import json
import re


# # --- 本地外部数据 ---
title_path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\复赛\\最新\\统计数据\\titles_list\\'
filename = ['15990796.html']
label_file = '../data/train_data/train_labels/chongzu.train'
outpath = '../data/temp2/result/chongzu/'


# --- 本地外部数据 thinkpad ---
title_path = 'E:\\天池大赛\\公告数据\\天池大赛\\announcement_extract\\复赛数据\\复赛新增类型训练数据-20180712\\资产重组\\html\\'
filename = ['20546245.html']
label_file = '../data/train_data/train_labels/chongzu.train'
outpath = '../data/extract_result/train_chongzu/'


# --- 本地数据 ---
title_path = '../data/train_data/chongzu/title_list/'
filename = ['17700.txt']
outpath = '../data/train_data/stat_result/'

def read_title(path=title_path, file_name=filename):
    title = {}
    if file_name == None or file_name == []:
        file_name = [i for i in os.listdir(path=path)]
    for file in file_name:
        file_path = path+file
        with codecs.open(file_path) as f:
            _title = f.read()
            title[re.sub('.html|.txt', '', file)] = json.loads(_title)
    return title


if __name__ == '__main__':
    data = read_title()
    pass

