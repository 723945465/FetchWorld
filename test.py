from flask import Flask, render_template, request, url_for, redirect
import pymysql
from datetime import datetime, timedelta

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
#
#
# def get_data(create_time=None, info_type=None, info_match_topic=None, time_range=None):
#     print(
#         f"create_time:{create_time} info_type:{info_type} info_match_topic:{info_match_topic} time_range:{time_range}")
#
#     conn = pymysql.connect(**DATABASE_CONFIG)
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#
#     # 基础SQL查询语句
#     sql = "SELECT * FROM `hismsg_info`"
#
#     # # 添加筛选条件
#     # where_clauses = []
#     # params = {}
#     #
#     # # 处理时间范围筛选
#     # if time_range:
#     #     if time_range == 'today':
#     #         start_date = datetime.now().date()
#     #         end_date = start_date
#     #     elif time_range == 'two_days':
#     #         start_date = datetime.now() - timedelta(days=2)
#     #         end_date = datetime.now().date()
#     #     elif time_range == 'one_week':
#     #         start_date = datetime.now() - timedelta(weeks=1)
#     #         end_date = datetime.now().date()
#     #
#     #     where_clauses.append("`create_time` >= %s AND `create_time` <= %s")
#     #     params['start_date'] = start_date
#     #     params['end_date'] = end_date
#     #
#     # # 添加其他筛选条件
#     # if create_time:
#     #     where_clauses.append("`create_time` = %s")
#     #     params['create_time'] = create_time
#     # if info_type:
#     #     where_clauses.append("`info_type` = %s")
#     #     params['info_type'] = info_type
#     # if info_match_topic:
#     #     where_clauses.append("`info_match_topic` = %s")
#     #     params['info_match_topic'] = info_match_topic
#     #
#     # if where_clauses:
#     #     sql += " WHERE " + " AND ".join(where_clauses)
#
#     sql += " LIMIT 5"
#     print(sql)
#     cursor.execute(sql)
#     # cursor.execute(sql, params)
#     results = cursor.fetchall()
#
#     cursor.close()
#     conn.close()
#     return results
#
#
# @app.route('/data')
# def data():
#     # 获取查询参数
#     create_time = request.args.get('create_time')
#     info_type = request.args.get('info_type')
#     info_match_topic = request.args.get('info_match_topic')
#     time_range = request.args.get('time_range')
#
#     print(f"create_time:{create_time} info_type:{info_type} info_match_topic:{info_match_topic} time_range:{time_range}")
#
#     # 获取数据
#     rows = get_data(create_time, info_type, info_match_topic, time_range)
#     print(rows)
#
#     # 将结果传递给模板
#     return render_template('data.html', rows=rows) + str(rows)
#
#
# @app.route('/')
# def index():
#     # 这里将编写用于展示所有数据和筛选功能的代码
#     return 'Hello, Flask!'
#
# if __name__ == '__main__':
#     app.run(debug=True)






import os
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():


    create_time = request.args.get('create_time')
    info_type = request.args.get('info_type')
    info_match_topic = request.args.get('info_match_topic')

    query = "SELECT create_time, info_source , info_author_name , info_type , info_title ,info_content , info_internet_address, info_match_topic FROM hismsg_info"
    filters = []
    if create_time:
        filters.append(f"create_time LIKE '%{create_time}%'")
    if info_type:
        filters.append(f"info_type = '{info_type}'")
    if info_match_topic:
        filters.append(f"info_match_topic LIKE '%{info_match_topic}%'")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY id desc LIMIT 20 "

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

if __name__ == '__main__':
    app.run(debug=True)