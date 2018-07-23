#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 小工具箱
Created on 2018-07-18
@author:David Yisun
@group:data
"""
from bs4 import BeautifulSoup
import codecs
import re


def get_tags(filepath='../data/temp2/', filename='23599.html'):
    with codecs.open(filepath+filename, 'r', 'utf8') as f:
        data = f.read()
        # 去掉换行符
    data = re.sub(re.compile('>\n* *<'), '><', data)
    data = re.sub(re.compile('\n'), '', data)
    _html = BeautifulSoup(data, 'lxml', from_encoding='utf-8')
    return _html


if __name__ == '__main__':
    pass