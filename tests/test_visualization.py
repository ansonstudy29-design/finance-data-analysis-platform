import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from src.analysis.financial_visualizer import (
    create_candlestick_chart,
    create_volume_analysis,
    create_interactive_chart
)


def test_visualizations():
    """测试所有可视化功能"""
    print("🚀 开始测试赛力斯(601127.SH)可视化功能...")

    # 创建测试目录
    os.makedirs('charts', exist_ok=True)

    # 加载赛力斯数据
    try:
        stock_file = 'stock_601127_2025.csv'
        stock_data = pd.read_csv(stock_file, parse_dates=['trade_date'])
        stock_data = stock_data.sort_values('trade_date')
        stock_data.set_index('trade_date', inplace=True)
        print(f"✅ 成功加载赛力斯(601127.SH)数据，共 {len(stock_data)} 条记录")
    except Exception as e:
        print(f"❌ 加载数据失败: {str(e)}")
        print("💡 提示: 请确认文件 'stock_601127_2025.csv' 存在于项目根目录")
        return

    # 1. 测试K线图
    create_candlestick_chart(
        stock_data,
        title="赛力斯(601127.SH) K线图测试",
        save_path="charts/sailisi_test_candlestick.png"
    )

    # 2. 测试成交量分析
    create_volume_analysis(
        stock_data,
        title="赛力斯(601127.SH) 成交量分析测试",
        save_path="charts/sailisi_test_volume_analysis.png"
    )

    # 3. 测试交互式图表
    create_interactive_chart(stock_data, "赛力斯(601127.SH) 交互式分析测试")

    print("✅✅✅ 所有可视化测试完成！")
    print("📊 生成的图表已保存至 ./charts/ 目录")


if __name__ == "__main__":
    test_visualizations()