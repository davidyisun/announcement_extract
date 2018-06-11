#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 
Created on 2018--
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""

def change_name():
    import os
    paths = ['增减持', '定增', '重大合同']

    for path in paths:
        p = './data/round2_adjust/{0}/html/'.format(path)
        files = os.listdir(p)
        for f in files:
            os.rename(p+f, p+f+'.html')
            print(p+f+'.html')


def del_files():
    import os
    paths = ['增减持', '定增', '重大合同']

    for path in paths:
        p = './data/round2_adjust/{0}/html/'.format(path)
        files = os.listdir(p)
        for f in files:
            os.remove(p+f)


if __name__ == '__main__':
    change_name()

