#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 内容转换分类合并
Created on 2018-07-16
@author:David Yisun
@group:data
"""
import sys
sys.path.append('../')
import re
from utils.html_table import *


# 检查text是否为title系列类型
def _check_title(text):
    """
        判断章节title
    :param text:
    :return:
    """
    res = ''
    # reg = '^目 *录'
    # reg0 = '^释 *义'
    # reg1 = '^重大事项提示'
    reg2 = '^第[一二三四五六七八九十\d]{1,2}章'
    reg3 = '^第[一二三四五六七八九十\d]{1,2}节'
    reg4 = '^[一二三四五六七八九十]{1,2}、'
    reg4_no = '星星点灯'
    reg5 = '^（[一二三四五六七八九十]{1,2}）'
    reg5_no = '星星点灯'
    reg6 = '^\d{1,2}[、．]'
    reg6_no = '星星点灯'
    # if len(re.findall(re.compile(reg), text)) == 1:
    #     if len(re.findall(re.compile(reg), text)[0]) == len(text):
    #         res = 'mulu'
    #         return res
    # if len(re.findall(re.compile(reg0), text)) == 1:
    #     if len(re.findall(re.compile(reg0), text)[0]) == len(text):
    #         res = 'shiyi'
    #         return res
    # if len(re.findall(re.compile(reg1), text)) == 1:
    #     if len(re.findall(re.compile(reg1), text)[0]) == len(text):
    #         res = 'zhongdashixiangtishi'
    #         return res
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


# 检查text是否为phrase类型
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


# 将xx:bb 转换为 key---->value
def _key_value_processing(text):
    key = text.split('：')[0]
    value = text.split('：')[1]
    return key+'---->'+value


# 检查text是否为提示性类型
def _check_promption(text):
    if re.findall(re.compile('：$'), text) != []:
        return 'key'
    if re.findall(re.compile('：'), text) != ['：'] or re.findall(re.compile('，|。|？|！'), text[:-1]) != []:
        return ''
    if re.findall(re.compile('，$'), text) != []:
        return 'key-part_value'
    return 'key-value'


# 检查text是否为sentence类型
def _check_sentence(text):
    res = False
    if re.findall(re.compile('。$'), text) != []:
        res = True
    return res


# 检查text是否为残句类型
def _check_part_sentence(text):
    res = False
    if re.findall(re.compile('，|。'), text) != [] and _check_sentence(text) == False:
        res = True
    return res


# text的分类函数
def text_classify(_text):
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
    text = _text.strip()
    text = re.sub(re.compile(' +$'), '', text)
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


# 内容的分类函数 包含 text和table
def content_classify(tag):
    """
        content节点分类
    :param tag: html tag标签
    :return:
    """
    if type(tag) == str:
        # ---文本---
        _text = tag
        cur_type = text_classify(_text)
        if cur_type != 'other':
            _text = re.sub(' ', '', _text)
        cur_content = _text.strip()
    else:
        cur_content = tag
        cur_type = 'table_trs'
    return cur_type, cur_content


# 检查前后content是否需要合并
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


# 检查是否添加表外title到table的title
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


# 检查是否处理表格类型数据 html ---> table_dict
def check_table(type, content, df_json=False):
    """
        检查数据是否为表格
    :param type:
    :param content: trs_tag 形式
    :param df_json: bool 是否以json形式存储dataframe
    :return:
    """
    table_trs = False
    res = [{'content': content, 'type': type}]
    if type in ['key-value']:
        res = [{'content': _key_value_processing(content), 'type': type}]
    if type in ['table_trs']:
        table_trs = True
        res = []
        try:
            table_list = table_processing(content, df_json)
        except IndexError:  # 不规范的表格
            table_list = 'buguifanbiaoge'
            return table_trs, table_list
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


# html tags ----> content_list 主函数
def tags_format(tags_list, df_json=False):
    """
        tags 转换
    :param tags_list: list 有tags组成的list
    :param df_json: bool 是否以json形式存储dataframe
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
            is_trans_table_trs, content = check_table(pre_type, pre_content, df_json)
            if content in ['normalize failed', 'buguifanbiaoge']:
                # 转换失败
                part_table = True
                file_failed.append(pre_content)
                # 更新当前记录器
                pre_type = _pre_type
                pre_content = _pre_content
                continue
            if is_trans_table_trs:  # 是否需要转换表格
                if contents != []:
                    _content = _check_title_merge(contents[-1], content)  # 合并title
                else:
                    _content = content
            else:
                _content = content
            contents = contents + _content
        pre_type = _pre_type
        pre_content = _pre_content

    if cur_type == 'table_trs':
        is_trans_table_trs, content = check_table(cur_type, cur_content, df_json=True)
        if content not in ['normalize failed', 'buguifanbiaoge']:
            if contents != []:
                _content = _check_title_merge(contents[-1], content)
            else:
                _content = content
    else:
        _content = [{'content': cur_content, 'type': pre_type}]
    contents = contents + _content
    return contents, part_table, file_failed


