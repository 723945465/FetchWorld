import os.path
import re
import string
import json
import mysql.connector
from mysql.connector import Error
import OCR_PaddleOCRTools
import FTPTools
import SQLStrPass
import time
import WXPublicContentParse
import CommonDbOpTools

db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'
charset='utf8mb4'

Dir_ocr_temp_image_folder = 'C:\\ocr_temp\\'

# def query_info_dwh_reletive_file_path(hismsg_id):
#     try:
#         # 连接到MySQL数据库
#         connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
#         if connection.is_connected():
#             cursor = connection.cursor()
#             # 查询数据库中是否存在相同的title或link
#             query = f"""SELECT dwh_reletive_file_path FROM msg_attach where hismsg_id = {hismsg_id};"""
#             cursor.execute(query)
#             rows = cursor.fetchall()
#             if(len(rows)>0):
#                 info_dwh_reletive_file_path = rows[0][0]
#                 return info_dwh_reletive_file_path
#
#     except Error as e:
#         print(f"Error while connecting to MySQL: {e}")
#         print(f"SQL STRING: {query}")
#         return ""  # 发生错误时返回空
#     finally:
#         # 关闭数据库连接
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
#
# def set_bad_hismsg(hismsg_id):
#     try:
#         # 连接到MySQL数据库
#         connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password,
#                                              charset=charset)
#         if connection.is_connected():
#             cursor = connection.cursor()
#             # 标记info_has_commit_tosend = yes
#             sql = f"""update hismsg_info set info_bad_for_analysis = 'bad' where id = {hismsg_id}"""
#             cursor.execute(sql)
#             # 提交更改到数据库
#             connection.commit()
#
#     except Error as e:
#         print(f"Error while connecting to MySQL: {e}")
#         print(f"SQL STRING: {sql}")
#         return ""  # 发生错误时返回空
#     finally:
#         # 关闭数据库连接
#         if connection.is_connected():
#             cursor.close()
#             connection.close()

def set_image_content_and_ready_analysis(hismsg_id, image_content_text):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password,
                                             charset=charset)
        if connection.is_connected():
            cursor = connection.cursor()

            sql = """update hismsg_info set info_content = %s, info_ready_for_analysis = 'yes' 
            where id = %s"""
            cursor.execute(sql, (image_content_text, hismsg_id))
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

def ocr_recent_wechat_image():
    info_rows = []
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password,
                                             charset=charset)
        if connection.is_connected():
            cursor = connection.cursor()
            query = """SELECT * FROM fetchtheworld.hismsg_info
            WHERE (info_ready_for_analysis != 'yes' OR info_ready_for_analysis IS NULL) 
            AND (info_bad_for_analysis != 'bad' OR info_bad_for_analysis IS NULL) 
            AND info_source = '微信' 
            and info_type = '微信聊天图片' 
            AND create_time  >= '2024-04-1';"""

            cursor.execute(query)
            info_rows = cursor.fetchall()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return "##Error## "+ f"Error while connecting to MySQL: {e}" + f"SQL STRING: {query}"

    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

    for temp_info in info_rows:
        temp_info_id = temp_info[0]
        temp_dwh_reletive_file_path = CommonDbOpTools.query_info_dwh_reletive_file_path(temp_info_id)
        temp_orc_local_image_file_path = Dir_ocr_temp_image_folder + temp_dwh_reletive_file_path
        print(f"下载文件：{temp_dwh_reletive_file_path}")
        download_res = FTPTools.download_file_from_dwh(temp_dwh_reletive_file_path,temp_orc_local_image_file_path)
        if download_res == "success":
            temp_image_content = OCR_PaddleOCRTools.PicToText_PaddleOCR(temp_orc_local_image_file_path)
            if "##Error##" in temp_image_content:
                #下载成功，但是ORC失败，则把消息设置为bad
                print(f"图片下载成功，但OCR失败，设置为bad：{temp_dwh_reletive_file_path}")
                CommonDbOpTools.set_bad_hismsg(temp_info_id)
                continue
            else:
                #下载成功且ORC成功。
                SQLStrPass_image_content = SQLStrPass.escape_sql_string(temp_image_content)
                set_image_content_and_ready_analysis(temp_info_id,SQLStrPass_image_content)
                print(f"图片OCR成功，设置待分析：{SQLStrPass_image_content}")
        else:
            #下载失败,放弃这一条
            print(f"图片下载失败，设置为bad：{temp_dwh_reletive_file_path}")
            CommonDbOpTools.set_bad_hismsg(temp_info_id)
            continue

    return "success"

