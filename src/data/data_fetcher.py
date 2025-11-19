"""
数据获取模块
职责：
1. 从本地文件加载赛力斯股票数据
2. 为可视化模块提供统一数据接口
"""

import pandas as pd
import os

def get_stock_data(stock_file="stock_601127_2025.csv"):
    """获取赛力斯股票历史数据"""
    # 确保数据目录存在
    os.makedirs('data', exist_ok=True)

    try:
        # 读取赛力斯数据
        file_path = os.path.join(os.getcwd(), stock_file)
        print(f"🔍 正在加载数据文件: {file_path}")

        # 加载数据，确保日期列为datetime类型
        stock_data = pd.read_csv(file_path, parse_dates=['trade_date'])

        # 按日期排序并设置索引
        stock_data = stock_data.sort_values('trade_date')
        stock_data.set_index('trade_date', inplace=True)

        # 重命名列以确保与可视化模块兼容
        if 'close_price' in stock_data.columns and 'close' not in stock_data.columns:
            stock_data.rename(columns={'close_price': 'close'}, inplace=True)
        if 'volume' in stock_data.columns and 'vol' not in stock_data.columns:
            stock_data.rename(columns={'volume': 'vol'}, inplace=True)

        print(f"✅ 成功加载 {len(stock_data)} 条赛力斯(601127.SH)数据")
        print(f"📊 数据日期范围: {stock_data.index.min().strftime('%Y-%m-%d')} 至 {stock_data.index.max().strftime('%Y-%m-%d')}")

        return stock_data

    except Exception as e:
        print(f"❌ 加载数据失败: {str(e)}")
        print("💡 提示: 请确认文件 'stock_601127_2025.csv' 存在于项目根目录")
        return None