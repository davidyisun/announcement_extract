#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 临时文件
Created on 2018-07-09
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import extract.increase_or_decrease as id
import pandas as pd
import codecs
import numpy as np
def t():
    res1, res2 = id.main()
    data = {'multi_keys': [],
            'no_keys': [],
            'normal': []}
    for index in res2:
        data[res2[index]].append(index)
    print('multi_keys:')
    print(data['multi_keys'])
    print('—'*20)
    print('no_keys:')
    print(data['no_keys'])
    print('—'*20)
    print('total:{0}'.format(len(res2)))
    print('multi_keys:{0}'.format(len(data['multi_keys'])))
    print('no_keys:{0}'.format(len(data['no_keys'])))
    print('normal:{0}'.format(len(data['normal'])))
    return data

# def full_short_merge(holder):
#     if
#     return
#
#
def read_full_short():
    with codecs.open('./data/full_short_name_pair/full_short.txt', 'r', 'utf8') as f:
        t = f.read()
    _t = [i.split('\t') for i in t.splitlines()]
    res = [[i[0].replace('.html', ''), i[1], i[2]] for i in _t]
    return res


def full_and_short_merge(df,full_short_list):
    res = df.drop('holders')
    full_name = df['holders']
    short_name = np.nan
    name_list = [i for i in full_short_list if i[0] == df['index']]
    _short_name = [i for i in name_list if i[0] == df['index'] and i[2] == df['holders']]
    _full_name = [i for i in name_list if i[0] == df['index'] and i[1] == df['holders']]
    if _full_name == [] and _short_name != []:
        # name为简称
        full_name = _short_name[0][1]
        short_name = df['holders']
    if _full_name != [] and _short_name == []:
        # name为全称
        full_name = df['holders']
        short_name = _full_name[0][2]
    if df['holders'] == np.nan and len(full_short_list) == 1:
        full_name = full_short_list[0]
        short_name = full_short_list[1]
    res['holders_fullname'] = full_name
    res['holders_shortname'] = short_name
    return res


def t1():
    # 统计单表中只含有标准格式的数据
    res1, res2, error = id.main()
    headers = ['index', 'holders', 'date', 'method', 'price', 'amount', 'amount_later', 'amount_ratio_later', 'share_nature']
    new_headers = ['index', 'holders_fullname', 'holders_shortname', 'date', 'method', 'price', 'amount', 'amount_later', 'amount_ratio_later', 'share_nature']
    data = pd.DataFrame(columns=new_headers)
    count = 0
    stat = []
    full_short = read_full_short()
    for index in res2:
        if res2[index][1] == 'complete':
            content = res2[index][0]
            content['index'] = index
            if list(set(content.columns).difference(set(headers))) != []:
                stat.append(index)
                continue
            a = []
            for i, j in content.iterrows():
                a.append(full_and_short_merge(j, full_short))
            df = pd.DataFrame(a)
            # try:
            #     data = pd.merge(data, df, how='outer')
            #     count += 1
            #     print('--- together {0} --- count {1}'.format(index, count))
            # except Exception as e:
            #     print('--- wrong with {0} --- {1}'.format(index, e))
            #     continue
            data = pd.concat([data, df], ignore_index=True)
            count += 1
            print('--- together {0} --- count {1}'.format(index, count))
            print('### headers: {0}'.format(' '.join(content.columns)))
    data = data.reindex(columns=new_headers)
    data = data.drop(labels=['method', 'share_nature'], axis=1)
    print('error:')
    print(error)
    print('failed:')
    print(stat)
    data.to_csv('./zengjianchi_table.csv', index=False)
    return


if __name__ == '__main__':
    t1()
    pass