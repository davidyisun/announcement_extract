#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名:
Created on 2018--
@author:David Yisun
@group:data
"""
import sys
sys.path.append('../')
from stat_scripts import title_structure
import pandas as pd
data = title_structure.main()

label = pd.read_table('data/train_data/train_labels/chongzu.train', sep='\t', header=None)
label.columns = ['id', 'mark', 'mark_com', 'jiaoyiduifang', 'price', 'method']

method = label.dropna(subset=['method'])
l = method['id'].astype('str').tolist()

has_no_reg = data['has_no_reg']

# 没抽出来

not_in_id = set(l).intersection(set(has_no_reg))


# have a look
t = data['content']['681722']
