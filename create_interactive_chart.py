"""
交互式图表创建脚本
独立运行版本
"""

import sys
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_interactive_chart(stock_data, title="赛力斯(601127.SH) 交互式价格分析"):
    """创建交互式图表"""
    # 确保数据按日期排序
    stock_data = stock_data.sort_index()

    fig = go.Figure()

    # 添加价格线
    fig.add_trace(go.Scatter(
        x=stock_data.index,
        y=stock_data['close'],
        mode='lines+markers',
        name='收盘价',
        line=dict(color='blue', width=2),
        hovertemplate='价格: %{y:.2f}<br>日期: %{x}<extra></extra>'
    ))

    # 添加移动平均线
    stock_data['MA10'] = stock_data['close'].rolling(window=10).mean()
    fig.add_trace(go.Scatter(
        x=stock_data.index,
        y=stock_data['MA10'],
        mode='lines',
        name='10日均线',
        line=dict(color='red', width=1.5, dash='dash')
    ))

    # 设置布局
    fig.update_layout(
        title=title,
        xaxis_title='日期',
        yaxis_title='价格 (CNY)',
        hovermode='x unified',
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        height=600
    )

    # 保存为HTML
    os.makedirs('charts', exist_ok=True)
    html_path = "charts/sailisi_standalone_interactive.html"
    fig.write_html(html_path)
    print(f"✅ 交互式图表已保存至: {html_path}")

    return fig


if __name__ == "__main__":
    print("🚀 开始创建赛力斯(601127.SH)独立交互式图表...")

    # 创建charts目录
    os.makedirs('charts', exist_ok=True)

    # 尝试加载赛力斯数据
    try:
        stock_file = 'stock_601127_2025.csv'
        stock_data = pd.read_csv(stock_file, parse_dates=['trade_date'])
        stock_data = stock_data.sort_values('trade_date')
        stock_data.set_index('trade_date', inplace=True)
        print(f"✅ 成功加载赛力斯(601127.SH)数据，共 {len(stock_data)} 条记录")
    except Exception as e:
        print(f"❌ 加载数据失败: {str(e)}")
        print("💡 提示: 请确认文件 'stock_601127_2025.csv' 存在于项目根目录")
        # 创建模拟数据
        dates = pd.date_range(start='2024-01-01', end='2024-03-31', freq='B')
        stock_data = pd.DataFrame({
            'open': np.random.uniform(80, 120, len(dates)),
            'high': np.random.uniform(120, 140, len(dates)),
            'low': np.random.uniform(75, 115, len(dates)),
            'close': np.random.uniform(90, 130, len(dates)),
            'vol': np.random.randint(10000000, 50000000, len(dates))
        }, index=dates)
        stock_data.index.name = 'trade_date'
        print("⚠️ 使用模拟数据（未找到真实数据文件）")
        stock_data['close'] = stock_data['close'].cumsum() / stock_data['close'].sum() * 100

    # 创建图表
    create_interactive_chart(stock_data, "赛力斯(601127.SH) 交互式分析")