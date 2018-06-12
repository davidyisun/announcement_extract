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
from bs4 import BeautifulSoup
import os
import re


path = 'D:\WorkSpace\Python\projects\\tianchi\\announcement_extract\\data\\round1_train_20180518\定增\html\\'
file = path+'12998.html'

files_name = os.listdir(path)
file_list = [path+i for i in files_name]

# --- 单个html ---
with codecs.open(file, 'r', 'utf8' ) as f:
    data = f.read()
d = BeautifulSoup(data, 'lxml', from_encoding='utf-8')

# 提取所有text
text = []
for i in d.stripped_strings:
    text.append(i.replace('\n', '').replace(' ', ''))

# --- 所有html ---
html_list = {}
for i, _file in enumerate(file_list):
    with codecs.open(_file, 'r', 'utf8') as f:
        data = f.read()
    _html = BeautifulSoup(data, 'lxml', from_encoding='utf-8')
    html_list[files_name[i]] = _html

# --- 提取公告基本信息 ---
basics = []
reg = '代码'
unknown = []
for i in html_list:
    t = []
    for j in html_list[i].stripped_strings:
        t.append(j.replace('\n', '').replace(' ', ''))
    basics.append(t[0])
    if not t[0].__contains__(reg):
        unknown.append(html_list[i])


# --- 提取公告文本 ---
text_path_save = 'D:\\WorkSpace\\Python\\projects\\tianchi\\announcement_extract\\data_output\\重大合同\\'
for i in html_list:
    _save_path = text_path_save+i.replace('html', 'txt')
    t = []
    for j in html_list[i].stripped_strings:
        t.append(j.replace('\n', '').replace(' ', ''))
    tt = '\n'.join(t)
    # 替换3位进位值
    tt = re.sub('(?<=[\d]),?(?=[\d]{3}[^\d])', '', tt)
    tt = tt.replace(',', '\n')
    tt = tt.replace('，', '\n')
    tt = tt.replace(';', '\n')
    tt = tt.replace('；', '\n')
    tt = tt.replace('。', '\n')
    tt = re.sub('\n(\n)+', '\n', tt)
    with codecs.open(_save_path, 'w', 'utf8') as f:
        f.write(tt)




# --- 相关统计 ---
tables = 0  # 存在表格
for i in html_list:
    t = i.find_all('table')
    if len(t) != 0:
        tables += 1


notations = 0 # 存在申明
no_notations_list = []
t1 = '本公司董事会及全体董事保证本公告内容不存在任何虚假记载、误导性陈述或者重大遗漏，并对其内容的真实性、准确性和完整性承担个别及连带责任。'
t2 = '本公司及董事会全体成员保证信息披露内容的真实、准确和完整，没有虚假记载、误导性陈述或重大遗漏'
reg = re.compile('本公司.*董事会.*全体.*保证.*')
for i in html_list:
    t = re.findall(reg, i.text)
    if len(t) != 0:
        notations += 1
    else:
        no_notations_list.append(i)