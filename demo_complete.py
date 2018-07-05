#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" 完整demo
    脚本名: html格式整理（含表格部分）
    html来源: 内部购买的商用软件转换的html
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
import pandas as pd
import json

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


def content_classify(tag):
    """
        content节点分类
    :param tag:
    :return:
    """
    if tag.name != 'table':
        # ---文本---
        _text = tag.get_text()
        _text = re.sub(' ', '', _text)
        cur_content = _text.strip()
        cur_type = text_classify(cur_content)
    else:
        cur_content = tag.find_all('tr')
        cur_type = 'table_trs'
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
    if cur_type in ['table_trs'] and pre_type in ['table_trs']:
        _cur_text = pre_text + cur_text
        _cur_type = 'table_trs'
        return True, _cur_text, _cur_type
    # other--table
    # if cur_type in ['table_trs'] and pre_type not in ['table_trs']:
    #     return True, cur_text, cur_type
    return False, cur_text, cur_type


def check_table(type, content):
    """
        检查数据是否为表格
    :param type: 
    :param content: trs_tag 形式
    :return: 
    """
    table_trs = False
    if type not in ['table_trs']:
        res = [{'content': content, 'type': type}]
    else:
        table_trs = True
        res = []
        table_list = table_processing(content)
        if table_list == 'normalize failed':
            # 转换失败
            return table_trs, table_list
        for table in table_list:
            if table['type'] in ['false_table']:
                # 假表
                type = 'sentence'
                content = table['title']
                res.append({'content': content, 'type': type})
                continue
            res.append({'content': table, 'type': table['type']})
    return table_trs, res


def find_title(tr_dict):
    """
        查找表格title
    :param tr_dict: 经过tr_processing处理过后的tr tag
    :return: 若有 输出 text; 否则 输出 -1
    """
    if tr_dict['n_tds'] == 1:
        return tr_dict['tr_content'][0][0, 0]
    else:
        return -1


def table_processing(trs_list):
    """
        对trs以list的形式parser
    :param trs_list: html tr标签 list
    :return: 
    """
    main_title = ''  # 表名
    tables = []
    # 计算表的基本信息
    cols = 0
    trs_content = []
    for i, tr in enumerate(trs_list):
        tr_info = tr_processing(tr)
        cols = max(cols, tr_info['tr_cols'])
        # 过滤空行
        if tr_info['tr_text'] in ['', ' ']:
            continue
        trs_content.append(tr_info)
    # 切表 按行
    _table = []
    trs_content.reverse()  # 倒序检索 分割表格
    for tr_dict in trs_content:
        _table.append(tr_dict)
        if tr_dict['tr_most_colspan'] == cols:
            _table.reverse()
            tables.append(_table)
            _table = []
    if _table != []:
        _table.reverse()
        tables.append(_table)  # append最前一个表
    tables.reverse()  # 还原顺序
    # 解析表格
    title_append = True # 总标题append开关
    n_subtable = 0
    # 寻找主标题
    while title_append:
        if len(tables) == 0: # 表头走完 假表
            title_append = False
            continue
        if len(tables[0]) != 1:  # 遍历完tables
            title_append = False
            continue
        main_title = tables[0][0]['tr_content'][0][0, 0] + main_title
        tables.pop(0)  # 删除
    # 检查假表
    if len(tables) == 0:
        type = 'false_table'
        return [{'title': main_title,
                 'type': type,
                 'df': main_title}]
    # 检查多行子表
    if len(tables) > 1:
        table_type = 'multi_row_tables'  # 多行子表
        _tables = []
        for i in tables: # 合成一张表
            _tables = _tables + i
        _table_col = _tables[0]['tr_cols']
        _table_row = len(_tables)
        try:
            _table, trs_letf = trs_formalized(_tables, array_shape=(_table_row, _table_col))
        except Exception as e:
            print('the Exception:', e)
            return 'normalize failed'
        _table = pd.DataFrame(_table)
        return [{'title': main_title,
                 'type': table_type,
                 'headers': [],
                 'df': _table}]
    # 单表解析
    table_parsed = parser_table(tables[0], main_title)
    return table_parsed

    # # 解析表格
    # for n, table in enumerate(tables):
    #     # 寻找总标题 获取主表名 main_title
    #     if len(table) == 1 and title_append:
    #         if main_title == None:
    #             main_title = tables[0][0]['tr_content'][0][0, 0]
    #         else:
    #             main_title = tables[0][0]['tr_content'][0][0, 0]+main_title
    #         continue
    #     else:
    #         title_append = False
    #         n_subtable = len(tables)-n # 字表数量
    #         # 检查多行子表
    #         if n_subtable >1:
    #             table_type = 'multi_row_tables' # 多行子表
    #             _table_col = table[0]['tr_cols']
    #             _table_row = len(table)
    #             try:
    #                 _table, trs_letf = trs_formalized(table, array_shape=(_table_row, _table_col))
    #             except Exception as e:
    #                 print('the Exception:', e)
    #                 return 'normalize failed'
    #             _table = pd.DataFrame(_table)
    #             return [{'title': main_title,
    #                     'type': table_type,
    #                      'headers': [],
    #                      'df': _table}]
    #     # 单表解析
    #     table_parsed = parser_table(table, main_title)
    #     if table_parsed == 'normalize failed':
    #         # 转换失败
    #         return table_parsed
    #
    #
    # # 完全分割的单表list
    # table_list = table_parsed
    # # table_type = 'complete_tables'
    # return table_list


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
    tr_content = []  # 行各单元内容 list
    tr_type = []  # 行各单元格数据类型
    tr_text = tr.get_text() # tr的get.text
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
           'tr_cols': tr_cols,
           'tr_text': tr_text}
    return res


