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
                            'info_abstract', info_abstract,
                            'info_match_topic', info_match_topic
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

def query_lastest_hismsg(num_of_msg):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
        if connection.is_connected():
            cursor = connection.cursor()
            # 定义SQL查询
            sql = f"""
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
                    ) AS latest_5_records_json
                    FROM (
                        SELECT *
                        FROM hismsg_info
                        ORDER BY create_time DESC
                        LIMIT {num_of_msg}
                    ) AS latest_records;
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


if __name__ == '__main__':

    res = query_lastest_hismsg(10)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    print(res)
    # print(len(res))
    # print(len(str(res)))
    # truncated_json = res[:2]
    #
    # print(json.dumps(truncated_json, indent=4, ensure_ascii=False))
    # print(len(str(truncated_json)))