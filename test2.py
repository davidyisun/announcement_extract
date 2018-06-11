#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 
Created on 2018--
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import os
from bs4 import BeautifulSoup
import codecs
import re


classify = '重大合同'
path = 'D:\WorkSpace\Python\projects\\tianchi\\announcement_extract\\data\\round1_train_20180518\\{0}\\html\\'.format(classify)
text_path_save = 'D:\\WorkSpace\\Python\\projects\\tianchi\\announcement_extract\\data_output\\{0}\\'.format(classify)
files_name = os.listdir(path)
file_list = [path+i for i in files_name]

# --- 所有html ---
html_dict = {}
for i, _file in enumerate(file_list):
    with codecs.open(_file, 'r', 'utf8') as f:
        data = f.read()
        print('read {0}'.format(i))
    _html = BeautifulSoup(data, 'lxml', from_encoding='utf-8')
    html_dict[files_name[i]] = _html

# --- 提取公告文本 ---
for i in html_dict:
    _save_path = text_path_save+i.replace('html', 'txt')
    t = []
    temp = html_dict[i]
    while temp.table != None:
        print('delect')
        temp.table.decompose()
    for j in temp.stripped_strings:
        t.append(j.replace('\n', '').replace(' ', ''))
    tt = '\n'.join(t)
    # 替换3位进位值
    tt = re.sub('(?<=[\d]),?(?=[\d]{3}[^\d])', '', tt)
    # tt = tt.replace(',', '\n')
    # tt = tt.replace('，', '\n')
    tt = tt.replace('?', '\n')
    tt = tt.replace('？', '\n')
    tt = tt.replace('!', '\n')
    tt = tt.replace('！', '\n')
    tt = tt.replace(';', '\n')
    tt = tt.replace('；', '\n')
    tt = tt.replace('。', '\n')
    tt = re.sub('\n(\n)+', '\n', tt)
    with codecs.open(_save_path, 'w', 'utf8') as f:
        f.write(tt)
