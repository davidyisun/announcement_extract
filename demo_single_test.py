#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名:
Created on 2018--
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""

def get_content(html):
    body = html.body
    # 去掉表格
    tables = body.find_all('table')
    for i in tables:
        i.decompose()
    for s in body.stripped_strings:

