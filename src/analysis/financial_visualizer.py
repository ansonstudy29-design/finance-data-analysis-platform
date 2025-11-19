"""
金融数据可视化模块
职责：
1. 生成专业K线图
2. 创建技术指标可视化
3. 生成交互式分析报告
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime


def create_candlestick_chart(stock_data, title="赛力斯(601127.SH) K线图", save_path=None):
    """
    创建专业K线图
    参数:
        stock_data: pandas DataFrame，包含OHLC数据
        title: 图表标题
        save_path: 保存路径（可选）
    """
    # 确保数据按日期排序
    stock_data = stock_data.sort_index()

    # 设置全局样式
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("deep")

    # 创建图表
    fig, ax = plt.subplots(figsize=(14, 8))

    # 将索引转换为数值以便绘图
    stock_data = stock_data.reset_index()
    stock_data['numeric_index'] = range(len(stock_data))

    # 确保必需的列存在
    required_columns = ['open', 'high', 'low', 'close']
    for col in required_columns:
        if col not in stock_data.columns:
            print(f"⚠️ 警告: 缺少 '{col}' 列，使用替代列")
            if col == 'open' and 'opening_price' in stock_data.columns:
                stock_data['open'] = stock_data['opening_price']
            elif col == 'close' and 'close_price' in stock_data.columns:
                stock_data['close'] = stock_data['close_price']
            elif col == 'high' and 'highest_price' in stock_data.columns:
                stock_data['high'] = stock_data['highest_price']
            elif col == 'low' and 'lowest_price' in stock_data.columns:
                stock_data['low'] = stock_data['lowest_price']

    # 计算上涨/下跌
    stock_data['color'] = stock_data['close'].pct_change().apply(
        lambda x: 'green' if x > 0 else 'red'
    )

    # 绘制K线
    width = 0.6  # 蜡烛宽度
    for i, row in stock_data.iterrows():
        # 确保有所有必需的数据
        if pd.isna(row['open']) or pd.isna(row['high']) or pd.isna(row['low']) or pd.isna(row['close']):
            continue

        # 绘制实体
        height = row['close'] - row['open']
        bottom = min(row['open'], row['close'])
        ax.bar(i, height, width, bottom=bottom,
               color=row['color'], edgecolor=row['color'])
        # 绘制影线
        ax.plot([i, i], [row['low'], row['high']], color=row['color'], linewidth=1)

    # 添加移动平均线
    stock_data['MA5'] = stock_data['close'].rolling(window=5).mean()
    stock_data['MA20'] = stock_data['close'].rolling(window=20).mean()

    ax.plot(stock_data['numeric_index'], stock_data['MA5'], 'b-', label='5日均线', linewidth=1.5)
    ax.plot(stock_data['numeric_index'], stock_data['MA20'], 'r-', label='20日均线', linewidth=1.5)

    # 设置x轴刻度
    tick_positions = np.linspace(0, len(stock_data) - 1, 10, dtype=int)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(stock_data.iloc[tick_positions]['trade_date'].dt.strftime('%Y-%m-%d'), rotation=45)

    # 设置标题和标签
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_ylabel('价格 (CNY)', fontsize=12)
    ax.set_xlabel('日期', fontsize=12)
    ax.legend()

    plt.tight_layout()

    # 保存或显示
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ K线图已保存至: {save_path}")
    else:
        plt.show()

    plt.close()
    return fig


def create_volume_analysis(stock_data, title="赛力斯(601127.SH) 成交量分析", save_path=None):
    """创建成交量与价格关系分析图"""
    # 确保数据按日期排序
    stock_data = stock_data.sort_index()
    stock_data = stock_data.reset_index()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10),
                                   gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

    # 价格图表
    ax1.plot(range(len(stock_data)), stock_data['close'], 'b-', linewidth=2, label='收盘价')
    ax1.set_title(title, fontsize=16, fontweight='bold')
    ax1.set_ylabel('价格 (CNY)', fontsize=12)
    ax1.legend()

    # 成交量图表
    colors = stock_data['close'].pct_change().apply(lambda x: 'green' if x > 0 else 'red')
    ax2.bar(range(len(stock_data)), stock_data['vol'], color=colors, alpha=0.7)
    ax2.set_ylabel('成交量', fontsize=12)
    ax2.set_xlabel('日期', fontsize=12)

    # 添加平均成交量线
    avg_vol = stock_data['vol'].mean()
    ax2.axhline(y=avg_vol, color='r', linestyle='--', alpha=0.7, label=f'平均成交量: {avg_vol:,.0f}')
    ax2.legend()

    # 设置x轴刻度
    tick_positions = np.linspace(0, len(stock_data) - 1, 10, dtype=int)
    ax2.set_xticks(tick_positions)
    ax2.set_xticklabels(stock_data.iloc[tick_positions]['trade_date'].dt.strftime('%Y-%m-%d'), rotation=45)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ 成交量分析图已保存至: {save_path}")

    plt.close()
    return fig


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
    html_path = "charts/interactive_analysis.html"
    fig.write_html(html_path)
    print(f"✅ 交互式图表已保存至: {html_path}")

    return fig