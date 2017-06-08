# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 13:22:19 2017

@author: gowit_000
text word frequenz post processing
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import seaborn as sns
def searchKey():
    return("交易");

res = [];
for day in range(17277, 17317):
        try:
            read_key = pd.read_csv('book_tfidf/'+str(day)+'.csv')
            li_key = read_key.values.tolist()
            for row in li_key:
                if (row[0] == searchKey()):
                    str_day = time.strftime('%m-%d', time.localtime(int(day) * 86400))
                    res.append([str_day, row[1]])
                    break
        except:
            pass
df = pd.DataFrame(res)
#sns.pointplot(x = 0, y = 1, data = df);
# df.to_csv('res_until_' + str(day) +'.csv', index=False, header=False, encoding='utf-8')  
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
df.plot(x = 0, y = 1, marker = '.', label = searchKey())
plt.xlabel("日期")
plt.ylabel("热度")
plt.show()