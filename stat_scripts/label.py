#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: label
Created on 2018-07-06
@author:David Yisun
@group:data
"""
import pandas as pd
path = './data/train_data/train_labels/'
filename = 'zengjianchi.train'
filepath = path+filename
heads = ['股东全称', '股东简称', '变动截止日期', '变动价格', '变动数量', '变动后持股数', '变动后持股比例']
data = pd.read_table(filepath, names=heads, sep='\t')





