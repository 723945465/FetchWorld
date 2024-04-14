from flask import Flask, render_template, request, url_for, redirect
import pymysql
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
import LLMsTools

app = Flask(__name__)
app.config['CHARSET'] = 'utf-8'  # 设置字符编码为 UTF-8

# 数据库连接配置，请根据实际情况修改
DATABASE_CONFIG = {
    'host': '114.55.128.212',
    'user': 'chris',
    'password': '19871127ldld',
    'db': 'fetchtheworld',
    'charset': 'utf8mb4'
}

db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'
charset='utf8mb4'


import os
from flask import Flask, render_template, request
import datetime


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    create_time_filter = request.args.get('create_time_filter')
    info_type = request.args.get('info_type')
    info_match_topic = request.args.get('info_match_topic')

    query = "SELECT id, create_time , info_author_name , info_type , info_title ,info_content , info_internet_address  FROM hismsg_info"
    filters = []

    if create_time_filter:
        current_date = datetime.date.today()
        if create_time_filter == 'today':
            filters.append(f"DATE(create_time) = '{current_date}'")
        elif create_time_filter == 'two_days':
            two_days_ago = current_date - datetime.timedelta(days=2)
            filters.append(f"DATE(create_time) BETWEEN '{two_days_ago}' AND '{current_date}'")
        elif create_time_filter == 'one_week':
            one_week_ago = current_date - datetime.timedelta(days=7)
            filters.append(f"DATE(create_time) BETWEEN '{one_week_ago}' AND DATE_ADD('{current_date}', INTERVAL 1 DAY)")
        elif create_time_filter == 'one_month':
            one_month_ago = current_date - datetime.timedelta(days=30)
            filters.append(f"DATE(create_time) BETWEEN '{one_month_ago}' AND DATE_ADD('{current_date}', INTERVAL 1 DAY)")

    if info_type:
        filters.append(f"info_type = '{info_type}'")
    if info_match_topic:
        filters.append(f"info_match_topic LIKE '%{info_match_topic}%'")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY id desc LIMIT 50 "

    print(query)
    conn = pymysql.connect(**DATABASE_CONFIG)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    print(rows)
    html_res = render_template('index.html', rows=rows)
    print(html_res)
    return html_res


@app.route('/timeline', methods=['POST'])
def timeline():
    ids_str = request.data.decode('utf-8')  # 获取请求的 body 中的数据
    print(ids_str)
    query = f"""SELECT info_content FROM hismsg_info WHERE id IN ({ids_str});"""
    print(query)
    content_s = ""
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
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
    res_str = ""
    if len(content_s)>0:
        res_str = LLMsTools.Kimi_refine_msg(content_s)
    else:
        res_str = "请提交有效的hismsg_id"

    return res_str, 200

if __name__ == '__main__':
    app.run(debug=True)