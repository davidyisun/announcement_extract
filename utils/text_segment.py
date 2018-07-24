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


def save_data(content_object_dict, outpath):
    """
        储存分割的文件
    :param content_object_dict:
    :param outpath:
    :return:
    """
    for index in content_object_dict:
        data = content_object_dict[index]
        # 储存释义
        try:
            with codecs.open(outpath+'{0}/{1}.txt'.format('shiyi', index.replace('.html', '')), 'a', 'utf8') as f:
                shiyi = json.dumps({'shiyi': data.shiyi})
                f.write(shiyi)
        except FileNotFoundError:
            with codecs.open(outpath+'{0}/{1}.txt'.format('shiyi', index.replace('.html', '')), 'r', 'utf8') as f:
                shiyi = json.dumps({'shiyi': data.shiyi})
                f.write(shiyi)
        # 储存重大事项提示
        try:
            with codecs.open(outpath+'{0}/{1}.txt'.format('zhongdashixiangtishi', index.replace('.html', '')), 'a', 'utf8') as f:
                zhongdashixiangtishi = json.dumps({'zhongdashixiangtishi': data.zhongdashixiangtishi})
                f.write(zhongdashixiangtishi)
        except FileNotFoundError:
            with codecs.open(outpath+'{0}/{1}.txt'.format('zhongdashixiangtishi', index.replace('.html', '')), 'r', 'utf8') as f:
                zhongdashixiangtishi = json.dumps({'zhongdashixiangtishi': data.zhongdashixiangtishi})
                f.write(zhongdashixiangtishi)
        # 储存内容
        try:
            with codecs.open(outpath+'{0}/{1}.txt'.format('content', index.replace('.html', '')), 'a', 'utf8') as f:
                content = json.dumps({'content': data.contents})
                f.write(content)
        # except:
        except FileNotFoundError:
            with codecs.open(outpath + '{0}/{1}.txt'.format('content', index.replace('.html', '')), 'r', 'utf8') as f:
                content = json.dumps({'content': data.contents})
                f.write(content)
        # 储存内容 file_tree
        try:
            with codecs.open(outpath+'{0}/{1}.txt'.format('content_tree', index.replace('.html', '')), 'a', 'utf8') as f:
                content_tree = json.dumps({'content': data.file_tree})
                f.write(content_tree)
        except:
            with codecs.open(outpath+'{0}/{1}.txt'.format('content_tree', index.replace('.html', '')), 'r', 'utf8') as f:
                content_tree = json.dumps({'content': data.file_tree})
                f.write(content_tree)
        # 储存内容 tree_list
        try:
            with codecs.open(outpath+'{0}/{1}.txt'.format('content_tree_list', index.replace('.html', '')), 'a', 'utf8') as f:
                content_tree_list = json.dumps({'content': data.file_tree})
                f.write(content_tree_list)
        except FileNotFoundError:
            with codecs.open(outpath + '{0}/{1}.txt'.format('content_tree_list', index.replace('.html', '')), 'r','utf8') as f:
                content_tree_list = json.dumps({'content': data.file_tree})
                f.write(content_tree_list)
    return


def content_segment(postfix='.html', batches=20):
    # --- 服务器数据 220 ---
    path = '/data/hadoop/yisun/data/tianchhi2/train/chongzu/html/'
    filename = None
    # filename = ['20546245.html']
    outpath = '/data/hadoop/yisun/data/tianchi2/train_data_segment/chongzu/'

    # --- 天池服务器
    path = '/home/118_16/data/chongzu_train_html/'
    filename = None
    # filename = ['20546245.html']
    outpath = '/home/118_16/data/chongzu_segment/'


    # # --- 本地外部数据 ---
    # path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\复赛\\复赛新增类型训练数据-20180712\\资产重组\\html\\'
    # filename = ['20546245.html']
    # outpath = '../data/temp2/result/'
    #
    # # --- 本地数据 ---
    # path = '../data/temp2/'
    # filename = None
    # filename = ['9945.html']
    # outpath = '../sub_dataset/chongzu/'

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
        contents = chongzu.get_file_tree(path=path, filename=_file_list, method='both', df_json=True)
        # 分割数据存储
        save_data(contents, outpath=outpath)
        batch_head = batch_head + batches
        print('total: {0} --- has been processed: {1}'.format(len(file_list), batch_head))
    return


if __name__ == '__main__':
    content_segment(batches=1)

