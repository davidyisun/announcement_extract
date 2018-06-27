#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 草稿本
Created on 2018-06-14
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
# link： table_preprocecess
t = tables_tag[8832]
t[1].find_all(text=True)
k = html_dict['1636740.html']
# 总表格数
len(tables_tag)
len(tables_tag_new)
# 横标
len(row_title)
index = 0
row_title[index][0]
row_title[index][1].tr
print(row_title[index][1].prettify())
row_title[index][1].find_all(text=r'指')
# 列标
len(col_title)

# 不含标题
len(table_content)

# 统计单元格中既有colspan又有rowspan

def has_class_but_no_id(tag):
    return tag.has_attr('colspan') and tag.has_attr('rowspan')

tds = []
for index in html_dict:
    print(index)
    t = html_dict[index]
    m = t['h'].find_all(has_class_but_no_id)
    if m == []:
        continue
    for i in m:
        tds.append([index, i.parent.parent])
print(len(tds))
tds[0][1].find_all(has_class_but_no_id)

# 统计 col 和 row 的先后关系
trs_all = []
trs_all_no = []
trs_head = []
trs_head_no = []

def has_colspan(tag):
    return tag.has_attr('colspan')


def has_rowspan(tag):
    return tag.has_attr('rowspan')


def has_class_but_no_id(tag):
    return tag.has_attr('colspan') and tag.has_attr('rowspan')


def t1(tr):
    colspan = tr.find_all(has_colspan)
    rowspan = tr.find_all(has_rowspan)
    if colspan == [] and rowspan == []:
        return 1
    if colspan == [] and rowspan != []:
        return 2
    if colspan != [] and rowspan == []:
        return 3
    col = False
    row = False
    r_c = False
    c_r = False
    res = False
    for k in tr.find_all('td'):  # 每个单元格
        if k.has_attr('rowspan'):
            row = True
            continue
        if k.has_attr('colspan') and row == True:
            return 4
    return 5

d1 = []
d2 = []
d3 = []
d4 = []
d5 = []




for index in html_dict:
    print(index)
    t = html_dict[index]
    m = t['h'].find_all('tr')
    if m == []:
        continue
    j = m[0]
    res = t1(j)
    if res == 1:
        d1.append([index, j])
    if res == 2:
        d2.append([index, j])
    if res == 3:
        d3.append([index, j])
    if res == 4:
        d4.append([index, j])
    if res == 5:
        d5.append([index, j])
len(d1)
len(d2)
len(d3)
len(d4)
len(d5)


# 统计行头每个都有colspan标签
data_list = []
for i, t in enumerate(tables_tag_new):
    text = t[0]
    print('{0}:{1}'.format(i, text))
    data = table_processing(t[1])
    if data['all_has_multi_colspan'] == True:
        data_list.append(t)


table_processing(tables_tag_new[0][1])

tbody = tables_tag_new[0][1]
trs = tbody.find_all('tr', recursive=False)
n_row = len(trs)  # 表行数
title = None  # 表名
headers_type = ''  # 表头类型
headers = []  # 表头
headers_array = np.array([None])  # 表头矩阵
fields_type = []  # 表字段类型
content = None
# --- 逐行填表 ---
for i, tr in enumerate(trs):
    # --- check title ---
    if title == None:
        title = find_title(tr)
        if title != -1:  # 表格内部不含title
            continue
    data = tr_processing(tr)
    break

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

len(data_list)
data_list[0][1]

d = tables[498]
m = table_processing(d[1])
d[1]


# 统计行头每个都有colspan标签
data_list = []
for i, t in enumerate(tables_tag_new):
    text = t[0]
    print('{0}:{1}'.format(i, text))
    data = table_processing(t[1])
    if data['all_has_multi_colspan'] == True:
        data_list.append(t)


# 统计连续整行
def stat_continous_rows(tables):
    data_list = []
    for i, t in enumerate(tables):
        text = t[0]
        print('{0}:{1}'.format(i, text))
        tbody = t[1]
        # --- 表属性定义 ---
        trs = tbody.find_all('tr', recursive=False)
        n_row = len(trs)  # 表行数
        title = None  # 表名
        headers_type = '' # 表头类型
        headers = []  # 表头
        headers_array = np.array([None]) # 表头矩阵
        fields_type = []  # 表字段类型
        content = None
        satisfied = False
        for j, tr in enumerate(trs):
            # --- check title ---
            if title == None:
                title = find_title(tr)
                if title != -1:  # 表格内部含title 迭代下一个tr
                    continue
            # --- check headers ---
            data = tr_processing(tr)
            type = ''
            if data['n_tds'] == 1:
                satisfied = True
                continue
            else:
                break
        if satisfied:
            data_list.append(t+[j])
    return data_list
d = stat_continous_rows(tables)



