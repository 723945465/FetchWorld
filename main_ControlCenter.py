from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'


@app.route('/report', methods=['POST'])
def receive_report():
    """
    这个接口用于接收外部传来的报告。
    :return: 返回一个确认接收的响应。
    """
    data = request.get_json()  # 获取JSON格式的报告数据
    if data and 'report' in data:
        print("Received report:", data['report'])
        return jsonify({'status': 'success', 'message': 'Report received'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid report data'}), 400

@app.route('/run', methods=['GET'])
def run_status():
    """
    这个接口用于向外界请求并输出运行情况。
    :return: 返回当前运行状态的响应。
    """
    # 这里只是一个示例，实际中可能需要向其他服务发送请求并获取状态
    run_status = {'cpu_usage': 60, 'memory_usage': 80, 'disk_usage': 50}
    return jsonify(run_status), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1868, debug=True)