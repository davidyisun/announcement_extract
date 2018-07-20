
#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名:
Created on 2018--
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
from multiprocessing import Pool
import time
import random


def t(a):
    return a % 5


def t1(**kwargs):
    m = kwargs.get('headers')
    print(m)


if __name__ == '__main__':
    # p = Pool(4)
    # c = []
    # for i in range(50000):
    #     result = p.apply_async(t, args=(i,))
    #     print(result.get())
    # p.close()
    # p.join()
    # print(c)
    t1(header='yisun')