def td_processing(td):
    """
        单元格信息
    :param td: tag 单元格
    :return: 字典包括以下：
        内容 类型 跨列 跨行
        res: 
           'td_content': ndarray,
           'td_type': str,
           'td_colspan': int,
           'td_rowspan': int
    """
    td_rowspan = 1
    td_colspan = 1
    if td.has_attr('rowspan'):
        td_rowspan = int(td['rowspan'])
    if td.has_attr('colspan'):
        td_colspan = int(td['colspan'])
    # -单元格原始text提取
    text = td.get_text()
    # -填充空单元格
    if td.get_text() == '':
        td_text = '---'
    else:
        td_text = td.text
    # print(cell_text_type(td.text))
    td_type = np.array([[cell_text_type(td_text)] * td_colspan] * td_rowspan).reshape(td_rowspan, td_colspan)
    td_content = np.array([[td_text] * td_colspan] * td_rowspan).reshape(td_rowspan, td_colspan)
    res = {'td_content': td_content,
           'td_type': td_type,
           'td_colspan': td_colspan,
           'td_rowspan': td_rowspan,
           'td_text': text}
    return res


def trs_formalized(trs_dict, array_shape):
    """
        填表
    :param trs_dict: dict trs字典对象 自定义 
    :param array_shape:  tuple 需要填充的table的shape
    :return: 
            outarray: np.array 填充完成的数组
            table: 剩余的trs_dict
    """
    out_array = np.empty(shape=array_shape, dtype='object')
    i = 0
    j = 0
    table = copy.deepcopy(trs_dict)
    while None in out_array:
        _tr = table[0]
        table.pop(0)
        for td in _tr['tr_content']:
            end_i = td.shape[0] + i
            end_j = td.shape[1] + j
            out_array[i:end_i, j:end_j] = td
            # 定位下一个空单元格
            _next_cell = cell_location(out_array, out_array.shape[0], out_array.shape[1])
            if _next_cell == 'filling_full':
                # 填完array
                break
            # 更新坐标
            i = _next_cell[0]
            j = _next_cell[1]
    return out_array, table


def cell_text_type(s):
    """
        判断单元格数据类型
    :param s:
    :return:
    """
    res = 'string'
    if s == '---':
        res = 'placeholder'
        return res
    return res


def cell_location(_np_array, n_row, n_col):
    i = 0
    j = 0
    # print(n_row)
    # print(n_col)
    while _np_array[i, j] != None:
        # print('indicator:({0},{1})'.format(i, j))
        # print('content:'+str(_np_array[i, j]))
        j += 1
        if j >= n_col:  # 先找行 再找列
            j = 0
            i += 1
        if i >= n_row:
            return 'filling_full'
    return [i, j]


