# -*- coding: utf-8 -*-
"""
As filter to fetch content from database
"""
import time
import datetime
import pymysql
import pandas as pd
import re
import env
import JN_connect

def main():
    ###
    # @start: start time format %Y-%m-%d
    # @end: end time format %Y-%m-%d
    # @key: keyword specific for intro and title
    # @group: 售电相关 'main', 全部 'full'
    # @include_text False 只搜索标题， True 搜索全文
    ###

    ###
    # 以下生成全文表格
    # content.csv 如果要读取，请先用记事本打开，另存为选择编码 Unicode，之后excel才能读取正确编码
    text_sql_condition = JN_connect.text_set_sql_conditon(start = '2017-05-21',
        end = '2017-05-31',
        group = 'full',
        keys = ['通知'],
        include_text = False)
    print(text_sql_condition)
    fulltxt = JN_connect.fetch_content(text_sql_condition)
    pd.DataFrame(fulltxt).to_csv('content.csv', mode = 'w', header = False, index = False, encoding = 'utf8')
    # content.csv 如果要读取，请先用记事本打开，另存为选择编码 Unicode，之后excel才能读取正确编码
    # 以上生成全文表格 用#开关

    #以下生成历史交易数据
    #JN_connect.trade_history(start = '2017-5-20')
    #以上生成历史交易 用#开关, 

    # 以下生成历史政策数据
    # policy_sql_condition = JN_connect.policy_set_sql_conditon(start = '2016-5-10', province = '江西')
    # res = JN_connect.fetch_policy(policy_sql_condition)
    # pd.DataFrame(res).to_csv('policy_result.csv', mode = 'w', header = False, index = True, encoding = 'gbk')
    # 以上生成历史政策数据

    # 以下生成公司有关数据
    # 可以用名字模糊查询出ID
    #res = JN_connect.fetch_company(company_name = '新奥')
    # 利用ID查询结果
    #res = JN_connect.fetch_company(company_id = 595)
    #pd.DataFrame(res).to_csv('company_result.csv', mode = 'w', header = False, index = False, encoding = 'gbk')
    # 以上生成公司有关数据
    pass

if __name__ == "__main__":
    main()
     
