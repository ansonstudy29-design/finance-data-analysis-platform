"""
数据获取模块
职责：
1. 从Tushare获取股票历史数据
2. 从中国统计局API获取宏观经济数据
3. 提供统一的数据接口
"""

import tushare as ts
import pandas as pd
from config import TUSHARE_TOKEN


def get_stock_data(ts_code, start_date, end_date):
    """获取股票历史数据"""
    # 设置token
    ts.set_token(TUSHARE_TOKEN)
    pro = ts.pro_api()

    # 获取数据
    stock_data = pro.daily(
        ts_code=ts_code,
        start_date=start_date,
        end_date=end_date
    )

    return stock_data