def parser_table(trs_dict, main_title):
    """
        单表解析
    :param trs_text:
    :return:
    """
    title = ''
    content = []
    # print('parser')
    # 找title
    if find_title(trs_dict[0]) != -1:
        title = find_title(trs_dict[0])
        trs_dict.pop(0)
    # 合并title
    main_title = main_title + title
    # 检查多列子表 和 单表
    _tr = trs_dict[0]
    if _tr['all_has_multi_colspan'] and _tr['tr_most_rowspan'] == 1:
        type = 'multi_col_tables'  # 多列子表
        _table_col = _tr['tr_cols'] # 列
        _table_row = len(trs_dict) # 行
        try:
            # 转换失败
            _table, _trs_left = trs_formalized(trs_dict, array_shape=(_table_row, _table_col))
        except Exception as e:
            print('the Exception:', e)
            return 'normalize failed'
        _table = pd.DataFrame(_table)
        return [{'title': main_title,
                 'type': type,
                 'headers': [],
                 'df': _table}]
    else:
        tables = [trs_dict]
        type = 'single_table'
    # 处理单表 可能是多个表并列而成 遍历每个表
    for table in tables:
        # 找子表名
        _title = ''
        if find_title(table[0]) != -1:
            _title = find_title(table[0])
            table.pop(0)
        sub_title = main_title+_title
        # 找 headers
        _tr = table[0] # 取首列 定大小
        n_col = _tr['tr_cols']  # 矩阵列数
        try:
            headers_array, table = trs_formalized(table, array_shape=(_tr['tr_most_rowspan'], _tr['tr_cols']))
        except Exception as e:
            print('the Exception:', e)
            return 'normalize failed'
        # i = 0
        # j = 0
        # while None in headers_array:
        #     _tr = table[0]
        #     table.pop(0)
        #     print('- - '*20)
        #     print(_tr['tr_content'])
        #     for td in _tr['tr_content']:
        #         end_i = td.shape[0]+i
        #         end_j = td.shape[1]+j
        #         headers_array[i:end_i, j:end_j] = td
        #         # 定位下一个空单元格
        #         print(headers_array)
        #         _next_cell = cell_location(headers_array, headers_array.shape[0], headers_array.shape[1])
        #         if _next_cell == 'complete':
        #             # 填完array
        #             break
        #         # 更新坐标
        #         i = _next_cell[0]
        #         j = _next_cell[1]

        # headers 按行合并
        _headers_list = []
        for i in headers_array.T:
            _h_list = []
            for k, j in enumerate(i):
                if j not in _h_list:
                    _h_list.append(j)
            _headers_list.append('-'.join(_h_list))
        # 找 table
        table_row = len(table)
        table_col = headers_array.shape[1]
        # table_array = np.empty(shape=(table_row, table_col), dtype='object')
        try:
            table_array, table = trs_formalized(table, array_shape=(table_row, table_col))
        except Exception as e:
            print('the Exception:', e)
            return 'normalize failed'
        # i = 0
        # j = 0
        # while None in table_array:
        #     _tr = table[0]
        #     table.pop(0)
        #     for td in _tr['tr_content']:
        #         end_i = td.shape[0]+i
        #         end_j = td.shape[1]+j
        #         table_array[i:end_i, j:end_j] = td
        #         # 定位下一个空单元格
        #         print(headers_array)
        #         _next_cell = cell_location(table_array, table_array.shape[0], table_array.shape[1])
        #         if _next_cell == 'complete':
        #             # 填完array
        #             break
        #         # 更新坐标
        #         i = _next_cell[0]
        #         j = _next_cell[1]
        # headers 按列合并
        df = pd.DataFrame()
        for i, head in enumerate(_headers_list):
            if head in df.columns:
                print(head)
                new_col = []
                for i in zip(df[head], table_array[:, i].astype(np.str)):
                    if i[0] == i[1]:
                        new_col.append(i[0])
                    else:
                        new_col.append(i[0]+'-'+i[1])
                df[head] = new_col
                # df[head] = df[head] + '-' + table_array[:, i].astype(np.str)
            else:
                df[head] = table_array[:, i].astype(np.str)
        # m = df.to_json()
        # n = json.loads(m)
        # p = pd.DataFrame(n)
        content.append({'title': sub_title,
                        'type': type,
                        'headers': _headers_list,
                        'df': df})
    # print('*  *  '*10)
    # print(content)
    return content


def check_title_merge(pre_content, content):
    """
        检查title合并
    :param pre_content: 不是当前tr的pre_content 而是pre_pre_content
    :param content: table_dict_list
    :return: 
    """
    if pre_content['type'] == 'promption_head':
        pre_title = pre_content['content']
    else:
        return content
    res = []
    for t in content:
        # 处理假表
        if t['type'] == 'sentence':
            res.append(t)
            continue
        _table_dict = t['content']
        _table_dict['title'] = pre_title + '-' + _table_dict['title']
        res.append({'content': _table_dict, 'type': _table_dict['type']})
        # # print(_table_dict)
        # # try:
        # #     print(_table_dict['title'] == -1)
        # # except:
        # #     print('ok')
        # try:
        #     _table_dict['title'] == -1
        # except:
        #     print('ok')
        # if _table_dict['title'] == -1:
        #     _table_dict['title'] = pre_title
        # else:
        #     if pre_title != -1:
        #         _table_dict['title'] = pre_title+'-'+_table_dict['title']
        # res.append({'content': _table_dict, 'type': _table_dict['type']})
    return res