# content_list ----> file_tree 文档树结构
def to_file_tree(content_list):
    file_tree = {'title_class': (),
                 'title_series': [],
                 'title_index': []}
    title_list = ['title_zhang', 'title_jie', 'title_h1', 'title_h1_', 'title_h2']
    # for content in content_list:
    types = [i['type'] for i in content_list]
    return


class FileTree(object):
    def __init__(self, mulu=[], shiyi={}, zhongdashixiangtishi='', content_list=[]):
        """
            初始化
        :param mulu: list 目录
        :param shiyi: dict 释义
        :param zhongdashixiangtishi: str 重大事项提示
        :param content_list: list 正文
        """
        self.mulu = mulu   # 文档目录
        self.shiyi = shiyi    # 文档释义
        self.zhongdashixiangtishi = zhongdashixiangtishi    # 文档重大事项提示
        self.contents = content_list     # 文档内容
        self.types = [i['type'] for i in content_list]      # 文档各内容类型
        self.contents_text = [i['content'] for i in content_list]        # 文档文段内容
        # 文档结构
        _titles = ['title_zhang', 'title_jie', 'title_h1', 'title_h1_', 'title_h2']
        if 'title_h1' in self.types and 'title_h1_' in self.types:
            if self.types.index('title_h1') > self.types.index('title_h1_'):
                _titles = ['title_zhang', 'title_jie', 'title_h1_', 'title_h1', 'title_h2']
        self.title_structure = []  # 文档title
        for i, _title in enumerate(_titles):
            if _title in self.types:
                self.title_structure.append(_title)
        self.depth = len(self.title_structure)  # 文档最大深度
        self.file_tree = ''
        self.tree_list = ''
        self.titles = []   # 文档所有章节标题
    def get_file_tree(self):
        """
            ---> 文档树结构
        :return:
        """
        # 切割文段
        res = self._recursion_tree(content=self.contents, title=self.title_structure+['aaaa'])
        self.file_tree = res
        return res

    def _recursion_tree(self, content, title):
        _content = copy.deepcopy(content)
        types = [i['type'] for i in _content]
        step = ''
        for i in title:
            if i in types:
                step = i
                break
        if step == '':
            return _content
        else:
            if _content[0]['type'] != step:
                _content = [{'content': '', 'type': 'pre-'+step}] + _content
            sub_content_list = []  # 存储分割后的数据
            _sub_content = [_content[0]]  # 缓存分割数据
            # 分割tag
            for i in _content[1:]:
                if i['type'] == step:
                    sub_content_list.append(_sub_content)
                    _sub_content = []
                _sub_content.append(i)
            if _sub_content != []:
                sub_content_list.append(_sub_content)
            res = []
            for i in sub_content_list:
                if i == []:
                    continue
                if len(i) == 1:
                    sub_res = i
                else:
                    sub_res = self._recursion_tree(content=i[1:], title=title)
                res.append({'title': i[0]['content'],
                            'type': i[0]['type'],
                            'content': sub_res})
        return res


    def get_tree_content_on_title(self, strcture=[], reg=True, method='sub_tree'):
        if self.file_tree == '':
            self.get_file_tree()
        content = self.file_tree
        res = []
        if reg == True:
            _structure = [re.compile(i.replace('\\', '')) for i in strcture]
        else:
            _structure = strcture
        for i, j in enumerate(_structure):
            _content = []
            for z in content:
                if z.get('title') == None:
                    continue
                if re.findall(j, z['title']) != []:
                    if isinstance(z['content'], list):
                        _content = _content + z['content']
                    else:
                        _content = _content + [z['content']]
            content = _content
        if method == 'sub_tree':
            res = content
        if method == 'content':
            res = self._recursion_get_tree_content(content=content)
        return res


    def _recursion_get_tree_content(self, content):
        res = []
        if isinstance(content, list):
            for i in content:
                if isinstance(i['content'], str) or isinstance(i['content'], dict):
                    _res = [i]
                else:
                    _res = self._recursion_get_tree_content(i['content'])
                    if _res == []:
                        continue
                res = res + _res
        else:
            return [content]
        return res


    def get_tree_list(self):
        """
            ---> title线性list结构
        :return:
        """
        # 确定title层级
        _titles = ['title_zhang', 'title_jie', 'title_h1', 'title_h1_', 'title_h2']
        if 'title_h1' in self.types and 'title_h1_' in self.types:
            if self.types.index('title_h1') > self.types.index('title_h1_'):
                _titles = ['title_zhang', 'title_jie', 'title_h1_', 'title_h1', 'title_h2']
        structure = []
        for i, _title in enumerate(_titles):
            if _title in self.types:
                structure.append(_title)
        self.depth = len(structure)  # 文档最大深度
        _content = self.contents
        # 切割文段
        res = self._recursion_tree_list(content=_content, title=structure+['aaaa'])
        self.tree_list = res
        # 获取title
        self.titles = list(set([i['title'] for i in res]))
        return res

    def _recursion_tree_list(self, content, title):
        _content = copy.deepcopy(content)
        types = [i['type'] for i in _content]
        step = ''
        for i in title:
            if i in types:
                step = i
                break
        if step == '':
            return [{'title_type': 'content', 'title': '', 'type': i['type'], 'content': i['content']} for i in _content]
            # return [{'content': _content, 'title_type': 'content', 'title': ''}]
        else:
            if _content[0]['type'] != step:
                _content = [{'content': '', 'type': 'pre-'+step}] + _content
            sub_content_list = []  # 存储分割后的数据
            _sub_content = [_content[0]]  # 缓存分割数据
            # 分割tag
            for i in _content[1:]:
                if i['type'] == step:
                    sub_content_list.append(_sub_content)
                    _sub_content = []
                _sub_content.append(i)
            if _sub_content != []:
                sub_content_list.append(_sub_content)
            res = []
            for i in sub_content_list:
                _title = i[0]['content']
                _title_type = i[0]['type']
                if i == []:
                    continue
                if len(i) == 1:
                    res = res + [{'content': _title, 'title_type': _title_type, 'title': _title, 'type':_title_type}]
                else:
                    sub_res = self._recursion_tree_list(content=i[1:], title=title)
                    for j in sub_res:
                        __title = _title + '--' + j['title']
                        __title_type = _title_type + '--' + j['title_type']
                        __content = j['content']
                        __type = j['type']
                        res = res + [{'content': __content, 'title_type': __title_type, 'title': __title, 'type':__type}]
        return res

    def get_tree_content_on_text(self, reg_object, reg=True, reget_tree_list=False):
        """
             在【正文】中全文检索，定位条件句，获取 tree_list 元素
        :param reg_object:
        :param reg:
        :param reget_tree_list: bool 是否重新生成tree_list
        :return:
        """
        res = []
        if self.tree_list == '' or reget_tree_list:
            self.get_tree_list()
        if reg:
            reg_object = re.compile(reg_object)
        for i in self.tree_list:
            if re.findall(re.compile('table'), i['type']) != []:  # 仅从text里面找，不考虑表格
                continue
            if re.findall(reg_object, i['content']) != []:
                title = [j for j in i['title'].split('--') if j!='']
                content = i['content']
                _res = [title, content]
                res.append(_res)
        return res

if __name__ == '__main__':
    s = '2．发起人出资情况'
    n = _check_title(s)