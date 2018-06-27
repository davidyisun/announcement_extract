#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名:
Created on 2018--
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
from demo_text import *
if __name__ == '__main__':
    file_info = get_path_args()
    html_dict = read_html2(filepath='./data/temp/', filename=file_info['file_name'])
    contents = {}
    for index in html_dict:
        content = get_content(html_dict[index])
        contents[index] = content
        """
        contents example:
                {'20526259.html': [{'content': '证券代码：600759', 'type': 'complete_promption'},
                                    {'content': '证券简称：洲际油气', 'type': 'complete_promption'},
                                    …………]}
        """
    # 写入txt
    for index in contents:
        # 有表格返回的是空值，跳过
        if contents[index] == None:
            continue
        with codecs.open('./data/temp/'+index+'.txt', 'w', 'utf-8') as f:
            print('--- writing {0}'.format(index+'.txt'))
            output = [i['content'] for i in contents[index]]
            f.writelines('\n'.join(output))