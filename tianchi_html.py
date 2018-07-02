#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 天池html非table格式转换 
    先将html抽出text
    再进行规则化
Created on 2018-07-02
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import codecs
from bs4 import BeautifulSoup
import os
import re
import copy
import numpy as np
import bs4
# 读入htmls 以字典形式保存
def read_html2(filepath, filename=None):
    file_list = []
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
        _html = BeautifulSoup(data, 'lxml', from_encoding='utf-8')
        html_dict[_file['file_name']] = _html
        text_dict[_file['file_name']] = data
    return html_dict


def get_content(tag):
    """
        获取text信息z
    :param tag: 
    :return: 
    """

    contents = []
    if type(tag) == bs4.element.NavigableString:
        contents.append(tag)
        return contents
    else:
        # 检查 title
        if tag.has_attr('title'):
            contents.append(tag['title'])
        # 没有文字
        if tag.find_all(text=True) == []:
            return contents
        # 没有子节点
        tags_children = tag.contents
        if tags_children == []:
            return contents
        for tag_child in tags_children:
            _contents = get_content(tag_child)
            if _contents != []:
                contents = contents + _contents
    return contents


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
        节点合并
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
        _cur_text = _cur_text.replace(' ', '')
        _cur_type = 'phrase'
        return True, _cur_text, _cur_type
    # 短语(长度较长)--残句或整句
    if cur_type in ['part_sentence', 'sentence'] and pre_type == 'phrase':
        if len(pre_text) > 14:
            _cur_text = pre_text + cur_text
            _cur_text = _cur_text.replace(' ', '')
            _cur_type = cur_type
            return True, _cur_text, _cur_type
    # 残句--短语
    if cur_type == 'phrase' and pre_type == 'part_sentence':
        _cur_text = pre_text+cur_text
        _cur_text = _cur_text.replace(' ', '')
        _cur_type = 'part_sentence'
        return True, _cur_text, _cur_type
    # 残句--残句
    if cur_type == 'part_sentence' and pre_type == 'part_sentence':
        _cur_text = pre_text+cur_text
        _cur_text = _cur_text.replace(' ', '')
        _cur_type = 'part_sentence'
        return True, _cur_text, _cur_type
    # 残句--整句
    if cur_type == 'sentence' and pre_type == 'part_sentence':
        _cur_text = pre_text+cur_text
        _cur_text = _cur_text.replace(' ', '')
        _cur_type = text_classify(_cur_text)
        return True, _cur_text, _cur_type
    # 残句--提示head
    if cur_type == 'promption_head' and pre_type == 'part_sentence':
        _cur_text = pre_text+cur_text
        _cur_type = 'promption_head'
        _cur_text = re.sub(re.compile('： *'), '：', _cur_text)
        return True, _cur_text, _cur_type
    # 残句--完整提示
    if cur_type == 'complete_promption' and pre_type == 'part_sentence':
        _cur_text = pre_text+cur_text
        _cur_type = 'complete_promption'
        _cur_text = re.sub(re.compile('： *'), '：', _cur_text)
        return True, _cur_text, _cur_type
    # 提示head--短语、整句
    if cur_type in ['phrase', 'sentence'] and pre_type == 'promption_head':
        _cur_text = pre_text+cur_text
        _cur_type = 'complete_promption'
        _cur_text = re.sub(re.compile('： *'), '：', _cur_text)
        return True, _cur_text, _cur_type
    # 提示head--残句
    if cur_type in ['part_sentence'] and pre_type == 'promption_head':
        _cur_text = pre_text+cur_text.replace(' ', '')
        _cur_type = 'part_sentence'
        _cur_text = re.sub(re.compile('： *'), '：', _cur_text)
        return True, _cur_text, _cur_type
    # table--table
    if cur_type in ['table'] and pre_type in ['table']:
        _cur_text = pre_text + cur_text
        _cur_type = 'table'
        return True, _cur_text, _cur_type
    return False, cur_text.replace(' ', ''), cur_type


def content_format(txt_list):
    contents = []
    pre_content = ''  # 之前的content
    pre_type = ''  # 之前的content 类型
    cur_content = ''  # 当前的content
    cur_type = ''  # 之前的content 类型
    for i in txt_list:
        if i == '':
            continue
        cur_content = i
        cur_type = text_classify(i)
        # 检查合并
        ismerge, cur_content, cur_type = check_merge(pre_type, cur_type, cur_content, pre_content)
        # print(cur_content.replace(' ', ''))
        if not ismerge:
            contents.append(copy.deepcopy({'content': pre_content, 'type': pre_type}))
        pre_content = cur_content
        pre_type = cur_type
    # 添加最后一个content
    contents.append({'content': cur_content, 'type': cur_type})
    return contents


if __name__ == '__main__':
    path = './data/0605/重大合同/html/'
    filename = None
    outpath = './data/0605_txt/重大合同/'
    html_dict = read_html2(filepath=path, filename=filename)
    total = 0
    for index in html_dict:
        # 去掉表格tag
        h = html_dict[index]
        for i in h.find_all('table'):
            i.decompose()
        content = get_content(h)
        content = [re.sub(' +', '', i) for i in content]
        content = content_format(content)
        content = [i['content'] for i in content]
        print(content)
        with codecs.open(outpath+index.replace('.html', '.txt'), 'w', 'utf-8') as f:
            print('--- writing {0}'.format(index.replace('.html', '.txt')))
            f.write('\n'.join(content))
            total += 1
            print('counts:'+str(total))