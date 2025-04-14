# -*- coding = utf-8 -*-
# @Time: 2024/4/2 10:21
# @Author: Chris
# @File: CommonDbOpTools.py
# @Software: PyCharm

import os.path
import re
import string
import json
import time
import mysql.connector
from mysql.connector import Error

db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'
charset='utf8mb4'

def query_info_dwh_reletive_file_path(hismsg_id):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
        if connection.is_connected():
            cursor = connection.cursor()
            # 查询数据库中是否存在相同的title或link
            query = f"""SELECT dwh_reletive_file_path FROM msg_attach where hismsg_id = {hismsg_id};"""
            cursor.execute(query)
            rows = cursor.fetchall()
            if(len(rows)>0):
                info_dwh_reletive_file_path = rows[0][0]
                return info_dwh_reletive_file_path

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return ""  # 发生错误时返回空
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

def set_bad_hismsg(hismsg_id):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password,
                                             charset=charset)
        if connection.is_connected():
            cursor = connection.cursor()
            # 标记info_has_commit_tosend = yes
            sql = f"""update hismsg_info set info_bad_for_analysis = 'bad' where id = {hismsg_id}"""
            cursor.execute(sql)
            # 提交更改到数据库
            connection.commit()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {sql}")
        return ""  # 发生错误时返回空
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()


def query_latest_hismsg_by_infosource(infosource):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
        if connection.is_connected():
            cursor = connection.cursor()
            # 查询数据库中是否存在相同的title或link
            query = f"""SELECT create_time FROM fetchtheworld.hismsg_info
                        where info_source = '{infosource}' 
                        ORDER BY id desc LIMIT 1;"""
            cursor.execute(query)
            rows = cursor.fetchall()
            if(len(rows)>0):
                return str(rows[0][0])
            else:
                return "Error info source input."

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return f"Error while connecting to MySQL: {e}"
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

def insert_new_wxmsg(source, sender, sender_remark, type, content):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password,
                                             charset=charset)
        if connection.is_connected():
            cursor = connection.cursor()
            query = """insert into wxmsg_info (
            msg_source, 
            msg_sender_name, 
            msg_sender_remark,
            msg_type,
            msg_content) values (%s, %s, %s, %s, %s)"""
            # 执行SQL语句
            cursor.execute(query, (source, sender, sender_remark, type, content))
            connection.commit()

            return "success"
        else:
            return "######ERROR###### cannot connect to mysql"
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
    # res = query_latest_hismsg_by_infosource("微信")
    res = insert_new_wxmsg("一笑","Chris","Chris-remark","文字","haha teset")
    print(res)