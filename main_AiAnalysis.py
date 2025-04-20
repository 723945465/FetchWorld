import json
import AiTools.CommonDataOpTools
import AiTools.MiniMaxTool
import MsgSendTool
import mysql.connector
from mysql.connector import Error
import time
import ControlCenterTools

Prompt_LastHour_Hismsg = """
    你是顶级的产业、投资、金融分析师，接下来请你帮我梳理过去一个短时间的信息简报，
    主要依据爬虫采集的一段或多段结构化后的信息集。
    要求：
    要对信息进行精炼，切忌抽象化、概念化的总结，不需要你来延伸解读，更不能泛泛而谈。
    一般而言，单条信息精炼后的简述约30字内，讲重点，讲精华，讲关键即可。
    如果一个条目是水文，只需10字内简述。水文指内容质量低、信息密度低、主题混乱的信息条目。
    对于有时间、地点、人物、主体对象、事件、新闻价值点、产业认知、产业逻辑、投资逻辑、风险因素等的信息条目，要更加重点分析。
    信息来源，例如微信消息发送人的名称（info_author_name）、url链接（info_internet_address）
    单条信息的格式：[年月日时分秒 · 消息来源][消息简报]
    主要针对以下几类主题的信息进行分析：大AI、自动驾驶、机器人、先锋热点
    不需要分析过程和礼貌寒暄。
    
"""


if __name__ == '__main__':
    # res = AiTools.CommonDataOpTools.query_lasthour_hismsg()
    res = AiTools.CommonDataOpTools.query_lastest_hismsg(50)
    print(json.dumps(res, indent=2, ensure_ascii=False))
    Prompt = Prompt_LastHour_Hismsg + str(res)
    AnalyRes, TokenCount = AiTools.MiniMaxTool.AiAnalysis_MiniMax(Prompt)
    print(AnalyRes)
    # 实例化企业微信群机器人对象
    MsgSummary_robot = "9748c011-448d-46e7-b130-a87dda76b609"
    QyRobotInstance = MsgSendTool.QyRobot(MsgSummary_robot)
    QyRobotInstance.send_text_message(AnalyRes)

    # while True:
    #     ControlCenterTools.report_to_ControlCenter("main_AiAnalysis", "AiAnalysis...")
    #     time.sleep(3)