
#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: temp_test
Created on 2018-07-30
@author:David Yisun
@group:data
"""
import sys
sys.path.append('../')
import pandas as pd
from utils import result_compare
result = pd.read_table('../data/temp/hzl_csv_duifang.txt', sep='\t', encoding='utf8', header=None)
lable = pd.read_table('../data/train_data/train_labels/chongzu.train', sep='\t', encoding='utf8', header=None)
headers = ['id', 'mark', 'mark_com', 'jiaoyiduifang', 'price', 'method']
result.columns = headers
lable.columns = headers

# res1 = result_compare.fields_compare(df_label=lable, df_result=result, main_key=['id', 'mark_com'], fileds=['mark'], is_print=True)
# res2 = result_compare.fields_compare(df_label=lable, df_result=result, main_key=['id', 'mark'], fileds=['mark_com'], is_print=True)

not_in_id = set(lable['id'].tolist()).difference(set(result['id'].tolist()))
d1 = lable[lable['id'].isin(not_in_id)]

res = result_compare.fields_compare(df_label=lable, df_result=result, main_key=['id', 'mark', 'mark'], fileds=headers[3:], is_print=True)

pass
