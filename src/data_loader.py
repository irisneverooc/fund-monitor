"""CSV 文件读取。

当前读取的 data/funds.csv 是模拟示例数据，
用于第一阶段框架验证，不代表真实持仓。
"""

import csv
from typing import List

from models import FundPosition

try:
    import pandas as pd
except ImportError:  # pandas 未安装时，使用内置 csv 兜底。
    pd = None


def _load_with_pandas(csv_path: str) -> List[FundPosition]:
    """使用 pandas 从 CSV 文件读取基金持仓列表。"""
    df = pd.read_csv(csv_path, encoding="utf-8-sig", dtype={"code": str})
    positions: List[FundPosition] = []

    for _, row in df.iterrows():
        position = FundPosition(
            code=str(row["code"]).zfill(6).strip(),
            name=str(row["name"]).strip(),
            fund_type=str(row["fund_type"]).strip(),
            units=float(row["units"]),
            cost_nav=float(row["cost_nav"]),
        )
        positions.append(position)

    return positions


def _load_with_csv(csv_path: str) -> List[FundPosition]:
    """使用内置 csv 模块读取基金持仓列表。"""
    positions: List[FundPosition] = []
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row["code"].strip().zfill(6)
            positions.append(
                FundPosition(
                    code=code,
                    name=row["name"].strip(),
                    fund_type=row["fund_type"].strip(),
                    units=float(row["units"]),
                    cost_nav=float(row["cost_nav"]),
                )
            )
    return positions


def load_positions(csv_path: str) -> List[FundPosition]:
    """读取基金持仓列表；优先使用 pandas。"""
    if pd is not None:
        return _load_with_pandas(csv_path)
    return _load_with_csv(csv_path)
