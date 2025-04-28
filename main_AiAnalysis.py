import json
import schedule
import AiTools.CommonDataOpTools
import AiTools.MiniMaxTool
import MsgSendTool
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import time
import ControlCenterTools

Prompt_Msg_Abstruct = """
    你是顶级的产业、投资、金融分析师，接下来请你帮我梳理过去一段时间的信息简报，
    主要依据爬虫采集的一段或多段Json结构化后的信息集。
    要求：
    要对信息真正有价值的部分准确提炼，切忌抽象化、概念化、模糊化的总结，不需要你来延伸解读，更不能泛泛而谈。
    一般而言，单条信息精炼后的简述约30字内，讲重点，讲精华，讲关键即可。
    如果一个条目是水文，只需10字内简述。水文指内容质量低、信息密度低、主题混乱的信息条目。
    对于有时间、地点、人物、主体对象、事件、新闻价值点、产业认知、产业逻辑、投资逻辑、风险因素等的信息条目，要更加重点分析。
    信息来源，例如微信消息发送人的名称（info_author_name）、url链接（info_internet_address）
    单条信息的格式：[年月日时分秒 · 消息来源][消息简报]
    主要针对以下几类主题的信息进行分析：大AI、自动驾驶、机器人、先锋热点
    不需要分析过程和礼貌寒暄。
    
    
"""

Prompt_WXMsg_Abstruct = """
    你是顶级的产业、投资、金融分析师，接下来请你帮我梳理过去一段时间的微信群聊记录简报，
    主要依据爬虫采集的一段或多段Json结构化后的微信群聊天记录集。
    要求：
    1. 因为是多人穿插的聊天记录，请你根据上下文综合分析他们的聊天主题。
    2. 提取有价值的观点，并准确表达原意即可，不要对聊天内容进行抽象化/概念化的总结。
    3. 如果有涉及到重要新闻事件、产业认知、产业逻辑的条目，要视作重点内容。
    不需要分析过程和礼貌寒暄。


"""

Prompt_CallStock_Abstruct = """
    你是顶级的产业、投资、金融分析师，接下来请你帮我梳理过去一段时间中券商call票的情况，
    主要依据爬虫采集的一段或多段Json结构化后的微信聊天语料。
    要求：
    首先把call票的原文（可能有多段）从纷杂的聊天记录中抽离出来，并整理好原文，请务必输出原文。
    然后对call票的语料进行梳理：介绍股票（如果有代码）、对应的投资逻辑、call票人（次数）。
    梳理的时候，提取有价值的观点，并准确表达原意即可，不要对内容进行抽象化/概念化的总结。
    总之，你的输出应该包括两个板块，一是call票聊天记录的原文整理；二是对其进行进行梳理。
    不需要分析过程和礼貌寒暄。
    如果语料中没有call票的信息，请直接这样输出：没有找到call票信息。
    
    
"""

def Ana_LastHour_Hismsg():
    res = AiTools.CommonDataOpTools.query_lasthour_hismsg()
    if res is None or len(res) < 3:
        return
    Prompt = Prompt_Msg_Abstruct + str(res)
    AnalyRes, TokenCount = AiTools.MiniMaxTool.AiAnalysis_MiniMax(Prompt)
    if(TokenCount == 0):
        #表示出错了,AnalyRes是错误信息
        print(AnalyRes)
        return

    current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    Msg_Contnet = f"{current_time}\n小时消息({len(res)})条 Token:{TokenCount}\n{AnalyRes}"
    # 实例化企业微信群机器人对象
    MsgSummary_robot = "9748c011-448d-46e7-b130-a87dda76b609"
    QyRobotInstance = MsgSendTool.QyRobot(MsgSummary_robot)
    QyRobotInstance.send_text_message(Msg_Contnet)
    return


