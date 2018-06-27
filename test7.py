# 统计连续整行
def stat_continous_rows(tables):
    data_list = []
    for i, t in enumerate(tables):
        text = t[0]
        print('{0}:{1}'.format(i, text))
        tbody = t[1]
        # --- 表属性定义 ---
        trs = tbody.find_all('tr', recursive=False)
        n_row = len(trs)  # 表行数
        title = None  # 表名
        headers_type = '' # 表头类型
        headers = []  # 表头
        headers_array = np.array([None]) # 表头矩阵
        fields_type = []  # 表字段类型
        content = None
        satisfied = False
        for j, tr in enumerate(trs):
            # --- check title ---
            if title == None:
                title = find_title(tr)
                if title != -1:  # 表格内部含title 迭代下一个tr
                    continue
            # --- check headers ---
            data = tr_processing(tr)
            type = ''
            if data['n_tds'] == 1:
                satisfied = True
                continue
            else:
                break
        if satisfied:
            data_list.append(list(t)+[j, len(trs), title])
        res = {'name': t[0],
               'title': title,
               'headers': headers}
    return data_list
d = stat_continous_rows(tables)




def parse_html(tag):
    print(tag.prettify())
    return

import pandas as pd
d1 = [[i[0], i[2], i[3]] for i in d]
d2 = pd.DataFrame(d1)
for j, i in enumerate(d):
    print('-'*20)
    print('****** {0} **** {1}'.format(i[0], j))
    parse_html(i[1])

d[11]
