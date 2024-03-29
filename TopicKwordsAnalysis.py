import re
import string
import json
import mysql.connector
from mysql.connector import Error

db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'

def construct_topic_keywords(topic):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password)
        if connection.is_connected():
            cursor = connection.cursor()

            query = """SELECT * FROM topickeywords WHERE topic = %s"""
            cursor.execute(query, (topic,))
            rows = cursor.fetchall()
            # 构造关键词列表
            topic_keywords = []
            for row in rows:
                if row[3] is not None and row[4] is not None:
                    keyword_dict = {'keyword': row[3], 'weight': int(row[4])}
                    topic_keywords.append(keyword_dict)

            return topic_keywords



    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return []  # 发生错误时返回空
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

def analyze_one_article(article_text, Topic_keywords_dict_list, Topic_name):
    # 文本预处理
    article_text = article_text.lower()
    article_text = re.sub(r'[%s]' % re.escape(string.punctuation), '', article_text)

    # 统计关键词出现次数
    keyword_counts = {}
    for keyword_dict in Topic_keywords_dict_list:
        keyword = keyword_dict['keyword']
        count = article_text.count(keyword)
        if count > 0:
            keyword_counts[keyword] = count

    # 根据出现次数降序排列
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)

    # 计算文章与"量化交易"主题的匹配度分数
    total_weight = sum(
        keyword_dict['weight'] * count for keyword_dict in Topic_keywords_dict_list for keyword, count in
        keyword_counts.items() if keyword_dict['keyword'] == keyword)
    article_length = len(article_text)
    match_score = total_weight / article_length if article_length > 0 else 0

    # eg。 {"量化##0.9294117647058824": ["量化@@2", "量化交易@@2", "算法交易@@1"]}
    topic_match_condition_dict = {}
    if(match_score > 0):
        topic_key = Topic_name + "##" + str(match_score)
        keywords_list = []
        itor = 0
        for temp_keyword in sorted_keywords:
            if itor < 3:
                itor = itor+1
                temp_keyword_string = str(temp_keyword[0]) + "@@" + str(temp_keyword[1])
                keywords_list.append(temp_keyword_string)

        topic_match_condition_dict[topic_key] = keywords_list

    return sorted_keywords, match_score, topic_match_condition_dict


def analyze_recent_articles(Topic_name, is_Refresh_mode = False):
    Topic_keywords_dict_list = construct_topic_keywords(Topic_name)
    if len(Topic_keywords_dict_list) == 0:
        print("Topic内没有关键词")
        return
    info_rows = []
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password)
        if connection.is_connected():
            cursor = connection.cursor()
            if is_Refresh_mode == True:
                query = """SELECT * FROM fetchtheworld.hismsg_info 
                WHERE info_ready_for_analysis = 'yes' AND info_content is not null 
                AND (info_bad_for_analysis != 'bad' OR info_bad_for_analysis IS NULL) 
                AND create_time  >= '2024-03-21';"""
            else:
                query = f"""SELECT * FROM fetchtheworld.hismsg_info 
                WHERE info_ready_for_analysis = 'yes' AND info_content is not null 
                AND (info_bad_for_analysis != 'bad' OR info_bad_for_analysis IS NULL) 
                AND create_time  >= '2024-03-21'
                AND (info_analysis_status not like '%{Topic_name}%' OR info_analysis_status IS null);"""
            cursor.execute(query)
            info_rows = cursor.fetchall()
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return []  # 发生错误时返回空
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

    for temp_info in info_rows:
        temp_info_id = temp_info[0]
        temp_info_title = '' if temp_info[6] is None else temp_info[6]
        temp_info_content = '' if temp_info[7] is None else temp_info[7]
        temp_info_analysis_status_dict = {} if temp_info[11] is None else json.loads(temp_info[11])
        temp_info_abstract = '' if temp_info[12] is None else temp_info[12]
        temp_info_match_topic = [] if temp_info[13] is None else json.loads(temp_info[13])
        match_condition_dict = {}
        match_score = 0
        matched_keyword_list = []
        matched_keyword_list, match_score, match_condition_dict = analyze_one_article(temp_info_content, Topic_keywords_dict_list, Topic_name)


        print(Topic_name + "分析进度：" + str(temp_info_id)) if temp_info_id % 100 == 0 else None
        print(match_condition_dict) if len(match_condition_dict) > 0 else None


        if('topic' in temp_info_analysis_status_dict.keys()):
            TopicList = list(temp_info_analysis_status_dict['topic'])
            if((Topic_name in TopicList) == False):
                TopicList.append(Topic_name)
                temp_info_analysis_status_dict['topic'] = TopicList
        else:
            temp_info_analysis_status_dict['topic'] = [Topic_name]

        # 如果从数据库中读出来的info_match_topic是[]
        if len(temp_info_match_topic) == 0:
            if len(match_condition_dict) == 0:
                temp_info_match_topic = []
            else:
                temp_info_match_topic = [match_condition_dict]

        # 如果从数据库中读出来的info_match_topic已经有内容了，且match_condition_dict有新的匹配
        # 则判断新的match_condition_dict是否和已有的记录存在分析同一个Topic的情况，
        # 如果是同一个Topic，则用的新覆盖老的。
        else:
            if len(match_condition_dict) > 0:
                has_topic_exsited = False
                for match_item in temp_info_match_topic:
                    first_key, first_value = next(iter(match_item.items()))
                    if(str(first_key).find(Topic_name) >= 0):
                        has_topic_exsited = True
                if has_topic_exsited == False:
                    temp_info_match_topic.append(match_condition_dict)

        try:
            # 连接到MySQL数据库
            connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password)
            if connection.is_connected():
                cursor = connection.cursor()
                sql = ("UPDATE hismsg_info SET info_analysis_status = %s, info_match_topic = %s  WHERE id =  %s")
                val = (json.dumps(temp_info_analysis_status_dict, ensure_ascii=False), json.dumps(temp_info_match_topic, ensure_ascii=False), temp_info_id)
                cursor.execute(sql, val)
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



# article_text = "量化交易是一种利用数学模型和计算机算力进行交易决策的方法。它涉及算法交易、机器学习、高频交易等技术。量化交易的目标是通过对市场数据进行分析，发现交易机会并进行有效的交易。"
# # 构造topic-keywords列表
# Topic_keywords = construct_topic_keywords('量化')
# # print(Topic_keywords)
#
# matched_keywords, match_score, match_Dict_toDB = analyze_one_article(article_text, Topic_keywords, '量化')
#
# # print("匹配的关键词及次数(按匹配度降序排列):")
# # for keyword, count in matched_keywords:
# #     weight = next(keyword_dict['weight'] for keyword_dict in quantitative_trading_keywords if keyword_dict['keyword'] == keyword)
# #     print(f"{keyword}: {count} (权重: {weight})")
# # # print(matched_keywords)
# # print(f"\n与'量化交易'主题的匹配度分数: {match_score}")
# # print(match_string_toDB)
# match_string_toDB = json.dumps(match_Dict_toDB, ensure_ascii=False)
# print(match_string_toDB)
# topic_key = list(json.loads(match_string_toDB).keys())[0]
# match_score = topic_key.split('##')[1]
# print(match_score)

if __name__ == '__main__':
   analyze_recent_articles('量化')
   analyze_recent_articles('小米汽车')


