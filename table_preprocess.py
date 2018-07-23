#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 表格预处理
Created on 2018-06-13
@author:David Yisun
@group:data
"""
import os
from bs4 import BeautifulSoup
import codecs
import re
import itertools
import numpy as np


# 读入htmls 以字典形式保存
def read_html():
    classify = ['重大合同', '增减持', '定增']
    file_list = []
    for _classify in classify:
        path = './data/round2_adjust/{0}/html/'.format(_classify)
        files_name = os.listdir(path)
        file_list = [{'file_name': i, 'path': path + i, 'classify': _classify} for i in files_name] + file_list
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
def get_all_tables():
    # --- 获取所有表格进行分析 ---
    tables_tag = []
    html_dict = read_html()
    for index in html_dict:
        print(index)
        t = html_dict[index]
        # 删去不含text 的"tr" "tbody"
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
    return tables_tag_new


def text_type(s):
    """
        判断单元格数据类型
    :param s:
    :return:
    """
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
        td_rowspan = int(td['rowspan'])
    if td.has_attr('colspan'):
        td_colspan = int(td['colspan'])
    # -填充空单元格
    if td.text == '':
        for t_child in td.stripped_strings:
            t_child.replace_with('---')
    print(text_type(td.text))
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
    print('good boy')
    tr_most_rowspan = 1 # 最大跨行数
    tr_most_colspan = 1 # 最大跨列数
    tds = tr.find_all('td')
    n_tds = len(tds)  # 行所含单元格数
    tr_content = []  # 行各单元内容
    tr_type = []  # 行各单元格数据类型
    tr_cols = 0  # 行长度
    count_tr_colspan = 0  # colspan大于1的td个数统计
    for td in tds:
        data = td_processing(td)
        if data['td_colspan'] > tr_most_colspan:
            tr_most_colspan = data['td_colspan']
        if data['td_rowspan'] > tr_most_rowspan:
            tr_most_rowspan = data['td_rowspan']
        tr_content.append(data['td_content'])
        tr_type.append(data['td_type'])
        tr_cols = tr_cols+data['td_colspan']
        if data['td_colspan'] > 1:
            count_tr_colspan += 1
    if count_tr_colspan == n_tds:
        all_has_multi_colspan = True
    else:
        all_has_multi_colspan = False
    res = {'tr_most_colspan': tr_most_colspan,
           'tr_most_rowspan': tr_most_rowspan,
           'n_tds': n_tds,
           'all_has_multi_colspan': all_has_multi_colspan,
           'tr_content': tr_content,
           'tr_cols': tr_cols}
    return res


def find_title(tr):
    """
        查找表格title
    :param tr:
    :return: 若有 输出 text; 否则 输出 -1
    """
    data = tr_processing(tr)
    if data['n_tds'] == 1:
        return data['tr_content'][0][0][0]
    else:
        return -1


def check_headers(tr):
    """
        检查表头headers
    :param tr:
    :return:
    """
    data = tr_processing(tr)
    type = ''
    headers_array = np.empty(shape=(data['tr_most_rowspan'], data['tr_cols']), dtype='object')
    res = {'type': type,
           'headers_array': headers_array}
    # --- 整个header被分为多个独立子header 暂不处理 example 10
    if data['all_has_multi_colspan']:
        res['type'] = 'multi_sub_tables'
        return res
    # --- 连续整行  暂不处理
    if data['n_tds'] == 1:
        res['type'] = 'continous_rows'
        return res
    # --- 单行多列 直接提取
    if data['tr_most_colspan'] == 1 and data['tr_most_rowspan'] == 1:
         pass
    # --- 不含rowspan 部分td有colspan 左右拆该单元格 然后将其下数据合并 记录colspan的位置 example 8
    # --- 不含colspan 部分td有rowspan 先拆后合


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
    type = ''
    # --- 逐行填表 ---
    for i, tr in enumerate(trs):
        # --- check title ---
        if title == None:
            title = find_title(tr)
            if title != -1: # 表格内部含title 迭代下一个tr
                continue
        else:  # 有 title 定义为多表嵌套（分为母子表和并列表） 暂不考虑
            sub_title = find_title(tr)
            if sub_title != -1: # 存在多表嵌套
                type = 'multi-tables'

        # --- check headers ---
        if headers_type == '':
            # 还没有表头
            headers_array = check_headers(tr)
            continue
        if headers_type == 'part_headers':
            # 残缺表头
            headers_array = complete_headers(tr, headers_array)


if __name__ == '__main__':
    tables = get_all_tables()
    data_list = []
    for i, t in enumerate(tables):
        text = t[0]
        print('{0}:{1}'.format(i, text))
        d = table_processing(t[1])
        if d == None:
            continue
        if d['all_has_multi_colspan'] and d['tr_most_rowspan']== True:
            data_list.append(t)
    print('ok')

