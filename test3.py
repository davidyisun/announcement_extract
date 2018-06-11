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


# --- 所有html --- 生成dict集
html_dict = {}
for i, _file in enumerate(file_list):
    with codecs.open(_file, 'r', 'utf8') as f:
        data = f.read()
        print('read {0}'.format(i))
    _html = BeautifulSoup(data, 'lxml', from_encoding='utf-8')
    html_dict[files_name[i]] = _html

# ############# 抽取信息 ##############
# --- 抽取基本信息 ---

titles = {}
titles_n = {}
no_titles = []
for index in html_dict:
    html = html_dict[index]  # html 为 beautifulsoup
    # 获取公告名 定位到 head 下   pdf 级
    _head = html.find_all('div', title=re.compile('.*'), type='pdf')[0]
    title = _head['title']
    # 提取一阶章节title
    title_1 = []
    reg_01 = re.compile("SectionCode_\d+$")
    p_1 = _head.find_all('div', id=reg_01, type='paragraph')
    if p_1 == None:
        titles[index] = 0
        titles_n[index] = 0
    n_1 = len(p_1)  # 一级段落的数量
    for section_1 in p_1:
        if not section_1.has_attr('title'):
            no_titles.append(index)
            continue
        title_1.append(section_1['title'])
    titles[index] = title_1
    titles_n[index] = n_1


# ############# 统计信息 ##############
"""

# - 查看body下有多少个child: 一个body下只有一个div
b_d = []
_name = []
for index in html_dict:
    html = html_dict[index]
    count = 0
    for i in html.body.children:
        if i == '\n':
            continue
        count += 1
    _name.append(index)
    b_d.append(count)
"""

