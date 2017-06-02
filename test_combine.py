# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 11:25:28 2017

@author: gowit_000

Jieba word split and statistics analyse
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df_org = pd.read_csv('content.csv');

li_org = [];
li_compress = [];

li_org=df_org.values.tolist()

for i in range (0, len(li_org)):
    row_compress = [];
    row_compress.append(li_org[i][1])
    row_compress.append(li_org[i][7])
    li_compress.append(row_compress)
    
    
my_df = pd.DataFrame(li_compress)
my_df.to_csv('content_compress.csv', index=False, header=False, encoding='utf-8')    
    