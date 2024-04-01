import requests
from bs4 import BeautifulSoup
from PIL import Image
import OCR_PaddleOCRTools
from io import BytesIO
import os

def download_image(local_file_path, image_url):
    # 尝试下载图片
    try:
        # 发起GET请求
        response = requests.get(image_url)

        # 检查请求是否成功
        if response.status_code == 200:
            # 以二进制写入模式打开文件
            with open(local_file_path, 'wb') as file:
                # 将图片数据写入文件
                file.write(response.content)
            print(f"Image downloaded and saved to {local_file_path}")
            return "success"
        else:
            return(f"Failed to download image. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # 捕获请求异常，如网络问题、URL错误等
        return(f"An error occurred during the request: {e}")
    except IOError as e:
        # 捕获文件操作异常，如无法写入文件等
        return(f"An error occurred while handling files: {e}")
    except Exception as e:
        # 捕获其他所有未预料到的异常
        return(f"An unexpected error occurred: {e}")

def parse_WXPublic_webpage(url, temp_ocr_image_filepath):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取网页中的所有文字
    all_text = soup.get_text()
    all_image_text = ""
    # 查找网页中的所有图片标签
    images = soup.find_all('img')
    for image in images:
        # 检查图片的类名，如果包含特定类名，则跳过该图片
        if 'rich_pages' not in image.get('class', []):
            continue

        # 获取图片链接
        image_url = image.get('data-src') or image.get('src')  # 尝试获取 data-src 属性，如果为空则获取 src 属性
        if image_url:
            # 使用 OCR 识别图片中的文本
            if(download_image(temp_ocr_image_filepath,image_url) != 'success'):
                print(f"图片下载失败，跳过继续：{image_url}")
                continue
            if os.path.exists(temp_ocr_image_filepath) == False:
                print(f"本地文件未找到，跳过继续：{image_url}")
                continue

            image_text = OCR_PaddleOCRTools.PicToText_PaddleOCR(temp_ocr_image_filepath)
            if "##Error##" in image_text:
                print(f"OCR解析失败，跳过继续。原始图片链接：{image_url}")
                continue

            if (len(image_text) > 0):
                print(image_text)
                all_image_text = all_image_text + image_text

    if len(all_image_text) > 0:
        all_text = all_text + "######插图文字######" + all_image_text

    return all_text


if __name__ == "__main__":
    webpage_url = 'https://mp.weixin.qq.com/s?__biz=Mzg5NjY2NjQ4Mg==&mid=2247484629&idx=1&sn=eaef8ed0556042288d6c33f5601a11c1&chksm=c07cdac8f70b53de4bb48bf3abdf6534354f0b0b7604910fdbee76b2cad9c6b1ce2b6e388d42&token=935428064&lang=zh_CN#rd'  # 你要解析的网页链接
    parsed_text = parse_WXPublic_webpage(webpage_url,'E:\\111.jpg')
    print(parsed_text)
