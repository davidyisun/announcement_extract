#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: html 表格格式处理
Created on 2018-07-17
@author:David Yisun
@group:data
"""
import pandas as pd
import numpy as np
import copy
import copy


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
    text = td.get_text().replace(' ', '')
    # -填充空单元格
    if text == '':
        td_text = '---'
    else:
        td_text = text
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
        填表 (转换方式应考虑换行的情况)
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
        try:
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
        except:
            break
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
    while _np_array[i, j] != None:
        j += 1
        if j >= n_col:  # 先找行 再找列
            j = 0
            i += 1
        if i >= n_row:
            return 'filling_full'
    return [i, j]


def parser_table(_trs_dict, main_title, df_json=False):
    """
        单表解析
    :param trs_dict:
    :param main_title: str title 前缀
    :param df_json: bool 是否以json形式存储dataframe
    :return:
    """
    title = ''
    content = []
    trs_dict = copy.deepcopy(_trs_dict)
    if find_title(trs_dict[0]) != -1:
        title = find_title(trs_dict[0])
        trs_dict.pop(0)
    # 合并title
    main_title = main_title + title
    # 检查多列子表 和 单表
    _tr = trs_dict[0]
    if _tr['all_has_multi_colspan'] and _tr['tr_most_rowspan'] == 1:
        type = 'multi_col_tables'   #  多列子表
        _table_col = _tr['tr_cols']  #  列
        _table_row = len(trs_dict)  #  行
        try:
            # 转换失败
            _table, _trs_left = trs_formalized(trs_dict, array_shape=(_table_row, _table_col))
        except Exception as e:
            print('the Exception:', e)
            return 'normalize failed'
        _table = pd.DataFrame(_table)
        if df_json:
            df = _table.to_json()
        else:
            df = _table
        return [{'title': main_title,
                 'type': type,
                 'headers': [],
                 'df': df}]
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
        _tr = table[0]  #  取首列 定大小
        n_col = _tr['tr_cols']  #  矩阵列数
        try:
            headers_array, table = trs_formalized(table, array_shape=(_tr['tr_most_rowspan'], _tr['tr_cols']))
        except Exception as e:
            print('the Exception:', e)
            return 'normalize failed'
        _headers_list = []
        for i in headers_array.T:
            _h_list = []
            for k, j in enumerate(i):
                if j not in _h_list:
                    _h_list.append(j)
            try:
                _headers_list.append('-'.join(_h_list))
            except:
                pass
        # 找 table
        table_row = len(table)
        table_col = headers_array.shape[1]
        try:
            table_array, table = trs_formalized(table, array_shape=(table_row, table_col))
        except Exception as e:
            print('the Exception:', e)
            return 'normalize failed'
        # headers 按列合并
        df = pd.DataFrame()
        for i, head in enumerate(_headers_list):
            if head in df.columns:
                # print(head)
                new_col = []
                for i in zip(df[head], table_array[:, i].astype(np.str)):
                    if i[0] == i[1]:
                        new_col.append(i[0])
                    else:
                        new_col.append(i[0]+'-'+i[1])
                df[head] = new_col
            else:
                df[head] = table_array[:, i].astype(np.str)
        if df_json:
            df = df.to_json()
        else:
            df = df
        content.append({'title': sub_title,
                        'type': type,
                        'headers': _headers_list,
                        'df': df})
    return content


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


def table2mat(trs):
    """
        table直接转换为df no head
    :param trs: beautifulsoup tag
    :return:
    """
    trs_dict = [tr_processing(i) for i in trs if i.get_text() not in ['', ' ']]
    table_col = trs_dict[0]['tr_cols']
    table_row = len(trs_dict)
    _table, trs_letf = trs_formalized(trs_dict, array_shape=(table_row, table_col))
    return _table


def table_processing(trs_list, df_json=False):
    """
        对trs以list的形式parser
    :param trs_list: html tr标签 list
    :param df_json: bool 是否以json形式存储dataframe
    :return:
    """
    main_title = ''  #  表名
    tables = []
    # 计算表的基本信息
    cols = 0
    trs_content = []
    for i, tr in enumerate(trs_list):
        tr_info = tr_processing(tr)
        trs_content.append(tr_info)
        # 过滤空行
        if tr_info['tr_text'] in ['', ' ']:
            continue
        cols = max(cols, tr_info['tr_cols'])
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
    title_append = True  # 总标题append开关
    # 寻找主标题
    while title_append:
        if len(tables) == 0:  # 表头走完 假表
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
        for i in tables:  # 合成一张表
            _tables = _tables + i
        _table_col = _tables[0]['tr_cols']
        _table_row = len(_tables)
        try:
            _table, trs_letf = trs_formalized(_tables, array_shape=(_table_row, _table_col))
        except Exception as e:
            print('the Exception:', e)
            return 'normalize failed'
        _table = pd.DataFrame(_table)
        if df_json:
            df = _table.to_json()
        else:
            df = _table
        return [{'title': main_title,
                 'type': table_type,
                 'headers': [],
                 'df': df}]
    # 单表解析
    table_parsed = parser_table(tables[0], main_title, df_json)
    return table_parsed