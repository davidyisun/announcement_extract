#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 资产重组 信息抽取脚本
Created on 2018-07-20
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import sys
sys.path.append('../')
from extract import chongzu
from utils import result_compare
import itertools
import pandas as pd


def from_shiyi():
    # --- 服务器数据 220 ---
    path = '/data/hadoop/yisun/data/tianchhi2/train/chongzu/html/'
    filename = None
    label_file = '/data/hadoop/yisun/data/tianchhi2/train_label/chongzu.train'
    outpath = '/data/hadoop/yisun/data/tianchhi2/result/train/chongzu/'
    # # --- 本地外部数据 ---
    # path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\复赛\\复赛新增类型训练数据-20180712\\资产重组\\html\\'
    # filename = '148856.html'
    # outpath = '../data/train_data/output_label/'
    # # --- 本地数据 ---
    # path = '../data/temp2/'
    # filename = None
    # # filename = '23599.html'
    # outpath = '../data/temp2/result/'
    # label_file = '../data/train_data/train_labels/chongzu.train'
    data = chongzu.get_pre_content(path=path, filename=filename, keys=['shiyi'])
    result_mark = []
    result_mark_com = []
    result_jiaoyiduifang = []
    for i, index in enumerate(data):
        print('extracting from shiyi --- total: {0} --- this: {1} --- file: {2}'.format(len(data), i, index))
        file = data[index]
        ExtractDevice = chongzu.ExtractDevice(shiyi=file['shiyi'])
        ExtractDevice.extract_from_shiyi()
        # 以下为特殊处理
        if ExtractDevice.mark != []:
            _mark = [i[1] for i in ExtractDevice.mark]
            _result = list(itertools.zip_longest([index.replace('.html', '')], _mark, fillvalue=index.replace('.html', '')))
            result_mark = result_mark + _result
        if ExtractDevice.mark_com != []:
            _mark_com = [i[1] for i in ExtractDevice.mark_com]
            _result = list(itertools.zip_longest([index.replace('.html', '')], _mark_com, fillvalue=index.replace('.html', '')))
            result_mark_com = result_mark_com + _result
        if ExtractDevice.jiaoyiduifang != []:
            _jiaoyiduifang = [i[1] for i in ExtractDevice.jiaoyiduifang]
            _result = list(itertools.zip_longest([index.replace('.html', '')], _jiaoyiduifang, fillvalue=index.replace('.html', '')))
            result_jiaoyiduifang = result_jiaoyiduifang + _result
    # to dataframe
    df_mark = pd.DataFrame(result_mark, columns=['id', 'mark'])
    df_mark_com = pd.DataFrame(result_mark_com, columns=['id', 'mark_com'])
    df_jiaoyiduifang = pd.DataFrame(result_jiaoyiduifang, columns=['id', 'jiaoyiduifang'])
    df_mark.to_csv(outpath+'mark.csv', index=False, encoding='utf8')
    df_mark_com.to_csv(outpath + 'mark_com.csv', index=False, encoding='utf8')
    df_jiaoyiduifang.to_csv(outpath + 'jiaoyiduifang.csv', index=False, encoding='utf8')


if __name__ == '__main__':
    from_shiyi()
    pass