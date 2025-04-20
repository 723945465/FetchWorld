"""
企业微信群聊机器人-发送消息
"""
import base64
import hashlib
import time

import requests




class QyRobot(object):

    def __init__(self, robot):
        # 设置企业微信群消息机器人key
        self.robot = robot

    @staticmethod
    def get_image_base64(image_file):
        with open(image_file, 'rb') as f:
            base64_data = base64.b64encode(f.read())
        return str(base64_data, 'utf-8')

    @staticmethod
    def get_image_md5(path):
        md5_l = hashlib.md5()
        with open(path, mode="rb") as f:
            by = f.read()
        md5_l.update(by)
        md5_code = md5_l.hexdigest()
        return md5_code.upper()

    def send_qy_robot(self, msg, max_retries=3, timeout=10):
        """
        企业微信机器人发送消息
        :param msg: 消息内容
        :param max_retries: 请求重试次数
        :param timeout:   请求失败等待时间
        :return:
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={}"
        real_url = url.format(self.robot)
        retries = 0
        while retries < max_retries:
            resp = requests.post(real_url, json=msg)
            if resp.status_code == 200 and resp.json().get('errcode') == 0:
                print("发送消息通知成功")
                return resp
            else:
                print(f"发送消息失败：{resp.json().get('errmsg')}")
            retries += 1
            print(f"正在进行第{retries}次重试...")
            time.sleep(timeout)
        return

    def send_image_message(self, img_path):
        # 图片消息
        img_msg = {
            "msgtype": "image",
            "image": {
                "base64": self.get_image_base64(img_path),
                "md5": self.get_image_md5(img_path)
            }
        }
        self.send_qy_robot(msg=img_msg)
        return

    def send_text_message(self, content):
        # 发送文本消息
        msg = {
            "msgtype": "text",
            "text": {
                "content": str(content)
            }
        }
        self.send_qy_robot(msg=msg)
        return


if __name__ == '__main__':
    # 实例化企业微信群机器人对象
    MsgSummary_robot = "9748c011-448d-46e7-b130-a87dda76b609"
    QyRobotInstance = QyRobot(MsgSummary_robot)
    # 发送文本消息
    content = "测试"
    QyRobotInstance.send_text_message(content)
    # # 发送图片消息
    # img_path = r"C:\img\48.jpg"
    # QyRobotInstance.send_image_message(img_path)