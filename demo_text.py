#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 非table 重大合同 信息整理
Created on 2018-06-27
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
import copy
from optparse import OptionParser

def get_path_args():
    usage = 'pdf_file_path_get'
    parser = OptionParser(usage=usage)
    parser.add_option('--filepath', action='store', dest='file_path', type='string', default='/data/hadoop/yisun/data/tianchi/重大合同html_new/')
    parser.add_option('--filename', action='store', dest='file_name', type='string', default='')
    parser.add_option('--savepath', action='store', dest='save_path', type='string', default='/data/hadoop/yisun/data/announcement_txt/no_table/major_contracts/')
    option, args = parser.parse_args()
    res = {'file_path': option.file_path,
           'file_name': option.file_name,
           'save_path': option.save_path}
    if res['file_name'] == '':
        res['file_name'] = None
    return res


# 读入htmls 以字典形式保存
def read_html():
    """
        读取html
    :return:
        example：
            html_dict['100103.html']['h']

   { '100103.html':{'classify': '定增',
                     'h': <html><head></head><body><div title="辽宁成………………}
   }
    """

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


def read_html2(filepath, filename=None):
    file_list = []
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
        _html = BeautifulSoup(data, 'lxml', from_encoding='utf-8')
        html_dict[_file['file_name']] = _html
        text_dict[_file['file_name']] = data
    return html_dict


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
        _text = re.sub(' ', '', _text)
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
        节点合并 非表格 text 为文本 表格 text 为trs
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
    # 短语(长度较长)--残句或整句
    if cur_type in ['part_sentence', 'sentence'] and pre_type == 'phrase':
        if len(pre_text) > 20:
            _cur_text = pre_text + cur_text
            _cur_type = cur_type
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


def check_table(type, content):
    if type not in ['table']:
        res = {'content': content, 'type': type}
    else:
        _content = table_processing(content)
        res = {'content': _content, 'type': type}
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


def table_processing(trs_list):
    table_type = ''
    title = None  # 表名
    tables = []
    res = {'title': title,
           'table_type': table_type,
           'tables': tables}
    # 计算表的基本信息
    rows = 0
    cols = 0
    trs_content = []
    for i, tr in enumerate(trs_list):
        tr_info = tr_processing(tr)
        cols = max(cols, tr_info['tr_cols'])
        trs_content.append(tr_info)
    # 切表 按行
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
    title_append = True # 总标题append开关
    n_subtable = 0
    for n, table in enumerate(tables):
        # 寻找总标题
        if len(table) == 1 and title_append:
            res['title'] = tables[0][0]['tr_content'][0][0]+res['title']
            continue
        else:
            title_append = False
            n_subtable = len(tables)-n # 字表数量
            # 检查多行子表
            if n_subtable > 1:
                res['table_type'] = 'multi_row_tables' # 多行子表
                return res
        # 单表解析
        single_type, single_content = parser_table(table)





    if n_subtable == 0:
        res['table_type'] = 'false_table' # 假表 只有title
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
    # print(cell_text_type(td.text))
    td_type = np.array([[cell_text_type(td.text)] * td_colspan] * td_rowspan).reshape(td_rowspan, td_colspan)
    td_content = np.array([[td.text] * td_colspan] * td_rowspan).reshape(td_rowspan, td_colspan)
    res = {'td_content': td_content,
           'td_type': td_type,
           'td_colspan': td_colspan,
           'td_rowspan': td_rowspan}
    return res


def cell_text_type(s):
    """
        判断单元格数据类型
    :param s:
    :return:
    """
    res = 'string'
    return res


def cell_location(_np_array, n_row, n_col):
    i = 0
    j = 0
    while _np_array[i, j] != None:
        j += 1
        if j + 1 > n_col:  # 先找行 再找列
            i += 1
        if i > n_row:
            return 'complete'
    return [i, j]




