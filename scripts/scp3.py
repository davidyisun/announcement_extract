#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 表格模块测试
Created on 2018-07-02
@author:David Yisun
@group:data
"""
from bs4 import BeautifulSoup
def t():
    from fomat_conversion import demo_complete as dc
    filepath = './data/temp/'
    filename = '1142820.html'
    html_dict =dc.read_html2(filepath, filename)
    contents = {}
    for index in html_dict:
        content = dc.get_content(html_dict[index])
        contents[index] = content
    print(contents)


# def test_table():
#     """
#         表格处理模块测试
#     :return:
#     """
#     from fomat_conversion import demo_complete as dc
#     t1 = '<table border="1"> <tr><td rowspan="2" style="vertical-align:middle;"> <p><span class="font3">股东名称</span></p></td><td rowspan="2" style="vertical-align:middle;"> <p><span class="font3">减持方式</span></p></td><td rowspan="2" style="vertical-align:middle;"> <p><span class="font3">减持时间期间</span></p></td><td colspan="2" style="vertical-align:bottom;"> <p><span class="font3">本次减持股份</span></p></td></tr> <tr><td style="vertical-align:bottom;"> <p><span class="font3">股数（万股）</span></p></td><td style="vertical-align:bottom;"> <p><span class="font3">占总股本比例</span></p></td></tr> <tr><td rowspan="3" style="vertical-align:middle;"> <p><span class="font3">惠州市德赛工业发展</span></p> <p><span class="font3">有限公司</span></p></td><td style="vertical-align:middle;"> <p><span class="font3">集中竞价交易</span></p></td><td style="vertical-align:middle;"> <p><span class="font2">2010 </span><span class="font3">年 </span><span class="font2">8 </span><span class="font3">月 </span><span class="font2">19 </span><span class="font3">日至</span></p> <p><span class="font2">2012</span><span class="font3">年</span><span class="font2">5</span><span class="font3">月</span><span class="font2">18</span><span class="font3">日</span></p></td><td style="vertical-align:middle;"> <p><span class="font2">191.56</span></p></td><td style="vertical-align:middle;"> <p><span class="font2">1.4%</span></p></td></tr> <tr><td style="vertical-align:bottom;"> <p><span class="font3">大宗交易</span></p></td><td> <p></p></td><td> <p></p></td><td> <p></p></td></tr> <tr><td style="vertical-align:bottom;"> <p><span class="font3">其它方式</span></p></td><td> <p></p></td><td> <p></p></td><td> <p></p></td></tr> </table>'
#     table = BeautifulSoup(t1, 'lxml')
#     trs = table.find_all('tr')
#     data = dc.table_processing(trs)
#     return


def html_to_test():
    """
        天池html转txt no table
    :return: 
    """
    import tianchi_html as th
    import re
    import codecs
    path = 'D:\\WorkSpace\Python\\to_github\\announcement_extract\\data\\0518_增减持\\no_table_html\\'
    filename = None
    outpath = './data/0518_txt/增减持/'
    path = './data/temp/'
    filename = '31395.html'
    outpath = './data/temp/'
    file_info = th.get_path_args()
    html_dict = th.read_html2(filepath=path, filename=filename)
    total = 0
    for index in html_dict:
        # 去掉表格tag
        h = html_dict[index]
        for i in h.find_all('table'):
            i.decompose()
        content = th.get_content(h)
        content = [re.sub(' +', '', i) for i in content]
        content = th.content_format(content)
        content = [i['content'] for i in content]
        with codecs.open(outpath+index.replace('.html', '.txt'), 'w', 'utf-8') as f:
            print('--- writing {0}'.format(index.replace('.html', '.txt')))
            f.writelines('\n'.join(content))
            total += 1
            print('counts:'+str(total))


