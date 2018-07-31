#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 结果比对
Created on 2018-07-20
@author:David Yisun
@group:data
"""
import pandas as pd
import codecs


# 获取label数据
def get_labels(file, **kwargs):
    hearders = kwargs.get('headers')
    data = pd.read_table(file, header=None, sep='\t')
    if hearders != None:
        data.columns = hearders
    return data


def fields_compare(df_label, df_result, main_key, fileds, **kwargs):
    label = df_label
    result = df_result[main_key+fileds]
    df_compare = pd.merge(left=label, right=result, how='outer', on=main_key, indicator=True)
    res = {}
    # id 数据集
    out_of_id = df_compare[df_compare['_merge']=='right_only'].reset_index(drop=True).copy()  # 多抽
    not_in_id = df_compare[df_compare['_merge']=='left_only'].reset_index(drop=True).copy()  # 少抽
    equl_id = df_compare[df_compare['_merge']=='both'].reset_index(drop=True).copy()  # id正确
    # id 各指标
    id_pos = max(label.shape[0], 1)
    id_act = max(result.shape[0], 1)
    # 合并后会有冗余信息
    _fields_y = [i+'_y' for i in fileds]
    _equl_id = equl_id.copy()
    if _fields_y != []:
        _equl_id.drop_duplicates(subset=_fields_y, keep='first', inplace=True)
    id_cor = max(_equl_id.shape[0], 1)
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
        res['fileds'][i] = {'right_filed': right_filed,
                            'wrong_filed': wrong_filed,
                            'pos': pos,
                            'act': act,
                            'cor': cor,
                            'recall': recall,
                            'precision': precision,
                            'f1': f1}

    # 结果打印
    outpath = kwargs.get('outpath')
    is_print = kwargs.get('is_print')
    # --- 打印 ---

        # 打印id
    s = []
    s1 = '-------------------------------'
    s2 = 'the possible of ID(标准数据结果数): {0}'.format(res['id']['id_pos'])
    s3 = 'the actual of ID（抽取数据结果数）: {0}'.format(res['id']['id_act'])
    s4 = 'the correct of ID(匹配正确数): {0}'.format(res['id']['id_cor'])
    s5 = 'the recall of ID(召回率): {0}'.format(res['id']['id_recall'])
    s6 = 'the precision of ID(精确率): {0}'.format(res['id']['id_precision'])
    s7 = 'the f1 of ID: {0}'.format(res['id']['id_f1'])
    s = s+ [s1, s1, s2, s3, s4, s5, s6, s7]
    if is_print==True:
        print('-------------------------------')
        print('-------------------------------')
        print('the possible of ID(标准数据结果数): {0}'.format(res['id']['id_pos']))
        print('the actual of ID（抽取数据结果数）: {0}'.format(res['id']['id_act']))
        print('the correct of ID(匹配正确数): {0}'.format(res['id']['id_cor']))
        print('the recall of ID(召回率): {0}'.format(res['id']['id_recall']))
        print('the precision of ID(精确率): {0}'.format(res['id']['id_precision']))
        print('the f1 of ID: {0}'.format(res['id']['id_f1']))
    if isinstance(outpath, str):
        res['id']['out_of_id'].to_csv(outpath+'out_of_id.csv', index=False, encoding='utf8')
        res['id']['not_in_id'].to_csv(outpath+'not_in_id.csv', index=False, encoding='utf8')

    # 打印各slot
    for _fields in res['fileds']:
        s1 = '>>>>>>> {0} >>>>>>>>'.format(_fields)
        s2 = 'the possible of {1}(标准数据结果数): {0}'.format(res['fileds'][_fields]['pos'], _fields)
        s3 = 'the actual of {1}（抽取数据结果数）: {0}'.format(res['fileds'][_fields]['act'], _fields)
        s4 = 'the correct of {1}(匹配正确数): {0}'.format(res['fileds'][_fields]['cor'], _fields)
        s5 = 'the recall of {1}(召回率): {0}'.format(res['fileds'][_fields]['recall'], _fields)
        s6 = 'the precision of {1}(精确率): {0}'.format(res['fileds'][_fields]['precision'], _fields)
        s7 = 'the f1 of {1}: {0}'.format(res['fileds'][_fields]['f1'], _fields)
        s = s + [s1, s2, s3, s4, s5, s6, s7]
        if is_print:
            print('>>>>>>> {0} >>>>>>>>'.format(_fields))
            print('the possible of {1}(标准数据结果数): {0}'.format(res['fileds'][_fields]['pos'], _fields))
            print('the actual of {1}（抽取数据结果数）: {0}'.format(res['fileds'][_fields]['act'], _fields))
            print('the correct of {1}(匹配正确数): {0}'.format(res['fileds'][_fields]['cor'], _fields))
            print('the recall of {1}(召回率): {0}'.format(res['fileds'][_fields]['recall'], _fields))
            print('the precision of {1}(精确率): {0}'.format(res['fileds'][_fields]['precision'], _fields))
            print('the f1 of {1}: {0}'.format(res['fileds'][_fields]['f1'], _fields))
        if isinstance(outpath, str):
            res['fileds'][_fields]['wrong_filed'].to_csv(outpath + '{0}_wrong.csv'.format(_fields), index=False, encoding='utf8')
            res['fileds'][_fields]['right_filed'].to_csv(outpath + '{0}_right.csv'.format(_fields), index=False, encoding='utf8')
    if isinstance(outpath, str):
        with codecs.open(outpath+'result.txt', 'w', 'utf8') as f:
            f.write('\n'.join(s))
    return res

