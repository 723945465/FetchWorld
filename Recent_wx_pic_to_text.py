import OCR_wx
import os
import mysql.connector
from mysql.connector import Error


db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'

def query_dwh_reletive_file_path_by_msgid(hismsg_id):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password)
        if connection.is_connected():
            cursor = connection.cursor()
            # 执行SQL查询
            query = "SELECT dwh_reletive_file_path FROM msg_attach where hismsg_id = %s;"  # 使用占位符 %s
            cursor.execute(query, (hismsg_id,))  # 使用 execute() 的第二个参数来传递参数值

            # 获取查询结果
            rows = cursor.fetchall()
            return rows[0][0]

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return ""  # 发生错误时返回""
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()


def construct_recent_wx_content(temp_pic_proc_folder_path):
    if os.path.exists(temp_pic_proc_folder_path) == False:
        print("微信图片OCR处理的临时文件夹不存在")
        return

    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password)
        if connection.is_connected():
            cursor = connection.cursor()
            query = ("SELECT * FROM fetchtheworld.hismsg_info "
                     "WHERE (info_ready_for_analysis != 'yes' OR info_ready_for_analysis IS NULL) "
                     "AND info_source = '微信' AND info_type = '图片'"
                     "AND create_time  >= '2024-03-21';")
            cursor.execute(query)
            #rows是微信消息中，消息类型为图片的，还没有准备好分析的原始数据，取近期的数据。
            rows = cursor.fetchall()
            for temp_row in rows:
                temp_dwh_reletive_file_path = query_dwh_reletive_file_path_by_msgid(temp_row[0])
                print(temp_dwh_reletive_file_path)
            print(len(rows))

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return False  # 发生错误时返回False
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == '__main__':
    construct_recent_wx_content("C:\\WXPicProcTempFold\\")
    # print(download_wx_pic(3369))