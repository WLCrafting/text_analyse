# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 11:25:28 2017

@author: gowit_000

Jieba word split and statistics analyse
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import codecs

def Combine_all():
    res = "";
    df_org = pd.read_csv('content.csv');
    li_org=df_org.values.tolist()
    for item in li_org:
        try:
            if float(item[0]) > 1300000000 and str(item[1]) != "":     
                res += str(item[1])
            with open("Output.txt", "a") as text_file:
                text_file.write("%s" % str(item[1]))    
        except:
            continue
    

df_org = pd.read_csv('content.csv', encoding = 'utf-8');

li_org = [];
li_compress = [];

sub1 = re.compile("\n")
subimg = re.compile("\"http://(.*)\"")

li_org=df_org.values.tolist()

for item in li_org:

    if (item[1] != ''):
        item[1] = str(item[1]).replace('，', '')
        item[1] = str(item[1]).replace(',', '')
    try:
        if float(item[0]) > 1300000000 and str(item[1]) != "":     
            li_compress.append([str(item[0]), str(item[1])])
    except:
        continue        

    
    
my_df = pd.DataFrame(li_compress)
my_df.to_csv('content_compress.csv', index=False, header=False, encoding='utf-8')    
    
Combine_all()