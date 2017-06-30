# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 11:25:28 2017

@author: gowit_000

Jieba word split and statistics analyse

Updated on Mon Jun 26 2017

word frequency comparison

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import jieba
import re
import math
import jieba.analyse

"""
change frequenz of picked words to improve accuracy
"""
def freq_chg() :
	dict_words = ['并网','潮汐能','充电桩','出清电量','储能','低碳','地热','电厂','电池','电动车','电动车电池','电动汽车','电改','电力负荷','电力改革','电力交易','电力金融衍生品','电力期货','电力市场','电力现货','电力销售','电力直接交易','电力中长期交易','电网','多能互补','分布式能源','风电','风光互补','风能','峰谷电价','负荷特性','光伏','合同电量','火电','家用电池','建筑节能','节能服务','可持续能源','可再生能源','垃圾焚烧','零碳','绿色电力','绿证','煤电','能效','能源','能源管理','能源互联网','能源结构','能源微网','配电','偏差考核','氢燃料','燃料','燃料电池','热电联产','售电','售电公示','售电公司','输配电','水电','太阳能','碳捕捉','碳交易','碳收集','替代能源','天然气','调频市场','微电网','系统调峰','新能源','新能源汽车','需求侧管理','蓄能','页岩气','用电量','智慧能源','北京','天津','河北','山西','内蒙古','辽宁','吉林','黑龙江','上海','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','广西','海南','重庆','四川','贵州','云南','西藏','陕西','甘肃','青海','宁夏','台湾','新疆','香港','澳门'];
	for word in dict_words:
	    jieba.suggest_freq(word, True)
	return     

def Compare_freq(file_name_1, file_name_2):
    df_f1 = pd.read_csv('book_tfidf/' + file_name_1 + '.csv')
    li_f1 = df_f1.values.tolist()
    df_f2 = pd.read_csv('book_tfidf/' + file_name_2 + '.csv')
    li_f2 = df_f2.values.tolist()
    res = []
    for i in range(0, len(li_f1)):
        word = li_f1[i][0]
        str_mark = ''
        for j in range(0, len(li_f2)):
            if word == li_f2[j][0]:
                if i - j > 0:
                    str_mark = '下降'
                if i - j == 0 :
                    str_mark = '不变'
                if i - j < 0 :
                    str_mark = '上升'
                print(word, str_mark, int(math.fabs(i - j)))            
                res.append([word, str_mark, int(math.fabs(i - j))]) 
                break
        if str_mark == '':
            print(word, '新上榜， 排名', int(math.fabs(i)))
            res.append([word, '上升', 100 - int(math.fabs(i))])        
    my_df = pd.DataFrame(res)
    my_df.to_csv('freq/word_ranking_' + file_name_1 + '_vs_' + file_name_2 +'.csv', index=False, header=True, encoding='gbk')        

def Analyze_freq():
    df_org = pd.read_csv('content_compress.csv');

    li_org = [];
    li_split = [];
    li_not_sort = [];
    li_sort = [];
    li_day = [];
    li_week = [];


    suburl = re.compile("\"http://(.+)\"") 
    sub1 = re.compile("nbsp")
    sub2 = re.compile("\d")


    li_org=df_org.values.tolist()

    for i in range(0, len(li_org)):
        day = int(li_org[i][0] / 86400);
        li_org[i][1] = re.sub(suburl, '', str(li_org[i][1]))
        li_org[i][1] = re.sub(sub1, '', li_org[i][1])
        li_org[i][1] = re.sub(sub2, '', li_org[i][1])
        new_row = [day, li_org[i][1]]
        li_not_sort.append(new_row)
        
    li_sort = sorted(li_not_sort, key = lambda x:x[0])

    # inital content for combine
    day_old = li_sort[0][0];
    week_old = li_sort[0][0];
    content_in_day = "" 
    content_in_week = ""
    content_in_all = ""
    # combine text of the same day
    for i in range(0, len(li_sort)):
        content_in_all += li_sort[i][1]
        if (int(week_old) + 7 > int(li_sort[i][0])):
            content_in_week += li_sort[i][1]
        else:
            li_week.append([week_old, content_in_week])
            print(week_old, content_in_week)
            content_in_day = ""
            week_old = li_sort[i][0]
            content_in_week += li_sort[i][1]

        if (day_old == li_sort[i][0]):
            content_in_day += li_sort[i][1]
        else:
            li_day.append([day_old, content_in_day])
            content_in_day = ""
            day_old = li_sort[i][0]
            content_in_day += li_sort[i][1]

               

    # tf-inf statistic
    freq_chg()
    li_freq = []

    jieba.analyse.set_stop_words("extra_dict/stop_words_non_power.txt")

    for i in range(0, len(li_day)):
        tags = jieba.analyse.extract_tags(li_day[i][1], topK = 100, withWeight = True)
        li_freq.append([li_day[i][0], tags])
        day_freq = pd.DataFrame(tags)     
        day_freq.to_csv('book_tfidf/'+str(li_day[i][0])+'.csv',mode='w',index=False,encoding='UTF-8')

    for i in range(0, len(li_week)):
        tags = jieba.analyse.extract_tags(li_week[i][1], topK = 100, withWeight = True)
        li_freq.append([li_week[i][0], tags])
        day_freq = pd.DataFrame(tags)     
        day_freq.to_csv('book_tfidf/week_' + str(li_week[i][0]) + '.csv',mode = 'w', index = False, encoding = 'UTF-8') 

    tags = jieba.analyse.extract_tags(content_in_all, topK = 100, withWeight = True)
    day_freq = pd.DataFrame(tags)     
    day_freq.to_csv('book_tfidf/all.csv',mode = 'w', index = False, encoding = 'gbk')       
    
#==============================================================================
# for i in range(len(li_freq) - 30, len(li_freq)):
#     for key in li_freq[i][1]:
#         if (key[0] == '售电'):
#             print(key[1])
#==============================================================================

def main():
    Analyze_freq()
    Compare_freq('week_17318', 'week_17304')

if __name__ == '__main__':
    main()
        

