#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 调试脚本
Created on 2018-07-06
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
def t():
    import extract.increase_or_decrease as id
    res = id.get_content()[0]
    return res

if __name__ == '__main__':
    t()
