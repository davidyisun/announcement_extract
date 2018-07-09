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


def t1():
    # 统计单表中只含有标准格式的数据
    res1, res2 = id.main()
    headers = ['index', 'holders', 'date', 'method', 'price', 'amount', 'amount_later', 'amount_ratio_later', 'share_nature']
    data = pd.DataFrame(columns=headers)
    count = 0
    for index in res2:
        if res2[index][1] == 'complete':
            content = res2[index][0]
            content['index'] = index
            if content.shape[1] > len(headers):
                continue
            data = pd.merge(data, content, how='outer')
            count += 1
            print('--- together {0} --- count {1}'.format(index, count))
    data.reindex(columns=headers)
    data.to_csv('./zengjianchi_table.csv', index=False)
    return
if __name__ == '__main__':
    t1()
    pass