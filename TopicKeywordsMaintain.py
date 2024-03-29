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

newInsertTopic('商业航天',TopicKeywordsLists.commercial_space_keywords)