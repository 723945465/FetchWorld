# -*- coding = utf-8 -*-
# @Time: 2024/4/8 22:28
# @Author: Chris
# @File: DevTest4.py
# @Software: PyCharm

import re
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error

db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'
charset='utf8mb4'


def is_within_N_days(datetime_str, DaysNum):
    # 定义日期时间格式
    datetime_format = '%Y-%m-%d %H:%M'

    # 将输入的日期字符串转换为datetime对象
    try:
        date_obj = datetime.strptime(datetime_str, datetime_format)
    except ValueError:
        # 如果输入的日期格式不正确，返回False
        return False

    # 获取当前时间
    current_time = datetime.now()
    # 计算给定日期与当前时间的差值
    time_difference = current_time - date_obj
    # 如果差值的天数小于或等于3天，则返回True，否则返回False
    return abs(time_difference.days) < DaysNum

def parseDataTimeFromToutiaoContent(raw_time_string):
    # 定义正则表达式模式，匹配日期和时间的格式
    date_time_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}'
    match = re.search(date_time_pattern, raw_time_string)
    if match:
        date_time = match.group(0)
        return date_time
    else:
        print("在字符串中未找到日期时间信息")
        return ""

def JudgeIsNew_Today(raw_time_string):
    datetime_str = parseDataTimeFromToutiaoContent(raw_time_string)
    if len(datetime_str) >0:
        return is_within_N_days(datetime_str,1)
    else:
        return  False

def JudgeIsNew_Yesterday(raw_time_string):
    datetime_str = parseDataTimeFromToutiaoContent(raw_time_string)
    if len(datetime_str) >0:
        return is_within_N_days(datetime_str,2)
    else:
        return  False

def JudgeIsNew_3Days(raw_time_string):
    datetime_str = parseDataTimeFromToutiaoContent(raw_time_string)
    if len(datetime_str) >0:
        return is_within_N_days(datetime_str,3)
    else:
        return  False

def JudgeIsNew_ThisWeek(raw_time_string):
    datetime_str = parseDataTimeFromToutiaoContent(raw_time_string)
    if len(datetime_str) >0:
        return is_within_N_days(datetime_str,7)
    else:
        return  False

def JudgeIsNew_ThisMonth(raw_time_string):
    datetime_str = parseDataTimeFromToutiaoContent(raw_time_string)
    if len(datetime_str) >0:
        return is_within_N_days(datetime_str,30)
    else:
        return  False


def newInsertNewTopicSearchHismsg_Toutiao(SearchKeyword, Title, BigContent, TimeAuthor, Url):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
        if connection.is_connected():
            cursor = connection.cursor()
            # 查询数据库中是否存在相同的title或link
            query = """SELECT * FROM topicsearch_hismsg_info where info_internet_address = %s"""
            cursor.execute(query, (Url,))
            rows = cursor.fetchall()
            if len(rows) == 0:
                query = """insert into topicsearch_hismsg_info 
                (search_platform, keyword, info_title, info_publish_time_str, info_content, info_internet_address) 
                values('头条资讯',%s,%s,%s,%s,%s)"""
                cursor.execute(query, (SearchKeyword, Title, TimeAuthor, BigContent, Url))
                connection.commit()

            return "success"

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return "######ERROR######" + f"Error while connecting to MySQL: {e}" + f"SQL STRING: {query}"
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()



if __name__ == '__main__':
    # 定义要提取日期时间的字符串列表
    log_entries = [
        "【主流程】中第17条指令【打印日志】: 2024-04-07 11:30·读懂财经研究所",
        "【主流程】中第17条指令【打印日志】: 2024-04-10 00:52·中国经济时报",
        "【主流程】中第17条指令【打印日志】: 原创2024-04-10 10:11·参考消息"
    ]

    for temp in log_entries:
        print(JudgeIsNew_Today(temp))
