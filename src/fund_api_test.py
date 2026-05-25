"""AkShare 基金接口测试脚本。

说明：
- 该脚本仅用于验证 AkShare 是否可按 data/funds.csv 的基金代码获取真实净值数据。
- 该脚本不会影响主程序，也不会接入当前日报生成流程。
"""

import csv
from pathlib import Path
from typing import List, Tuple

import akshare as ak


def load_funds(csv_path: str = "data/funds.csv") -> List[Tuple[str, str]]:
    """从 CSV 读取基金代码和基金名称。"""
    funds: List[Tuple[str, str]] = []
    file_path = Path(csv_path)

    with file_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row.get("code", "").strip()
            name = row.get("name", "").strip()
            if code:
                funds.append((code, name))

    return funds


def fetch_latest_nav(code: str) -> dict:
    """调用 AkShare 获取单只基金最新净值信息。"""
    df = ak.fund_open_fund_info_em(symbol=code, indicator="单位净值走势")

    if df is None or df.empty:
        raise ValueError("返回为空，可能代码不存在或接口暂时不可用")

    latest = df.iloc[-1]

    # 不同版本字段可能有差异，这里做兼容。
    nav_date = latest.get("净值日期", latest.get("x", "未知"))
    latest_nav = latest.get("单位净值", latest.get("y", "未知"))
    daily_change_rate = latest.get("日增长率", "未知")
    subscribe_status = latest.get("申购状态", "未知")
    redeem_status = latest.get("赎回状态", "未知")

    return {
        "nav_date": nav_date,
        "latest_nav": latest_nav,
        "daily_change_rate": daily_change_rate,
        "subscribe_status": subscribe_status,
        "redeem_status": redeem_status,
    }


def main() -> None:
    """执行基金接口测试。"""
    funds = load_funds()
    if not funds:
        print("未在 data/funds.csv 中读取到基金代码，请先检查文件内容。")
        return

    print("开始测试 AkShare 基金净值接口...\n")

    for code, name in funds:
        try:
            result = fetch_latest_nav(code)
            print(f"基金代码: {code}")
            print(f"基金名称: {name}")
            print(f"净值日期: {result['nav_date']}")
            print(f"最新净值: {result['latest_nav']}")
            print(f"日增长率: {result['daily_change_rate']}")
            print(f"申购状态: {result['subscribe_status']}")
            print(f"赎回状态: {result['redeem_status']}")
            print("-" * 60)
        except Exception as e:
            print(f"基金代码: {code}")
            print(f"基金名称: {name}")
            print(f"接口获取失败: {e}")
            print("提示: 请检查网络、基金代码或 AkShare 接口可用性。")
            print("-" * 60)


if __name__ == "__main__":
    main()
