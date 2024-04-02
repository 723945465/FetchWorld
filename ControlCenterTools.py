import requests
from requests.exceptions import Timeout
from datetime import datetime
import time

# 远程Flask应用的URL
ControlCenterUrl = 'http://47.97.219.6:1868'  # 请替换为你的Flask应用的实际URL
timeout_seconds = 5

def test_get_status():
    """
    测试远程/run接口
    """
    response = requests.get(f"{ControlCenterUrl}/run_status")
    print(response.json())
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    # expected_status = {'cpu_usage': 60, 'memory_usage': 80, 'disk_usage': 50}
    # assert response.json() == expected_status, "Expected specific run status data"


def report_to_ControlCenter(reportService, reportStr):

    report_data = {}
    report_data["reportService"] = reportService
    report_data["reportStr"] = reportStr
    report_data["reportTime"] = str(datetime.now())

    try:
        response = requests.post(f"{ControlCenterUrl}/report", json=report_data, timeout=timeout_seconds)
        if response.status_code != 200:
            print("######ControlCenter报错，请检2######")
            return False
        return True

    except Timeout:
        # 如果请求超时，则捕获异常并处理
        print("report_to_ControlCenter()请求超时！")
        return False
    except requests.exceptions.HTTPError as errh:
        # 处理HTTP错误
        print("report_to_ControlCenter()HTTP错误:", errh)
        return False
    except requests.exceptions.ConnectionError as errc:
        # 处理连接错误
        print("连接错误:", errc)
        return False
    except requests.exceptions.Timeout as errt:
        # 处理超时错误
        print("report_to_ControlCenter()请求超时:", errt)
        return False
    except requests.exceptions.RequestException as err:
        # 处理请求异常
        print("report_to_ControlCenter()请求错误:", err)
        return False


if __name__ == "__main__":
    report_to_ControlCenter("main_OCR","haha")
    report_to_ControlCenter("main_TopicKeywordsAnalysis", "haha")
    report_to_ControlCenter("main_Commit_tosend", "haha")

    test_get_status()