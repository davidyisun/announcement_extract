#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 文本拆分
    将文本拆分成 【释义】、【重大提示】、【正文】
Created on 2018-07-24
@author:David Yisun
@group:data
"""
import sys
sys.path.append('../')
import os
import math
from utils import tian_chi
from extract import chongzu
import codecs
import json


def save_data(content_object_dict, outpath):
    """
        储存分割的文件
    :param content_object_dict:
    :param outpath:
    :return:
    """
    for index in content_object_dict:
        data = content_object_dict[index]
        # 储存释义
        try:
            with codecs.open(outpath+'{0}/{1}.txt'.format('shiyi', index.replace('.html', '')), 'a', 'utf8') as f:
                shiyi = json.dumps({'shiyi': data.shiyi})
                f.write(shiyi)
        except FileNotFoundError:
            with codecs.open(outpath+'{0}/{1}.txt'.format('shiyi', index.replace('.html', '')), 'r', 'utf8') as f:
                shiyi = json.dumps({'shiyi': data.shiyi})
                f.write(shiyi)
        # 储存重大事项提示
        try:
            with codecs.open(outpath+'{0}/{1}.txt'.format('zhongdashixiangtishi', index.replace('.html', '')), 'a', 'utf8') as f:
                zhongdashixiangtishi = json.dumps({'zhongdashixiangtishi': data.zhongdashixiangtishi})
                f.write(zhongdashixiangtishi)
        except FileNotFoundError:
            with codecs.open(outpath+'{0}/{1}.txt'.format('zhongdashixiangtishi', index.replace('.html', '')), 'r', 'utf8') as f:
                zhongdashixiangtishi = json.dumps({'zhongdashixiangtishi': data.zhongdashixiangtishi})
                f.write(zhongdashixiangtishi)
        # 储存内容
        try:
            with codecs.open(outpath+'{0}/{1}.txt'.format('content', index.replace('.html', '')), 'a', 'utf8') as f:
                content = json.dumps({'content': data.contents})
                f.write(content)
        # except:
        except FileNotFoundError:
            with codecs.open(outpath + '{0}/{1}.txt'.format('content', index.replace('.html', '')), 'r', 'utf8') as f:
                content = json.dumps({'content': data.contents})
                f.write(content)
        # 储存内容 file_tree
        try:
            with codecs.open(outpath+'{0}/{1}.txt'.format('content_tree', index.replace('.html', '')), 'a', 'utf8') as f:
                content_tree = json.dumps({'content': data.file_tree})
                f.write(content_tree)
        except FileNotFoundError:
            with codecs.open(outpath+'{0}/{1}.txt'.format('content_tree', index.replace('.html', '')), 'r', 'utf8') as f:
                content_tree = json.dumps({'content': data.file_tree})
                f.write(content_tree)
        # 储存内容 tree_list
        try:
            with codecs.open(outpath+'{0}/{1}.txt'.format('content_tree_list', index.replace('.html', '')), 'a', 'utf8') as f:
                content_tree_list = json.dumps({'content': data.file_tree})
                f.write(content_tree_list)
        except FileNotFoundError:
            with codecs.open(outpath + '{0}/{1}.txt'.format('content_tree_list', index.replace('.html', '')), 'r','utf8') as f:
                content_tree_list = json.dumps({'content': data.file_tree})
                f.write(content_tree_list)
        # 存储title结构
        try:
            with codecs.open(outpath+'{0}/{1}.txt'.format('titles_list', index.replace('.html', '')), 'a', 'utf8') as f:
                content_tree_list = json.dumps({'content': data.file_tree})
                f.write(content_tree_list)
        except FileNotFoundError:
            with codecs.open(outpath + '{0}/{1}.txt'.format('titles_list', index.replace('.html', '')), 'r','utf8') as f:
                content_tree_list = json.dumps({'content': data.file_tree})
                f.write(content_tree_list)
    return


def content_segment(path, filename, outpath, postfix='.html', batches=20):

    if filename == None:
        files_name = os.listdir(path)
    else:
        files_name = filename
    file_list = [i for i in files_name if i.endswith(postfix)]
    n_files = len(file_list)  # 总文件数
    n_batch = math.ceil(n_files / batches)
    batch_head = 0
    file_list.reverse()

    # 批处理
    for batch in range(n_batch):
        _file_list = file_list[batch_head:batch_head+batches]
        if len(_file_list) == 0:
            break
        contents = chongzu.get_file_tree(path=path, filename=_file_list, method='both', df_json=True)
        # 分割数据存储
        save_data(contents, outpath=outpath)
        batch_head = batch_head + batches
        print('total: {0} --- has been processed: {1}'.format(len(file_list), batch_head))
    return


if __name__ == '__main__':
    pass

