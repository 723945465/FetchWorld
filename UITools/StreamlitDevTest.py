import streamlit as st
import mysql.connector
import pandas as pd
from io import BytesIO
import json


db_host= '114.55.128.212'
db_databasename= 'fetchtheworld'
db_user= 'chris'
db_password= '19871127ldld'
charset='utf8mb4'

# **连接 MySQL**
def get_connection():
    return mysql.connector.connect(host=db_host, database=db_databasename, user=db_user, password=db_password, charset = charset)

# **查询数据库**
def fetch_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # 返回字典格式数据
    query = """
        SELECT id, create_time , info_author_name , info_type ,info_content , info_internet_address  FROM hismsg_info 
        where  (info_bad_for_analysis != 'bad' OR info_bad_for_analysis IS NULL) 
        and info_match_topic LIKE '%Lidar%'
        LIMIT 15
        """

    cursor.execute(query)  # 修改为你的表名
    data = cursor.fetchall()
    conn.close()
    print(pd.DataFrame(data))
    return pd.DataFrame(data)

# **转换数据为 Excel**
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
    output.seek(0)
    return output

# **页面标题**
st.title("MySQL 数据查询 & Excel 导出")

# **获取数据**
df = fetch_data()

# 显示表格
st.write("### SQL 表格数据：")
st.dataframe(df)

# 将 DataFrame 转换为 JSON
json_data = df.to_json(
    orient="records",
    indent=4,
    index=False,
    force_ascii=False,
    date_format='iso'
)

def create_download_link(json_data):
    # 使用 utf-8 编码确保中文正常显示
    json_str = json.dumps(json_data, ensure_ascii=False, indent=4)
    return json_str

# 提供下载功能
st.write("### 下载 JSON 文件")
json_str = create_download_link(json_data)
st.download_button(
    label="下载 JSON (.json)",
    data=json_str.encode('utf-8'),  # 编码为 UTF-8
    file_name="data.txt",  # 建议使用 .json 扩展名
    mime="application/json"  # 使用正确的 MIME 类型
)