def parser_table(trs):
    """
        单表解析
    :param trs_text:
    :return:
    """
    title = ''
    type = ''
    content = []
    check_multi_col_tables = False
    # 找title
    title = find_title(trs[0])
    if title != -1:
        trs = trs[1:]
    # 检查多列子表
    _tr = tr_processing(trs[0])
    if _tr['all_has_multi_colspan'] and _tr['tr_most_rowspan'] == 1:
        type = 'multi_col_tables'  # 多列子表
        tables = []
        return type, content
    else:
        tables = [trs]
    # 处理单表
    for table in tables:
        # 找子表名
        _title = find_title(table[0])
        if _title == -1 and title == -1:
            sub_title = -1
        if _title == -1 and title != -1:
            sub_title = title
        if _title != -1 and title != -1:
            sub_title = title+_title
            table = table[1:]
        if _title != -1 and title == -1:
            sub_title = _title
            table = table[1:]
        # 找 headers
        _tr = tr_processing(table[0])
        n_col = _tr['tr_cols']  # 矩阵列数
        headers_array = np.empty(shape=(_tr['tr_most_rowspan'], _tr['tr_cols']), dtype='object')
        i = 0
        j = 0
        while None in headers_array:
            _tr = tr_processing(table[0])
            table = table[1:0]
            for td in _tr['content']:
                end_i = td.shape[0]+i
                end_j = td.shape[1]+j
                headers_array[i:end_i, j:end_j] = td
                # 定位下一个空单元格
                _next_cell = cell_location(headers_array, _tr['tr_most_rowspan'], _tr['tr_cols'])
                if _next_cell == 'complete':
                    # 填完array
                    break
                # 更新坐标
                i = _next_cell[0]
                j = _next_cell[1]


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


def get_content(html):
    body = html.body
    if body.find_all('table') == []:
        content_tags = body.find_all('p', recursive=False)
        contents = []
        pre_content = ''  # 之前的content
        pre_type = ''  # 之前的content 类型
        cur_content = ''  # 当前的content
        cur_type = ''  # 之前的content 类型
        for i in content_tags:
            # 滤过不含text和表格的 div
            t = i.find_all(text=True)
            if t == []:
                continue
            # tag 分类
            cur_type, cur_content = content_classify(i)
            # 检查合并
            ismerge, cur_content, cur_type = check_merge(pre_type, cur_type, cur_content, pre_content)
            if not ismerge:
                content = check_table(pre_type, pre_content)
                contents.append(copy.deepcopy({'content': content, 'type': pre_type}))
            pre_content = cur_content
            pre_type = cur_type
        contents.append({'content': cur_content, 'type': cur_type})
        return contents
    return


if __name__ == '__main__':
    file_info = get_path_args()
    html_dict = read_html2(filepath=file_info['file_path'], filename=file_info['file_name'])
    contents = {}
    for index in html_dict:
        content = get_content(html_dict[index])
        contents[index] = content
        """
        contents example:
                {'20526259.html': [{'content': '证券代码：600759', 'type': 'complete_promption'},
                                    {'content': '证券简称：洲际油气', 'type': 'complete_promption'},
                                    …………]}
        """
    # 写入txt
    for index in contents:
        # 有表格返回的是空值，跳过
        if contents[index] == None:
            continue
        with codecs.open(file_info['save_path']+index+'.txt', 'w', 'utf-8') as f:
            print('--- writing {0}'.format(index+'.txt'))
            output = [i['content'] for i in contents[index]]
            f.writelines('\n'.join(output))



    # with codecs.open('./data/temp/20526259.html', 'r', 'utf-8') as f:
    #     text = f.read()
    # text = re.sub(re.compile('>\n* *<'), '><', text)
    # text = re.sub(re.compile('\r*\n*\t*'), '', text)
    # b = BeautifulSoup(text, 'lxml')
    # print(b)
    # body = b.html.body
    # if b.find_all('table') == []:
    #     content_tags = body.find_all('p', recursive=False)
    #     contents = []
    #     pre_content = ''  # 之前的content
    #     pre_type = ''  # 之前的content 类型
    #     cur_content = ''  # 当前的content
    #     cur_type = ''  # 之前的content 类型
    #     for i in content_tags:
    #         # 滤过不含text和表格的 div
    #         t = i.find_all(text=True)
    #         if t == []:
    #             continue
    #         # tag 分类
    #         cur_type, cur_content = content_classify(i)
    #         # 检查合并
    #         ismerge, cur_content, cur_type = check_merge(pre_type, cur_type, cur_content, pre_content)
    #         if not ismerge:
    #             contents.append(copy.deepcopy({'content': pre_content, 'type': pre_type}))
    #         pre_content = cur_content
    #         pre_type = cur_type
    #     contents.append({'content': cur_content, 'type': cur_type})
    #     # print(contents)
    #     with codecs.open('output3.txt', 'a', 'utf8') as f:
    #         output = [i['content'] for i in contents]
    #         f.writelines('\n'.join(output))





