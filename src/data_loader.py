"""基金基础信息读取。"""

import csv
from typing import List

from models import FundMeta

try:
    import pandas as pd
except ImportError:
    pd = None


def _load_with_pandas(csv_path: str) -> List[FundMeta]:
    """使用 pandas 读取基金基础信息。"""
    df = pd.read_csv(csv_path, encoding="utf-8-sig", dtype={"code": str})
    funds: List[FundMeta] = []

    for _, row in df.iterrows():
        funds.append(
            FundMeta(
                code=str(row["code"]).zfill(6).strip(),
                name=str(row["name"]).strip(),
                fund_type=str(row["fund_type"]).strip(),
            )
        )

    return funds


def _load_with_csv(csv_path: str) -> List[FundMeta]:
    """使用内置 csv 读取基金基础信息。"""
    funds: List[FundMeta] = []
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            funds.append(
                FundMeta(
                    code=row["code"].strip().zfill(6),
                    name=row["name"].strip(),
                    fund_type=row["fund_type"].strip(),
                )
            )

    return funds


def load_funds(csv_path: str) -> List[FundMeta]:
    """读取基金基础信息。"""
    if pd is not None:
        return _load_with_pandas(csv_path)
    return _load_with_csv(csv_path)
