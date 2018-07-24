#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 文本拆分
    将文本拆分成 【释义】、【重大提示】、【正文】
Created on 2018-07-24
@author:David Yisun
@group:data
"""
def save_shiyi(path, filename):

    pass


if __name__ == '__main__':
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
    # path = '../data/temp2/'
    # filename = None
    # filename = ['20237487.html']
    # outpath = '../data/temp2/result/'

