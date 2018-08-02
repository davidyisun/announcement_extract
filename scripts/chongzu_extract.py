#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 资产重组 信息抽取脚本
Created on 2018-07-20
@author:David Yisun
@group:data
"""
import sys
sys.path.append('../')
from extract import chongzu
from utils import result_compare, tian_chi
import itertools
import pandas as pd
import os
import math
import codecs
import json
import copy


def from_shiyi(path, filename, outpath, result_append=True):
    data = chongzu.get_pre_content(path=path, filename=filename, keys=['shiyi'])
    result_mark = []
    result_mark_com = []
    result_jiaoyiduifang = []
    for i, index in enumerate(data):
        print('extracting from shiyi --- total: {0} --- this: {1} --- file: {2}'.format(len(data), i, index))
        file = data[index]
        ExtractDevice = chongzu.ExtractDevice(shiyi=file['shiyi'])
        ExtractDevice.extract_from_shiyi()
        # 以下为特殊处理
        if ExtractDevice.mark != []:
            _mark = [i[1] for i in ExtractDevice.mark]
            _result = list(itertools.zip_longest([index.replace('.html', '')], _mark, fillvalue=index.replace('.html', '')))
            result_mark = result_mark + _result
        if ExtractDevice.mark_com != []:
            _mark_com = [i[1] for i in ExtractDevice.mark_com]
            _result = list(itertools.zip_longest([index.replace('.html', '')], _mark_com, fillvalue=index.replace('.html', '')))
            result_mark_com = result_mark_com + _result
        if ExtractDevice.jiaoyiduifang != []:
            _jiaoyiduifang = [i[1] for i in ExtractDevice.jiaoyiduifang]
            _result = list(itertools.zip_longest([index.replace('.html', '')], _jiaoyiduifang, fillvalue=index.replace('.html', '')))
            result_jiaoyiduifang = result_jiaoyiduifang + _result
    # 去重赋值
    result_mark = list(set(result_mark))
    result_mark_com = list(set(result_mark_com))
    result_jiaoyiduifang = list(set(result_jiaoyiduifang))
    # to dataframe
    df_mark = pd.DataFrame(result_mark, columns=['id', 'mark'])
    df_mark_com = pd.DataFrame(result_mark_com, columns=['id', 'mark_com'])
    df_jiaoyiduifang = pd.DataFrame(result_jiaoyiduifang, columns=['id', 'jiaoyiduifang'])

    result = {'mark': df_mark,
              'mark_com': df_mark_com,
              'jiaoyiduifang': df_jiaoyiduifang}
    out_names = ['mark', 'mark_com', 'jiaoyiduifang']
    for i in out_names:
        out_name = outpath+i+'.csv'
        if result_append:
            with codecs.open(out_name, 'a', 'utf8') as f:
                result[i].to_csv(f, index=False, header=False)
        else:
            result[i].to_csv(out_name, index=False)
    return result


def from_content(path, filename, outpath, result_append=True, title_depth=0):
    data = chongzu.get_pre_content(path=path, filename=filename, keys=['content'], text_trans=True, df_json=True)
    result = {}
    reg = '交易标的 *$|标的资产 *$|标的股权 *$'
    for i, index in enumerate(data):
        print('extracting from content --- total: {0} --- this: {1} --- file: {2}'.format(len(data), i, index))
        content = data[index]['content']
        ExtractDevice = chongzu.ExtractDevice(content_list=content)
        _res = ExtractDevice.extract_from_content_on_title(reg_object=reg, title_depth=title_depth)
        result[index.replace('.html', '')] = _res
    out = json.dumps(result)
    with codecs.open(outpath+'mark_in_content.csv', 'a', 'utf8') as f:
        f.write('\n')
        f.write(out)
    return result


def extract_method_from_content(path, filename, outpath):
    data = chongzu.get_pre_content(path=path, filename=filename, keys=['content'], text_trans=True, df_json=True)
    result = {}
    # reg = '收益法|资产基础法|成本分析法|市场比较法|市场法|收益法|'
    reg = '收益法|资产基础法|市场法|市场比较法|估值法|成本法|现金流折现法|内含价值调整法|' \
          '可比公司市净率法|重置成本法|收益现值法|基础资产法|假设清偿法|成本逼近法|单项资产加和法|' \
          '成本加和法|基准地价修正法|收益还原法|现金流量法|成本发|单项资产加总法|折现现金流量法'
    for i, index in enumerate(data):
        print('extracting method from content --- total: {0} --- this: {1} --- file: {2}'.format(len(data), i, index))
        content = data[index]['content']
        ExtractDevice = chongzu.ExtractDevice(content_list=content)
        _res = ExtractDevice.get_tree_content_on_text(reg_object=reg)
        if _res == []:
            continue
        result[index.replace('.html', '')] = _res
    out = json.dumps(result)
    with codecs.open(outpath+'method_text.csv', 'a', 'utf8') as f:
        f.write('\n')
        f.write(out)
    return result


def main(postfix='.html', batches=20):
    """
        信息抽取抽取主程序
    :return:
    """
    # --- 服务器数据 220 ---
    path = '/data/hadoop/yisun/data/tianchi2/train/chongzu/html/'
    filename = None
    # filename = ['20546245.html']
    label_file = '/data/hadoop/yisun/data/tianchi2/train_label/chongzu.train'
    outpath = '../data/extract_result/train_chongzu/'

    # --- 天池服务器
    path = '/home/118_16/data/chongzu_train_html/'
    filename = None
    # filename = ['20546245.html']
    label_file = '../data/train_data/train_labels/chongzu.train'
    outpath = '../data/extract_result/train_chongzu/'

    # # --- 本地外部数据 thinkpad ---
    # path = 'E:\\天池大赛\\公告数据\\天池大赛\\announcement_extract\\复赛数据\\复赛新增类型训练数据-20180712\\资产重组\\html\\'
    # filename = ['9898901.html']
    # label_file = '../data/train_data/train_labels/chongzu.train'
    # outpath = '../data/extract_result/train_chongzu/'
    #
    # --- 本地外部数据 ---
    path = 'D:\\TianChi_competition\\公告信息抽取\\materials\\复赛\\复赛新增类型训练数据-20180712\\资产重组\\html\\'
    filename = ['1871176.html', '1074177.html', '282992.html', '1503346.html', '6122878.html']
    label_file = '../data/train_data/train_labels/chongzu.train'
    outpath = '../data/extract_result/train_chongzu/'

    # --- 本地数据 ---
    # path = '../data/temp2/samples/'
    # filename = None
    # # filename = ['8515.html']
    # outpath = '../data/extract_result/train_chongzu/'
    # label_file = '../data/train_data/train_labels/chongzu.train'

    # --- label 字段 ---
    headers = ['id', 'mark', 'mark_com', 'jiaoyiduifang', 'price', 'method']
    df_label = result_compare.get_labels(file=label_file+'', headers=headers)

    if filename == None:
        files_name = os.listdir(path)
    else:
        files_name = filename
    file_list = [i for i in files_name if i.endswith(postfix)]
    n_files = len(file_list)  # 总文件数
    n_batch = math.ceil(n_files/batches)
    batch_head = 0
    # 清除已有result文件
    f = [outpath+i for i in os.listdir(outpath)]
    for i in f:
        os.remove(i)
    # 批量读取写入
    for batch in range(n_batch):
        _file_list = file_list[batch_head:batch_head+batches]
        if len(_file_list) == 0:
            break
        # --- 从【释义】抽取 ---
        # from_shiyi(path=path, outpath=outpath, filename=_file_list)

        # --- 从【正文】抽取 ---
        # r1 = from_content(path=path, outpath=outpath, filename=_file_list, title_depth=0)

        # --- 从【正文】中定位【评估方法】 ---
        res = extract_method_from_content(path=path, outpath=outpath, filename=_file_list)
        extract_id = res.keys()
        df = df_label.dropna(subset=['method']).reset_index(drop=True).copy()

        # --- 基本评测 ---
        label_id = [str(i) for i in df['id'].unique().tolist()]
        not_in_id = copy.deepcopy(label_id)  # 缺失
        in_id = []
        out_of_id = []  # 多余

        in_id = in_id+list(set(label_id).intersection(set(extract_id)))
        not_in_id = list(set(not_in_id).difference(set(extract_id)))
        out_of_id = out_of_id+list(set(extract_id).difference(set(label_id)))
        batch_head = batch_head+batches
        print('total: {0} --- has been processed: {1}'.format(len(file_list), min(len(file_list), batch_head)))
        print('in id :{0}'.format(len(in_id)))
    with codecs.open(outpath+'stat_result.txt', 'w', 'utf8') as f:
        f.write('------------------------\n')
        f.write('in_id: {0}'.format(len(in_id)))
        f.write('------------------------\n')
        f.write('not_in_id: {0}'.format(len(not_in_id))+'\n')
        f.write(' '.join(not_in_id))
        f.write('\n------------------------\n')
        f.write('out_of_id: {0}'.format(len(out_of_id))+'\n')
        f.write(' '.join(out_of_id))
    return


def delete_ouput():
    pass


if __name__ == '__main__':
    main(batches=20)
    pass