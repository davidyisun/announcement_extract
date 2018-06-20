#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 表格预处理单个表格
Created on 2018-06-13
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""

#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名:单个html test
Created on 2018-06-12
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import codecs
from bs4 import BeautifulSoup
import os
import re
import copy


catalogue = '增减持'
path = './data/round2_adjust/{0}/html/'.format(catalogue)
file = path+'7544.html'
# --- 单个html ---
with codecs.open(file, 'r', 'utf8' ) as f:
    data = f.read()
data = re.sub(re.compile('>\n* *<'), '><', data)
data = re.sub(re.compile('\n'), '', data)
d = BeautifulSoup(data, 'lxml', from_encoding='utf-8')

tables = d.find_all('table')
table = tables[0].tbody

# 获取行总数
rows = table.find_all('tr', recursive=False)
n_rows = len(rows)

# 获取列总数
cols = t[0].find_all('td')

t = cols[0]




import pandas as pd
d1 = pd.read_html(file, header=0)
df = pd.DataFrame(d1)


# 统计单元格中既有colspan又有rowspan


