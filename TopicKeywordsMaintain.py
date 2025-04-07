# -*- coding = utf-8 -*-
# @Time: 2024/3/20 21:05
# @Author: Chris
# @File: TopicKeywordsMaintain.py
# @Software: PyCharm

import mysql.connector
from mysql.connector import Error
import TopicKeywordsLists


db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'
charset='utf8mb4'

def newInsertTopic(Topic_name, Topic_keywords):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password)
        if connection.is_connected():
            cursor = connection.cursor()
            # 插入数据
            for keyword in Topic_keywords:
                sql = ("INSERT INTO topickeywords (topic, keyword, weight) VALUES (%s, %s, %s)")
                val = (Topic_name, str(keyword['keyword']).lower(), keyword['weight'])
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



# def UpdateTopic(Topic_name, Topic_keywords):
#     try:
#         # 连接到MySQL数据库
#         connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password)
#         if connection.is_connected():
#             cursor = connection.cursor()
#             # 查询数据库中是否存在相同的title或link
#             query = """SELECT * FROM topickeywords WHERE topic = %s"""
#             cursor.execute(query, (Topic_name,))
#             rows = cursor.fetchall()
#             if len(rows) > 0:
#                 query = """DELETE FROM topickeywords WHERE topic = %s"""
#                 cursor.execute(query, (Topic_name,))
#         connection.commit()
#
#         newInsertTopic(Topic_name, Topic_keywords)
#
#     except Error as e:
#         print(f"Error while connecting to MySQL: {e}")
#         print(f"SQL STRING: {query}")
#         return []  # 发生错误时返回空
#     finally:
#         # 关闭数据库连接
#         if connection.is_connected():
#             cursor.close()
#             connection.close()

#如果数据库中已经存在Topic_name的主题关键词，全部删除，然后重新插入。
#可以用于更新主题关键词，也可以直接用于插入新的主题关键词
def UpdateTopic(Topic_name, Topic_keywords):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password)
        if connection.is_connected():
            cursor = connection.cursor()
            # 查询数据库中是否存在相同的title或link
            query = """SELECT * FROM topickeywords WHERE topic = %s"""
            cursor.execute(query, (Topic_name,))
            rows = cursor.fetchall()
            if len(rows) > 0:
                query = """DELETE FROM topickeywords WHERE topic = %s"""
                cursor.execute(query, (Topic_name,))
        connection.commit()

        newInsertTopic(Topic_name, Topic_keywords)

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return []  # 发生错误时返回空
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    # UpdateTopic('机器人', TopicKeywordsLists.ai_robot_keywords) # 已停用
    UpdateTopic('商业航天', TopicKeywordsLists.commercial_space_keywords)
    UpdateTopic('低空经济', TopicKeywordsLists.low_altitude_economy_keywords)
    UpdateTopic('通用价值点', TopicKeywordsLists.common_value_keywords)
    UpdateTopic('先锋热点', TopicKeywordsLists.HotPoint_keywords)
    UpdateTopic('生物制造', TopicKeywordsLists.Biomanufacturing_keywords)
    UpdateTopic('激光雷达', TopicKeywordsLists.LidarADAS_keywords)
    # UpdateTopic('AI算力', TopicKeywordsLists.AIHPC_keywords)  # 已停用
    UpdateTopic('量化', TopicKeywordsLists.quantitative_trading_keywords)
    UpdateTopic('大AI', TopicKeywordsLists.ai_keywords)
