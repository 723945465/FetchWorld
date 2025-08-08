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
import ControlCenterTools

db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'
charset='utf8mb4'
conn_timeout = 20,  # 设置连接超时

def CommitSearchInfoToHismsg():
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, connect_timeout = conn_timeout)
        if connection.is_connected():
            cursor = connection.cursor()
            # 查询数据库中是否存在相同的title或link
            query = """SELECT * FROM topicsearch_hismsg_info 
            where (has_committed_hismsg != 'yes' OR has_committed_hismsg IS NULL) 
            AND create_time >= NOW() - INTERVAL 1 DAY"""
            cursor.execute(query)
            rows = cursor.fetchall()

            for temp_info in rows:
                temp_searchinfo_id = temp_info[0]
                temp_searchinfo_searchplatform = '' if temp_info[2] is None else str(temp_info[2])+'搜索'
                temp_searchinfo_searchkeyword = '' if temp_info[3] is None else temp_info[3]
                temp_searchinfo_title = '' if temp_info[4] is None else temp_info[4]
                temp_searchinfo_timeauthor = '' if temp_info[5] is None else temp_info[5]
                temp_searchinfo_content = '' if temp_info[7] is None else temp_info[7]
                temp_searchinfo_url = '' if temp_info[12] is None else temp_info[12]

                query = """insert into hismsg_info (info_source,info_author_name, info_type,info_title,info_content,info_internet_address, info_ready_for_analysis)
                                      values (%s, %s, '头条百度资讯搜索', %s, %s, %s, 'yes')"""
                # 执行SQL语句
                cursor.execute(query, (temp_searchinfo_searchplatform, temp_searchinfo_timeauthor, temp_searchinfo_title, temp_searchinfo_content, temp_searchinfo_url))
                connection.commit()

                query = """update topicsearch_hismsg_info set has_committed_hismsg = 'yes' where id = %s"""
                cursor.execute(query,(temp_searchinfo_id,))
                connection.commit()

            print(f"提交{str(len(rows))}个最新搜索文章的结果到hismsg_info")
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

    while True:
        res = CommitSearchInfoToHismsg()
        if res == "success":
            ControlCenterTools.report_to_ControlCenter("main_SelectSearchInfo","running(waiting)...")
        else:
            ControlCenterTools.report_to_ControlCenter("main_SelectSearchInfo", "Error: "+str(res))
        time.sleep(3)