
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
result = pd.read_table('../data/temp/hzl_csv.txt', sep='\t', encoding='utf8', header=None)
lable = pd.read_table('../data/train_data/train_labels/chongzu.train', sep='\t', encoding='utf8', header=None)
headers = ['id', 'mark', 'mark_com', 'jiaoyiduifang', 'price', 'method']
result.columns = headers[:-1]
lable.columns = headers

res1 = result_compare.fields_compare(df_label=lable, df_result=result, main_key=['id', 'mark_com'], fileds=['mark'], is_print=True)
res2 = result_compare.fields_compare(df_label=lable, df_result=result, main_key=['id', 'mark'], fileds=['mark_com'], is_print=True)
pass
