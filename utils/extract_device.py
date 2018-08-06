#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 抽取工具
Created on 2018-08-03
@author:David Yisun
@group:data
"""
from utils import content_format, tian_chi
import re


def get_pre_content(path, filename, drop_table=False, keys=['mulu', 'shiyi', 'major_promption', 'content'], text_trans=False, df_json=True):
    """
        获取文件的预信息
    :param path:
    :param filename:
    :param drop_table:
    :param keys:
    :param text_trans:
    :return:
    """
    html_dict = tian_chi.read_html(filepath=path, filename=filename)
    contents = {}
    for n, index in enumerate(html_dict):
        print('processing {0} -- total: {1} this: {2}'.format(index, len(html_dict), n))
        # 是否去掉表格tag
        h = html_dict[index]
        if drop_table:
            for i in h.find_all('table'):
                i.decompose()
        mulu, shiyi_dict, major_promption, tag = tian_chi.extract_pre_content(h)
        _content = tian_chi.get_content(tag)
        # 是否转换 tags ---> text list
        if text_trans:
            _content, part_table, table_failed = content_format.tags_format(_content, df_json=True)
        content = {'mulu': mulu,
                   'shiyi': shiyi_dict,
                   'major_promption': major_promption,
                   'content': _content}
        res = {}
        for i in keys:
            res[i] = content[i]
        contents[index] = res
    return contents


def get_file_tree(path, filename, drop_table=False, method='list', df_json=False):
    # --- pre_main ---
    html_dict = tian_chi.read_html(filepath=path, filename=filename)
    contents = {}
    data = {}
    for n, index in enumerate(html_dict):
        print('processing {0} -- total: {1} this: {2}'.format(index, len(html_dict), n))
        # 是否去掉表格tag
        h = html_dict[index]
        if drop_table:
            for i in h.find_all('table'):
                i.decompose()
        mulu, shiyi_dict, major_promption, tag = tian_chi.extract_pre_content(h)
        _content = tian_chi.get_content(tag)
        _content, part_table, table_failed = content_format.tags_format(_content, df_json=df_json)
        content = {'mulu': mulu,
                   'shiyi': shiyi_dict,
                   'major_promption': major_promption,
                   'content': _content}
        contents[index] = content
        res = content_format.FileTree(content['mulu'], content['shiyi'],
                           content['major_promption'], content['content'])
        # data = res.get_file_tree()
        if method == 'tree':
            res.get_file_tree()
        if method == 'list':
            res.get_tree_list()
        if method == 'both':
            res.get_file_tree()
            res.get_tree_list()
        data[index] = res
    return data


class RegObject(object):
    def __init__(self, name, reg_on_title='', reg_on_text='', reg_on_key='', title_depth=0):
        self.name = name
        self.reg_on_title = reg_on_title
        self.reg_on_text = reg_on_text
        self.reg_on_key = reg_on_key
        self.title_depth = title_depth



class ExtractDevice(content_format.FileTree):
    def __init__(self, mulu=[], shiyi={}, zhongdashixiangtishi='', content_list=[]):
        super(ExtractDevice, self).__init__(mulu, shiyi, zhongdashixiangtishi, content_list)

    def extract_from_shiyi(self, reg_object):
        """
            从【释义】中抽取信息
        :return:
        """
        if not isinstance(reg_object, RegObject):
            raise ValueError('Please Input The Object in the type RegObject')
        reg = reg_object.reg_on_key
        result = []
        for key in self.shiyi:
            if re.findall(reg, key) != []:
                result.append([key, self.shiyi[key]])
        return result

    def extract_from_content_on_title(self, reg_object, is_reg=True, reget_tree_list=False):
        """
            从【正文】中抽取信息
        :param reg_object: str 正则对象
        :param is_reg: bool 是否用正则
        :param title_depth: title 深度--与末端级别title的距离
        :return:
        """
        if not isinstance(reg_object, RegObject):
            raise ValueError('Please Input The Object in the type RegObject')
        if self.tree_list == '' or reget_tree_list:
            self.get_tree_list()
        reg = reg_object.reg_on_title
        title_depth = reg_object.title_depth
        res = []
        for title in self.titles:
            title_info = self._title_reg(reg=reg, title=title)
            if len(title_info) == 0:
                continue
            if title_info['distance'] == title_depth:
                content = self.get_tree_content_on_title(strcture=title_info['title'], method='content', reg=is_reg)
                if content == []:
                    continue
                res.append(['->'.join(title_info['title']), content])
        return res

    def _title_reg(self, reg, title):
        res = {}
        _title = re.sub(re.compile('--$'), '', title)
        _title = [i for i in _title.split('--')]
        n = 100
        for i, j in enumerate(_title):
            if re.findall(reg, j):
                n = len(_title) - i - 1
        if n < 100:
            res = {'title': _title, 'distance': n}
        return res


if __name__ == '__main__':
    pass
