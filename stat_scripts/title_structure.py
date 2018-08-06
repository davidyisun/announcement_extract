#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名:文章结构统计title
Created on 2018-07-30
@author:David Yisun
@group:data
"""
import sys
sys.path.append('../')
import os
import codecs
import json
import re
import pandas as pd
from utils import result_compare


# # --- 本地外部数据 ---
title_path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\复赛\\最新\\统计数据\\titles_list\\'
filename = ['9123.txt']
filename = None
label_file = '../data/train_data/train_labels/chongzu.train'
outpath = '../data/temp2/result/chongzu/'
import copy

#
# # --- 本地外部数据 thinkpad ---
# title_path = 'E:\\天池大赛\\公告数据\\天池大赛\\announcement_extract\\复赛数据\\复赛新增类型训练数据-20180712\\资产重组\\html\\'
# filename = ['20546245.html']
# label_file = '../data/train_data/train_labels/chongzu.train'
# outpath = '../data/extract_result/train_chongzu/'
#
#
# # --- 本地数据 ---
# title_path = '../data/train_data/chongzu/title_list/'
# filename = ['6004.txt']
# filename = None
# outpath = '../data/train_data/stat_result/'

def read_title(path=title_path, file_name=filename):
    title = {}
    if file_name == None or file_name == []:
        file_name = [i for i in os.listdir(path=path)]
    for i, file in enumerate(file_name):
        print('doc_total: {0}, has read {1}'.format(len(file_name), i+1))
        file_path = path+file
        with codecs.open(file_path, 'r', 'utf8') as f:
            _title = f.read()
            title[re.sub('.html|.txt', '', file)] = json.loads(_title)
    return title


def get_reg(reg, title):
    res = {}
    _title = [i for i in title.split('--') if i!='']
    n = 100
    for i,j in enumerate(_title):
        if re.findall(reg, j):
            n = len(_title)-i-1
    if n < 100:
        res = {'title': _title, 'distance': n}
    return res


def stat(titles_dict):
    """
        统计main函数
    :return:
    """
    failed = []
    has_no_reg = []
    successed = {}
    successed_index = []
    # reg = re.compile('交易标的 *$|标的资产 *$|标的股权 *$')
    # reg = re.compile('资产的*评估 *$|评估概述 *$|评估情况说明 *$|评估情况 *$|[评预]估的?方法|定价方式|定价依据')
    # reg = re.compile('（标的资产的*估值）$|（标的资产的*估值）[和及、]|（交易价格）$|（交易价格）[和及、]|交易标的的*资产价格|资产价格|定价$|定价[及、和]')
    reg = re.compile('交易对方')
    for i, index in enumerate(titles_dict):
        try:
            _content = []
            distance = 100
            titles = titles_dict[index]['content']
            for title in titles:
                res = get_reg(reg=reg, title=title)
                if len(res) != 0:
                    _content.append(res)
                    if res['distance'] < distance:
                        distance = res['distance']
            if _content == []:
                has_no_reg.append(index)
            else:
                successed[index] = _content
                successed_index.append([index, distance])
        except:
            failed.append(index)
    return failed, has_no_reg, successed, successed_index


def get_title_in_depth(depth, successed_index, successed):
    res = [(i[0], successed[i[0]]) for i in successed_index if i[1]==depth]
    return res


def main(depth=0):
    title_dict = read_title()
    # out = json.dumps(title_dict)
    # with codecs.open('../data/temp/title_list.txt', 'w', 'utf8') as f:
    #     f.write(out)


    # --- label 字段 ---
    headers = ['id', 'mark', 'mark_com', 'jiaoyiduifang', 'price', 'method']
    df_label = result_compare.get_labels(file=label_file+'', headers=headers)
    key = 'jiaoyiduifang'
    df = df_label.dropna(subset=[key]).reset_index(drop=True).copy()
    label_id = [str(i) for i in df['id'].unique().tolist()]


    failed, has_no_reg, successed, successed_index = stat(title_dict)
    print('total for fialed: {0}'.format(len(failed)))
    print('total for has_no_reg: {0}'.format(len(has_no_reg)))
    print('total for successed: {0}'.format(len(successed)))
    data = pd.DataFrame(successed_index)
    data.columns = ['index', 'distance']
    end_success = {}
    for i in successed_index:
        if i[1] == depth:
            end_success[i[0]] = successed[i[0]]


    in_id = list(set(label_id).intersection(set(end_success.keys())))
    not_in_id = list(set(label_id).difference(set(end_success.keys())))
    out_of_id = list(set(end_success.keys()).difference(set(label_id)))


    res = {'content': title_dict,
            'failed': failed,
            'has_no_reg': has_no_reg,
            'successed': successed,
            'successed_index': successed_index,
            'end_success': end_success,
            'in_id': in_id,
            'not_in_id': not_in_id,
            'out_of_id': out_of_id}
    return res


if __name__ == '__main__':
    res = main(depth=0)
    pass