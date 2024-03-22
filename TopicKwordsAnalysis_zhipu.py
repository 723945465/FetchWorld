# -*- coding = utf-8 -*-
# @Time: 2024/3/20 15:18
# @Author: Chris
# @File: TopicKwordsAnalysis_zhipu.py
# @Software: PyCharm
import re

# 定义量化交易关键词系统字典
quant_trading_keywords = {
    "量化交易策略": {
        "A级": [
            "量化", "量化交易", "算法", "算法交易", "阿尔法策略", "阿尔法", "阿尔法值", "阿尔法收益", "贝塔收益", "贝塔",
            "Beta", "Beta值", "Beta收益", "超额收益", "超额回报", "择时策略", "择时", "配置策略", "资产配置", "资产配置策略",
            "策略优化", "优化", "优化策略", "模型优化", "机器学习", "算法交易", "DMA策略", "DMA", "DMA交易", "动态市场分析",
            "高频交易", "高频", "高频策略", "对冲策略", "量化对冲", "多空策略", "股票多空", "CTA", "CTA策略", "跨品种套利",
            "事件驱动", "事件驱动策略", "统计套利", "统计学", "统计学策略", "风格投资", "风格因子", "量化选股", "基本面选股",
            "量化择时", "基本面", "基本面分析", "深度强化学习交易", "蒙特卡罗模拟", "神经网络模型", "生成对抗网络"
        ],
        "B级": [
            "指数增强", "动量策略", "均值回复", "均值回复策略", "价值投资", "价值投资策略", "基本面量化", "基本面量化策略",
            "技术分析策略", "市场中性", "市场中性策略", "趋向跟踪", "趋向跟踪策略", "投机策略", "指数化投资", "进化算法优化", "张量计算"
        ],
        "C级": [
            "期现套利", "商品期货", "商品期货策略", "管理期货", "管理期货策略", "做市", "做市策略", "指数跟踪", "现金增强"
        ]
    },
    "交易成本及风险管理": {
        "A级": [
            "换手率", "Turnover", "Turnover Rate", "调仓策略", "重仓", "重仓策略", "回撤管理", "Drawdown管理", "风险管理",
            "Risk Management", "波动率", "Volatility", "资金成本", "Funding Costs", "市场冲击", "市场冲击成本", "Market Impact",
            "交易成本", "Trading Costs", "风险偏好", "Risk Preference"
        ],
        "B级": [
            "成交量", "流动性", "冲击成本", "杠杆", "杠杆比例", "最大回撤", "Drawdown", "夏普比率", "风险收益比", "Turnover"
        ],
        "C级": [
            "波动率曲面", "隐含波动率", "Delta", "Delta值", "Gamma", "Gamma值", "Vega", "Vega值"
        ]
    },
    "投资组合及资产管理": {
        "A级": [
            "投资组合", "Portfolio", "资产配置", "Asset Allocation", "投资回报", "Investment Return", "收益优化", "Profit Optimization",
            "申购", "申购费", "认购", "认购费", "Subscription Fee", "赎回", "赎回费", "Redemption Fee", "大宗交易", "大资金交易",
            "微盘股", "微盘股票", "数字货币对冲基金", "CTA"
        ],
        "B级": [
            "多空组合", "行业轮动", "风险平价", "风险平价策略", "证券组合优化", "均值方差模型", "主动投资", "被动投资"
        ],
        "C级": [
            "另类投资", "结构化产品", "期权投资组合", "私募基金"
        ]
    },
    "市场行情及数据分析": {
        "A级": [
            "市场回报", "市场收益率", "Market Return", "市场效率", "有效市场", "Market Efficiency", "市场趋势", "Trend", "基本面分析",
            "基本面", "Fundamental Analysis", "技术面分析", "技术分析", "Technical Analysis", "资金流向", "Capital Flow", "投资者情绪",
            "Sentiment", "模型回测", "Strategy Backtesting", "参数优化", "Parameter Optimization", "策略绩效评估", "Strategy Performance Evaluation",
            "数据挖掘", "Data Mining", "信号处理", "Signal Processing", "人工智能", "机器学习", "深度学习", "强化学习", "数据科学",            "大数据", "自然语言处理", "计算机视觉", "图像识别"
        ],
        "B级": [
            "技术指标", "K线形态", "均线系统", "波浪理论", "能量潮理论", "分型分析", "分型理论", "压力支撑位", "突破形态", "SAR",
            "SAR指标"
        ],
        "C级": [
            "ATR指标", "ATR", "VR指标", "VR", "DMI指标", "DMI", "CCI指标", "CCI", "KDJ指标", "KDJ", "VSTOP指标", "VSTOP", "BOLL指标",
            "BOLL", "RSI指标", "RSI"
        ]
    },
    "专业术语及行业用语": {
        "A级": [
            "胜率", "大数定律", "索提诺比率", "市值", "市盈率", "贝塔系数", "阿尔法系数", "投资效率", "行业资金流向", "波动率曲面",
            "隐含波动率", "风险值", "希腊值", "套利定价", "有效市场假说", "期权", "期货", "互换", "股指期货", "商品", "外汇", "区块链",
            "数字货币", "加密资产", "ICO", "STO", "钱包", "去中心化", "Token", "挖矿", "智能合约", "预言机", "DeFi", "NFT"
        ],
        "B级": [
            "行为经济学", "心理账户", "获得偏好", "损失厌恶", "从众心理", "羊群效应", "过度自信", "框架效应", "交易员", "研究员", "工程师",
            "策略师", "执行系统", "订单管理系统", "云端计算", "高性能计算"
        ],
        "行业用语": [
            "赢率", "大数法则", "索提诺比率", "市值", "PE", "Beta值", "Alpha值", "资金流", "波率曲面", "IV", "VAR", "希腊值", "无风险套利",
            "市场有效"
        ]
    },
    "关键词统计": {
        "A级高密切关键词": 196,
        "B级次密切关键词": 84,
        "C级低关联关键词": 44,
        "合计关键词": 324
    }
}



