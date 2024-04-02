import requests

# 远程Flask应用的URL
ControlCenterUrl = 'http://47.97.219.6:1868'  # 请替换为你的Flask应用的实际URL

def test_receive_report():
    """
    测试远程/report接口
    """
    report_data = {"report": "This is a test report from remote"}
    response = requests.post(f"{ControlCenterUrl}/report", json=report_data)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.json() == {'status': 'success', 'message': 'Report received'}, "Expected successful report receipt message"

def test_run_status():
    """
    测试远程/run接口
    """
    response = requests.get(f"{ControlCenterUrl}/run")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    expected_status = {'cpu_usage': 60, 'memory_usage': 80, 'disk_usage': 50}
    assert response.json() == expected_status, "Expected specific run status data"

if __name__ == "__main__":
    test_receive_report()
    test_run_status()
    print("All tests passed!")