def ocr_recent_weibo_xueqiu_image():
    info_rows = []
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password,
                                             charset=charset)
        if connection.is_connected():
            cursor = connection.cursor()
            query = """SELECT * FROM fetchtheworld.hismsg_info 
            WHERE (info_ready_for_analysis != 'yes' OR info_ready_for_analysis IS NULL) 
            AND (info_bad_for_analysis != 'bad' OR info_bad_for_analysis IS NULL) 
            AND (info_source = '微博' OR info_source = '雪球') 
            AND create_time  >= '2024-04-1';"""

            cursor.execute(query)
            info_rows = cursor.fetchall()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return "##Error## "+ f"Error while connecting to MySQL: {e}" + f"SQL STRING: {query}"

    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

    for temp_info in info_rows:
        temp_info_id = temp_info[0]
        temp_dwh_reletive_file_path = CommonDbOpTools.query_info_dwh_reletive_file_path(temp_info_id)
        temp_orc_local_image_file_path = Dir_ocr_temp_image_folder + temp_dwh_reletive_file_path
        print(f"下载文件：{temp_dwh_reletive_file_path}")
        download_res = FTPTools.download_file_from_dwh(temp_dwh_reletive_file_path,temp_orc_local_image_file_path)
        if download_res == "success":
            temp_image_content = OCR_PaddleOCRTools.PicToText_PaddleOCR(temp_orc_local_image_file_path)
            if "##Error##" in temp_image_content:
                #下载成功，但是ORC失败，则把消息设置为bad
                print(f"图片下载成功，但OCR失败，设置为bad：{temp_dwh_reletive_file_path}")
                CommonDbOpTools.set_bad_hismsg(temp_info_id)
                continue
            else:
                #下载成功且ORC成功。
                SQLStrPass_image_content = SQLStrPass.escape_sql_string(temp_image_content)
                set_image_content_and_ready_analysis(temp_info_id,SQLStrPass_image_content)
                print(f"图片OCR成功，设置待分析：{SQLStrPass_image_content}")
        else:
            #下载失败,放弃这一条
            print(f"图片下载失败，设置为bad：{temp_dwh_reletive_file_path}")
            CommonDbOpTools.set_bad_hismsg(temp_info_id)
            continue

    return "success"


def ocr_recent_WXPublic_image():
    info_rows = []
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password,
                                             charset=charset)
        if connection.is_connected():
            cursor = connection.cursor()
            query = """SELECT * FROM fetchtheworld.hismsg_info 
            WHERE (info_ready_for_analysis != 'yes' OR info_ready_for_analysis IS NULL) 
            AND (info_bad_for_analysis != 'bad' OR info_bad_for_analysis IS NULL) 
            AND info_source = '公众号'
            AND create_time  >= '2024-03-30';"""

            cursor.execute(query)
            info_rows = cursor.fetchall()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return "##Error## "+ f"Error while connecting to MySQL: {e}" + f"SQL STRING: {query}"

    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

    for temp_info in info_rows:
        temp_info_id = temp_info[0]
        temp_info_url = '' if temp_info[7] is None else temp_info[8]
        temp_info_title = '' if temp_info[6] is None else temp_info[6]
        # temp_info_content = '' if temp_info[7] is None else temp_info[7]
        ocr_temp_image_filepath = Dir_ocr_temp_image_folder + "WXPublic_ocr_temp.jpg"
        content_with_pic_parse = WXPublicContentParse.parse_WXPublic_webpage(temp_info_url,ocr_temp_image_filepath)
        sql_pass_text_content = SQLStrPass.escape_sql_string(content_with_pic_parse)
        print(f"######公号推文《{temp_info_title}》解析完毕######")
        print(temp_info_url)
        print(sql_pass_text_content)
        try:
            # 连接到MySQL数据库
            connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user,
                                                 password=db_password, charset=charset)

            if connection.is_connected():
                cursor = connection.cursor()
                # 创建插入SQL语句
                query = """update hismsg_info set info_content = %s, info_ready_for_analysis = 'yes' where id = %s"""
                # 执行SQL语句
                cursor.execute(query, (sql_pass_text_content, temp_info_id))
                connection.commit()
        except Error as e:
            return "##Error## " + f"Error while connecting to MySQL: {e}" + f"SQL STRING: {query}"


        finally:
            # 关闭数据库连接
            if connection.is_connected():
                cursor.close()
                connection.close()


    return "success"

if __name__ == '__main__':
    if os.path.exists(Dir_ocr_temp_image_folder) == False:
        print(f"OCR临时文件夹不存在：{Dir_ocr_temp_image_folder}")
        exit(0)

    while True:
        try:
            res = ocr_recent_wechat_image()
            if (res != "success"):
                print("ocr_recent_wechat_image严重发生错误：" + res)
                print("无限循环退出")
                break
        except Exception as e:
            print(f"ocr_recent_wechat_image发生捕获到未处理异常: {e}")
            print("无限循环继续")

        try:
            res = ocr_recent_weibo_xueqiu_image()
            if (res != "success"):
                print("ocr_recent_weibo_xueqiu_image严重发生错误：" + res)
                print("无限循环退出")
                break
        except Exception as e:
            print(f"ocr_recent_weibo_xueqiu_image发生捕获到未处理异常: {e}")
            print("无限循环继续")

        try:
            res = res = ocr_recent_WXPublic_image()
            if (res != "success"):
                print("ocr_recent_WXPublic_image严重发生错误：" + res)
                print("无限循环退出")
        except Exception as e:
            print(f"ocr_recent_WXPublic_image发生捕获到未处理异常: {e}")
            print("无限循环继续")

        print("main_OCR is running(waiting)...")
        time.sleep(3)


