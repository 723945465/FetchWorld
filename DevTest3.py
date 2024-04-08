from flask import Flask, render_template, request, url_for, redirect
import pymysql
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
import LLMsTools
import os

db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'
charset='utf8mb4'



if __name__ == '__main__':

    query = f"""SELECT info_content FROM hismsg_info WHERE id > 8100"""
    print(query)
    content_s = ""
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password,
                                             charset=charset)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                content_s = content_s + str(row[0])

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()
    # res_str = ""
    # if len(content_s) > 0:
    #     res_str = LLMsTools.Kimi_refine_msg(content_s)
    # else:
    #     res_str = "请提交有效的hismsg_id"


    # 定义输出文件路径
    output_file_path = "E:\\1.txt"

    # 将结果写入到指定的文件中
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(content_s)

    print(f"内容已写入到{output_file_path}")

