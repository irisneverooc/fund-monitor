"""交易流水读取。"""

import csv
from typing import List

from models import Transaction

try:
    import pandas as pd
except ImportError:
    pd = None


ALLOWED_ACTIONS = {"buy", "sell"}


def _normalize_action(action: str) -> str:
    """把 action 统一为小写并校验。"""
    value = action.strip().lower()
    if value not in ALLOWED_ACTIONS:
        raise ValueError(f"不支持的 action: {action}")
    return value


def _load_with_pandas(csv_path: str) -> List[Transaction]:
    """使用 pandas 读取交易流水。"""
    df = pd.read_csv(csv_path, encoding="utf-8-sig", dtype={"code": str})
    txs: List[Transaction] = []

    for _, row in df.iterrows():
        txs.append(
            Transaction(
                date=str(row["date"]).strip(),
                code=str(row["code"]).zfill(6).strip(),
                action=_normalize_action(str(row["action"])),
                amount=float(row["amount"]),
                nav=float(row["nav"]),
                fee=float(row.get("fee", 0.0)),
            )
        )

    return txs


def _load_with_csv(csv_path: str) -> List[Transaction]:
    """使用内置 csv 读取交易流水。"""
    txs: List[Transaction] = []
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            txs.append(
                Transaction(
                    date=row["date"].strip(),
                    code=row["code"].strip().zfill(6),
                    action=_normalize_action(row["action"]),
                    amount=float(row["amount"]),
                    nav=float(row["nav"]),
                    fee=float(row.get("fee", 0.0)),
                )
            )

    return txs


def load_transactions(csv_path: str) -> List[Transaction]:
    """读取交易流水并按日期排序。"""
    txs = _load_with_pandas(csv_path) if pd is not None else _load_with_csv(csv_path)
    txs.sort(key=lambda x: (x.date, x.code))
    return txs
