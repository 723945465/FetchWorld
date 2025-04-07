import requests
import json

# 设置API的URL和Chat ID
url_structure = "http://{address}/api/v1/chats_openai/{chat_id}/chat/completions"
chat_id = "cf5e1cdafb2f11ef85fc0242ac120006"  #
api_key = "ragflow-QxNDYzNTJlZmIzMjExZWY5ZDI1MDI0Mm"  # 替换为你的API密钥

# 设置请求头
headers = {
    'Accept-Charset': 'utf-8',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

def QueryRagFlow(Query):
    if Query is None or Query == "":
        return "##Error## Query is empty"

    try:
        data = {
            "model": "model",  # 可以根据实际需要设置为模型名称
            "messages": [
                {"role": "user",
                 # "content": "简要分析DeepSeek对上下游产业链的冲击，返回200字以内,markdonw格式"}
                 "content": f"{Query}"}
            ],
            "stream": False  # 设置为True表示使用流式响应
        }

        url = url_structure.format(address="localhost:81", chat_id=chat_id)
        # 发送POST请求
        response = requests.post(url,
                                 headers=headers,
                                 data=json.dumps(data))

        # 打印响应状态码和文本
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text)

        if response.status_code == 200:
            response_data = response.json()
            message_content = response_data["choices"][0]["message"]["content"]
            # 打印返回的消息内容
            print("Message Content:", message_content)

            # 提取 total_tokens 并打印
            total_tokens = response_data["usage"]["total_tokens"]
            print("Total Tokens:", total_tokens)

            return str(message_content)
        else:
            return f"##Error## {response.text}"




    except Exception as e:
        print(f"Exception while QueryRagFlow: {e}")
        return f"##Error## Exception while QueryRagFlow: {e}"



if __name__ == '__main__':
    print(QueryRagFlow("简要分析DeepSeek对上下游产业链的冲击，返回200字以内,markdonw格式"))

