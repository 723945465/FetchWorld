import time
import CommonDbOpTools
from wxauto import WeChat
import ControlCenterTools

# 获取当前微信客户端
wx = WeChat()

listen_list = [
    '信息平权-产业',
    '一笑投研交流群'
]

print(1)

for i in listen_list:
    wx.AddListenChat(who=i, savepic=False)

print(2)

# 持续监听消息，并且收到消息后回复“收到”
wait = 4  # 设置1秒查看一次是否有新消息
while True:
    msgs = wx.GetListenMessage()
    # print(msgs)
    for new_msg_chatwindow in msgs:
        name_of_chatwindow = new_msg_chatwindow.who  # 获取聊天窗口名（人或群名）
        print("1.1")
        print(name_of_chatwindow)
        temp_new_msgs = msgs.get(new_msg_chatwindow)  # 获取消息内容
        print("1.2")
        print(temp_new_msgs)
        # 回复收到
        for msg in temp_new_msgs:
            msgtype = msg.type  # 获取消息类型
            if msgtype == 'friend':
                print("msgtype == friend")
                print("2.1")
                print("sender: " + msg.sender)
                print("sender_remark: " + msg.sender_remark)
                print("content: " + msg.content)
                content = msg.content
                if(content == "[链接]"):
                    content = "发送了一条链接消息"
                res = CommonDbOpTools.insert_new_wxmsg(
                    name_of_chatwindow,msg.sender,msg.sender_remark,"common",content)
                print(f'【{name_of_chatwindow}】 {msg.sender_remark} sent: {content}')

    ControlCenterTools.report_to_ControlCenter("main_WXMsgFetchTools", "running(waiting)...")
    time.sleep(wait)