# 关键词匹配函数
def match_keywords(article, keywords):
    matches = {}
    for keyword in keywords:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        match_count = len(re.findall(pattern, article, re.IGNORECASE))
        if match_count > 0:
            matches[keyword] = match_count
    return matches


# 匹配度排序函数
def sort_by_match_count(matches):
    sorted_matches = sorted(matches.items(), key=lambda x: x[1], reverse=True)
    return sorted_matches


# 量化交易主题匹配度计算函数
def calculate_theme_match(article, theme_keywords):
    total_theme_keywords = len(theme_keywords)
    matched_theme_keywords = match_keywords(article, theme_keywords)
    matched_count = sum(matched_theme_keywords.values())
    match_percentage = (matched_count / total_theme_keywords) * 100 if total_theme_keywords > 0 else 0
    return match_percentage


# 文章主要观点推测函数
def infer_main_points(sorted_matches):
    top_keywords = [keyword for keyword, _ in sorted_matches[:5]]
    return '，'.join(top_keywords)


# 分析文章函数
def analyze_article(article, keywords_system):
    all_keywords = []
    for category in keywords_system.values():
        for level in category.values():
            all_keywords.extend(level)

    # 关键词匹配
    all_matches = match_keywords(article, all_keywords)

    # 匹配度排序
    sorted_matches = sort_by_match_count(all_matches)

    # 量化交易主题匹配度
    quant_trading_keywords = [keyword for keyword in all_keywords if keyword in quant_trading_keywords]
    theme_match = calculate_theme_match(article, quant_trading_keywords)

    # 文章主要观点推测
    main_points = infer_main_points(sorted_matches)

    return {
        'sorted_matches': sorted_matches,
        'theme_match': theme_match,
        'main_points': main_points
    }


# 示例文章
article_example = "量化交易是一种利用数学模型和算法来分析金融市场并执行交易的策略。它包括多种策略，如阿尔法策略、择时策略和统计套利。"

# 调用函数进行分析
analysis_result = analyze_article(article_example, quant_trading_keywords)
print(analysis_result)
