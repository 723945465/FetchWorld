import os.path
from ftplib import FTP
import OCR_PaddleOCRTools

# 设置FTP服务器的详细信息
ftp_host = '111.229.29.217'
ftp_user = 'ftpuser'
ftp_passwd = 'lhins-1wsdpang'

def download_file_from_dwh(temp_dwh_reletive_file_path, local_filepath):
    try:
        # 连接到FTP服务器
        ftp = FTP(ftp_host)
        ftp.encoding = "GB18030"
        ftp.timeout = 30
        ftp.login(ftp_user, ftp_passwd)
        # 从FTP下载文件
        with open(local_filepath, 'wb') as file:
            ftp.retrbinary('RETR ' + str(temp_dwh_reletive_file_path), file.write)
        if os.path.exists(local_filepath):
            if os.path.getsize(local_filepath) > 0:
                return 'success'

        return 'DWH文件下载失败：' + temp_dwh_reletive_file_path

    except Exception as e:
        print(f"Exception while download file from dwh: {e}")
        return f"Exception while download file from dwh: {e}"
    finally:
        # 关闭FTP连接
        ftp.quit()




if __name__ == '__main__':
    # print(download_file_from_dwh('1234.png','D:\\1.png'))
    print(OCR_PaddleOCRTools.PicToText_PaddleOCR('D:\\135.png'))




