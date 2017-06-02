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
def searchKey():
    return("售电");

res = [];
for day in range(17277, 17307):
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
df.to_csv('res_until_' + str(day) +'.csv', index=False, header=False, encoding='utf-8')  
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
df.plot(x=0, y=1, label=searchKey())
plt.xlabel("日期")
plt.show(df.plot)