#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名:
Created on 2018--
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import codecs

with codecs.open('./data/temp/14045441.html', 'r', 'utf8') as f:
    k = f.readlines()
print(k)