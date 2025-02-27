import TopicKwordsAnalysis
import mysql.connector
from mysql.connector import Error
import TopicKeywordsLists
import time
import ControlCenterTools

db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'
def getTopicList():
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password)
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

if __name__ == '__main__':
    while True:
        TopicList = getTopicList()
        print("进行关键词分析的主题如下：\n" + str(TopicList))
        ControlCenterTools.report_to_ControlCenter("main_TopicKeywordsAnalysis", "开始对如下主题进行关键词分析：\n" + str(TopicList))
        time.sleep(3)

        for tempTopic in TopicList:
            TopicKwordsAnalysis.analyze_recent_articles(tempTopic)

