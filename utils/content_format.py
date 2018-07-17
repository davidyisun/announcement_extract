#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 内容转换合并
Created on 2018-07-16
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import re


def _check_title(text):
    res = 0
    reg = '^目 *录'
    reg0 = '^释 *义'
    reg1 = '^重大事项提示'
    reg2 = '^第[一二三四五六七八九十\d]{1,2}章'
    reg3 = '^第[一二三四五六七八九十\d]{1,2}节'
    reg4 = '^[一二三四五六七八九十]{1,2}、'
    reg4_no = '^[一二三四五六七八九十]{1,2}、'
    if len(re.findall(re.compile(reg), text)) == 1:
        if len(re.findall(re.compile(reg), text)[0]) == len(text):
            res = 'mulu'
            return res
    if len(re.findall(re.compile(reg0), text)) == 1:
        if len(re.findall(re.compile(reg0), text)[0]) == len(text):
            res = 'shiyi'
            return res
    if len(re.findall(re.compile(reg1), text)) == 1:
        if len(re.findall(re.compile(reg1), text)[0]) == len(text):
            res = 'zhongdashixiangtishi'
            return res
    if len(re.findall(re.compile(reg2), text)) == 1:
        res = 'title_zhang'
        return res
    if len(re.findall(re.compile(reg3), text)) == 1:
        res = 'title_jie'
        return res
    if len(re.findall(re.compile(reg4), text)) == 1:
        res = 'title_jie'
        return res

    return res


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
    title = _check_title()  # 找title
    if title != 0 :
        return title


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


def content_classify(tag):
    """
        content节点分类
    :param tag:
    :return:
    """
    if type(tag) == str:
        # ---文本---
        _text = tag
        _text = re.sub(' ', '', _text)
        cur_content = _text.strip()
        cur_type = text_classify(cur_content)
    else:
        cur_content = tag
        cur_type = 'table_trs'
    return cur_type, cur_content



def tags_format(tags_list):
    """
        tags转换
    :param tags_list: list 有tags组成的list
    :return:
    """
    part_table = False # 是否有残表
    file_failed = [] # 残表名单
    contents = []
    pre_content = ''  # 之前的content
    pre_type = ''  # 之前的content 类型
    cur_content = ''  # 当前的content
    cur_type = ''  # 之前的content 类型
    for j, i in enumerate(tags_list):
        # 获取当前tag的类型
        cur_type, cur_content = content_classify(i)  # cur_content 包含tr 形式的 table --'table_trs'
    return