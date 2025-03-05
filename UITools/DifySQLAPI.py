# sql_tools.py

from flask import Flask, request, jsonify
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



# 数据库连接配置
config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'your_database',
    'raise_on_warnings': True
}


# 初始化Flask应用
app = Flask(__name__)


# 连接数据库
def connect_to_database():
    try:
        conn = mysql.connector.connect(**config)
        print("Connected to MySQL database")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# 执行SQL查询
def execute_query(conn, sql):
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        if sql.strip().lower().startswith("select"):
            # 如果是查询操作，返回结果
            result = cursor.fetchall()
            return result
        else:
            # 如果是插入、更新、删除操作，提交事务并返回受影响的行数
            conn.commit()
            return cursor.rowcount
    except mysql.connector.Error as err:
        print(f"Error executing SQL: {err}")
        return None
    finally:
        cursor.close()


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