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


catalogue = '增减持'
path = './data/round2_adjust/{0}/html/'.format(catalogue)
file = path+'7544.html'
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



def text_classify(text):
    """
        文段分类
    :param text:
    :return:
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



def check_text_merge(pre_type, cur_type, cur_text, pre_text):
    """
        文段合并
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
    return False, cur_text, cur_type




# 按tail层切割文档
div = {}
for _sec in section_list:
    d1 = d.find_all('div', id=_sec['node_name'])[0]
    contents = []
    pre_content = ['']     # 之前的content
    pre_type = ''        # 之前的content 类型
    cur_content = ['']     # 当前的content
    cur_type = ''        # 之前的content 类型
    content_sec = d1.find_all('div', type='content')

    for i in content_sec:
        # 滤过不含text和表格的 div
        t = i.find_all(text=True)
        if t==[]:
            continue
        if i.find_all('table') == []:
            # ---文本---
            _text = t[0].strip()
            cur_content=[_text]
            cur_type = text_classify(cur_content[0])
            ismerge, cur_content[0], cur_type = check_text_merge(pre_type, cur_type, cur_content[0], pre_content[0])
            if not ismerge:
                contents.append(copy.deepcopy({'content': pre_content, 'type': pre_type}))
            pre_content[0] = cur_content[0]
            pre_type = cur_type
        else:
            continue
            # ---表格---
    # 添加最后一个content
    contents.append({'content': cur_content, 'type': cur_type})
    div[_sec['node_name']] = contents

























