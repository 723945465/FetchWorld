import requests
import readline

def AiAnalysis_MiniMax(prompt):
    group_id = "1906964265516929343"
    api_key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJDaHJpcyIsIlVzZXJOYW1lIjoiQ2hyaXMiLCJBY2NvdW50IjoiIiwiU3ViamVjdElEIjoiMTkwNjk2NDI2NTUyNTMxNzk1MSIsIlBob25lIjoiMTg2MDY3MTMzOTYiLCJHcm91cElEIjoiMTkwNjk2NDI2NTUxNjkyOTM0MyIsIlBhZ2VOYW1lIjoiIiwiTWFpbCI6IiIsIkNyZWF0ZVRpbWUiOiIyMDI1LTA0LTE2IDE5OjA2OjUxIiwiVG9rZW5UeXBlIjoxLCJpc3MiOiJtaW5pbWF4In0.tN8RuxSZ7C9YPCeAktBtgUTT7RWhdknSZUyGO91pPQAeLZn8hpRsWp02ssSgyri7uch8smH1hv5i0UlNglOP1mVxV1tcpZtqNiM8LOND_-orZpxmjzFWlSLvotYWLQ6PP9GXr4ZjmnJz8cH2iU6kA--4juCMCaaG_HHpo4bMEjo6uRinXJPKUp_injomCCvKZe5OGsudgFtoEVTW4Gt6QvPXVkU4FO2OkhgmAtOo7ldSDGdli6TjYdlpurq5t36gURHYZOMlBzYVjoSJwsbKScaaRAd_MlNgIz3cztrsEpjpTSIL3xkKyLsDoEAziq1mMd3-0YBTJ3RFi7p4gsb47A"

    url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={group_id}"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        # tokens_to_generate/bot_setting/reply_constraints可自行修改
        request_body = payload = {
            "model": "MiniMax-Text-01",
            "max_tokens": 100000,  # 最大生成token数,设置为10万
            "tokens_to_generate": 100000,  # 这俩参数好像是一个意思
            "reply_constraints": {"sender_type": "BOT", "sender_name": "MM智能助理"},
            "messages": [],
            "bot_setting": [
                {
                    "bot_name":"MM智能助理",
                    "content":"MM智能助理是顶级的产业研究专家和金融投资专家",
        }
            ],
        }

        request_body["messages"].append(
            {"sender_type": "USER", "sender_name": "小明", "text": prompt}
        )
        response = requests.post(url, headers=headers, json=request_body)
        reply = response.json()["reply"]
        # print(response.json())
        total_tokens = response.json()["usage"]["total_tokens"]
        # print(f"TokensUsage: {total_tokens}")
        return reply, total_tokens

    except Exception as e:
        print(e)
        print(f"Error from AiAnalysis_MiniMax: {e}")
        return f"Error from AiAnalysis_MiniMax: {e}",0




if __name__ == '__main__':
    reply, total_tokens = AiAnalysis_MiniMax("1+1")
    print(reply)
    print(total_tokens)