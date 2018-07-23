#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 天池公告格式再整理
Created on 2018-07-16
@author:David Yisun
@group:data
"""
import codecs
from bs4 import BeautifulSoup
import os
import re
import copy
import numpy as np
import bs4
from optparse import OptionParser
import pandas as pd


# 获取读写路径
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


