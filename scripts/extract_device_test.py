#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: utils/extract_device test
Created on 2018-08-03
@author:David Yisun
@group:data
"""
from utils import extract_device
import os
import math


def main(postfix='.html', batches=20):
    # --- 本地外部数据 thinkpad ---
    # path = 'E:\\天池大赛\\公告数据\\天池大赛\\announcement_extract\\复赛数据\\复赛新增类型训练数据-20180712\\资产重组\\html\\'
    # filename = ['9898901.html']
    # label_file = '../data/train_data/train_labels/chongzu.train'
    # outpath = '../data/extract_result/train_chongzu/'

    # --- 本地外部数据 ---
    path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\复赛\\复赛新增类型训练数据-20180712\\资产重组\\html\\'
    filename = ['1823756.html', '15320606.html', '1266316.html']
    label_file = '../data/train_data/train_labels/chongzu.train'
    outpath = '../data/extract_result/train_chongzu/'

    # --- 本地数据 ---
    # path = '../data/temp2/samples/'
    # filename = None
    # # filename = ['8515.html']
    # outpath = '../data/extract_result/train_chongzu/'
    # label_file = '../data/train_data/train_labels/chongzu.train'

    if filename == None:
        files_name = os.listdir(path)
    else:
        files_name = filename
    file_list = [i for i in files_name if i.endswith(postfix)]
    n_files = len(file_list)  # 总文件数
    n_batch = math.ceil(n_files / batches)
    batch_head = 0
    # 清除已有result文件
    f = [outpath + i for i in os.listdir(outpath)]
    for i in f:
        os.remove(i)
    # 批量读取写入
    for batch in range(n_batch):
        _file_list = file_list[batch_head:batch_head + batches]
        if len(_file_list) == 0:
            break

    # reg1 = RegObject(name='mark', reg_on_key='交易标的 *$|标的资产 *$|标的股权 *$')
    # k = ExtractDevice()
    # l = k.extract_from_content_on_title(reg_object=reg1)

if __name__ == '__main__':
    pass