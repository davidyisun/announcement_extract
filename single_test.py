#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名:单个html test
Created on 2018-06-12
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

def content_classify(tag):
    """
        content节点分类
    :param tag:
    :return:
    """
    table_node = tag.find_all('table')
    if table_node == []:
        # ---文本---
        _text = tag.get_text()
        cur_content = _text.strip()
        cur_type = text_classify(cur_content)
    else:
        cur_content = tag.tbody.find_all('tr', recursive=False)
        cur_type = 'table'
    return cur_type, cur_content


def text_classify(text):
    """
        文段分类
    :param text:
    :return:
        phrase: 短语
        complete_promption： 完整提示
        sentence： 整句
        promption_head:  提示头
        part_sentence: 残句

    """
    if re.findall(re.compile('：|，|。|？'), text) == []:
        return 'phrase'
    if re.findall(re.compile('。$'), text) != []:
        if re.findall(re.compile('.+：.+'), text) != []:
            return 'complete_promption'
        return 'sentence'
    if re.findall(re.compile('：$'), text) != []:
        return 'promption_head'
    if re.findall(re.compile('，|。'), text) != []:
        return 'part_sentence'
    if re.findall(re.compile('.+：.+'), text) != []:
        return 'complete_promption'



def check_merge(pre_type, cur_type, cur_text, pre_text):
    """
        节点合并
    :param pre_type:
    :param cur_type:
    :param cur_text:
    :param pre_text:
    :return:
    """
    # 前一个为表格或完整句子
    if pre_type in ['']:
        _cur_text = cur_text
        _cur_type = cur_type
        return True, _cur_text, _cur_type
    # 两个连续短语
    if cur_type == 'phrase' and pre_type == 'phrase':
        _cur_text = pre_text+cur_text
        _cur_type = 'phrase'
        return True, _cur_text, _cur_type
    # 残句--短语
    if cur_type == 'phrase' and pre_type == 'part_sentence':
        _cur_text = pre_text+cur_text
        _cur_type = 'part_sentence'
        return True, _cur_text, _cur_type
    # 残句--残句
    if cur_type == 'part_sentence' and pre_type == 'part_sentence':
        _cur_text = pre_text+cur_text
        _cur_type = 'part_sentence'
        return True, _cur_text, _cur_type
    # 残句--整句
    if cur_type == 'sentence' and pre_type == 'part_sentence':
        _cur_text = pre_text+cur_text
        _cur_type = text_classify(_cur_text)
        return True, _cur_text, _cur_type
    # 残句--提示head
    if cur_type == 'promption_head' and pre_type == 'part_sentence':
        _cur_text = pre_text+cur_text
        _cur_type = 'promption_head'
        return True, _cur_text, _cur_type
    # 残句--完整提示
    if cur_type == 'complete_promption' and pre_type == 'part_sentence':
        _cur_text = pre_text+cur_text
        _cur_type = 'complete_promption'
        return True, _cur_text, _cur_type
    # 提示head--短语、整句
    if cur_type in ['phrase', 'sentence'] and pre_type == 'promption_head':
        _cur_text = pre_text+cur_text
        _cur_type = 'complete_promption'
        return True, _cur_text, _cur_type
    # 提示head--残句
    if cur_type in ['part_sentence'] and pre_type == 'promption_head':
        _cur_text = pre_text+cur_text
        _cur_type = 'part_sentence'
        return True, _cur_text, _cur_type
    # table--table
    if cur_type in ['table'] and pre_type in ['table']:
        _cur_text = pre_text + cur_text
        _cur_type = 'table'
        return True, _cur_text, _cur_type
    return False, cur_text, cur_type


def content_append(pre_type, pre_text):
    if pre_type not in ['table']:
        res = {'content': pre_text, 'type': pre_type}
    else:
        content = table_processing(pre_text)
    return


