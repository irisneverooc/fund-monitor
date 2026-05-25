"""数据模型定义。"""

from dataclasses import dataclass


@dataclass
class FundPosition:
    """表示一条基金持仓记录。"""

    code: str
    name: str
    fund_type: str
    units: float
    cost_nav: float


@dataclass
class FundSnapshot:
    """表示某只基金在当前净值下的计算结果。"""

    code: str
    name: str
    fund_type: str
    units: float
    cost_nav: float
    current_nav: float
    market_value: float
    profit: float
    profit_rate: float
    weight: float