# def table_to_txt_test():
#     from fomat_conversion import demo_complete as dc
#     import codecs
#     path = './data/data_train_shifeng_html/增减持/html/'
#     filename = None
#     # filename = '18820899.html'
#     outpath = './data/data_train_shifeng_txt/增减持/'
#     # outpath = './data/temp/'
#     html_dict = dc.read_html2(filepath=path, filename=filename)
#     contents = {}
#     for n, index in enumerate(html_dict):
#         print('processing {0} -- total: {1} this: {2}'.format(index, len(html_dict), n))
#         tags_list=dc.html_to_tags_list(html=html_dict[index], _from='inner')
#         content = dc.get_content(tags_list)
#         contents[index] = content
#     # 写入txt
#     for index in contents:
#         # 有表格返回的是空值，跳过
#         if contents[index] == None:
#             continue
#         with codecs.open(outpath+index.replace('.html', '.txt'), 'w', 'utf-8') as f:
#             print('--- writing {0}'.format(index.replace('.html', '.txt')))
#             output = []
#             for i in contents[index]:
#                 output = output + dc.check_table_write(i)
#             f.write('\n'.join(output))


# 天池公告html转txt
def tianchi_html_to_text_no_table(drop_table=True):
    import tianchi_html as th
    import re
    path = './data/0605/增减持/html/'
    filename = None
    outpath = './data/0605_txt/增减持/'
    # path = './data/temp/'
    # filename = '31395.html'
    # outpath = './data/temp/'
    html_dict = th.read_html2(filepath=path, filename=filename)
    total = 0
    for index in html_dict:
        # 去掉表格tag
        h = html_dict[index]
        for i in h.find_all('table'):
            i.decompose()
        content = th.get_content(h)
        content = [re.sub(' +', '', i) for i in content]
        content = th.content_format(content)
        content = [i['content'] for i in content]
        with th.codecs.open(outpath+index.replace('.html', '.txt'), 'w', 'utf-8') as f:
            print('--- writing {0}'.format(index.replace('.html', '.txt')))
            f.write('\n'.join(content))
            total += 1
            print('counts:'+str(total))


# 天池公告html转txt
def tianchi_html_to_text_complete(drop_table=True):
    """
        天池公告HTML转换完整版
    :param drop_table: 
    :return: 
    """
    from fomat_conversion import tianchi_html_complete as th
    import codecs
    # path = '../data/0605/增减持/html/'
    # filename = None
    # outpath = '../data/0605_txt/增减持/'
    # path = '../data/0605/增减持/html/'
    # path = '../data/temp2/'
    # filename = '5885.html'
    # outpath = '../data/temp2/'

    # --- 本地外部数据 ---
    path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\参赛数据2\\round1_train_20180518\\增减持\\html\\'
    filename = '1823756.html'
    filename = None
    outpath = 'D:\\TianChi_competition\\公告信息抽取\\materials\\format_data\\zengjianchi_train\\'

    html_dict = th.read_html2(filepath=path, filename=filename)
    total = 0
    contents = {}
    for n, index in enumerate(html_dict):
        print('processing {0} -- total: {1} this: {2}'.format(index, len(html_dict), n))
        # 是否去掉表格tag
        h = html_dict[index]
        if drop_table:
            for i in h.find_all('table'):
                i.decompose()
        content = th.get_content(h)
        content, part_table, table_failed = th.content_format(content)
        contents[index] = content
    # 写入txt
    for index in contents:
        # 有表格返回的是空值，跳过
        if contents[index] == None:
            continue
        with codecs.open(outpath + index.replace('.html', '.txt'), 'w', 'utf-8') as f:
            print('--- writing {0}'.format(index.replace('.html', '.txt')))
            output = []
            for i in contents[index]:
                output = output + th.check_table_write(i)
            f.write('\n'.join(output))


if __name__ == '__main__':
    tianchi_html_to_text_complete(drop_table=True)
    # test_table()
    # html_to_test()
    # table_to_txt_test() # 批量转换含表格html  仕锋软件
    # tianchi_html_to_text_no_table()
