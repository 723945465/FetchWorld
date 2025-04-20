import os.path
import re
import string
import json
import time
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'
charset='utf8mb4'

def query_timescope_wxmsg(start_time, end_time):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # 使用字典游标，方便转换为 JSON

            # 编写 SQL 查询
            sql_query = """
                            SELECT 
                            id,  create_time, msg_source, msg_sender_remark,msg_content
                            FROM wxmsg_info
                            WHERE create_time >= %s AND create_time < %s
                            ORDER BY msg_source ASC, id ASC
                        """

            # 执行查询
            cursor.execute(sql_query, (start_time, end_time))

            # 获取所有结果
            results = cursor.fetchall()


            # 按 msg_source 分类
            grouped_results = {}
            for row in results:
                source = row['msg_source']
                if source not in grouped_results:
                    grouped_results[source] = []
                grouped_results[source].append(row)

            # 将结果转换为 JSON
            # json_result = json.dumps(grouped_results, indent=4, default=str, ensure_ascii=False)
            json_result = json.dumps(grouped_results, default=str, ensure_ascii=False)
            # print(json_result)
            return json_result


    except Error as e:
        print(f"Error while connecting to MySQL by query_lasthour_hismsg: {e}")
        print(f"SQL STRING: {sql_query}")
        return f"Error while connecting to MySQL: {e}"
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

def query_lasthour_wxmsg():
    # 获取当前时间
    now = datetime.now()
    # 计算上一个整点小时的时间
    last_hour = (now - timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

    # 定义时间范围
    start_time = last_hour
    end_time = last_hour + timedelta(hours=1)

    return query_timescope_wxmsg(start_time, end_time)


def query_today_wxmsg():
    # 获取当前时间
    now = datetime.now()

    # 定义今天的开始时间和结束时间
    start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    return query_timescope_wxmsg(start_time, end_time)

def query_yesterday_wxmsg():
    # 获取当前时间
    now = datetime.now()
    # 计算昨天的日期
    yesterday = now - timedelta(days=1)

    # 定义昨天的开始时间和结束时间
    start_time = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

    return query_timescope_wxmsg(start_time, end_time)


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
                            'info_author_name', info_author_name,
                            'info_type', info_type,
                            'info_content', info_content,
                            'info_internet_address', info_internet_address,
                            'info_match_topic', info_match_topic
                        )
                    ) AS result
                    FROM hismsg_info
                    WHERE create_time BETWEEN 
                        DATE_SUB(DATE_FORMAT(NOW(), '%Y-%m-%d %H:00:00'), INTERVAL 1 HOUR) 
                        AND 
                        DATE_FORMAT(NOW(), '%Y-%m-%d %H:00:00')
                    AND info_ready_for_analysis = 'yes' AND info_content is not null 
                    AND (info_bad_for_analysis != 'bad' OR info_bad_for_analysis IS NULL)
                    AND info_match_topic != '[]'
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
                            'info_author_name', info_author_name,
                            'info_type', info_type,
                            'info_content', info_content,
                            'info_internet_address', info_internet_address,
                            'info_match_topic', info_match_topic
                        )
                    ) AS latest_5_records_json
                    FROM (
                        SELECT *
                        FROM hismsg_info
                        WHERE info_ready_for_analysis = 'yes' 
                        AND info_content is not null 
                        AND (info_bad_for_analysis != 'bad' OR info_bad_for_analysis IS NULL) 
                        AND info_match_topic != '[]'
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

    # res = query_lasthour_wxmsg()
    # print(res)
    # res = query_yesterday_wxmsg()
    # print(res)
    res = query_today_wxmsg()
    print(res)
    # res = query_lastest_hismsg(10)
    # print(json.dumps(res, indent=2, ensure_ascii=False))
    # print(res)
    # print(len(res))
    # print(len(str(res)))
    # truncated_json = res[:2]
    #
    # print(json.dumps(truncated_json, indent=4, ensure_ascii=False))
    # print(len(str(truncated_json)))