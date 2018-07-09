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

if __name__ == '__main__':
    t()
    pass