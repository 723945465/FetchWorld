import mysql.connector
from mysql.connector import Error
import TopicSearchKeywordsList

db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'
charset='utf8mb4'

def newInsertTopic(Topic_name, SearchPlatform, Topic_keywords):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password)
        if connection.is_connected():
            cursor = connection.cursor()
            # 插入数据
            for keyword in Topic_keywords:
                sql = ("INSERT INTO topicsearchkeywords (topic, search_platform, keyword, weight) VALUES (%s, %s, %s, %s)")
                val = (Topic_name, SearchPlatform, str(keyword['keyword']).lower(), keyword['weight'])
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


#如果数据库中已经存在Topic_name,且在SearchPlatform平台下的搜索关键词，全部删除，然后重新插入。
#可以用于更新主题关键词，也可以直接用于插入新的主题关键词
def UpdateTopic(Topic_name, SearchPlatform, Topic_keywords):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password)
        if connection.is_connected():
            cursor = connection.cursor()
            # 查询数据库中是否存在相同的title或link
            query = """SELECT * FROM topicsearchkeywords WHERE topic = %s and search_platform = %s"""
            cursor.execute(query, (Topic_name,SearchPlatform))
            rows = cursor.fetchall()
            if len(rows) > 0:
                query = """DELETE FROM topicsearchkeywords WHERE topic = %s and search_platform = %s"""
                cursor.execute(query, (Topic_name,SearchPlatform))
        connection.commit()

        newInsertTopic(Topic_name, SearchPlatform, Topic_keywords)

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return []  # 发生错误时返回空
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

def GetTopicsBySearchPlatform(SearchPlatform):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password)
        if connection.is_connected():
            cursor = connection.cursor()
            # 查询数据库中是否存在相同的title或link
            query = """SELECT distinct topic FROM topicsearchkeywords where search_platform = %s"""
            cursor.execute(query, (SearchPlatform,))
            rows = cursor.fetchall()
            TopicList = []
            if len(rows) > 0:
                for row in rows:
                    TopicList.append(str(row[0]))
                return TopicList
            else:
                return []
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return []  # 发生错误时返回空
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

def GetKeywordsByTopicsAndSearchPlatform(Topic, SearchPlatform):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password)
        if connection.is_connected():
            cursor = connection.cursor()
            # 查询数据库中是否存在相同的title或link
            query = """SELECT distinct keyword FROM topicsearchkeywords where search_platform = %s and topic = %s"""
            cursor.execute(query, (SearchPlatform, Topic))
            rows = cursor.fetchall()
            KeywordsList = []
            if len(rows) > 0:
                for row in rows:
                    KeywordsList.append(str(row[0]))
                return KeywordsList
            else:
                return []
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
        return []  # 发生错误时返回空
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    # SearchPlatform = '头条资讯'
    # TopicList = GetTopicsBySearchPlatform(SearchPlatform)
    # for topic in TopicList:
    #     print(GetKeywordsByTopicsAndSearchPlatform(topic,SearchPlatform))
    UpdateTopic('大AI', '头条资讯', TopicSearchKeywordsList.ai_toutiaonews_keywords)
    # UpdateTopic('大AI', '百度资讯', TopicSearchKeywordsList.ai_baidunews_keywords)
    UpdateTopic('算力', '头条资讯', TopicSearchKeywordsList.HPC_toutiaonews_keywords)
    UpdateTopic('机器人', '头条资讯', TopicSearchKeywordsList.ai_robot_toutiaonews_keywords)
    UpdateTopic('机器人', '百度资讯', TopicSearchKeywordsList.ai_robot_baidunews_keywords)
    UpdateTopic('低空经济', '头条资讯', TopicSearchKeywordsList.low_altitude_economy_toutiaonews_keywords)
    UpdateTopic('低空经济', '百度资讯', TopicSearchKeywordsList.low_altitude_economy_baidunews_keywords)
    UpdateTopic('商业航天', '头条资讯', TopicSearchKeywordsList.commercial_space_toutiaonews_keywords)
    UpdateTopic('商业航天', '百度资讯', TopicSearchKeywordsList.commercial_space_baidunews_keywords)
    UpdateTopic('生物制造', '头条资讯', TopicSearchKeywordsList.Biomanufacturing_toutiaonews_keywords)
    UpdateTopic('生物制造', '百度资讯', TopicSearchKeywordsList.Biomanufacturing_baidunews_keywords)
    UpdateTopic('先锋热点', '头条资讯', TopicSearchKeywordsList.HotPoint_toutiaonews_keywords)
    UpdateTopic('先锋热点', '百度资讯', TopicSearchKeywordsList.HotPoint_baidunews_keywords)
    UpdateTopic('激光雷达', '头条资讯', TopicSearchKeywordsList.LidarADAS_toutiaonews_keywords)
    UpdateTopic('激光雷达', '百度资讯', TopicSearchKeywordsList.LidarADAS_baidunews_keywords)
    UpdateTopic('AI算力', '头条资讯', TopicSearchKeywordsList.AIHPC_toutiaonews_keywords)
    UpdateTopic('AI算力', '百度资讯', TopicSearchKeywordsList.AIHPC_baidunews_keywords)
    UpdateTopic('量化', '头条资讯', TopicSearchKeywordsList.quantitative_trading_toutiaonews_keywords)
    UpdateTopic('量化', '百度资讯', TopicSearchKeywordsList.quantitative_trading_baidunews_keywords)
