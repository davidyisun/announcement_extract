#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 天池html文本工具
Created on 2018-07-16
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import codecs
from bs4 import BeautifulSoup
import os
import re
import copy
import numpy as np
import bs4
from optparse import OptionParser
import pandas as pd


# 读入htmls 以字典形式保存
def read_html(filepath, filename=None):
    """
        天池html格式读入
    :param filepath: html文件地址
    :param filename: html文件名  None 表示 读入filepath下所有以.html结尾的文件
    :return: dict key为html文件名 value为beautifulsoup对象
    """
    if filename == None:
        files_name = os.listdir(filepath)
    else:
        files_name = [filename]
    file_list = [{'file_name': i, 'file_path': filepath+i} for i in files_name if i.endswith('.html')]
    html_dict = {}
    text_dict = {}
    for i, _file in enumerate(file_list):
        with codecs.open(_file['file_path'], 'r', 'utf8') as f:
            data = f.read()
            print('read {0}'.format(_file['file_name']))
        # 去掉换行符
        data = re.sub(re.compile('>\n* *<'), '><', data)
        data = re.sub(re.compile('\n'), '', data)
        # # 去掉特殊空格
        # data = re.sub(' ', '', data)
        _html = BeautifulSoup(data, 'lxml', from_encoding='utf-8')
        html_dict[_file['file_name']] = _html
        text_dict[_file['file_name']] = data
    return html_dict


# 获取text信息
def get_content(tag):
    """
        获取text信息 递归
    :param tag:
    :return:
    """
    contents = []
    # 如果是string 树的终点
    if type(tag) == bs4.element.NavigableString:
        s = str(tag).replace(' ', '')
        s = s.replace(' +', '')
        contents.append(s)
        return contents
    else:
        # 检查 title
        if tag.has_attr('title'):
            s = str(tag['title']).replace(' ', '')
            s = s.replace(' +', '')
            contents.append(s)
        # 检查表格
        tables = tag.find_all('table', recursive=False)
        if tables != [] and tables[0].get_text() != '':
            try:  # 奇葩的非表格 table
                _content = tables[0].tbody.find_all('tr')
            except:
                _content = tables[0].get_text()
            contents.append(_content)
            return contents
        # 没有文字
        if tag.find_all(text=True) == []:
            return contents
        # 没有子节点
        tags_children = tag.contents
        if tags_children == []:
            return contents
        for tag_child in tags_children:
            _contents = get_content(tag_child)
            if _contents != []:
                contents = contents + _contents
    return contents

