#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 增减持表格信息抽取
Created on 2018-07-06
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import re
import pandas as pd
from fomat_conversion import tianchi_html_complete as convert
import copy
import numpy as np


# 获取数据
def get_content(has_table=True):
    path = '/data/hadoop/yisun/data/tianchi/train_data/增减持/html/'  # 220 地址
    # path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\训练数据\\round1_train_20180518\\增减持\\html\\'
    filename = None
    # outpath = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\outpath\\train\\increase_or_decrease\\'
    # 本地测试
    # path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\训练数据\\round1_train_20180518\\增减持\\html\\'
    # filename = '100829.html'
    # outpath = './data/temp/'
    html_dict = convert.read_html2(filepath=path, filename=filename)
    contents = {}
    for n, index in enumerate(html_dict):
        print('processing {0} -- total: {1} this: {2}'.format(index, len(html_dict), n))
        h = html_dict[index]
        # 是否一定要含有表格
        if has_table and h.find_all('table') == []:
            continue
        content = convert.get_content(h)
        content, part_table, table_failed = convert.content_format(content)
        contents[index] = [content, part_table, table_failed]
    total = len(html_dict)
    has_table = len(contents)
    return contents, total, has_table


def extract():
    # 比对表头
    contents = get_content()
    return


def extract_table(table_dict):
    # 寻找日期及股东名称
    # --- 正则格式为 [匹配， 不匹配]
    reg_date = [re.compile('日期|时间|期间'), re.compile('星星点灯')]
    reg_holders = [re.compile('股东名称|股东姓名'), re.compile('星星点灯')]
    reg_price = [re.compile('价格|均价|元'), re.compile('星星点灯')]
    reg_amount = [re.compile('股数'), re.compile('前|后')]
    reg_amount_later = [re.compile('后持有+.*股数'), re.compile('星星点灯')]
    reg_amount_ratio_later = [re.compile('后持有+.*比例*'), re.compile('星星点灯')]
    reg_method = [re.compile('持方式'), re.compile('星星点灯')]  # 增减持方式
    reg_share_nature = [re.compile('性质'), re.compile('星星点灯')] # 股份性质
    reg_dict = {'date': reg_date,                      # 变动截止日期
                'method': reg_method,                  # 增减持方式
                'holders': reg_holders,                # 股东名称
                'price': reg_price,                    # 增减持价格
                'amount': reg_amount,                  # 增减持数量
                'amount_later': reg_amount_later,      # 变动后持股数
                'amount_ratio_later': reg_amount_ratio_later,   # 变动后持股比例
                'share_nature': reg_share_nature}    # 股份性质
    data = pd.DataFrame(columns=['holders', 'date','method', 'price', 'amount', 'amount_later', 'amount_ratio_later', 'share_nature'])
    headers = table_dict['headers']
    df = table_dict['df']
    for header in headers:
        for reg in reg_dict:
            if re.search(reg_dict[reg][0], header) != None and re.search(reg_dict[reg][1], header) == None:
                data[reg] = df[header]
    data = data.dropna(axis=1) # 删除空列
    # 标记含主键的表格
    has_key = False
    if 'date' in data and data.shape[0] != 0:
        has_key = True
    return [data, has_key]


def tables_merge(tables):
    """
        多表合并
    :return:
    """
    _tables = copy.deepcopy(tables)
    # 找主键  --- 日期
    main_table = []
    other_tables = []
    for table in _tables:
        if table[1]:
            main_table.append(table[0])
        else:
            other_tables.append(table[0])
    # if len(main_table) > 1:
    #     return 'multi_keys'
    # if len(main_table) == 0:
    #     return 'no_keys'
    # return 'normal'
    if len(main_table) != 1:  # 只解析单个日期表
        return 'pass'
    date_table = copy.deepcopy(main_table[0])
    date_table = date_table.dropna(subset=['date'])
    # 有日期的
    date_table = date_table[date_table['date'].str.match(re.compile('\d{4}.{0,1}\d{1,2}'))]
    if 'holders' in date_table.columns:
        for _t in other_tables:
            if 'date' in _t.columns:
                # 有日期列
                _table = _t.dropna(subset=['date'])
                date_table = pd.merge(date_table, _table, on=['date'], how='left')
            else:
                if 'holders' in _t.columns:
                    # 含股东名字段 且 含有 股份性质
                    if 'share_nature' in _t.columns:
                        _other_table = _t[_t['share_nature'].str.contains('合计')]
                        _other_table = _other_table.reset_index(drop=True)
                    else:
                        _other_table = _t
                    date_table = pd.merge(date_table, _other_table, on=['holders'], how='left')
                else:
                    return [date_table, 'other has no holders']
    else:
        for _t in other_tables:
        # 没有主键的就直接拼接
            date_table = pd.concat([date_table, _t], axis=1)
        return [date_table, 'no_holders']
    # 整理表格内部结构
    date_list = date_table['date'].tolist()
    date = list(map(lambda x: re.findall(r'\d{4}[年\.-]\d{1,2}[月\.-]\d*日*', x)[-1], date_list))
    date = [re.sub(re.compile(r'日|月|年|\.'), '-', i) for i in date]
    date_table['date'] = date
    # 整理变动后股份
    if 'amount_later' in date_table.columns:
        amount_later = date_table['amount_later'].value_counts()
        if date_table.shape[0] > 1 and amount_later.shape[0] == 1:
            date_table['amount_later'][date_table['date'] != date_table['date'].max()] = np.nan
    # 整理变动后占比的信息
    if 'amount_ratio_later' in date_table.columns:
        amount_ratio_later = date_table['amount_ratio_later'].value_counts()
        if date_table.shape[0] > 1 and amount_ratio_later.shape[0] == 1:
            date_table['amount_ratio_later'][date_table['date'] != date_table['date'].max()] = np.nan
    return [date_table, 'complete']


def main():
    res, total, has_table = get_content(True)
    result1 = {}
    result2 = {}
    for n, index in enumerate(res):
        contents = res[index][0]
        name = index.replace('.html', '')
        result1[name] = []
        print('extract {0} -- total: {1} this: {2}'.format(index, len(res), n))
        for content in contents:
            if content['type'] in ['single_table']:
                # 提取信息
                data = extract_table(content['content'])
                result1[name].append(data)
        print('-----merge ********')
        result2[name] = tables_merge(result1[name])
    return result1, result2


if __name__ == '__main__':
    res1, res2 = main()
    pass


