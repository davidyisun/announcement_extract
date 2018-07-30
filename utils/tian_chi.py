#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 天池html文本工具
Created on 2018-07-16
@author:David Yisun
@group:data
"""
import sys
sys.path.append('../')
import codecs
from bs4 import BeautifulSoup
import os
import re
from utils import html_table
import itertools
import bs4
import os


# 读入html 单个
def read_single_html(filepath, filename=None):
    """
        单个天池html格式读入
    :param filepath: html文件地址
    :param filename: html文件名
    :return: dict key为html文件名 value为beautifulsoup对象
    """
    with codecs.open(filepath+os.sep+filename, 'r', 'utf8') as f:
        data = f.read()
    # 去掉换行符
    data = re.sub(re.compile('>\n* *<'), '><', data)
    data = re.sub(re.compile('\n'), '', data)
    html = BeautifulSoup(data, 'lxml', from_encoding='utf-8')
    return html


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
        files_name = filename
    try:
        file_list = [{'file_name': i, 'file_path': filepath+i} for i in files_name if i.endswith('.html')]
    except:
        pass
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


def extract_pre_content(tag):
    """
        抽取 天池 html 的 目录 风险提示 释义 和正文
    :param tag:
    :return:
        mulu --- list 目录 元素为str
        shiyi_dict --- dict 释义
        major_promption --- str 重大事项提示
        tag --- tag 余下的tag
    """
    # 获取【释义】
    shiyi_dict = {}
    # --- 方法一 ---
    ShiYi_tag = tag.find_all('div', title=re.compile('释 *义'))
    if ShiYi_tag != []:
        for shiyi_tag in ShiYi_tag:
            trs_dict_list = []
            if len(shiyi_tag.find_all(text=re.compile('^ *指 *$'))) < 4:
                continue
            for i in shiyi_tag.find_all('tr'):
                if len(i.find_all(text=re.compile('^ *指 *$'))) == 1 and len(i.find_all('td')) == 3:
                # if re.findall(re.compile('指'), i.get_text()) != []:
                    tr_dict = html_table.tr_processing(i)
                    tr_tds_text = tr_dict['tr_tds_text']
                    key = tr_tds_text[0].split('、|/')
                    value = tr_tds_text[2]
                    _kv = dict(itertools.zip_longest(key, [value], fillvalue=value))
                    shiyi_dict.update(_kv)
            # shiyi_list = []
            # if len(trs) > 0:
            #     shiyi_list = html_table.table2mat(trs).tolist()
            # for i in shiyi_list:
            #     if None in i:
            #         continue
            #     key = i[0].split('、')
            #     value = i[2]
            #     _kv = dict(itertools.zip_longest(key, [value], fillvalue=value))
            #     shiyi_dict.update(_kv)
            shiyi_tag.decompose()
    # --- 方法二 --- 直接检索 table 标签
    _trs = tag.find_all('tr')
    for shiyi_tr in _trs:
        shiyi_trs = []
        if len(shiyi_tr.find_all('td', text=re.compile('^ *指 *$'))) == 1 and len(shiyi_tr.find_all('td')) == 3:
            tr_dict = html_table.tr_processing(i)
            tr_tds_text = tr_dict['tr_tds_text']
            key = tr_tds_text[0].split('、|/')
            value = tr_tds_text[2]
            _kv = dict(itertools.zip_longest(key, [value], fillvalue=value))
            shiyi_dict.update(_kv)
            shiyi_tr.decompose()
    # 获取【目录】
    mulu = []
    mulu_tag = tag.find_all('div', title=re.compile('目 *录'))
    if mulu_tag != []:
        mulu_tag = mulu_tag[0]
        for i in mulu_tag.find_all(True, text=True):
            mulu.append(str(i.string).strip())
        mulu_tag.decompose()

    # 获取【重大事项提示】
    major_promption = ''
    mp_tag = tag.find_all('div', title=re.compile('重大事项提示'))
    if mp_tag != []:
        mp_tag = mp_tag[0]
        major_promption = mp_tag.get_text()
        mp_tag.decompose()
    return mulu, shiyi_dict, major_promption, tag


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

