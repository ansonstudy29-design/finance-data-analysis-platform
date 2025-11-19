import baostock as bs
import pandas as pd

# 1. 登录baostock系统
lg = bs.login()
print(f"登录状态：错误码{lg.error_code}，错误信息{lg.error_msg}")

# 2. 下载数据（以上证50成分股为例，可替换为目标股票代码）
stock_codes = ["sh.600000", "sh.600036", "sz.000001"]  # 示例股票代码，格式为“交易所.股票代码”
start_date = "2025-01-01"
end_date = "2025-10-31"

# 定义要获取的字段（可根据需求调整）
fields = "date,code,open,high,low,close,volume,amount,adjustflag"

data_list = []
for code in stock_codes:
    # 查询历史K线数据
    rs = bs.query_history_k_data_plus(
        code=code,
        fields=fields,
        start_date=start_date,
        end_date=end_date,
        frequency="d",  # 日线数据，可改为“w”（周线）、“m”（月线）或“5”（5分钟线）等
        adjustflag="2"  # 2=前复权，1=后复权，3=不复权
    )
    while rs.error_code == '0' and rs.next():
        data_list.append(rs.get_row_data())

# 3. 转换为DataFrame并整理格式
df = pd.DataFrame(data_list, columns=rs.fields)
# 转换数值类型（根据字段需求调整）
df[["open", "high", "low", "close", "volume", "amount"]] = df[["open", "high", "low", "close", "volume", "amount"]].astype(float)
df["date"] = pd.to_datetime(df["date"])  # 转换日期格式

# 4. 保存或输出结果
print("转换后的数据示例：")
print(df.head())
# 保存为CSV（可选）
# df.to_csv("baostock_data.csv", index=False)

# 5. 登出系统
bs.logout()