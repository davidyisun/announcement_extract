#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 所有公告的共同信息
Created on 2018-06-07
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import os
from bs4 import BeautifulSoup
import codecs
import re
import pandas as pd
import json


classify = ['重大合同', '增减持', '定增']
file_list = []
for _classify in classify:
    path = './data/round2_adjust/{0}/html/'.format(_classify)
    files_name = os.listdir(path)[0:10]
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
def get_title():
    html_dict = read_html()

    # 提取title 样本公告中全部含有title
    total = len(html_dict)
    t_uk = []
    t_r = {}
    for index in html_dict:
        h = html_dict[index]
        # title 标签
        t = h['h'].find_all('div', title=re.compile('.*'), type='pdf')
        if len(t) == 0:
            t_uk.append({index: h})
            continue
        t_r[index] = {'title': t[0]['title'],
                      'classify': h['classify']}
    title_list = [[i, t_r[i]['title'], t_r[i]['classify']] for i in t_r]
    titles = pd.DataFrame(title_list, columns=['id', 'title', 'classify'])
    return titles


# 提取公共注释
html_dict = read_html()
notations = 0 # 存在申明
t1 = '本公司董事会及全体董事保证本公告内容不存在任何虚假记载、误导性陈述或者重大遗漏，并对其内容的真实性、准确性和完整性承担个别及连带责任。'
t2 = '本公司及董事会全体成员保证信息披露内容的真实、准确和完整，没有虚假记载、误导性陈述或重大遗漏'
t3 = '本公司及全体董事、监事、高级管理人员保证本发行情况报告书内容的真实、准确和完整，并对虚假记载、误 导性陈述或者重大遗漏负连带责任。'
t4 = '本公司全体董事承诺本发行情况报告书不存在虚假记载、误导性陈述或重大遗漏，并对其真实性、准确性、完整性承担个别和连带的法律责任。'
reg= re.compile('公司.*全体.*[保证|承诺].*[真实|完整|准确]')
no_notations = []
multi = []
for i in html_dict:
    text = html_dict[i]['h'].text
    t = re.findall(reg, text.replace('\n', '').replace(' ', ''))
    if len(t) != 0:
        notations += 1
    elif len(t)==0:
        no_notations.append([i, html_dict[i]])
    else:
        multi.append([i, html_dict[i]])


print(len(no_notations))
print(len(multi))

