#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 仕锋软件转换 no table  子标签 含有 <p> <h*> <table>
Created on 2018--
@author:David Yisun
@group:data
"""
import codecs
import re
from bs4 import BeautifulSoup
import copy
import os
# 读入htmls 以字典形式保存
def read_html2(filepath, filename=None):
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


def content_classify(s):
    """
        content text 分类
    :param s:
    :return:
    """
    text = s
    text = re.sub(' ', '', text)
    cur_content = text.strip()
    cur_type = text_classify(cur_content)
    return cur_type, cur_content


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
        _cur_type = 'phrase'
        return True, _cur_text, _cur_type
    # 短语(长度较长)--残句或整句
    if cur_type in ['part_sentence', 'sentence'] and pre_type == 'phrase':
        if len(pre_text) > 20:
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
    # table--table
    if cur_type in ['table'] and pre_type in ['table']:
        _cur_text = pre_text + cur_text
        _cur_type = 'table'
        return True, _cur_text, _cur_type
    return False, cur_text, cur_type


def get_content(html):
    body = html.body
    # 去掉表格
    tables = body.find_all('table')
    for i in tables:
        i.decompose()
    s = []
    for p in body.find_all(True, recursive=False):
        _s = p.get_text()
        if _s == '':
            continue
        _s = _s.strip()
        s.append(_s)
    contents = []
    pre_content = ''  # 之前的content
    pre_type = ''  # 之前的content 类型
    cur_content = ''  # 当前的content
    cur_type = ''  # 之前的content 类型
    for i in s:
        cur_type, cur_content = content_classify(i)
        ismerge, cur_content, cur_type = check_merge(pre_type, cur_type, cur_content, pre_content)
        if not ismerge:
            contents.append(copy.deepcopy({'content': pre_content, 'type': pre_type}))
        pre_content = cur_content
        pre_type = cur_type
    contents.append({'content': cur_content, 'type': cur_type})
    return contents


if __name__ == '__main__':
    html_dict = read_html2(filepath='./data/data_shifeng/html/', filename=None)
    contents = {}
    for index in html_dict:
        content = get_content(html_dict[index])
        contents[index] = content
    # 写入txt
    for index in contents:
        # 有表格返回的是空值，跳过
        if contents[index] == None:
            continue
        with codecs.open('./data/data_shifeng_txt/'+index.replace('.html', '.txt'), 'w', 'utf-8') as f:
            print('--- writing {0}'.format(index+'.txt'))
            output = [i['content'] for i in contents[index]]
            f.writelines('\n'.join(output))
