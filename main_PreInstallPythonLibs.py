# -*- coding = utf-8 -*-
# @Time: 2024/4/1 10:56
# @Author: Chris
# @File: main_PreInstallPythonLibs.py
# @Software: PyCharm
import os

required_libraries = [
    'schedule',#定时调度
    'wxauto', #微信消息提取
    'pyreadline3', #MiniMax需要
    'jieba', #分词
    'stylecloud', 'wordcloud', #词云
    'imageio',
    'openai', #调用Kimi
    'emoji', #表情包字符
    'ftplib', #FTP
    'mysql-connector-python==9.0.0', 'pymysql', #mysql
    'flask', #flask WebApi
    'numpy', 'pandas', 'matplotlib', 'seaborn',  # 数据处理和可视化
    'beautifulsoup4', 'requests', 'selenium',  # 网络数据获取和处理
    'streamlit','xlsxwriter',
    # 'scipy', 'statsmodels', 'scikit-learn', 'xgboost', 'lightgbm',  # 数据分析和机器学习
    # 'tensorflow', 'keras', 'pytorch', 'fastai',  # 深度学习框架
    # 'jupyter', 'spyder', 'vscode',  # 开发环境
    # 'sqlalchemy', 'pymysql', 'psycopg2', 'sqlite',  # 数据库连接和操作
    # 'openpyxl', 'xlrd', 'xlwt', 'pandasql',  # Excel 和 SQL 数据操作
    # 'pyodbc', 'pandas-profiling', 'missingno',  # 数据质量分析和处理
    # 'plotly', 'dash', 'cufflinks',  # 交互式数据可视化
    # 'geopandas', 'folium',  # 地理数据分析和可视化
    # 'nltk', 'spaCy', 'gensim',  # 文本处理和自然语言处理
    # 'networkx', 'igraph',  # 图论和网络分析
    # 'statspy', 'pingouin',  # 统计分析
    # 'pandasgui', 'dtale',  # 数据分析 GUI 工具
    # 'auto_ml', 'tpot',  # 自动化机器学习
    # 'vaex', 'dask',  # 大数据集处理
    # 'yellowbrick', 'shap',  # 可视化模型解释
    # 'sympy', 'quantstats',  # 数学和金融分析
    # 'tabulate', 'pandas-flavor',  # 数据转换和操作
    # 'arrow', 'zope.interface',  # 日期和时间处理
    # 'cryptography', 'paramiko',  # 加密和远程连接
]

for i in required_libraries:
    code = f"pip install {i} -i https://pypi.tuna.tsinghua.edu.cn/simple"   # 可根据自己需求自行变更本行代码，本质就是cmd中输入的内容
    os.system('cmd /c "{}"'.format(code))
    print('\n')
    print(f'==================================')
    print(f'============{i}已经安装============')
    print(f'==================================')
    print('\n')

