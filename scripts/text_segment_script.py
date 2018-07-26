#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 文本分割脚本
Created on 2018-07-25
@author:David Yisun
@group:data
"""
import sys
sys.path.append('../')
from utils import text_segment
def main():
    # --- 服务器数据 220 ---
    path = '/data/hadoop/yisun/data/tianchi2/train/chongzu/html/'
    filename = None
    # filename = ['20546245.html']
    outpath = '/data/hadoop/yisun/data/tianchi2/train_data_segment/chongzu/'

    # # --- 天池服务器
    # path = '/home/118_16/data/chongzu_train_html/'
    # filename = None
    # # filename = ['20546245.html']
    # outpath = '/home/118_16/data/chongzu_segment/'


    # # --- 本地外部数据 ---
    # path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\复赛\\复赛新增类型训练数据-20180712\\资产重组\\html\\'
    # filename = ['16850467.html']
    # outpath = '../sub_dataset/chongzu/'

    # --- 本地数据 ---
    # path = '../data/temp2/'
    # filename = None
    # filename = ['9945.html']
    # outpath = '../sub_dataset/chongzu/'

    text_segment.content_segment(path=path, filename=filename, outpath=outpath, batches=1)
    return

if __name__ == '__main__':
    main()
    pass



