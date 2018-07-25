#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 资产重组 信息抽取脚本
Created on 2018-07-20
@author:David Yisun
@group:data
"""
import sys
sys.path.append('../')
from extract import chongzu
from utils import result_compare, tian_chi
import itertools
import pandas as pd
import os
import math
import codecs


def from_shiyi(path, filename, outpath, result_append=True):
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

    result = {'mark': df_mark,
              'mark_com': df_mark_com,
              'jiaoyiduifang': df_jiaoyiduifang}
    out_names = ['mark', 'mark_com', 'jiaoyiduifang']
    for i in out_names:
        out_name = outpath+i+'.csv'
        if result_append:
            with codecs.open(out_name, 'a', 'utf8') as f:
                result[i].to_csv(f, index=False, header=False)
        else:
            result[i].to_csv(out_name, index=False)
    return


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
    filename = ['20505659.html']
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
    n_files = len(file_list)  # 总文件数
    n_batch = math.ceil(n_files/batches)
    batch_head = 0
    # 清除已有result文件
    f = [outpath+i for i in os.listdir(outpath)]
    for i in f:
        os.remove(i)
    # 批量读取写入
    for batch in range(n_batch):
        _file_list = file_list[batch_head:batch_head+batches]
        if len(_file_list) == 0:
            break
        from_shiyi(path=path, outpath=outpath, filename=_file_list)
        batch_head = batch_head+batches
        print('total: {0} --- has been processed: {1}'.format(len(file_list), min(len(file_list), batch_head)))
    return


def delete_ouput():
    pass


if __name__ == '__main__':
    main(batches=20)
    pass