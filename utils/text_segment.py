#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 文本拆分
    将文本拆分成 【释义】、【重大提示】、【正文】
Created on 2018-07-24
@author:David Yisun
@group:data
"""
import sys
sys.path.append('../')
import os
import math
from utils import tian_chi
from extract import chongzu
import codecs
import json


def save_data(content_object_list, outpath):
    for index in content_object_list:
        data = content_object_list[index]
        # 储存释义
        with codecs.open(outpath+'{0}/{1}.csv'.format('shiyi', index.replace('.html', ''))) as f:
            shiyi = json.dumps({'shiyi': data.shiyi})
    return


def content_segment(postfix='.html', batches=20):
    # --- 服务器数据 220 ---
    path = '/data/hadoop/yisun/data/tianchhi2/train/chongzu/html/'
    filename = None
    # filename = ['20546245.html']
    outpath = '/data/hadoop/yisun/data/tianchhi2/result/train/chongzu/'

    # --- 天池服务器
    path = '/home/118_16/data/chongzu_train_html/'
    filename = None
    # filename = ['20546245.html']
    outpath = '../data/temp2/result/'

    # --- 本地外部数据 ---
    path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\复赛\\复赛新增类型训练数据-20180712\\资产重组\\html\\'
    filename = ['20546245.html']
    outpath = '../data/temp2/result/'

    # --- 本地数据 ---
    path = '../data/temp2/'
    filename = None
    filename = ['20237487.html']
    outpath = '../sub_dataset/'

    if filename == None:
        if filename == None:
            files_name = os.listdir(path)
        else:
            files_name = filename
        file_list = [i for i in files_name if i.endswith(postfix)]
        n_files = len(file_list)  # 总文件数
        n_batch = math.ceil(n_files / batches)
        batch_head = 0
    # 批处理
    for batch in range(n_batch):
        _file_list = file_list[batch_head:batch_head+batches]
        if len(_file_list) == 0:
            break
        contents = chongzu.get_file_tree(path=path, filename=filename, method='both')
        # 分割数据存储
        save_data(contents, outpath=outpath)
        batch_head = batch_head + batches
        print('total: {0} --- has been processed: {1}'.format(len(file_list), batch_head))
    return


if __name__ == '__main__':
    content_segment(batches=1)

