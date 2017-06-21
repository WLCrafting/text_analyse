# -*- coding: utf-8 -*-
"""
Spyder Editor

As filter to fetch content from database
"""
import time
import datetime
import pymysql
import pandas as pd
import re
import env

class url_info(object):
    ### as transfer from source to target
    def __init__(self, md5, url, title, time, intro, source, txt):
        self.md5 = md5
        self.url = url
        self.title = title
        self.time = time
        self.intro = intro
        self.source = source
        self.txt = txt
    def print(self):
        print ('来源:' + self.source + "标题:" + self.title) 

class trade_corp_info(object):
    ### as transfer from source to target
    def __init__(self, ID, name, time, volume, preis):
        self.ID = ID
        self.name = name
        self.time = time
        self.volume = volume
        self.preis = preis
    def print(self):
        print ('公司:' + self.name + " 交易:" + self.preis + ' 量:' + self.volume) 

class trade_overall_info(object):
    ### as transfer from source to target
    def __init__(self, prov, name, time, volume, preis):
        self.prov = prov
        self.name = name
        self.time = time
        self.volume_deal = volume_deal
        self.preis_deal = preis_deal

    def print(self):
        print ('省份:' + self.prov + " 成交价:" + self.preis_deal + ' 量:' + self.volume_deal)                   
        
def get_db_table_source():
    return ('`content`') 

def get_db_table_trade_result_source():
    return ('`corptrade`')     

def get_timestamp(string_input):
    st = time.strptime(string_input, '%Y-%m-%d')
    return(int(time.mktime(st)))    

def text_set_sql_conditon(start = 0, end = 0, keys = [], group = 'full'):
    ###
    # @start: start time format %Y-%m-%d
    # @end: end time format %Y-%m-%d
    # @key: keyword specific for intro and title
    # @group : group range, default all sources, avaliable: 'main' or any single source,
    #     mutil source unacceptable
    ###
    # set time
    time_delay = (datetime.datetime.now() - datetime.timedelta(days = 7))
    t_start_default = int(time.mktime(time_delay.timetuple()))
    t_end_default = int(time.mktime(datetime.datetime.now().timetuple()))
    
    end = t_end_default if (end == 0) else get_timestamp(end)
    start = t_start_default if (start == 0) else get_timestamp(start)
    
    sql_query = " WHERE time > " + str(start) + " AND time < " + str(end)
    # set key for txt and title
    if keys != []:
        # fake query
        sql_query += " AND ( title != '' "
        for key in keys:
            sql_query += "AND title LIKE '%" + key + "%' "
        sql_query += " ) OR ( txt != ''"    
        for key in keys:
            sql_query += " AND txt LIKE '%" + key + "%' " 
        sql_query += ") "       
    # set source range    
    if group == 'full':
        return(sql_query)    
    if group == 'main':
        
        # false init. query
        sql_query += " AND (wechat_id = 'EnergyStudies'" 
        for medien_id in env.id_dict_medien:
                sql_query = sql_query +" or wechat_id = '" + medien_id + "'"                  
        sql_query += ')'
    else:
        sql_query += " AND wechat_id = " + group 
    print(sql_query)      
    return(sql_query) 


def trade_set_sql_conditon(start = 0, end = 0, province = ''):
    ###
    # @start: start time format %Y-%m-%d
    # @end: end time format %Y-%m-%d
    # @key: keyword specific for intro and title
    # @group : group range, default all sources, avaliable: 'main' or any single source,
    #     mutil source unacceptable
    ###
    # set time
    time_delay = (datetime.datetime.now() - datetime.timedelta(days = 7))
    t_start_default = int(time.mktime(time_delay.timetuple()))
    t_end_default = int(time.mktime(datetime.datetime.now().timetuple()))
    
    end = t_end_default if (end == 0) else get_timestamp(end)
    start = t_start_default if (start == 0) else get_timestamp(start)
    
    sql_query = " WHERE T > " + str(start / 86400) + " AND T < " + str(end / 86400)
    # set query province
    if province != '':
        sql_query += (" AND Prov LIKE '%" + province + "%' ")   
    else:
        print("Province not set!")
        return('null') 
    return(sql_query) 

