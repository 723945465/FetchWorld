from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import json

app = Flask(__name__)
db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'


ServiceStatusDict = {
    "WXPublicWebApi": ["2024-04-02 13:29:40","last message"],
    "WeiboXueqiuFetch": ["2024-04-02 13:29:40","last message"],
    "WechatPicAndFile": ["2024-04-02 13:29:40","last message"],
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
        print(ServiceStatusDict)

        return jsonify({'status': 'success', 'message': 'Report received'}), 200
    else:
        print(f"receive_report()收到错误信息：{str(data)}")
        return jsonify({'status': 'error', 'message': 'Invalid report data'}), 400


@app.route('/run', methods=['GET'])
def run_status():
    json_str = json.dumps(ServiceStatusDict, indent=4)
    return jsonify(json_str), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1868, debug=True)