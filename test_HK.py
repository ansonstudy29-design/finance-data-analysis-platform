import tushare as ts
import pandas as pd

# 1. 确保使用正确的代码格式
ts_code = "601127.SH"  # 注意：没有前导零

# 2. 设置您的token
ts.set_token("6fa199e5fba006bd9597b4bce16181cfae6bbef8cc38bd724d4f0beb")
pro = ts.pro_api()

try:
    # 3. 使用正确的日期格式，获取数据
    stock_data = pro.daily(
        ts_code=ts_code,
        start_date='20250101',  # 8位数字格式
        end_date='20251101'
    )

    # 检查是否获取到数据
    if stock_data.empty:
        print("⚠️ 仍然没有获取到数据，请尝试以下方法：")
        print("1. 检查您的Tushare账户级别（需普通用户以上）")
        print("2. 尝试获取A股数据测试：ts_code='000001.SZ'")
    else:
        print(f"✅ 成功获取 {len(stock_data)} 条数据")
        print("数据前5行信息：")
        print(stock_data.head())

        # 查看数据基本信息（行数、列数、数据类型等）
        print("\n数据基本信息：")
        stock_data.info()

        # 将数据保存为CSV文件
        csv_path = "stock_601127_2025.csv"
        stock_data.to_csv(csv_path, index=False)
        print(f"\n数据已保存至：{csv_path}")

except Exception as e:
    print(f"程序运行出错：{e}")