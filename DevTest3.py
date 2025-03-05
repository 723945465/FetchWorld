from flask import Flask, render_template, request, url_for, redirect
import pymysql
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
import LLMsTests
import os
from stylecloud import gen_stylecloud
import pandas as pd
import jieba
import jieba.analyse
from wordcloud import WordCloud
import imageio
from PIL import ImageFont



db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'
charset='utf8mb4'



if __name__ == '__main__':

    query = f"""SELECT info_content FROM hismsg_info WHERE id > 8100"""
    print(query)
    content_s = ""
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password,
                                             charset=charset)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                content_s = content_s + str(row[0])

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print(f"SQL STRING: {query}")
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()
    # res_str = ""
    # if len(content_s) > 0:
    #     res_str = LLMsTools.Kimi_refine_msg(content_s)
    # else:
    #     res_str = "请提交有效的hismsg_id"


    # 定义输出文件路径
    output_file_path = "E:\\1.txt"

    # 将结果写入到指定的文件中
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(content_s)

    print(f"内容已写入到{output_file_path}")
    # gen_stylecloud(file_path=output_file_path)
    #
    # # 读取文件
    # pd_data = pd.read_excel('鸿星尔克.xlsx')
    #
    # # 读取内容
    # text = pd_data['发帖内容'].tolist()

    # 切割分词
    wordlist = jieba.cut(content_s, cut_all = True)
    result = ' '.join(wordlist)
    print(result)

    wordlist = jieba.lcut_for_search(content_s)
    result = ' '.join(wordlist)
    print(result)

    # 设置停用词
    stop_words = ['你', '我', '的', '了', '们']
    ciyun_words = ''

    for word in result:
        if word not in stop_words:
            ciyun_words += word

    # 权重分析
    tag = jieba.analyse.extract_tags(sentence=ciyun_words, topK=10, withWeight=True)
    print(tag)

    # 导入模块


    # 文本数据
    text = 'he speak you most bueatiful time|Is he first meeting you'
    # 准备禁用词，需要为set类型
    stopwords = set(['he', 'is'])
    # 设置参数，创建WordCloud对象


    mk = imageio.v2.imread("E:\\1.jpg")
    wc = WordCloud(
        font_path="msyh.ttc",
        width=200,  # 设置宽为400px
        height=150,  # 设置高为300px
        background_color='white',  # 设置背景颜色为白色
        # mask = mk,
        stopwords=stopwords,  # 设置禁用词，在生成的词云中不会出现set集合中的词
        max_font_size=100,  # 设置最大的字体大小，所有词都不会超过100px
        min_font_size=10,  # 设置最小的字体大小，所有词都不会超过10px
        max_words=10,  # 设置最大的单词个数
        scale=2  # 扩大两倍
    )
    # 生成词云
    wc.generate(ciyun_words)
    # 保存词云文件
    wc.to_file('E:\\12333.jpg')

    gen_stylecloud(text='Hello World',
                   output_name='E:\\12444.jpg')

    gen_stylecloud(text=result,
                   icon_name='fas fa-comment-dots',
                   font_path='msyh.ttc',
                   background_color='white',
                   output_name='E:\\666.jpg',
                   custom_stopwords=['你', '我', '的', '了', '在', '吧', '相信', '是', '也', '都', '不', '吗', '就',
                                     '我们', '还', '大家', '你们', '就是', '以后']
                   )
    print('绘图成功！')