def html_to_tags_list(html, _from='inner'):
    """
        原始html格式转换
    :param html: beautifulsoup 
    :param _from: str 文件来源
    :return: 
    """
    if _from=='inner':
        # 内部商用软件转换
        body = html.body
        content_tags = body.find_all(True, recursive=False)
        return content_tags


def get_content(tags_list):
    file_failed = [] # 转换失败的名单
    contents = []
    pre_content = ''  # 之前的content
    pre_type = ''  # 之前的content 类型
    cur_content = ''  # 当前的content
    cur_type = ''  # 之前的content 类型
    for j, i in enumerate(tags_list):
        # 滤过不含text和表格的 div
        t = i.find_all(text=True)
        if t == []:
            continue
        # tag 分类
        cur_type, cur_content = content_classify(i) # cur_content 包含tr 形式的 table --'table_trs'
        # print(cur_type)
        # 检查合并
        ismerge, cur_content, cur_type = check_merge(pre_type, cur_type, cur_content, pre_content)
        # print('---------------------------')
        # print(ismerge)
        # print('pre_type: ', pre_type, '   cur_type: ', cur_type)
        # print('####')
        # print('cur:')
        # print(cur_content)
        # print('####')
        # print('pre:')
        # print(pre_content)
        _pre_content = cur_content
        _pre_type = cur_type
        # append 最后一行
        if not ismerge:
            is_trans_table_trs, content = check_table(pre_type, pre_content)
            if content == 'normalize failed':
                # 转换失败
                file_failed.append(pre_content)
                # 更新当前记录器
                pre_type = _pre_type
                pre_content = _pre_content
                continue
            # print(content[0]['type'])
            # print(len(content))
            if is_trans_table_trs: # 是否需要转换表格
                if contents != []:
                    _content = check_title_merge(contents[-1], content) # 合并title
                else:
                    _content = content
                # _pre_content = _content[-1]['content'] error
                # _pre_type = _content[-1]['type'] error
            else:
                _content = content
                # _pre_content = cur_content error
                # _pre_type = cur_type error
            contents = contents + _content
        pre_type = _pre_type
        pre_content = _pre_content

    if cur_type == 'table_trs':
        is_trans_table_trs, content = check_table(cur_type, cur_content)
        if contents != []:
            _content = check_title_merge(contents[-1], content)
        else:
            _content = content
    else:
        _content = [{'content': cur_content, 'type': pre_type}]
    contents = contents + _content
    return contents


def check_table_write(content):
    """
        打印表格， 目前仅支持打印单表
                        {'title': sub_title,
                         'type': type,
                         'headers': _headers_list,
                         'df': df}
    :param content: 
    :return: 
    """
    res = []
    # 打印单表 single_table
    if content['type'] in ['single_table']:
        res.append('#--table---')
        _content = content['content']
        res.append('type:{0}'.format(_content['type']))
        if _content['title'] != -1:
            res.append('-  title  - {0}'.format(_content['title']))
        else:
            res.append('-  title  - {0}'.format('None'))
        res.append('headers:' + '  |  '.join(_content['headers']))
        table = _content['df'].astype('str').values.tolist()
        _table = ['  |  '.join(i) for i in table]
        res = res + _table
        res.append('#--table---')
        return res
    # 杂表
    if content['type'] in ['multi_col_tables', 'multi_row_tables']:
        res.append('#--table---')
        _content = content['content']
        res.append('type:{0}'.format(_content['type']))
        if _content['title'] != -1:
            res.append('-  title  - {0}'.format(_content['title']))
        else:
            res.append('-  title  - {0}'.format('None'))
        try:
            table = _content['df'].astype('str').values.tolist()
        except:
            pass
        _table = ['  |  '.join(i) for i in table]
        res = res + _table
        res.append('#--table---')
        return res
    # 其他
    return [content['content']]
        

if __name__ == '__main__':
    file_info = get_path_args()
    html_dict = read_html2(filepath=file_info['file_path'], filename=file_info['file_name'])
    contents = {}
    for n, index in enumerate(html_dict):
        print('processing {0} -- total: {1} this: {2}'.format(index, len(html_dict), n))
        tags_list = html_to_tags_list(html=html_dict[index], _from='inner')
        content = get_content(tags_list)
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
        with codecs.open(file_info['save_path'] + index.replace('.html', '.txt'), 'w', 'utf-8') as f:
            print('--- writing {0}'.format(index + '.txt'))
            output = []
            for i in contents[index]:
                output = output + check_table_write(i)
            f.write('\n'.join(output))


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