# sql_tools.py

from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error



db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'
charset='utf8mb4'


# 初始化Flask应用
app = Flask(__name__)


# HTTP接口：执行SQL
@app.route('/execute', methods=['POST'])
def execute_sql():
    # 获取请求中的SQL语句
    data = request.json
    print(data)
    if not data or 'sql' not in data:
        return jsonify({"error": "SQL statement is required"}), 400

    sql = data['sql']
    return jsonify(sql)

    # try:
    #     # 连接到MySQL数据库
    #     connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
    #     if connection.is_connected():
    #         cursor = connection.cursor()
    #         cursor.execute(sql)
    #         res_rows = cursor.fetchall()
    #
    #         if res_rows is None:
    #             return jsonify({"error": "Failed to execute SQL"}), 500
    #         # 返回结果
    #         return jsonify({"result": res_rows})
    #         # return jsonify(res_rows)
    #
    #     else:
    #         return jsonify({"error": "Failed to connect to database"}), 500
    # except Error as e:
    #     return jsonify({f"Error from MySQL: {e}"}), 500
    #
    # finally:
    #     # 关闭数据库连接
    #     if connection.is_connected():
    #         cursor.close()
    #         connection.close()
    #

# 启动Flask应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)