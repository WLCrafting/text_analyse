# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 11:25:28 2017

@author: gowit_000

Jieba word split and statistics analyse
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import jieba
import re
import jieba.analyse

df_org = pd.read_csv('content_compress.csv');

li_org = [];
li_split = [];
li_not_sort = [];
li_sort = [];
li_day = [];

suburl = re.compile("\"http://(.+)\"") 
sub1 = re.compile("nbsp")
sub2 = re.compile("2017")

li_org=df_org.values.tolist()

for i in range(0, len(li_org)):
    day = int(li_org[i][0] / 86400);
    li_org[i][1] = re.sub(suburl, '', li_org[i][1])
    li_org[i][1] = re.sub(sub1, '', li_org[i][1])
    li_org[i][1] = re.sub(sub2, '', li_org[i][1])
    new_row = [day, li_org[i][1]]
    li_not_sort.append(new_row)
    
li_sort = sorted(li_not_sort, key = lambda x:x[0])

# inital content for combine
day_old = li_sort[0][0];
content_in_day = "" 
# combine text of the same day
for i in range(0, len(li_sort)):
    if (day_old == li_sort[i][0]):
        content_in_day += li_sort[i][1]
    else:
        li_day.append([day_old, content_in_day])
        content_in_day = ""
        day_old = li_sort[i][0]
        content_in_day += li_sort[i][1]

# tf-inf statistic
li_freq = []
for i in range(0, len(li_day)):
    tags = jieba.analyse.extract_tags(li_day[i][1], topK = 50, withWeight = True)
    li_freq.append([li_day[i][0], tags])
    day_freq = pd.DataFrame(tags)     
    day_freq.to_csv('book_tfidf/'+str(li_day[i][0])+'.csv',mode='w',index=False,encoding='UTF-8')
    
#==============================================================================
# for i in range(len(li_freq) - 30, len(li_freq)):
#     for key in li_freq[i][1]:
#         if (key[0] == '售电'):
#             print(key[1])
#==============================================================================
        