def fetch_content(sql_condition):
    ###
    # @ sql_condition shall be set by text_set_sql_condition function
    ###
    res = []
    if sql_condition == '' :
        return('failed')

    connection_get = pymysql.connect(host = env.LOCAL_HOST,
                             port = env.LOCAL_PORT,
                             user = env.LOCAL_USER,
                             password = env.LOCAL_PW,
                             db = env.LOCAL_DB,
                             charset = 'utf8',
                             cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection_get.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM " + get_db_table_source() + sql_condition
            #print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                new_url_info = url_info(item['md5'],
                                        item['link'],
                                        item['title'], 
                                        item['time'], 
                                        item['intro'],
                                        item['wechat_id'],
                                        purify(item['txt']))
                print(new_url_info.title)
                # prevent input error
                if float(new_url_info.time) > 1300000000 and str(new_url_info.txt) != "": 
                    res.append([new_url_info.time, new_url_info.txt])

    finally:
        connection_get.close()
    #print(res)    
    return res 

def fetch_trade_company(sql_condition):
    ###
    # @ sql_condition shall be set by text_set_sql_condition function
    ###
    res = []
    if sql_condition == '' :
        return('failed')

    connection_get = pymysql.connect(host = env.REMOTE_HOST,
                             port = env.REMOTE_PORT,
                             user = env.REMOTE_USER,
                             password = env.REMOTE_PW,
                             db = env.REMOTE_DB,
                             charset = 'utf8',
                             cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection_get.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM " + get_db_table_trade_result_source() + sql_condition
            #print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                new_trade_corp_info = trade_corp_info(item['ID'],
                    item['N'],
                    item['T'], 
                    item['V'], 
                    item['P']
                )
                # prevent input error
                if float(new_trade_corp_info.time) > 10000 and str(new_trade_corp_info.volume) != "": 
                    res.append([
                        new_trade_corp_info.ID,
                        new_trade_corp_info.name,
                        datetime.datetime.fromtimestamp(
                            int(new_trade_corp_info.time) * 86400
                        ).strftime('%Y-%m'),
                        new_trade_corp_info.volume,
                        new_trade_corp_info.preis
                    ])

    finally:
        connection_get.close()
    #print(res)    
    return res 

def purify(str_input):
    ###
    # @str_input to exclude unneccessary words from original texts.
    ###
    sub1 = re.compile("\n")
    subimg = re.compile("\"http://(.*)\"")
    str_input = re.sub(subimg, "", str(str_input))
    str_input = re.sub(sub1, "", str(str_input))
    str_input = str_input.replace('，', '')
    str_input = str_input.replace(',', '')
    #去除连续的换行符  
    r = re.compile("\\s{2,}")  
    str_input = re.sub(r, "", str_input)
    return(str_input)                               
    
def main():
    ###
    # @start: start time format %Y-%m-%d
    # @end: end time format %Y-%m-%d
    # @key: keyword specific for intro and title
    # @group : group range, default all sources, avaliable: 'main' or any single source,
    #     mutil source unacceptable
    ###
    ###
    # 以下生成全文表格
    text_sql_condition = text_set_sql_conditon(start = '2017-05-01', group = 'main', keys = ['山西', '售电'])
    fulltxt = fetch_content(text_sql_condition)
    pd.DataFrame(fulltxt).to_csv('content.csv', mode = 'w', header = False, index = False, encoding = 'utf-8')
    # 以上生成全文表格 用#开关
    # 以下生成历史交易数据
    trade_sql_condition = trade_set_sql_conditon(start = '2017-5-10', province = '广东')
    res = fetch_trade_company(trade_sql_condition)
    pd.DataFrame(res).to_csv('trade_result_company.csv', mode = 'w', header = False, index = True, encoding = 'gbk')
    # 以上生成历史交易 用#开关


if __name__ == "__main__":
    main()
     
