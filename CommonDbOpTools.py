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

def query_lasthour_hismsg():
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
        if connection.is_connected():
            cursor = connection.cursor()
            # 定义SQL查询
            sql = """
                    SELECT JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'id', id,
                            'create_time', create_time,
                            'info_source', info_source,
                            'info_author_name', info_author_name,
                            'info_author_uid', info_author_uid,
                            'info_type', info_type,
                            'info_title', info_title,
                            'info_content', info_content,
                            'info_internet_address', info_internet_address,
                            'info_bad_for_analysis', info_bad_for_analysis,
                            'info_ready_for_analysis', info_ready_for_analysis,
                            'info_analysis_status', info_analysis_status,
                            'info_abstract', info_abstract,
                            'info_match_topic', info_match_topic,
                            'info_match_hot_discussion', info_match_hot_discussion,
                            'info_has_commit_tosend', info_has_commit_tosend
                        )
                    ) AS result
                    FROM hismsg_info
                    WHERE create_time BETWEEN 
                        DATE_SUB(DATE_FORMAT(NOW(), '%Y-%m-%d %H:00:00'), INTERVAL 1 HOUR) 
                        AND 
                        DATE_FORMAT(NOW(), '%Y-%m-%d %H:00:00')
                    ORDER BY create_time DESC;
                    """

            # 执行查询
            cursor.execute(sql)
            sql_result = cursor.fetchall()[0][0]  # 获取单行结果

            # 获取JSON数据
            if sql_result and len(sql_result) > 0:
                # 解析JSON数据
                res_json = json.loads(sql_result)
                # print(len(res_json))
                # print(res_json)
                return res_json
            else:
                # print("查询结果为空。")
                return None


    except Error as e:
        print(f"Error while connecting to MySQL by query_lasthour_hismsg: {e}")
        print(f"SQL STRING: {sql}")
        return f"Error while connecting to MySQL: {e}"
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

def truncate_json(json_data, max_keys=100):
    """
    截取 JSON 数据，保留最多 max_keys 个顶级键。
    """
    if json_data is None or len(json_data) == 0:
        return None
    else:
        data = json_data[0]

    if isinstance(data, dict):
        # 截取前 max_keys 个键
        truncated_data = {k: data[k] for k in list(data.keys())[:max_keys]}
        # return json.dumps(truncated_data, indent=4)
        print(len(truncated_data))
        return truncated_data

    else:
        return None

if __name__ == '__main__':
    res = query_latest_hismsg_by_infosource("微信")

    res = query_lasthour_hismsg()
    # print(json.dumps(res, indent=2, ensure_ascii=False))
    print(res)
    print(len(res))
    print(len(str(res)))
    truncated_json = res[:10]

    print(json.dumps(truncated_json, indent=4, ensure_ascii=False))
    print(len(str(truncated_json)))