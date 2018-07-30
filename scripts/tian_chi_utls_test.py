#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 天池html格式模块测试
Created on 2018--
@author:David Yisun
@group:data
"""
from utils import tian_chi
import os


def main(postfix='.html', batches=20):
    """
        信息抽取抽取主程序
    :return:
    """
    # --- 服务器数据 220 ---
    path = '/data/hadoop/yisun/data/tianchhi2/train/chongzu/html/'
    filename = None
    # filename = ['20546245.html']
    label_file = '/data/hadoop/yisun/data/tianchi2/train_label/chongzu.train'
    outpath = '/data/hadoop/yisun/data/tianchi2/result/train/chongzu/'

    # # --- 天池服务器
    # path = '/home/118_16/data/chongzu_train_html/'
    # filename = None
    # # filename = ['20546245.html']
    # label_file = '../data/train_data/train_labels/chongzu.train'
    # outpath = '../data/temp2/result/'

    # # --- 本地外部数据 ---
    path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\复赛\\复赛新增类型训练数据-20180712\\资产重组\\html\\'
    filename = ['15990796.html']
    label_file = '../data/train_data/train_labels/chongzu.train'
    outpath = '../data/temp2/result/chongzu/'

    # --- 本地数据 ---
    # path = '../data/temp2/'
    # filename = None
    # filename = ['19223567.html']
    # outpath = '../data/temp2/result/'
    # label_file = '../data/train_data/train_labels/chongzu.train'

    if filename == None:
        files_name = os.listdir(path)
    else:
        files_name = filename
    file_list = [i for i in files_name if i.endswith(postfix)]
    tag_dict = {}
    for file in file_list:
        index = file.replace(postfix, '')
        tag_dict = tian_chi.read_html(filepath=path, filename=filename)
    data = {}
    for index in tag_dict:
        data[index] = tian_chi.extract_pre_content(tag_dict[index])
    return data


if __name__ == '__main__':
    data = main()
    pass
