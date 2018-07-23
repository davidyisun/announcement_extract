#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 结果比对
Created on 2018-07-20
@author:David Yisun
@group:data
"""
import pandas as pd


# 获取label数据
def get_labels(file, **kwargs):
    hearders = kwargs.get('headers')
    data = pd.read_table(file, header=None, sep='\t')
    if hearders != None:
        data.columns = hearders
    return data


def fields_compare(df_label, df_result, main_key, fileds):
    label = df_label[main_key+fileds]
    result = df_result[main_key+fileds]
    df_compare = pd.merge(left=label, right=result, how='outer', on=main_key, indicator=True)
    res = {}
    # id 数据集
    out_of_id = df_compare[df_compare['_merge']=='right_only'].reset_index(drop=True).copy()  # 多抽
    not_in_id = df_compare[df_compare['_merge']=='right_only'].reset_index(drop=True).copy()  # 少抽
    equl_id = df_compare[df_compare['_merge']=='right_only'].reset_index(drop=True).copy()  # id正确
    # id 各指标
    id_pos = max(label.shape[0], 1)
    id_act = max(result.shape[0], 1)
    id_cor = max(equl_id.shape[0], 1)
    id_recall = id_cor/id_pos
    id_precision = id_cor/id_act
    id_f1 = (2*id_recall*id_precision)/(id_recall+id_precision)
    res['id'] = {'out_of_id': out_of_id,
                 'not_in_id': not_in_id,
                 'id_pos': id_pos,
                 'id_act': id_act,
                 'id_cor': id_cor,
                 'id_recall': id_recall,
                 'id_precision': id_precision,
                 'id_f1': id_f1}
    res['fileds'] = {}
    # 各 slot 情况
    for i in fileds:
        left = i+'_x'
        right = i+'_y'
        d = equl_id[main_key+[left, right]].copy()
        wrong_filed = d[d[left] != d[right]].reset_index(drop=True).copy()  # 错误字段
        right_filed = d[d[left] == d[right]].reset_index(drop=True).copy()  # 正确字段
        # 各 slot 指标
        pos = max(label.dropna(subset=[i]).shape[0], 1)
        act = max(result.dropna(subset=[i]).shape[0], 1)
        cor = max(right_filed.dropna(subset=[left, right]).shape[0], 1)
        recall = cor / pos
        precision = cor / act
        f1 = (2 * recall * precision) / (recall + precision)
        res['fileds'][i] = {'wrong_filed': wrong_filed,
                            'pos': pos,
                            'act': act,
                            'cor': cor,
                            'recall': recall,
                            'precision': precision,
                            'f1': f1}
    return res