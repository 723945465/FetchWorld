import requests
def main(sql: str) -> dict:
    # 定义API的URL
    url = "http://114.55.128.212:3000/execute"

    # 构造请求体
    payload = {
        "sql": sql
    }

    # 发送POST请求
    try:
        response = requests.post(url, json=payload)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析响应数据
            result = response.json()
            return {
                "result": f"{result}"
            }
        else:
            return {
                "result": f"请求失败，状态码：{response.status_code},{response.json()}"
            }
    except requests.exceptions.RequestException as e:
        return {
            "result": f"请求异常：{e}"
        }

res = main("SELECT * FROM hismsg_info limit 10")
print(res)