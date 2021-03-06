#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 增减持表格信息抽取
Created on 2018-07-06
@author:David Yisun
@group:data
"""
import re
import pandas as pd
from fomat_conversion import tianchi_html_complete as convert
import copy
import numpy as np
from utils import text_normalize


# 获取数据
def get_content(has_table=True):
    path = './data/temp/'
    path = '/data/hadoop/yisun/data/tianchi/train_data/增减持/html/'  # 220 地址
    # path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\训练数据\\round1_train_20180518\\增减持\\html\\'
    filename = None
    # outpath = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\outpath\\train\\increase_or_decrease\\'
    # 本地测试
    path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\训练数据\\round1_train_20180518\\增减持\\html\\'
    filename = '10898.html'
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


def extract_table(table_dict):
    # 寻找日期及股东名称
    # --- 正则格式为 [匹配， 不匹配]
    reg_date = [re.compile('日期|时间|期间'), re.compile('星星点灯')]
    reg_holders = [re.compile('股东名称|股东姓名|姓名|股东及其一致行动人名称'), re.compile('星星点灯')]
    reg_price = [re.compile('价格|均价|价'), re.compile('总.*额|金额')]
    reg_amount = [re.compile('股数|数量'), re.compile('前|后|持有股数|持股数量|持有数量|比例*')]
    reg_amount_later = [re.compile('后持有.*股*数量*|[增减]持后.*股*数量*|当前持.*股*数量*'), re.compile('比例*')]
    reg_amount_ratio_later = [re.compile('后持有.*比例*|[增减]持后.*比例|当前持.*比例'), re.compile('星星点灯')]
    reg_method = [re.compile('持方式'), re.compile('星星点灯')]  # 增减持方式
    reg_share_nature = [re.compile('性质'), re.compile('星星点灯')] # 股份性质
    # 正则字典
    reg_dict = {'date': reg_date,                      # 变动截止日期
                'method': reg_method,                  # 增减持方式
                'holders': reg_holders,                # 股东名称
                'price': reg_price,                    # 增减持价格
                'amount': reg_amount,                  # 增减持数量
                'amount_later': reg_amount_later,      # 变动后持股数
                'amount_ratio_later': reg_amount_ratio_later,   # 变动后持股比例
                'share_nature': reg_share_nature}    # 股份性质
    data = pd.DataFrame(columns=['holders', 'date', 'method', 'price', 'amount', 'amount_later', 'amount_ratio_later', 'share_nature'])
    headers = table_dict['headers']
    df = table_dict['df']
    unit = {}  # 表头单位识别
    for header in headers:
        for reg in reg_dict:
            if re.search(reg_dict[reg][0], header) != None and re.search(reg_dict[reg][1], header) == None:
                unit[reg] = text_normalize.unit_recognize(header)
                data[reg] = df[header]
    data = data.dropna(axis=1)  # 删除空列
    # 转换数值型字段
    filed_to_float = ['price', 'amount_ratio_later']
    filed_to_int = ['amount', 'amount_later']
    for head in filed_to_float:
        if head in data.columns:
            f = lambda x: text_normalize.float_normalize(x, type='float', unit=unit[head], dim=4)
            data[head] = data[head].map(f)
    for head in filed_to_int:
        if head in data.columns:
            f = lambda x: text_normalize.float_normalize(x, type='int', unit=unit[head], dim=4)
            data[head] = data[head].map(f)
    # 股东名空值 --> 向上填充
    if 'holders' in data.columns and data.shape[0] > 0:
        if data['holders'][0] != '---':
            f = lambda x: np.nan if x == '---' else x
            data['holders'] = data['holders'].map(f)
            data['holders'] = data['holders'].fillna(method='pad')
    # 标记含主键的表格
    has_key = False
    if 'date' in data and data.shape[0] != 0:
        has_key = True
    return [data, has_key]


def _groupby_fun1(df):
    """
        股份性质的聚合函数
    :param df:
    :return:
    """
    d = df[df['share_nature'].str.contains('合计|持有股份总数')]
    if d.shape[0] != 0:
        data = d.copy()
    else:
        data = df.copy()
    return data


def _groupby_fun2(df):
    """
        变动后持股数和比例的聚合函数
    :param df:
    :return:
    """
    data = df.copy()
    # 整理变动后股份
    if 'amount_later' in df.columns:
        amount_later = df['amount_later'].value_counts()
        if df.shape[0] > 1 and amount_later.shape[0] == 1:
            data['amount_later'][data['date'] != data['date'].max()] = np.nan
    # 整理变动后占比的信息
    if 'amount_ratio_later' in df.columns:
        amount_ratio_later = df['amount_ratio_later'].value_counts()
        if df.shape[0] > 1 and amount_ratio_later.shape[0] == 1:
            data['amount_ratio_later'][data['date'] != data['date'].max()] = np.nan
    return data


def date_transform(date_str):
    """
        时间格式转换
    :param date_str:
    :return:
    """
    res = date_str
    date = re.findall(r'\d{4}[年\.-]\d{1,2}[月\.-]\d*日*|\d{4}/\d{1,2}/\d*日*', date_str)
    if len(date) != 0:
        res = date [-1]
    res = re.sub(re.compile(r'月|年|\.|/'), '-', res)
    res = re.sub(r'日', '', res)
    s = res.split('-')
    if len(s) != 0:
        _res = []
        for i in s:
            k = i
            if len(i)<2:
                k = '0'+i
            _res.append(k)
        res = '-'.join(_res)
    return res


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
                        # 按股东分组抽取数据
                        _other_table = _t.groupby('holders').apply(_groupby_fun1)
                        # _other_table = _t[_t['share_nature'].str.contains('合计')]
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
    # 整理表格内部结构 --日期
    date_list = date_table['date'].tolist()
    date = list(map(date_transform, date_list))
    date_table['date'] = date
    # 整理表格内部结构 --价格
    # 按股东聚合
    if 'holders' in date_table.columns:
        date_table = date_table.groupby('holders').apply(_groupby_fun2)
    else:
        date_table = _groupby_fun2(date_table)
    date_table = date_table.reset_index(drop=True)
    return [date_table, 'complete']


def main():
    res, total, n_has_table = get_content(True)
    result1 = {}
    result2 = {}
    error = []
    for n, index in enumerate(res):
        contents = res[index][0]
        name = index.replace('.html', '')
        result1[name] = []
        print('extract {0} -- total: {1} this: {2}'.format(index, len(res), n))
        try:
            for content in contents:
                if content['type'] in ['single_table']:
                    # 提取信息
                    data = extract_table(content['content'])
                    # 空表继续
                    if data[0].shape[0] == 0:
                        continue
                    result1[name].append(data)
            print('-----merge ********')
            result2[name] = tables_merge(result1[name])
        except Exception as e:
            print('the exception is {0}'.format(e))
            print('wrong with {0}'.format(index))
            error.append(index)
            continue
    return result1, result2, error


if __name__ == '__main__':
    res1, res2, error = main()
    pass


