# -*- coding = utf-8 -*-
# @Time: 2024/3/20 21:05
# @Author: Chris
# @File: MaintainTopicKeywords.py
# @Software: PyCharm

import mysql.connector
from mysql.connector import Error


db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'


# # 关键词列表,每个元素是一个字典,包含关键词和对应权重
# quantitative_trading_keywords = [
# {'keyword': '量化', 'weight': 10},
# {'keyword': '量化交易', 'weight': 10},
# {'keyword': '算法', 'weight': 9},
# {'keyword': '算法交易', 'weight': 10}
# ]

# xiaomi_car_keywords = [
#     {'keyword': '小米汽车', 'weight': 10},
#     {'keyword': 'SU7', 'weight': 10},
#     {'keyword': '小米首款车型', 'weight': 10},
#     {'keyword': '发布会', 'weight': 9},
#     {'keyword': '定价', 'weight': 9},
#     {'keyword': '雷军', 'weight': 9},
#     {'keyword': 'V8S超级电机', 'weight': 8}
# ]

sorted_integrated_low_altitude_economy_keywords = [
    {'keyword': '低空物流', 'weight': 10},
    {'keyword': '低空经济', 'weight': 10},
    {'keyword': 'eVTOL', 'weight': 10},
    {'keyword': '低空医疗', 'weight': 10},
    {'keyword': '低空航线', 'weight': 10},
    {'keyword': '低空出行', 'weight': 10},
    {'keyword': '垂直起降', 'weight': 8},
    {'keyword': '空中交通', 'weight': 8},
    {'keyword': '低空飞行器', 'weight': 8},
    {'keyword': '智能飞行', 'weight': 8},
]

commercial_space_keywords = [
    {'keyword': '运载火箭', 'weight': 9.5},
    {'keyword': '卫星互联网', 'weight': 9.0},
    {'keyword': '低轨', 'weight': 9.0},
    {'keyword': '星链', 'weight': 9.5},
    {'keyword': '可回收', 'weight': 8.5},
    {'keyword': '星座', 'weight': 9.0},
    {'keyword': '中国卫星通信集团', 'weight': 8},
    {'keyword': '中国卫通', 'weight': 8},
    {'keyword': '上海微小卫星', 'weight': 8},
    {'keyword': 'SMIC', 'weight': 8},
    {'keyword': '航天长峰', 'weight': 8},
    {'keyword': '长峰航天', 'weight': 8},
    {'keyword': '银河航天', 'weight': 8},
    {'keyword': '银河互联网', 'weight': 8},
    {'keyword': 'Galactic Network', 'weight': 8},
    {'keyword': '蓝箭', 'weight': 8},
    {'keyword': 'LandSpace', 'weight': 8},
    {'keyword': '星际荣耀', 'weight': 8},
    {'keyword': 'iSpace', 'weight': 8},
    {'keyword': '零壹', 'weight': 8},
    {'keyword': 'OneSpace', 'weight': 8},
    {'keyword': '中科微星', 'weight': 7},
    {'keyword': '天仪研究院', 'weight': 7},
    {'keyword': '天仪', 'weight': 7},
    {'keyword': 'Spacety', 'weight': 7},
    {'keyword': '星网', 'weight': 9},
    {'keyword': 'China Satellite Network', 'weight': 9},
    {'keyword': '鸿雁星座', 'weight': 8},
    {'keyword': '鸿雁', 'weight': 8},
    {'keyword': '虹云', 'weight': 8},
    {'keyword': '快舟', 'weight': 8},
]

def newInsertTopic(Topic_name, Topic_keywords):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password)
        if connection.is_connected():
            cursor = connection.cursor()
            # 插入数据
            for keyword in Topic_keywords:
                sql = ("INSERT INTO topickeywords (topic, keyword, weight) VALUES (%s, %s, %s)")
                val = (Topic_name, keyword['keyword'], keyword['weight'])
                cursor.execute(sql, val)

            # 提交更改到数据库
        connection.commit()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {sql}")
        return False  # 发生错误时返回False
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

newInsertTopic('商业航天',commercial_space_keywords)