#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    脚本名: 数据格式规整
Created on 2018-07-10
@author:David Yisun
@group:data
@contact:davidhu@wezhuiyi.com
"""
import re
def unit_recognize(text):
    """
        单位识别
    :param text:
    :return:
    """
    res = re.findall(r'[十亿万千仟百佰%]', text)
    res = ''.join(res)
    return res


def float_normalize(text, type, dim=2, unit=''):
    """
        数值型数据转换
    :param text: str 需提取数值的文段
    :param type: str 转换类型 int or float
    :param unit: str 数值单位 一般由外部给出 如表头（万/股）
    :param dim: int 小数点保留位数
    :return:
    """
    coeff = 1.0
    # 转换
    if '十' in text:
        coeff *= 10
    if '亿' in text:
        coeff *= 100000000
    if '万' in text:
        coeff *= 10000
    if '千' in text or '仟' in text:
        coeff *= 1000
    if '百' in text or '佰' in text:
        coeff *= 100
    if '%' in text:
        coeff *= 0.01
    # 转换2
    if '十' in text:
        coeff *= 10
    if '亿' in unit:
        coeff *= 100000000
    if '万' in unit:
        coeff *= 10000
    if '千' in unit or '仟' in unit:
        coeff *= 1000
    if '百' in unit or '佰' in unit:
        coeff *= 100
    if '%' in unit:
        coeff *= 0.01
    d = re.split(re.compile('[-－~至]'), text)[-1]
    d1 = re.findall(re.compile('[\.|\d]'), d)
    d2 = ''.join(d1)
    if d2 == '':
        return d2
    try:
        res = round(float(d2) * coeff, dim)
    except:
        pass
    if type == 'float' and str(res).endswith('.0'):
        res = int(res)
    if type == 'int':
        res = int(res)
    return str(res)


if __name__ == '__main__':
    test = '12%'
    print(float_normalize(test, 'float', dim=4))

