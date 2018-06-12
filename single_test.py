#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名:单个html test
Created on 2018-06-12
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import codecs
from bs4 import BeautifulSoup
import os
import re


catalogue = '增减持'
path = './data/round2_adjust/{0}/html/'.format(catalogue)
file = path+'7544.html'
# --- 单个html ---
with codecs.open(file, 'r', 'utf8' ) as f:
    data = f.read()
data = re.sub(re.compile('>\n* *<'), '><', data)
d = BeautifulSoup(data, 'lxml', from_encoding='utf-8')

# 去掉空行
d.text.replace('\n', '')


# 甄别层级结构




for i in d.find_all('div', text='\n'):
    i.decompose()

# 获取body下的子节点
t = d.body.find_all('div', title=re.compile('.*'), recursive=False)[0]

title = t['title']
_children = []
for child in t.children:
    _children.append(child)
