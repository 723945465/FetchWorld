import easyocr

# 创建EasyOCR对象，使用英语和中文
reader = easyocr.Reader(['en', 'zh'])

# 读取图像并识别文本
result = reader.readtext('E:\\1.jpg')

# 打印结果
for detection in result:
    text = detection[1]
    print(text)
