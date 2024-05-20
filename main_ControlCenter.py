from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import json
import re

import FTPTools
import CommonDbOpTools

app = Flask(__name__)
db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'


ServiceStatusDict = {
    "WXPublicWebApi": ["2024-04-02 13:29:40","last message"],
    "WeiboXueqiuFetch": ["2024-04-02 13:29:40","last message"],
    "WechatPicAndFile": ["2024-04-02 13:29:40","last message"],
    "ToutiaoBaiduTopicSearch": ["2024-04-02 13:29:40", "last message"],
    "main_SelectSearchInfo": ["2024-04-02 13:29:40", "last message"],
    "main_OCR": ["2024-04-02 13:29:40","last message"],
    "main_TopicKeywordsAnalysis": ["2024-04-02 13:29:40","last message"],
    "main_Commit_tosend": ["2024-04-02 13:29:40","last message"],
    "SendNewMsg": ["2024-04-02 13:29:40","last message"],
}


@app.route('/report', methods=['POST'])
def receive_report():
    """
    这个接口用于接收外部传来的报告。
    :return: 返回一个确认接收的响应。
    """
    data = request.get_json()  # 获取JSON格式的报告数据
    if (data and 'reportService' in data
            and 'reportStr' in data
            and 'reportTime' in data):
        reportService = data['reportService']
        reportStr = data['reportStr']
        reportTime = data['reportTime']

        if reportService not in ServiceStatusDict:
            print(f"receive_report()收到错误信息：{str(data)}")
            return jsonify({'status': 'error', 'message': 'Invalid report data'}), 400

        ServiceStatusDict[reportService] = [str(reportTime),str(reportStr)]
        # print(ServiceStatusDict)

        return jsonify({'status': 'success', 'message': 'Report received'}), 200
    else:
        print(f"receive_report()收到错误信息：{str(data)}")
        return jsonify({'status': 'error', 'message': 'Invalid report data'}), 400


@app.route('/run_status', methods=['GET'])
def run_status():
    res_string = ""
    for service, status in ServiceStatusDict.items():
        # print(f"{str(status[0])}  {service}: {str(status[1])}")
        res_string = (res_string
                      + f"{str(status[0])} &nbsp;{service}:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {str(status[1])}"
                      + "</br>")

    if(FTPTools.FTP_test() == 'success'):
        res_string += " </br>FTP test is OK.  </br>"

    res = CommonDbOpTools.query_latest_hismsg_by_infosource("微信")
    res_string += f" </br>latest msg from 微信： {res} </br>"
    res = CommonDbOpTools.query_latest_hismsg_by_infosource("公众号")
    res_string += f" </br>latest msg from 公号： {res} </br>"
    res = CommonDbOpTools.query_latest_hismsg_by_infosource("微博")
    res_string += f" </br>latest msg from 微博： {res} </br>"
    res = CommonDbOpTools.query_latest_hismsg_by_infosource("雪球")
    res_string += f" </br>latest msg from 雪球： {res} </br>"
    res = CommonDbOpTools.query_latest_hismsg_by_infosource("头条资讯搜索")
    res_string += f" </br>latest msg from 搜索： {res} </br>"

    return res_string, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1868, debug=False)