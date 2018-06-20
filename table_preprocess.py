#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 表格预处理
Created on 2018-06-13
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""

import os
from bs4 import BeautifulSoup
import codecs
import re
import itertools
import numpy as np

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
        # 去掉换行符
        data = re.sub(re.compile('>\n* *<'), '><', data)
        data = re.sub(re.compile('\n'), '', data)
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

# --- 获取所有表格进行分析 ---
tables_tag = []
html_dict = read_html()
for index in html_dict:
    print(index)
    t = html_dict[index]
    # 删去不含text 的 "td" "tr" "tbody"
    # --- td
    m = t['h'].find_all('td')
    for j in m:
        if j.find_all(text=True) == []:
            j.decompose()
    # --- tr
    m = t['h'].find_all('tr')
    for j in m:
        if j.find_all(text=True) == []:
            j.decompose()
    # --- tbody
    m = t['h'].find_all('tbody')
    for j in m:
        if j.find_all(text=True) == []:
            j.decompose()
    _tables_tag = t['h'].find_all('tbody')
    # 不含表格的公告滤过
    if _tables_tag == []:
        continue
    # 过滤空表格
    tables_tag = tables_tag+list(itertools.zip_longest([index], _tables_tag, fillvalue=index))

# --- 扣除 《释义》
tables_tag_new = []
for i, t in enumerate(tables_tag):
    text = t[0]
    annotation = t[1].find_all(text=re.compile('^ *指 *$'))
    if len(annotation) > 10:
        continue
    tables_tag_new.append(t)


# --- 头行 ---
row_title = []
col_title = []
table_content = []
for i, t in enumerate(tables_tag_new):
    text = t[0]
    # 第一行
    print('{0}:{1}'.format(i, text))
    trs = t[1].find_all('tr', recursive=False)
    rows_len = len(trs) #总行数
    tr_1 = trs[0]
    tr_1_tds = tr_1.find_all('td')
    if len(tr_1_tds)== 1:
        row_title.append(t)
        continue
    # 第一列头
    td_1 = tr_1_tds[0]
    row_len = td_1.get('rowspan')
    if row_len == rows_len:
        col_title.append(t)
        continue
    # 不含表名的
    table_content.append(t)


# --- 表名在第一行
temp = []
only_one_row = []
for i in row_title:
    text = i[0]
    table = i[1]
    trs = table.find_all('tr')
    if len(trs) == 1:
        only_one_row.append((i))
        continue
    if len(trs[1].find_all('td')) == 1:
        temp.append(i)
        
def text_type(s):
    res = 'string'
    return res

 
def td_processing(td):
    """
        单元格信息
    :param td: tag 单元格
    :return: 字典包括以下：
        内容 类型 跨列 跨行
    """
    td_rowspan = 1
    td_colspan = 1
    if td.has_attr('rowspan'):
        td_rowspan = td['rowspan']
    if td.has_attr('colspan'):
        td_colspan = td['colspan']
    td_type = np.array([[text_type(td.text)] * td_colspan] * td_rowspan).reshape(td_rowspan, td_colspan)
    td_content = np.array([[td.text] * td_colspan] * td_rowspan).reshape(td_rowspan, td_colspan)
    res = {'td_content': td_content,
           'td_type': td_type,
           'td_colspan': td_colspan,
           'td_rowspan': td_rowspan}
    return res

def tr_processing(tr):
    """
        行信息
    :param tr: tag 行
    :return: 字典
    """
    tr_most_rowspan = 1 # 最大跨行数
    tr_most_colspan = 1 # 最大跨列数
    tds = tr.find_all('td')
    n_tds = len(tds)  # 行所含单元格数
    tr_content = [] # 行各单元内容
    tr_type = [] # 行各单元格数据类型
    tr_col = 0 # 行 长度
    count_tr_colspan = 0 # colspan大于1的td个数统计
    for td in tds:
        data = td_processing(td)
        if data['td_colspan'] > tr_most_colspan:
            tr_most_colspan = data['td_colspan']
        if data['td_rowspan'] > tr_most_rowspan:
            tr_most_rowspan = data['td_rowspan']
        tr_content.append(data['td_content'])
        tr_type.append(data['td_type'])
        tr_col = tr_col+td['td_colspan']
        if td['td_colspan'] > 1:
            count_tr_colspan += 1
    if count_tr_colspan == n_tds:
        all_has_multi_colspan = True
    else:
        all_has_multi_colspan = False
    res = {'tr_most_span': tr_most_colspan,
           'tr_most_rowspan': tr_most_rowspan,
           'n_tds': n_tds,
           'all_has_multi_colspan': all_has_multi_colspan}
    return res

