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


def basic_info():
    """
    基本信息抽取 包括：
        title:公告名
        name:上市公司名
        stock:上市公司代码
        time:公告发布时间
        mark:公告编号
    :return: 
    """

    return

