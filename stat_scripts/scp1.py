#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 统计脚本1
Created on 2018-07-06
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
def t():
    import extract.increase_or_decrease as id
    import re
    res, total, has_table = id.get_content(True)
    normal = []
    negative = {}
    neg_part_table = {} # 负样本中的残表
    stat =['元|均价|价格']
    reg = re.compile(stat[0])
    for index in res:
        satisfied = False  # 是否满足条件
        contents = res[index][0]
        part_table = res[index][1]
        tables = []
        for content in contents:
            if content['type'] in ['single_table', 'multi_col_tables', 'multi_row_tables']:
                table = content['content']
                tables.append(table)
                headers = [i.strip() for i in table['headers'] if re.search(reg, i.strip()) != None]
                if headers != []:
                    satisfied = True
                    normal.append(index)
        if satisfied == False and not part_table:
            negative[index] = tables
        if satisfied == False and part_table:
            neg_part_table[index] = contents
    print('总公告数:{0}'.format(total))
    print('含表格数:{0}'.format(has_table))
    print('--------------------'*3)
    print('统计字段:'+' '.join(stat))
    print('满足条件:{0}'.format(len(normal)))
    print('负样本:{0}'.format(len(negative)))
    print('负样本（含残表）:{0}'.format(len(neg_part_table)))
    return
if __name__ == '__main__':
    t()
    pass