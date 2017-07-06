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
    def __init__(self, prov, trade_type, time, volume, preis):
        self.prov = prov
        self.type = trade_type
        self.time = time
        self.volume_deal = volume_deal
        self.preis_deal = preis_deal

    def print(self):
        print ('省份:' + self.prov + " 成交价:" + self.preis_deal + ' 量:' + self.volume_deal)                   
        
def get_db_table_source():
    return ('`content`') 

def get_db_table_trade_result_source():
    return ('`corptrade`') 

def get_db_table_trade_overall_source():
    return ('`trade_Overall`')     

def get_db_table_policy_source():
    return ('`Timeline2`') 

def get_db_company_source():
    return ('`corp`')            

def get_timestamp(string_input):
    st = time.strptime(string_input, '%Y-%m-%d')
    return(int(time.mktime(st)))    

def text_set_sql_conditon(start = 0, end = 0, keys = [], group = 'full', include_text = False):
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
    
    sql_query = " WHERE `time` > " + str(start) + " AND `time` < " + str(end)
    # set key for txt and title
    if keys != []:
        # fake query
        sql_query += " AND (( `title` != '' "
        for key in keys:
            sql_query += "AND `title` LIKE '%" + key + "%' "
        if include_text == True:    
            sql_query += " ) OR ( `txt` != ''"    
            for key in keys:
                sql_query += " AND `txt` LIKE '%" + key + "%' " 
        sql_query += ")) "       
    # set source range    
    if group == 'full':
        return(sql_query)    
    if group == 'main':
        
        # false init. query
        sql_query += " AND (`wechat_id` = 'EnergyStudies'" 
        for medien_id in env.id_dict_medien:
                sql_query = sql_query +" or `wechat_id` = '" + medien_id + "'"                  
        sql_query += ')'
    else:
        sql_query += " AND `wechat_id` = " + group 
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
    
    sql_query = " WHERE `T` > " + str(start / 86400) + " AND `T` < " + str(end / 86400)
    # set query province
    if province != '':
        sql_query += (" AND `Prov` LIKE '%" + province + "%' ")   
    else:
        print("Province not set!")
        #return('null') 
    return(sql_query) 

def policy_set_sql_conditon(start = 0, end = 0, province = '', key = ''):
    ###
    # @start: start time format %Y-%m-%d
    # @end: end time format %Y-%m-%d
    # @key: keyword specific for intro and title
    # @province : specific for province
    ###
    # set time
    time_delay = (datetime.datetime.now() - datetime.timedelta(days = 7))
    t_start_default = time.strftime('%Y-%m-%d', time_delay.timetuple())
    t_end_default = time.strftime('%Y-%m-%d', datetime.datetime.now().timetuple())
    
    end = t_end_default if (end == 0) else end
    start = t_start_default if (start == 0) else start
    
    sql_query = " WHERE Date > '" + start + "' AND Date < '" + end + "' "
    # set query province
    if province != '':
        sql_query += (" AND Prov LIKE '%" + province + "%' ")   
    if key != '':
        sql_query += (" AND Name LIKE '%" + key + "%' ")
    print(sql_query)    
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
                    res.append([new_url_info.time, 
                        new_url_info.txt, 
                        new_url_info.title, 
                        new_url_info.source,
                        datetime.datetime.fromtimestamp(
                            int(new_url_info.time)
                            ).strftime('%Y-%m-%d %H') + '时' 
                        ])

    finally:
        connection_get.close()
    #print(res)    
    return res 

def fetch_trade_company(sql_condition = '', company_id = 0):
    ###
    # @ sql_condition shall be set by text_set_sql_condition function
    ###
    res = []
    if sql_condition == '' and company_id == 0:
        return('failed')
    if company_id != 0:
        sql_condition = "WHERE ID = " + str(company_id) + "  ORDER BY T DESC"    
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
                        new_trade_corp_info.preis,
                        item['Prov']
                    ])

                     
    finally:
        connection_get.close()
    #print(res)    
    return res 

