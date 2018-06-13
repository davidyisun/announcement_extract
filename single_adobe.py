#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: acrabat html 数据格式整理
Created on 2018-06-12
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import codecs
from bs4 import BeautifulSoup
import os
import re

catalogue = '人事变动'
path = './data/round2_adjust/{0}/'.format(catalogue)
file = path+'000010_20180409_1204590295.html'

# --- 单个html ---
with codecs.open(file, 'r', 'utf8' ) as f:
    data = f.read()
data = re.sub(re.compile('>\n* *<'), '><', data)
d = BeautifulSoup(data, 'lxml', from_encoding='utf-8')

# 去掉空行
d.text.replace('\n', '')

body = d.find_all('body')[0]
