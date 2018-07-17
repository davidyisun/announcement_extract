#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 内容转换分类合并
Created on 2018-07-16
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import re
import copy
from html_table import table_preprocess


def _check_title(text):
    """
        判断章节title
    :param text:
    :return:
    """
    res = ''
    reg = '^目 *录'
    reg0 = '^释 *义'
    reg1 = '^重大事项提示'
    reg2 = '^第[一二三四五六七八九十\d]{1,2}章'
    reg3 = '^第[一二三四五六七八九十\d]{1,2}节'
    reg4 = '^[一二三四五六七八九十]{1,2}、'
    reg4_no = '星星点灯'
    reg5 = '^（[一二三四五六七八九十]{1,2}）'
    reg5_no = '星星点灯'
    reg6 = '^\d{1,2}[、.]'
    reg6_no = '星星点灯'
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
    if len(re.findall(re.compile(reg2), text)) == 1 and _check_phrase(text):
        res = 'title_zhang'
        return res
    if len(re.findall(re.compile(reg3), text)) == 1 and _check_phrase(text):
        res = 'title_jie'
        return res
    if len(re.findall(re.compile(reg4), text)) == 1 and _check_phrase(text):
        res = 'title_h1'
        return res
    if len(re.findall(re.compile(reg5), text)) == 1 and _check_phrase(text):
        res = 'title_h1_'
        return res
    if len(re.findall(re.compile(reg6), text)) == 1 and _check_phrase(text):
        res = 'title_h2'
        return res
    return res


def _check_phrase(text):
    """
        判断短语
    :param text:
    :return:
    """
    res = False
    reg = re.compile('.')
    reg_no = re.compile('：|，|。|？|！')
    if re.findall(reg, text) != [] and re.findall(reg_no, text) == []:
        res = True
    return res


def _key_value_processing(text):
    key = text.split('：')[0]
    value = text.split('：')[1]
    return key+'---->'+value


def _check_promption(text):
    if re.findall(re.compile('：$'), text) != []:
        return 'key'
    if re.findall(re.compile('：'), text) != ['：'] or re.findall(re.compile('，|。|？|！'), text[:-1]) != []:
        return ''
    if re.findall(re.compile('，$'), text) != []:
        return 'key-part_value'
    return 'key-value'


def _check_sentence(text):
    res = False
    if re.findall(re.compile('。$'), text) != []:
        res = True
    return res


def _check_part_sentence(text):
    res = False
    if re.findall(re.compile('，|。'), text) != [] and _check_sentence(text) == []:
        res = True
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
    text = text.strip()
    text = re.sub(re.compile(' +$'), text)
    title = _check_title(text)  # 找title
    if title != '':
        return title
    # 判断是否为短语
    if _check_phrase(text):
        return 'phrase'
    # 判断是否为提示语
    promption = _check_promption(text)
    if promption != '':
        return promption
    # 判断是否为sentence
    if _check_sentence(text):
        return 'sentence'
    # 判断是否为 part_sentence
    if _check_part_sentence(text):
        return 'part_sentence'
    return 'other'

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


def _check_merge(pre_type, cur_type, cur_text, pre_text):
    """
        节点合并 非表格 text 为文本 表格 text 为trs
    :param pre_type:
    :param cur_type:
    :param cur_text:
    :param pre_text:
    :return:
    """
    # 首个文段判断
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
        if len(pre_text) > 16:
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
    # 残句--提示head/完整提示/残句提示
    if cur_type == 'promption_head' and pre_type in ['key', 'key-part_value', 'key-value']:
        _cur_text = pre_text+cur_text
        _cur_type = text_classify(_cur_text)
        return True, _cur_text, _cur_type
    # table--table
    if cur_type in ['table_trs'] and pre_type in ['table_trs']:
        _cur_text = pre_text + cur_text
        _cur_type = 'table_trs'
        return True, _cur_text, _cur_type
    return False, cur_text, cur_type


def _check_title_merge(pre_content, content):
    """
        检查table title合并
    :param pre_type:
    :param pre_content: 不是当前tr的pre_content 而是pre_pre_content
    :param content:
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
    return res


def check_table(type, content):
    """
        检查数据是否为表格
    :param type:
    :param content: trs_tag 形式
    :return:
    """
    table_trs = False
    res = [{'content': content, 'type': type}]
    if type in ['key-value']:
        res = [{'content': _key_value_processing(content), 'type': type}]
    if type in ['table_trs']:
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
        pass
    return table_trs, res


def tags_format(tags_list):
    """
        tags转换
    :param tags_list: list 有tags组成的list
    :return:
    """
    part_table = False  # 是否有残表
    file_failed = []  # 残表名单
    contents = []
    pre_content = ''  # 之前的content
    pre_type = ''  # 之前的content 类型
    cur_content = ''  # 当前的content
    cur_type = ''  # 之前的content 类型
    for j, i in enumerate(tags_list):
        # 获取当前tag的类型
        cur_type, cur_content = content_classify(i)  # cur_content 包含tr 形式的 table --'table_trs'
        # 检查合并
        ismerge, cur_content, cur_type = _check_merge(pre_type, cur_type, cur_content, pre_content)
        _pre_content = cur_content
        _pre_type = cur_type
        if not ismerge:
            is_trans_table_trs, content = check_table(pre_type, pre_content)
            if content == 'normalize failed':
                # 转换失败
                part_table = True
                file_failed.append(pre_content)
                # 更新当前记录器
                pre_type = _pre_type
                pre_content = _pre_content
                continue
            if is_trans_table_trs: # 是否需要转换表格
                if contents != []:
                    _content = _check_title_merge(contents[-1], content) # 合并title
                else:
                    _content = content
            else:
                _content = content
            contents = contents + _content
        pre_type = _pre_type
        pre_content = _pre_content

    if cur_type == 'table_trs':
        is_trans_table_trs, content = check_table(cur_type, cur_content)
        if contents != []:
            _content = _check_title_merge(contents[-1], content)
        else:
            _content = content
    else:
        _content = [{'content': cur_content, 'type': pre_type}]
    contents = contents + _content
    return contents, part_table, file_failed