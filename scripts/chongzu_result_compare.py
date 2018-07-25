#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 资产重组抽取结果对比
Created on 2018-07-24
@author:David Yisun
@group:data
"""
import sys
sys.path.append('../')
from utils import result_compare
import pandas as pd


headers = ['id', 'mark', 'mark_com', 'jiaoyiduifang', 'price', 'method']


# 统计脚本
def stat(label_path, result_path, main_key, other_fields, **kwargs):
    outpath = kwargs.get('outpath')
    is_print = kwargs.get('is_print')
    df_label = result_compare.get_labels(file=label_path, headers=headers)
    df_result = pd.read_csv(result_path, header=None)
    df_result.columns = main_key+other_fields
    res = result_compare.fields_compare(df_label=df_label, df_result=df_result,
                                        main_key=main_key, fileds=other_fields,
                                        is_print=is_print,
                                        outpath=outpath)
    return res, df_result


if __name__ == '__main__':
    label_path = '../data/train_data/train_labels/chongzu.train'
    label_name = ['mark', 'mark_com', 'jiaoyiduifang']
    result_path = '../data/extract_result/train_chongzu/{0}.csv'
    output_path = '../data/stat_result/chongzu/'
    res = {}
    for label in label_name[1:2]:
        _result_path = result_path.format(label)
        res[label] = stat(label_path=label_path, result_path=_result_path, main_key=['id'], other_fields=['mark_com'], is_print=True, outpath=output_path)
    pass
