
#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 
Created on 2018--
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""

import codecs
path = './data/0605_txt/重大合同/13023.txt'
with codecs.open(path, 'r', 'utf8') as f:
    l = f.read()
print(l.splitlines())