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


# 获取数据
def get_content(has_table=True):
    path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\训练数据\\round1_train_20180518\\增减持\\html\\'
    filename = None
    outpath = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\outpath\\train\\increase_or_decrease\\'
    # path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\数据\\训练数据\\round1_train_20180518\\增减持\\html\\'
    # filename = '100829.html'
    # outpath = './data/temp/'
    path = '/data/hadoop/yisun/data/tianchi/train_data/增减持/html/'  # 220 地址
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
                'amount_later_ratio_later': reg_amount_ratio_later,   # 变动后持股比例
                'share_nature': reg_share_nature}    # 股份性质
    data = pd.DataFrame(columns=['holders', 'date', 'price', 'amount', 'amount_later', 'amount_ratio_later'])
    headers = table_dict['headers']
    df = table_dict['df']
    for header in headers:
        for reg in reg_dict:
            if re.search(reg_dict[reg][0], header) != None and re.search(reg_dict[reg][1], header) == None:
                data[reg] = df[header]
    data = data.dropna(axis=1) # 删除空列
    # 标记含主键的表格
    has_key = False
    if 'date' in data:
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
    other_table = []
    for table in _tables:
        if table[1]:
            main_table.append(table[0])
        else:
            other_table.append(table[0])
    if len(main_table) > 1:
        return 'multi_keys'
    if len(main_table) == 0:
        return 'no_keys'
    return 'normal'


def main():
    res, total, has_table = get_content(True)
    result = {}
    result2 = {}
    for n, index in enumerate(res):
        print('processing {0} -- total: {1} this: {2}'.format(index, len(res), n))
        contents = res[index][0]
        result[index.replace('.html', '')] = []
        for content in contents:
            if content['type'] in ['single_table']:
                # 提取信息
                data = extract_table(content['content'])
                result[index.replace('.html', '')].append(data)
        result2[index.replace('.html', '')] = tables_merge(result[index])
    return result2


if __name__ == '__main__':
    res = main()
    pass


