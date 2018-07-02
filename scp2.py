#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 
Created on 2018--
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
from demo_txt import *

file_info = get_path_args()
txt_dict = read_txt(filepath='./data/data_txt/major_contracts/', filename='2379.txt')
contents = {}
for index in txt_dict:
    content = get_content(txt_dict[index])
    text = [j['content'] for j in content]
    contents[index] = text
    total = 0
    with codecs.open('./data/temp/a' + index, 'w', 'utf-8') as f:
        print('--- writing {0}'.format(index))
        s = '\n'.join(text)
        f.write(s)
        total += 1
        print('counts:' + str(total))
print('ok')