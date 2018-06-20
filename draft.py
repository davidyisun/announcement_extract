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



