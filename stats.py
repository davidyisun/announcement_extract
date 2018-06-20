#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 相关数据统计
Created on 2018-06-04
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import os
from bs4 import BeautifulSoup
import codecs
import re


classify = ['重大合同', '增减持', '定增']
file_list = []
for _classify in classify:
    path = './data/round2_adjust/{0}/html/'.format(_classify)
    files_name = os.listdir(path)
    file_list = [{'file_name': i, 'path': path+i, 'classify': _classify} for i in files_name]+file_list


# 读入htmls 以字典形式保存
def read_html():
    html_dict = {}
    text_dict = {}
    for i, _file in enumerate(file_list):
        with codecs.open(_file['path'], 'r', 'utf8') as f:
            data = f.read()
            print('read {0}'.format(_file['file_name']))
        _html = BeautifulSoup(data, 'lxml', from_encoding='utf-8')
        html_dict[_file['file_name']] = {'classify': _file['classify'], 'h': _html}
        text_dict[_file['file_name']] = {'classify': _file['classify'], 't': data}
    return html_dict


"""
输出样例:  html_dict['100103.html']['h']

   { '100103.html':{'classify': '定增',
                     'h': <html><head></head><body><div title="辽宁成………………}
    } 
"""

def check_notations():
    html_dict = read_html()
    notations = 0  # 存在申明
    no_notations_list = []
    reg = re.compile(r'本公司.*董事会.*全体.*保证.*')
    for i in html_dict:
        t = re.findall(reg, html_dict[i]['h'].text)
        if len(t) != 0:
            notations += 1
        else:
            no_notations_list.append(i)
    print('text total -- {0}'.format(len(html_dict)))
    print('notation exists -- {0}'.format(notations))
    return no_notations_list

def check_punctuation():
    html_dict = read_html()
    count = 0
    for i in html_dict:
        a = html_dict[i].find_all(text=',')
        if len(a) != 0:
            count +=1
    print('逗号: {0}'.format(len(count)))
    return

count = 0
m = []
n = []
for i in html_dict:
    a = html_dict[i]['h'].find_all(text=re.compile('、'))
    if len(a) != 0:
        count +=1
        m.append(i)
    else:
        n.append(i)
print(r'逗号: {0}'.format(count))
