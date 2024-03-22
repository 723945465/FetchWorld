from collections import Counter


def calculate_matching(article, keyword_system):
    keyword_counter = Counter()

    # 遍历关键词系统中的每个关键词
    for keyword in keyword_system:
        # 检查关键词是否出现在文章中
        if keyword in article:
            # 如果是，则计数加一
            keyword_counter[keyword] += 1

    # 输出匹配结果并按匹配度排序
    matching_result = keyword_counter.most_common(5)

    # 计算文章与量化交易主题的匹配度
    total_words = len(article)
    matching_words = sum(keyword_counter.values())
    matching_percentage = (matching_words / total_words) * 100

    # 输出文章的主要观点
    main_points = [word for word, _ in matching_result if word in keyword_system[:196]]

    return matching_result, matching_percentage, main_points


# 测试用例
keyword_system = [
    '量化', '量化交易', '算法', '算法交易', '阿尔法策略', '阿尔法', '阿尔法值', '阿尔法收益', '贝塔收益', '贝塔',
    'Beta', 'Beta值', 'Beta收益', '超额收益', '超额回报', '择时策略', '择时', '配置策略', '资产配置', '资产配置策略',
    '策略优化', '优化', '优化策略', '模型优化', '机器学习', '算法交易', 'DMA策略', 'DMA', 'DMA交易', '动态市场分析',
    '高频交易', '高频', '高频策略', '对冲策略', '量化对冲', '多空策略', '股票多空', 'CTA', 'CTA策略', '跨品种套利',
    '事件驱动', '事件驱动策略', '统计套利', '统计学', '统计学策略', '风格投资', '风格因子', '量化选股', '基本面选股',
    '量化择时', '基本面', '基本面分析', '深度强化学习交易', '蒙特卡罗模拟', '神经网络模型', '生成对抗网络',
    '指数增强', '动量策略', '均值回复', '均值回复策略', '价值投资', '价值投资策略', '基本面量化', '基本面量化策略',
    '技术分析策略', '市场中性', '市场中性策略', '趋向跟踪', '趋向跟踪策略', '投机策略', '指数化投资', '进化算法优化',
    '张量计算',
    '期现套利', '商品期货', '商品期货策略', '管理期货', '管理期货策略', '做市', '做市策略', '指数跟踪', '现金增强',
    '换手率', 'Turnover', 'Turnover Rate', '调仓策略', '重仓', '重仓策略', '回撤管理', 'Drawdown管理', '风险管理',
    'Risk Management', '波动率', 'Volatility', '资金成本', 'Funding Costs', '市场冲击', '市场冲击成本', 'Market Impact',
    '交易成本', 'Trading Costs', '风险偏好', 'Risk Preference',
    '成交量', '流动性', '冲击成本', '杠杆', '杠杆比例', '最大回撤', 'Drawdown', '夏普比率', '风险收益比', 'Turnover',
    '波动率曲面', '隐含波动率', 'Delta', 'Delta值', 'Gamma', 'Gamma值', 'Vega', 'Vega值',
    '投资组合', 'Portfolio', '资产配置', 'Asset Allocation', '投资回报', 'Investment Return', '收益优化',
    'Profit Optimization', '申购', '申购费', '认购', '认购费', 'Subscription Fee', '赎回', '赎回费', 'Redemption Fee',
    '大宗交易', '大资金交易', '微盘股', '微盘股票', '数字货币对冲基金', 'CTA',
    '多空组合', '行业轮动', '风险平价', '风险平价策略', '证券组合优化', '均值方差模型', '主动投资', '被动投资',
    '另类投资', '结构化产品', '期权投资组合', '私募基金',
    '市场回报', '市场收益率', 'Market Return', '市场效率', '有效市场', 'Market Efficiency', '市场趋势', 'Trend',
    '基本面分析', '基本面', 'Fundamental Analysis', '技术面分析', '技术分析', 'Technical Analysis', '资金流向',
    'Capital Flow', '投资者情绪', 'Sentiment', '模型回测', 'Strategy Backtesting', '参数优化', 'Parameter Optimization',
    '策略绩效评估', 'Strategy Performance Evaluation', '数据挖掘', 'Data Mining', '信号处理', 'Signal Processing',
    '人工智能', '机器学习', '深度学习', '强化学习', '数据科学', '大数据', '自然语言处理', '计算机视觉', '图像识别',
    '技术指标', 'K线# 线形态、均线系统、波浪理论、能量潮理论、分型分析、分型理论、压力支撑位、突破形态、SAR、SAR指标',
    'ATR指标', 'ATR', 'VR指标', 'VR', 'DMI指标', 'DMI', 'CCI指标', 'CCI', 'KDJ指标', 'KDJ', 'VSTOP指标', 'VSTOP', 'BOLL指标', 'BOLL', 'RSI指标', 'RSI',
    '胜率', '大数定律', '索提诺比率', '市值', '市盈率', '贝塔系数', '阿尔法系数', '投资效率', '行业资金流向', '波动率曲面', '隐含波动率', '风险值', '希腊值', '套利定价', '有效市场假说', '期权', '期货', '互换', '股指期货', '商品', '外汇', '区块链', '数字货币', '加密资产', 'ICO', 'STO', '钱包', '去中心化', 'Token', '挖矿', '智能合约', '预言机', 'DeFi', 'NFT',
    '行为经济学', '心理账户', '获得偏好', '损失厌恶', '从众心理', '羊群效应', '过度自信', '框架效应', '交易员', '研究员', '工程师', '策略师', '执行系统', '订单管理系统', '云端计算', '高性能计算',
    '赢率', '大数法则', '索提诺比率', '市值', 'PE', 'Beta值', 'Alpha值', '资金流', '波率曲面', 'IV', 'VAR', '希腊值', '无风险套利', '市场有效'
]

# 定义一个简单的测试文章
test_article = "量化交易是一种利用数学模型和计算机算力进行交易决策的方法。它涉及算法交易、机器学习、高频交易等技术。量化交易的目标是通过对市场数据进行分析，发现交易机会并进行有效的交易。"

# 调用函数计算匹配情况
matching_result, matching_percentage, main_points = calculate_matching(test_article, keyword_system)

# 输出匹配结果
print("匹配结果:")
for word, count in matching_result:
    print(f"{word}: {count}")

# 输出匹配度
print("\n文章与量化交易主题的匹配度:", matching_percentage)

# 输出主要观点
print("\n文章的主要观点:", main_points)

