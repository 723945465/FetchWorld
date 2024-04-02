# -*- coding = utf-8 -*-
# @Time: 2024/3/28 20:45
# @Author: Chris
# @File: OCR_PaddleOCRTools.py
# @Software: PyCharm
# from paddleocr import PaddleOCR, draw_ocr
# from PIL import Image
#
# # 初始化PaddleOCR模型
# ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
#
# # 读取图片
# img_path = 'complex_example.jpg'
# image = Image.open(img_path)
#
# # 进行多语种文字识别
# result = ocr.ocr(img_path, cls=True)
#
# # 可视化识别结果
# image = draw_ocr(image, result, font_path='simfang.ttf')
# image.show()
#
# # 进行手写体文字识别
# handwriting_ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, det_model_dir='handwriting_det', rec_model_dir='handwriting_rec')
# result_handwriting = handwriting_ocr.ocr('handwriting_example.jpg', cls=True)
# image_handwriting = Image.open('handwriting_example.jpg')
# image_handwriting = draw_ocr(image_handwriting, result_handwriting, font_path='simfang.ttf')
# image_handwriting.show()


from paddleocr import PaddleOCR, draw_ocr
import re


# 把一堆string拼接起来，汉字之间没有空格，英文单词之间留一个空格，其他字符之间不留空格
def string_concat(strings):
    # 定义一个函数来检查字符是否为汉字
    def is_chinese_char(char):
        return '\u4e00' <= char <= '\u9fff'

    # 使用正则表达式来匹配英文单词之间的空格
    def replace_spaces(match):
        # 如果前后都是字母，则保留一个空格
        if match.group(1).isalpha() and match.group(2).isalpha():
            return ' '
        else:
            return ''

    # 将列表中的字符串连接成一个长字符串
    all_str = ''.join(strings)

    # 使用正则表达式替换掉不需要的空格
    # 保留汉字之间无空格，英文单词之间留一个空格
    result = re.sub(r'(\s)([a-zA-Z])', replace_spaces, all_str)
    result = re.sub(r'([a-zA-Z])(\s)', replace_spaces, result)

    return result

def PicToText_PaddleOCR(img_path):
    try:
        ocr = PaddleOCR(use_angle_cls=False, lang="ch")  # need to run only once to download and load model into memory
        str_list = []
        result = ocr.ocr(img_path, cls=True)
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                str_list.append(line[1][0])
        return string_concat(str_list)

    except Exception as e:
        return f"##Error## Exception while ocr file {img_path}:{e}"




if __name__ == '__main__':
    print(PicToText_PaddleOCR("C:\\1.jpg"))


