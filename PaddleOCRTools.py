# -*- coding = utf-8 -*-
# @Time: 2024/3/28 20:45
# @Author: Chris
# @File: PaddleOCRTools.py
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

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=False, lang="ch")  # need to run only once to download and load model into memory
img_path = 'E:\\1.jpg'
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)
img_path = 'E:\\2.jpg'
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)
img_path = 'E:\\3.jpg'
result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)

# # 显示结果
# from PIL import Image
# result = result[0]
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')
