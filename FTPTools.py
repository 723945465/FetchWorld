from ftplib import FTP
import OCR_PaddleOCRTools

# 设置FTP服务器的详细信息
ftp_host = '43.140.208.184'
ftp_user = 'ftpuser'
ftp_passwd = 'lhins-1wsdpang'

# 设置要下载的文件路径和保存的本地路径
# remote_file_path = '1.png'
local_file_path = 'E:\\11.png'

# 连接到FTP服务器
ftp = FTP(ftp_host)
ftp.encoding = "GB18030"
ftp.login(ftp_user, ftp_passwd)

file_list = ftp.nlst()

file_count = 0
# 打印文件列表
for remote_file_path in file_list:
    file_count = file_count +1
    if file_count <= 10:
        print(remote_file_path)
        # 从FTP下载文件
        with open(local_file_path, 'wb') as file:
            print(f"Downloading {remote_file_path}...")
            ftp.retrbinary('RETR 1.png', file.write)
        print(f"Downloaded {remote_file_path} successfully.")
        print(OCR_PaddleOCRTools.PicToText_PaddleOCR(local_file_path))





# 关闭FTP连接
ftp.quit()