def fetch_policy(sql_condition):
    ###
    # @ sql_condition shall be set by policy_set_sql_condition function
    ###
    res = []
    if sql_condition == '' :
        return('failed')

    connection_get = pymysql.connect(host = env.REMOTE_HOST,
                             port = env.REMOTE_PORT,
                             user = env.REMOTE_USER,
                             password = env.REMOTE_PW,
                             db = env.REMOTE_DB,
                             charset = 'gbk',
                             cursorclass = pymysql.cursors.DictCursor)
    try:
        with connection_get.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM " + get_db_table_policy_source() + sql_condition
            #print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                res.append([
                    item['Name'],
                    item['Date'],
                    item['Link'],
                    item['Prov']
                ])

    finally:
        connection_get.close()
    #print(res)    
    return res 

def fetch_company(company_name = '', company_id = 0):
    res_info = [];
    res = [];
    if company_id == 0 and company_name == '':
        return('Error. No info about the company is given')

    connection_get = pymysql.connect(host = env.REMOTE_HOST,
                             port = env.REMOTE_PORT,
                             user = env.REMOTE_USER,
                             password = env.REMOTE_PW,
                             db = env.REMOTE_DB,
                             charset = 'utf8',
                             cursorclass = pymysql.cursors.DictCursor)

    if company_id != 0:
        sql = "SELECT * from " + get_db_company_source() + "WHERE ID=" + str(company_id)
        try:
            with connection_get.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                res_info.append(str(
                    " ID: " + str(result['ID']) + '\n' +
                    "名称:" + result['N'] +
                    "省：" + result['P'] +
                    "市：" + result['City'] + '\n'
                ))
                res_info.append(str(
                    "最高售电额：" + result['V_Y'] +
                    "法人：" + result['Pres'] + '\n'
                ))
                res_info.append(str(
                    "电话：" + result['Tel'] +
                    "网站：" + result['Web'] +
                    "邮箱：" + result['Email'] +
                    "手机：" + result['Phone'] +
                    "地址：" + result['Add'] + '\n'
                ))
                res_info.append(str("股东：" + result['Init'] +
                    "经营范围：" + result['Addinfo']
                ))
                print(res_info)
                res.append(res_info)    
                trade_res = fetch_trade_company(company_id = company_id)    
                if len(trade_res) > 0:
                    res.append(["以上是公司基本信息\n"])
                    res.append(["*********************************************\n"])
                    res.append(["以下是公司交易信息\n"])
                    for item in trade_res:    
                        res.append(item)
                trade_res = fetch_trade_overall(" WHERE Prov LIKE '%" + result['P'] + "%'")
                if len(trade_res) > 0:
                    res.append(["以上是公司交易信息\n"])
                    res.append(["*********************************************\n"])
                    res.append(["以下是公司所在省大盘信息\n"])
                    for item in trade_res:    
                        res.append(item)        
        finally:
            connection_get.close()
    else: 
        sql = "SELECT * from " + get_db_company_source() + "WHERE N LIKE '%" + str(company_name) + "%'"                                                
        try:
            with connection_get.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                print("总共有" + str(len(result)) + "个名字类似公司")
                for item in result:
                    print( "ID: " + str(item['ID']) + ":   " + item['N'])
                print("之后设定 company_id 再搜索")    
        finally:
            connection_get.close()
    return(res)

def fetch_trade_overall(sql_condition):
    ###
    # @ sql_condition shall be set by policy_set_sql_condition function
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
            sql = "SELECT * FROM " + get_db_table_trade_overall_source() + sql_condition
            #print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                res.append([
                    item['Prov'],
                    item['Trade_type'],
                    time.strftime("%Y %m", time.localtime(int(item['Time']))),
                    item['P_deal'],
                    item['V_deal'],
                    item['V_deal_com']
                ])
    finally:
        cnnection_get.close()
    #print(res)    
    return res     

def trade_history(start = 0, end = 0, province = ''):
    trade_sql_condition = trade_set_sql_conditon(start = start, province = province)
    res = fetch_trade_company(trade_sql_condition)
    trade_res = fetch_trade_overall(" WHERE Prov LIKE '%" + province + "%'")
    if len(trade_res) > 0:
        res.append(["以上是各公司历史交易数据\n"])
        res.append(["*********************************************\n"])
        res.append(["以下是该省大盘数据\n"])
        for item in trade_res:    
            res.append(item)
    pd.DataFrame(res).to_csv('trade_result_company.csv', mode = 'w', header = False, index = False, encoding = 'gbk')

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