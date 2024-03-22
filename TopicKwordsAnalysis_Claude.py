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
            # 查询数据库中是否存在相同的title或link
            query = """SELECT * FROM topickeywords WHERE topic = %s"""
            cursor.execute(query, (topic,))
            rows = cursor.fetchall()
            # 构造关键词列表
            topic_keywords = []
            for row in rows:
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

def analyze_article(article_text, Topic_name):
    # 文本预处理
    article_text = article_text.lower()
    article_text = re.sub(r'[%s]' % re.escape(string.punctuation), '', article_text)

    # 构造topic-keywords列表
    Topic_keywords = construct_topic_keywords(Topic_name)
    # print(Topic_keywords)

    # 统计关键词出现次数
    keyword_counts = {}
    for keyword_dict in Topic_keywords:
        keyword = keyword_dict['keyword']
        count = article_text.count(keyword)
        if count > 0:
            keyword_counts[keyword] = count

    # 根据出现次数降序排列
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)

    # 计算文章与"量化交易"主题的匹配度分数
    total_weight = sum(
        keyword_dict['weight'] * count for keyword_dict in Topic_keywords for keyword, count in
        keyword_counts.items() if keyword_dict['keyword'] == keyword)
    article_length = len(article_text)
    match_score = total_weight / article_length if article_length > 0 else 0

    match_Dict_toDB = {}
    topic_key = Topic_name + "##" + str(match_score)
    keywords_list = []
    itor = 0
    for temp_keyword in sorted_keywords:
        if itor < 3:
            itor = itor+1
            temp_keyword_string = str(temp_keyword[0]) + "@@" + str(temp_keyword[1])
            keywords_list.append(temp_keyword_string)


    match_Dict_toDB[topic_key] = keywords_list

    return sorted_keywords, match_score,match_Dict_toDB





article_text = "量化交易是一种利用数学模型和计算机算力进行交易决策的方法。它涉及算法交易、机器学习、高频交易等技术。量化交易的目标是通过对市场数据进行分析，发现交易机会并进行有效的交易。"

matched_keywords, match_score, match_Dict_toDB = analyze_article(article_text,'量化')

# print("匹配的关键词及次数(按匹配度降序排列):")
# for keyword, count in matched_keywords:
#     weight = next(keyword_dict['weight'] for keyword_dict in quantitative_trading_keywords if keyword_dict['keyword'] == keyword)
#     print(f"{keyword}: {count} (权重: {weight})")
# # print(matched_keywords)
# print(f"\n与'量化交易'主题的匹配度分数: {match_score}")
# print(match_string_toDB)
match_string_toDB = json.dumps(match_Dict_toDB, ensure_ascii=False)
print(match_string_toDB)
topic_key = list(json.loads(match_string_toDB).keys())[0]
match_score = topic_key.split('##')[1]
print(match_score)

#mark1