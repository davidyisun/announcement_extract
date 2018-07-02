#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 表格模块测试
Created on 2018-07-02
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
from demo_text import *
from bs4 import BeautifulSoup
def t():
    filepath = './data/temp/'
    filename = '1142820.html'
    html_dict = read_html2(filepath, filename)
    contents = {}
    for index in html_dict:
        content = get_content(html_dict[index])
        contents[index] = content
    print(contents)


def test_table():
    """
        表格处理模块测试
    :return: 
    """
    t1 = '<table border="1"> <tr><td rowspan="2" style="vertical-align:middle;"> <p><span class="font3">股东名称</span></p></td><td rowspan="2" style="vertical-align:middle;"> <p><span class="font3">减持方式</span></p></td><td rowspan="2" style="vertical-align:middle;"> <p><span class="font3">减持时间期间</span></p></td><td colspan="2" style="vertical-align:bottom;"> <p><span class="font3">本次减持股份</span></p></td></tr> <tr><td style="vertical-align:bottom;"> <p><span class="font3">股数（万股）</span></p></td><td style="vertical-align:bottom;"> <p><span class="font3">占总股本比例</span></p></td></tr> <tr><td rowspan="3" style="vertical-align:middle;"> <p><span class="font3">惠州市德赛工业发展</span></p> <p><span class="font3">有限公司</span></p></td><td style="vertical-align:middle;"> <p><span class="font3">集中竞价交易</span></p></td><td style="vertical-align:middle;"> <p><span class="font2">2010 </span><span class="font3">年 </span><span class="font2">8 </span><span class="font3">月 </span><span class="font2">19 </span><span class="font3">日至</span></p> <p><span class="font2">2012</span><span class="font3">年</span><span class="font2">5</span><span class="font3">月</span><span class="font2">18</span><span class="font3">日</span></p></td><td style="vertical-align:middle;"> <p><span class="font2">191.56</span></p></td><td style="vertical-align:middle;"> <p><span class="font2">1.4%</span></p></td></tr> <tr><td style="vertical-align:bottom;"> <p><span class="font3">大宗交易</span></p></td><td> <p></p></td><td> <p></p></td><td> <p></p></td></tr> <tr><td style="vertical-align:bottom;"> <p><span class="font3">其它方式</span></p></td><td> <p></p></td><td> <p></p></td><td> <p></p></td></tr> </table>'
    table = BeautifulSoup(t1, 'lxml')
    trs = table.find_all('tr')
    data = table_processing(trs)
    return


if __name__ == '__main__':
    test_table()