def table_processing(trs_list):
    title = None  # 表名
    headers = []  # 表头
    tables = []
    # 计算表的基本信息
    rows = 0
    cols = 0
    trs_content = []
    for i, tr in enumerate(trs_list):
        tr_info = tr_processing(tr)
        cols = max(cols, tr_info['tr_cols'])
        trs_content.append(tr_info)
    # 切表
    _table = []
    trs_content.reverse()  # 倒序检索 分割表格
    for tr in trs_content:
        _table.append(tr)
        if tr['tr_cols'] == cols:
            tables.append(_table.reverse())
            _table = []
    if _table != []:
        tables.append(_table)  # append最前一个表
    tables.reverse()  # 还原顺序

    # 解析表格
    n_subtable = len(tables) # 子表数量
    title_append = True
    for table in tables:
        # 寻找总标题
        if len(table) == 1 and title_append:
            title = tables[0][0]['tr_content'][0][0]+title
            continue
        else:
            title_append = False
            n_subtable = len(tables)
        # 解析单表
        parser_single_table(table)
    return


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


def text_type(s):
    """
        判断单元格数据类型
    :param s:
    :return:
    """
    res = 'string'
    return res


def parser_single_table(trs):
    """
        单表解析
    :param trs_text:
    :return:
    """
    title = ''
    for tr in trs:
        if title == '':
            title = find_title(tr)
            if title != -1: # 内涵表格 title 迭代下一个 tr
                continue
    return


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




catalogue = '重大合同'
path = './data/round2_adjust/{0}/html/'.format(catalogue)
file = path+'2467.html'
# --- 单个html ---
with codecs.open(file, 'r', 'utf8' ) as f:
    data = f.read()
data = re.sub(re.compile('>\n* *<'), '><', data)
data = re.sub(re.compile('\n'), '', data)
d = BeautifulSoup(data, 'lxml', from_encoding='utf-8')

# 甄别层级结构
reg = re.compile('SectionCode(_\d*)*')
section = []
parent_set = set() # 非终点子节点集合
for i in d.find_all('div', id=reg):
    # 空节点忽略
    if i.find_all(text=True) == []:
        continue
    # 是否含有表格
    has_table = True
    if i.find_all('table') == []:
        has_table = False
    # 确定 id 级别
    id = i['id']
    grade = len(re.findall('-', id))
    # 确定 节点 父节点
    if grade == 0:
        parent = 0
    else:
        parent = re.findall('.*?(?=-\d+$)', id)[0]
        parent_set.add(parent)
    # 获取 节点 title
    if i.has_attr('title'):
        _title = i['title']
    else:
        _title = None
    # 产生节点tree
    section.append({'node_name': id,
                    'parent_node': parent,
                    'node_grade': grade,
                    'title': _title,
                    'has_table':has_table})

section_list = [i for i in section if i['node_name'] not in parent_set]


# 按tail层切割文档
div = {}
for _sec in section_list:
    d1 = d.find_all('div', id=_sec['node_name'])[0]
    contents = []
    pre_content = ''     # 之前的content
    pre_type = ''        # 之前的content 类型
    cur_content = ''     # 当前的content
    cur_type = ''        # 之前的content 类型
    content_sec = d1.find_all('div', type='content') # 每个node下一层的content

    # for i in content_sec:
    #     # 滤过不含text和表格的 div
    #     t = i.find_all(text=True)
    #     if t==[]:
    #         continue
    #     table_node = i.find_all('table')
    #     if table_node == []:
    #         # ---文本---
    #         _text = t[0].strip()
    #         cur_content=[_text]
    #         cur_type = text_classify(cur_content[0])
    #         ismerge, cur_content[0], cur_type = check_text_merge(pre_type, cur_type, cur_content[0], pre_content[0])
    #         if not ismerge:
    #             contents.append(copy.deepcopy({'content': pre_content, 'type': pre_type}))
    #         pre_content[0] = cur_content[0]
    #         pre_type = cur_type
    #     else:
    #         if pre_type == 'table':
    #             cur_content = 0

    for i in content_sec:
        # 滤过不含text和表格的 div
        t = i.find_all(text=True)
        if t == []:
            continue
        # tag 分类
        cur_type, cur_content = content_classify(i)
        # 检查合并
        ismerge, cur_content, cur_type = check_merge(pre_type, cur_type, cur_content, pre_content)
        if not ismerge:
            contents.append(copy.deepcopy({'content': pre_content, 'type': pre_type}))
        pre_content = cur_content
        pre_type = cur_type

        # ---表格---
    # 添加最后一个content
    contents.append({'content': cur_content, 'type': cur_type})
    div[_sec['node_name']] = contents
    print(contents)

























