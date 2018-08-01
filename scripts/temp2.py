#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名:
Created on 2018-08-01
@author:David Yisun
@group:data
"""
import sys
sys.path.append('../')
import codecs
import json
import re


with codecs.open('../data/train_data/chongzu/mark_in_content/mark_in_content.csv', 'r', 'utf8') as f:
    data = f.read()
    data = data.replace('\u200c', '')
d = re.sub(re.compile('{(?="\d{3,10}":)'), '\n{', data).splitlines()
res = {}
for i in d:
    if i == '':
        continue
    d1 = json.loads(i)
    res.update(d1)

result = {}
for i in res:
    if res[i] == []:
        continue
    result[i] = res[i]


for i in result:
    d3 = json.dumps(result[i])
    with codecs.open('../data/train_data/chongzu/mark_in_content_sub/'+i+'.txt', 'w', 'utf8') as f:
        f.write(d3)
pass