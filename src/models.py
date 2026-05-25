"""数据模型定义。"""

from dataclasses import dataclass


@dataclass
class FundMeta:
    """表示基金基础信息。"""

    code: str
    name: str
    fund_type: str


@dataclass
class FundPosition:
    """表示一条基金持仓记录。"""

    code: str
    name: str
    fund_type: str
    units: float
    cost_nav: float


@dataclass
class Transaction:
    """表示一条交易流水。"""

    date: str
    code: str
    action: str
    amount: float
    nav: float
    fee: float


@dataclass
class FundSnapshot:
    """表示某只基金在当前净值下的计算结果。"""

    code: str
    name: str
    fund_type: str
    units: float
    cost_nav: float
    nav_date: str
    previous_nav: float
    current_nav: float
    daily_change_rate: float
    market_value: float
    profit: float
    profit_rate: float
    weight: float