def find_title(tr):
    """
        查找表格title
    :param tr:
    :return: 若有 输出 text; 否则 输出 -1
    """

    data = tr_processing(tr)
    if data['n_tds'] == 1:
        return data['tr_content'][0][0]
    else:
        return -1


def create_headers(tr):
    """
        建表头headers
    :param tr:
    :param headers:
    :return:
    """
    data = tr_processing(tr)
    headers_array = []

def complete_headers(tr, headers_array):
    """
        完善表头
    :param tr:
    :param headers_array:
    :return:
    """
    return


def table_processing(tbody):
    """
        表格处理
    :param tbody:str html格式
    :return: df or str : pandas dateframe 标准二维表 或者是 无法识别的表格类型
             type: ['df', 'df_no_title', 'no_parse', 'part_df_content', 'only_one']
                   df: ndarray 完全解析
                   df_no_title: ndarray 无title
                   no_parse: html.tbody 无法解析
                   part_df_content: ndarray+html.trs 部分解析
                   only_one: list 独行
    """
    trs = tbody.find_all('tr', recursive=False)
    n_row = len(trs)  # 表行数
    title = None  # 表名
    headers_type = '' # 表头类型
    headers = []  # 表头
    headers_array = np.array([None]) # 表头矩阵
    fields_type = []  # 表字段类型
    content = None
    # --- 逐行填表 ---
    for i, tr in enumerate(trs):
        # --- check title ---
        if title == None:
            title = find_title(tr)
            continue
        # --- check headers ---
        if headers_type == '':
            # 还没有表头
            headers_array = create_headers(tr)
            continue
        if headers_type == 'part_headers':
            # 残缺表头
            headers_array = complete_headers(tr, headers_array)



    
    
    
    tr_1 = trs[0]
    tr_1_content, tr_1_type, tr_1_col, tr_1_n_tds = tr_processing(tr_1)
    n_col = tr_1_col # 表列数
    # --- 初始化 内容表和类型表、表结构
    content = np.array([None]*n_col*n_row).reshape(n_row, n_col)
    td_type = np.array([None]*n_col*n_row).reshape(n_row, n_col)
    table_structure = np.array([None]*n_col*n_row).reshape(n_row, n_col)
    # --- 填表 ---
    i = 0 # 行游标
    j = 0 # 列游标
    for tr in trs:
        # 获取各行的单元格内容、单元格类型、列跨度、所含单元格数
        tr_content, tr_type, tr_col, tr_n_tds = tr_processing(tr)
        for td in tr_1_content:
            # 寻找下一个空位
            while content[i,j] != None:
                j += 1
            content[i:i+tr]

        i += 1
        j = 0







def tr_processing(tr):
    """
        行处理        
    :param tr: html的tr tag 
    :return: 
            tr_content: ndarray 行内容
            tr_type: list 行类型
            tr_col: 行长度
            n_tds: 所含单元格数
    """
    tr_col = 0 # 行长度
    tr_content = [] # 行各单元内容
    tr_type = [] # 行各单元格数据类型
    tds = tr.find_all('td')
    n_tds = len(tds)
    for i, td in enumerate(tds):
        if td.has_attr('colspan'):
            td_colspan = td['colspan']
        else:
            td_colspan = 1
        if td.has_attr('rowspan'):
            td_rowspan = td['rowspan']
        else:
            td_rowspan = 1
        td_type = np.array([[text_type(td.text)]*td_colspan]*td_rowspan).reshape(td_rowspan, td_colspan)
        td_content = np.array([[td.text]*td_colspan]*td_rowspan).reshape(td_rowspan, td_colspan)
        tr_type.append(td_type)
        tr_col = tr_col+td_colspan
        tr_content.append(td_content)
    return tr_content, tr_type, tr_col, n_tds



    





# --- title 判断 ---
for i, t in enumerate(tables_tag_new):
    text = t[0]
    # 第一行  tr 行  td 单元格
    print('{0}:{1}'.format(i, text))
    trs = t[1].find_all('tr', recursive=False)
    rows_len = len(trs) # 总行数












