import re
import string
import json
import mysql.connector
from mysql.connector import Error
import time
import SQLStrPass
import ControlCenterTools


db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'
charset='utf8mb4'

def getTopicList():
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
        if connection.is_connected():
            cursor = connection.cursor()
            # 查询数据库中是否存在相同的title或link
            query = """SELECT DISTINCT topic FROM topickeywords;"""
            cursor.execute(query)
            rows = cursor.fetchall()
            #返回的是 [('量化',), ('商业航天',), ('小米汽车',), ('低空经济',), ('通用价值点',)] 这样的元祖列表，需要处理下
            TopicList = [item[0] for item in rows]
            return TopicList

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return []  # 发生错误时返回空
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()



# def insert_tosend(where_to_send, info_type, info_dwh_reletive_file_path)

def keywords_list_to_string(keywordsList):
    keywords_str = ""
    for item in keywordsList:
        keyword = str(item).split("@@")[0]
        keywords_str = keywords_str + keyword + " "
    return  keywords_str

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


def commit_wx_chat_pic_tosend(hismsg_id, temp_info_author_name, topic_matched, keywords_str):
    info_dwh_reletive_file_path = query_info_dwh_reletive_file_path(hismsg_id)
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
        if connection.is_connected():
            cursor = connection.cursor()
            # 插入文字提示
            content = ("【"+ str(topic_matched) +"："
                       + str(keywords_str) + "】"
                       +str(temp_info_author_name)+" 微信新发图片或文件 ")
            content = SQLStrPass.escape_sql_string(content)
            sql = f"""insert into to_send_info 
            (where_to_send,has_send,msg_type,info_content,info_dwh_reletive_file_path) 
            values ('{topic_matched}','no','文字','{content}','')"""
            cursor.execute(sql)
            # 提交更改到数据库
            connection.commit()

            # 插入图片
            sql = f"""insert into to_send_info 
                        (where_to_send,has_send,msg_type,info_content,info_dwh_reletive_file_path) 
                        values ('{topic_matched}','no','图片','','{info_dwh_reletive_file_path}')"""
            cursor.execute(sql)
            # 提交更改到数据库
            connection.commit()

            # 标记info_has_commit_tosend = yes
            sql = f"""update hismsg_info set info_has_commit_tosend = 'yes' where id = {hismsg_id}"""
            cursor.execute(sql)
            # 提交更改到数据库
            connection.commit()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {sql}")
        return False  # 发生错误时返回False
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

def commit_wb_tosend(hismsg_id, temp_info_author_name, temp_info_url, topic_matched, keywords_str):
    info_dwh_reletive_file_path = query_info_dwh_reletive_file_path(hismsg_id)
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
        if connection.is_connected():
            cursor = connection.cursor()
            # 插入文字提示
            content = ("【"+ str(topic_matched) +"："
                       + str(keywords_str) + "】"
                       +str(temp_info_author_name)+" 新发微博： " + str(temp_info_url))

            sql = """insert into to_send_info 
            (where_to_send,has_send,msg_type,info_content,info_dwh_reletive_file_path) 
            values ( %s,'no','文字', %s,'')"""
            cursor.execute(sql, (topic_matched, content))
            # 提交更改到数据库
            connection.commit()

            # 插入图片
            sql = f"""insert into to_send_info 
                        (where_to_send,has_send,msg_type,info_content,info_dwh_reletive_file_path) 
                        values ('{topic_matched}','no','图片','','{info_dwh_reletive_file_path}')"""
            cursor.execute(sql)
            # 提交更改到数据库
            connection.commit()

            # 标记info_has_commit_tosend = yes
            sql = f"""update hismsg_info set info_has_commit_tosend = 'yes' where id = {hismsg_id}"""
            cursor.execute(sql)
            # 提交更改到数据库
            connection.commit()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {sql}")
        return False  # 发生错误时返回False
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

