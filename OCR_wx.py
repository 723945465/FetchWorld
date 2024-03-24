import time
from wechat_ocr.ocr_manager import OcrManager, OCR_MAX_TASK_ID
import os

wechat_ocr_dir = "C:\\Users\\Administrator\\AppData\Roaming\\Tencent\\WeChat\\XPlugin\\Plugins\\WeChatOCR\\7061\\extracted\\WeChatOCR.exe"
wechat_dir = "C:\\Program Files\\Tencent\\WeChat\\[3.9.8.15]"
temp_text = ""

def ocr_result_callback(img_path: str, results: dict):
    global temp_text
    # 解析 OCR 结果
    ocr_results = results['ocrResult']
    for idx, result in enumerate(ocr_results, start=1):
        temp_text = str(temp_text) + result['text']
    print(temp_text)


def pic_to_text(pic_path):
    global temp_text
    if os.path.exists(pic_path) == False:
        print("微信图片OCR处理的图片文件")
        return
    ocr_manager = OcrManager(wechat_dir)
    # 设置WeChatOcr目录
    ocr_manager.SetExePath(wechat_ocr_dir)
    # 设置微信所在路径
    ocr_manager.SetUsrLibDir(wechat_dir)
    # 设置ocr识别结果的回调函数
    ocr_manager.SetOcrResultCallback(ocr_result_callback)
    # 启动ocr服务
    ocr_manager.StartWeChatOCR()
    # 开始识别图片
    ocr_manager.DoOCRTask(pic_path)
    # ocr_manager.DoOCRTask()
    time.sleep(1)
    while ocr_manager.m_task_id.qsize() != OCR_MAX_TASK_ID:
        pass
    # 识别输出结果
    ocr_manager.KillWeChatOCR()
    time.sleep(0.5)
    return temp_text
