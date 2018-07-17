#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 规整txt文件（输入为从txt）
Created on 2018-06-28
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import sys
sys.path.append('../')
import copy
import os
import codecs
import re
from optparse import OptionParser


def get_path_args():
    usage = 'pdf_file_path_get'
    parser = OptionParser(usage=usage)
    parser.add_option('--filepath', action='store', dest='file_path', type='string', default='/data/hadoop/yisun/data/tianchi/重大合同html_new/')
    parser.add_option('--filename', action='store', dest='file_name', type='string', default='')
    parser.add_option('--savepath', action='store', dest='save_path', type='string', default='/data/hadoop/yisun/data/announcement_txt/no_table/major_contracts/')
    option, args = parser.parse_args()
    res = {'file_path': option.file_path,
           'file_name': option.file_name,
           'save_path': option.save_path}
    if res['file_name'] == '':
        res['file_name'] = None
    return res


def read_txt(filepath, filename=None):
    if filename == None:
        files_name = os.listdir(filepath)
    else:
        files_name = [filename]
    file_list = [{'file_name': i, 'file_path': filepath+i} for i in files_name if i.endswith('.txt')]
    txt_dict = {}
    for i, _file in enumerate(file_list):
        with codecs.open(_file['file_path'], 'r', 'utf8') as f:
            data = f.read()
            print('read {0}'.format(_file['file_name']))
        data = re.split(re.compile('\n+ {0,1}\n*'), data)
        txt_dict[_file['file_name']] = data
    return txt_dict


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
        if len(pre_text) > 20:
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


def get_content(txt_list):
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
    file_info = get_path_args()
    file_path = file_info['file_path']
    file_name = file_info['file_name']
    save_path = file_info['save_path']
    # file_path = './'
    # file_name = '600393_20180704_1205119639.txt'
    # save_path = './123/'
    txt_dict = read_txt(filepath=file_path, filename=file_name)
    contents = {}
    for index in txt_dict:
        content = get_content(txt_dict[index])
        text = [j['content'] for j in content]
        contents[index] = text
        total = 0
        with codecs.open(save_path+index, 'w', 'utf-8') as f:
            print('--- writing {0}'.format(index))
            f.write('\n'.join(text))
            total += 1
            print('counts:'+str(total))
