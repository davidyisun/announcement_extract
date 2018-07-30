#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 资产重组的相关统计
Created on 2018-07-19
@author:David Yisun
@group:data
"""
import sys
sys.path.append('../')
import pandas as pd
import re


data = pd.read_table('data/train_data/train_labels/chongzu.train', header=None, sep='\t')
data.columns = ['id', '交易标的', '标的公司', '交易对方', '交易标的作价', '评估方法']
#单篇公告抽取条数分布
id = data['id'].value_counts()
id = id.sort_values(ascending=False)
distribute_ratio = pd.concat([id.value_counts(), id.value_counts()/id.shape[0]], axis=1)
distribute_ratio.columns = ['amount', 'ratio']


# 统计【交易标的】相关
reg = re.compile('.*%的*')
d1 = data['交易标的'].str.replace(reg, '')
amount = d1.value_counts()
ratio = amount/d1.shape[0]
mark_dis = pd.DataFrame({'amount': amount, 'ratio': ratio})
mark_dis.to_csv('./result/mark_dis.csv', index=False)