def commit_xq_tosend(hismsg_id, temp_info_author_name, temp_info_url, topic_matched, keywords_str):
    info_dwh_reletive_file_path = query_info_dwh_reletive_file_path(hismsg_id)
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
        if connection.is_connected():
            cursor = connection.cursor()
            # 插入文字提示
            content = ("【"+ str(topic_matched) +"："
                       + str(keywords_str) + "】"
                       +str(temp_info_author_name)+" 新发雪球： " + str(temp_info_url))
            sql = """insert into to_send_info 
            (where_to_send,has_send,msg_type,info_content,info_dwh_reletive_file_path) 
            values ( %s,'no','文字', %s,'')"""
            cursor.execute(sql, (topic_matched, content))
            # 提交更改到数据库
            connection.commit()

            # 插入图片
            sql = f"""insert into to_send_info 
                        (where_to_send,has_send,msg_type,info_content,info_dwh_reletive_file_path) 
                        values ('{topic_matched}','no','图片','','{info_dwh_reletive_file_path}')"""
            cursor.execute(sql)
            # 提交更改到数据库
            connection.commit()

            # 标记info_has_commit_tosend = yes
            sql = f"""update hismsg_info set info_has_commit_tosend = 'yes' where id = {hismsg_id}"""
            cursor.execute(sql)
            # 提交更改到数据库
            connection.commit()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {sql}")
        return False  # 发生错误时返回False
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

def commit_wxpublic_tosend(hismsg_id, temp_info_author_name, temp_info_title, temp_info_url, topic_matched, keywords_str):
    info_dwh_reletive_file_path = query_info_dwh_reletive_file_path(hismsg_id)
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
        if connection.is_connected():
            cursor = connection.cursor()
            # 插入文字提示
            content = ("【"+ str(topic_matched) +"："
                       + str(keywords_str) + "】"
                       +str(temp_info_author_name)+" 公众号新推文： " + str(temp_info_title) + "  " + str(temp_info_url))
            sql = """insert into to_send_info 
            (where_to_send,has_send,msg_type,info_content,info_dwh_reletive_file_path) 
            values ( %s,'no','文字', %s,'')"""
            cursor.execute(sql, (topic_matched, content))
            # 提交更改到数据库
            connection.commit()

            # 标记info_has_commit_tosend = yes
            sql = f"""update hismsg_info set info_has_commit_tosend = 'yes' where id = {hismsg_id}"""
            cursor.execute(sql)
            # 提交更改到数据库
            connection.commit()
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {sql}")
        return False  # 发生错误时返回False
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()


def commit_toutiaobaidu_search_tosend(hismsg_id, temp_info_time_author, temp_info_title, temp_info_url, topic_matched, keywords_str):

    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
        if connection.is_connected():
            cursor = connection.cursor()
            # 插入文字提示
            content = ("【"+ str(topic_matched) +"："
                       + str(keywords_str) + "】"
                       +str(temp_info_time_author)+" 头百搜索新资讯： " + str(temp_info_title) + "  " + str(temp_info_url))
            sql = """insert into to_send_info 
            (where_to_send,has_send,msg_type,info_content,info_dwh_reletive_file_path) 
            values ( %s,'no','文字', %s,'')"""
            cursor.execute(sql, (topic_matched, content))
            # 提交更改到数据库
            connection.commit()

            # 标记info_has_commit_tosend = yes
            sql = f"""update hismsg_info set info_has_commit_tosend = 'yes' where id = {hismsg_id}"""
            cursor.execute(sql)
            # 提交更改到数据库
            connection.commit()
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {sql}")
        return False  # 发生错误时返回False
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()



