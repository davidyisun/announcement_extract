#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 天池html格式整理
Created on 2018-06-04
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import os
from bs4 import BeautifulSoup
import codecs
import re


classify = '重大合同'
path = 'D:\WorkSpace\Python\projects\\tianchi\\announcement_extract\\data\\round2_adjust\\{0}\\html\\'.format(classify)
text_path_save = 'D:\\WorkSpace\\Python\\projects\\tianchi\\announcement_extract\\data_output\\{0}\\'.format(classify)
files_name = os.listdir(path)
file_list = [path+i for i in files_name]


# 读入htmls 以字典形式保存
def read_html():
    html_dict = {}
    for i, _file in enumerate(file_list):
        with codecs.open(_file, 'r', 'utf8') as f:
            data = f.read()
            print('read {0}'.format(i))
        _html = BeautifulSoup(data, 'lxml', from_encoding='utf-8')
        html_dict[files_name[i]] = _html
    return html_dict


html_dict = read_html()
h = html_dict['17829.html']

# 检查基本信息是否存在
# - 抽取title -
for index in html_dict:
    t1 = html_dict[index]
