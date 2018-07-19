#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名:test
Created on 2018-07-18
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import sys
sys.path.append('../')
from utils import other_tools, tian_chi, content_format
def t():
    """
        抽取预信息
    :return:
    """
    data = other_tools.get_tags()
    d = tian_chi.extract_pre_content(data)
    return d
if __name__ == '__main__':
    d = t()
    pass