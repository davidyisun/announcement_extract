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
    res = id.main()
    data = {'multi_keys': [],
            'no_keys': [],
            'normal': []}
    for index in res:
        data[res[index]].append(index)
    print('total:{0}'.format(len(res)))
    print('multi_keys:{0}'.format(len(data['multi_keys'])))
    print('no_keys:{0}'.format(len(data['no_keys'])))
    print('normal:{0}'.format(len(data['normal'])))
    return data

if __name__ == '__main__':
    t()
    pass