def commit_hismsg_tosend(LengthThreshold):
    info_rows = []
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)
        if connection.is_connected():
            cursor = connection.cursor()
            query = f"""SELECT * FROM hismsg_info 
                WHERE info_ready_for_analysis = 'yes' AND info_content is not null 
                AND (info_bad_for_analysis != 'bad' OR info_bad_for_analysis IS NULL) 
                AND LENGTH(info_analysis_status) > {LengthThreshold}
                and LENGTH(info_match_topic) >= 2
                AND (info_has_commit_tosend != 'yes' or info_has_commit_tosend IS null)
                AND create_time  >= '2024-03-29'
                order by id desc;"""

            cursor.execute(query)
            # 过滤出所有符合条件,可以推送的hismsg
            info_rows = cursor.fetchall()


    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return "##Error## "+ f"in commit_hismsg_tosend() Error while connecting to MySQL: {e}" + f"SQL STRING: {query}"
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

    print(len(info_rows))
    for temp_info in info_rows:
        temp_info_id = temp_info[0]
        temp_info_author_name =  '' if temp_info[3] is None else temp_info[3]
        temp_info_type = '' if temp_info[5] is None else temp_info[5]
        temp_info_title = '' if temp_info[6] is None else temp_info[6]
        temp_info_content = '' if temp_info[7] is None else temp_info[7]
        temp_info_url =  '' if temp_info[7] is None else temp_info[8]
        temp_info_analysis_status_dict = {} if temp_info[11] is None else json.loads(temp_info[11])
        temp_info_abstract = '' if temp_info[12] is None else temp_info[12]
        temp_info_match_topic_list = [] if temp_info[13] is None else json.loads(temp_info[13])

        for matched_topic in temp_info_match_topic_list:
            print(matched_topic)
            topic_key = list(dict(matched_topic).keys())[0]
            keywords_list = list(dict(matched_topic).values())[0]
            keywords_str = keywords_list_to_string(keywords_list)
            topic = topic_key.split('##')[0]
            match_score = topic_key.split('##')[1]
            if temp_info_type == "微信聊天图片":
                commit_wx_chat_pic_tosend(temp_info_id,temp_info_author_name,topic,keywords_str)
            elif temp_info_type == "微博推文":
                commit_wb_tosend(temp_info_id,temp_info_author_name,temp_info_url,topic,keywords_str)
            elif temp_info_type == "雪球推文":
                commit_xq_tosend(temp_info_id,temp_info_author_name,temp_info_url,topic,keywords_str)
            elif temp_info_type == "公众号推文":
               commit_wxpublic_tosend(temp_info_id,temp_info_author_name,temp_info_title,temp_info_url,topic,keywords_str)
            elif temp_info_type == "头条百度资讯搜索":
               commit_toutiaobaidu_search_tosend(temp_info_id,temp_info_author_name,temp_info_title,temp_info_url,topic,keywords_str)
            else:
                print("未识别的temp_info_type：" + temp_info_type)

        if len(temp_info_match_topic_list) == 0:
            if temp_info_type == "微信聊天图片":
                commit_wx_chat_pic_tosend(temp_info_id, temp_info_author_name, 'unmatched', '')
            elif temp_info_type == "微博推文":
                commit_wb_tosend(temp_info_id, temp_info_author_name, temp_info_url, 'unmatched', '')
            elif temp_info_type == "雪球推文":
                commit_xq_tosend(temp_info_id, temp_info_author_name, temp_info_url, 'unmatched', '')
            elif temp_info_type == "公众号推文":
                commit_wxpublic_tosend(temp_info_id, temp_info_author_name, temp_info_title, temp_info_url, 'unmatched','')
            elif temp_info_type == "头条百度资讯搜索":
                commit_toutiaobaidu_search_tosend(temp_info_id, temp_info_author_name, temp_info_title, temp_info_url, 'unmatched','')
            else:
                print("未识别的temp_info_type：" + temp_info_type)

    return "success"


if __name__ == '__main__':
    # query_info_dwh_reletive_file_path(5739)

    while True:
        TopicList = getTopicList()
        # 对 info_analysis_status 字段按照长度过滤
        LengthThreshold = 8 + len(str(TopicList))
        commit_hismsg_tosend(LengthThreshold)

        ControlCenterTools.report_to_ControlCenter("main_Commit_tosend","running(waiting)...")
        time.sleep(3)