def Ana_Today_Hismsg(Topic):
    res = AiTools.CommonDataOpTools.query_today_hismsg(Topic)
    if res is None or len(res) < 3:
        return
    Prompt = Prompt_WXMsg_Abstruct + str(res)
    AnalyRes, TokenCount = AiTools.MiniMaxTool.AiAnalysis_MiniMax(Prompt)
    if(TokenCount == 0):
        #表示出错了,AnalyRes是错误信息
        print(AnalyRes)
        return

    current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    Msg_Contnet = f"{current_time}\n今日消息（{len(res)}）条 Token:{TokenCount}\n{AnalyRes}"
    # 实例化企业微信群机器人对象
    MsgSummary_robot = "9748c011-448d-46e7-b130-a87dda76b609"
    QyRobotInstance = MsgSendTool.QyRobot(MsgSummary_robot)
    QyRobotInstance.send_text_message(Msg_Contnet)
    return


def Ana_Today_WXMsg():
    res = AiTools.CommonDataOpTools.query_today_wxmsg()
    if res is None or len(res) < 3:
        return
    Prompt = Prompt_WXMsg_Abstruct + str(res)
    AnalyRes, TokenCount = AiTools.MiniMaxTool.AiAnalysis_MiniMax(Prompt)
    if(TokenCount == 0):
        #表示出错了,AnalyRes是错误信息
        print(AnalyRes)
        return

    current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    Msg_Contnet = f"{current_time}\n微信群消息解析 Token:{TokenCount}\n{AnalyRes}"
    # 实例化企业微信群机器人对象
    MsgSummary_robot = "9748c011-448d-46e7-b130-a87dda76b609"
    QyRobotInstance = MsgSendTool.QyRobot(MsgSummary_robot)
    QyRobotInstance.send_text_message(Msg_Contnet)
    return

def Ana_Today_CallStock():
    res = AiTools.CommonDataOpTools.query_today_wxmsg()
    if res is None or len(res) < 3:
        return
    Prompt = Prompt_CallStock_Abstruct + str(res)
    AnalyRes, TokenCount = AiTools.MiniMaxTool.AiAnalysis_MiniMax(Prompt)
    if(TokenCount == 0):
        #表示出错了,AnalyRes是错误信息
        print(AnalyRes)
        return

    current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    Msg_Contnet = f"{current_time}\n微信群call票 Token:{TokenCount}\n{AnalyRes}"
    # 实例化企业微信群机器人对象
    MsgSummary_robot = "9748c011-448d-46e7-b130-a87dda76b609"
    QyRobotInstance = MsgSendTool.QyRobot(MsgSummary_robot)
    QyRobotInstance.send_text_message(Msg_Contnet)
    return

if __name__ == '__main__':
    # Ana_Today_Hismsg("激光雷达")
    # Ana_LastHour_Hismsg()
    # Ana_Today_WXMsg()
    # Ana_Today_CallStock()

    # 使用 schedule.every().hour.do() 来安排每小时执行一次函数 A
    schedule.every().hour.do(Ana_LastHour_Hismsg)

    # 使用 schedule.every().day.at("HH:MM").do() 来安排每天的特定时间执行函数 B
    schedule.every().day.at("12:05").do(Ana_Today_WXMsg)
    schedule.every().day.at("12:10").do(Ana_Today_CallStock)
    schedule.every().day.at("15:05").do(Ana_Today_WXMsg)
    schedule.every().day.at("15:10").do(Ana_Today_CallStock)
    schedule.every().day.at("19:05").do(Ana_Today_WXMsg)
    schedule.every().day.at("19:10").do(Ana_Today_CallStock)


    # 主循环，持续运行并检查调度任务
    while True:
        # 运行所有待执行的任务
        schedule.run_pending()
        # 每隔 1 秒检查一次
        time.sleep(3)
        ControlCenterTools.report_to_ControlCenter("main_AiAnalysis", "running(waiting)...")

    # # res = AiTools.CommonDataOpTools.query_lasthour_hismsg()
    # res = AiTools.CommonDataOpTools.query_lastest_hismsg(50)
    # print(json.dumps(res, indent=2, ensure_ascii=False))
    # Prompt = Prompt_LastHour_Hismsg + str(res)
    # AnalyRes, TokenCount = AiTools.MiniMaxTool.AiAnalysis_MiniMax(Prompt)
    # print(AnalyRes)
    # # 实例化企业微信群机器人对象
    # MsgSummary_robot = "9748c011-448d-46e7-b130-a87dda76b609"
    # QyRobotInstance = MsgSendTool.QyRobot(MsgSummary_robot)
    # QyRobotInstance.send_text_message(AnalyRes)
