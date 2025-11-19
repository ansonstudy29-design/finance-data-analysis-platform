import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.analysis.financial_visualizer import (
    create_candlestick_chart,
    create_volume_analysis,
    create_interactive_chart
)
from src.data.data_fetcher import get_stock_data


def main():
    """主函数：生成所有赛力斯(601127.SH)分析图表"""
    print("=" * 60)
    print("🚀 开始生成赛力斯(601127.SH)金融分析图表...")
    print("=" * 60)

    # 确保charts目录存在
    os.makedirs('charts', exist_ok=True)

    # 1. 获取赛力斯数据
    print("\n1. 🔍 获取赛力斯(601127.SH)股票数据...")
    stock_data = get_stock_data("stock_601127_2025.csv")

    if stock_data is None or stock_data.empty:
        print("❌ 无法获取赛力斯数据，程序终止")
        return

    # 2. 专业K线图
    print("\n2. 📈 生成专业K线图...")
    create_candlestick_chart(
        stock_data,
        title="赛力斯(601127.SH) 专业K线图",
        save_path="charts/sailisi_candlestick.png"
    )

    # 3. 成交量分析
    print("\n3. 📊 生成成交量分析图...")
    create_volume_analysis(
        stock_data,
        title="赛力斯(601127.SH) 成交量与价格关系分析",
        save_path="charts/sailisi_volume_analysis.png"
    )

    # 4. 价格波动率分析
    print("\n4. 📉 生成价格波动率分析图...")
    stock_data['daily_return'] = stock_data['close'].pct_change() * 100
    stock_data['volatility'] = stock_data['daily_return'].rolling(window=20).std()

    plt.figure(figsize=(14, 6))
    plt.plot(stock_data.index, stock_data['volatility'], 'purple', linewidth=2)
    plt.title('赛力斯(601127.SH) 价格波动率分析 (20日标准差)', fontsize=16, fontweight='bold')
    plt.ylabel('波动率 (%)', fontsize=12)
    plt.xlabel('日期', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.savefig('charts/sailisi_volatility.png', dpi=300, bbox_inches='tight')
    print("✅ 波动率分析图已保存至: charts/sailisi_volatility.png")

    # 5. 交互式图表
    print("\n5. 🌐 生成交互式图表...")
    create_interactive_chart(stock_data, "赛力斯(601127.SH) 交互式分析")

    # 6. 统计分布图
    print("\n6. 📐 生成日收益率分布图...")
    plt.figure(figsize=(12, 8))
    sns.histplot(stock_data['daily_return'].dropna(), kde=True, bins=50, color='skyblue')
    plt.title('赛力斯(601127.SH) 日收益率分布', fontsize=16, fontweight='bold')
    plt.xlabel('日收益率 (%)', fontsize=12)
    plt.ylabel('频数', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.savefig('charts/sailisi_return_distribution.png', dpi=300, bbox_inches='tight')
    print("✅ 收益率分布图已保存至: charts/sailisi_return_distribution.png")

    print("\n" + "=" * 60)
    print("✅✅✅ 所有6张专业图表已成功生成！")
    print("📁 图表保存位置: ./charts/")
    print("📊 今日任务完成: 赛力斯(601127.SH) 金融数据分析")
    print("=" * 60)


if __name__ == "__main__":
    main()