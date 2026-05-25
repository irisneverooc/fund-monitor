"""收益计算与配置分析逻辑。"""

from typing import Dict, List

from models import FundPosition, FundSnapshot
from mock_nav_provider import get_mock_nav


def build_snapshots(positions: List[FundPosition]) -> List[FundSnapshot]:
    """把持仓列表转换为含收益信息的快照列表。"""
    snapshots: List[FundSnapshot] = []
    total_market_value = 0.0

    for position in positions:
        current_nav = get_mock_nav(position.code)
        cost_value = position.units * position.cost_nav
        market_value = position.units * current_nav
        profit = market_value - cost_value
        profit_rate = (profit / cost_value) if cost_value else 0.0

        snapshot = FundSnapshot(
            code=position.code,
            name=position.name,
            fund_type=position.fund_type,
            units=position.units,
            cost_nav=position.cost_nav,
            current_nav=current_nav,
            market_value=market_value,
            profit=profit,
            profit_rate=profit_rate,
            weight=0.0,
        )
        snapshots.append(snapshot)
        total_market_value += market_value

    # 第二次遍历，计算持仓占比。
    for snapshot in snapshots:
        snapshot.weight = (
            snapshot.market_value / total_market_value if total_market_value else 0.0
        )

    return snapshots


def calculate_type_allocation(snapshots: List[FundSnapshot]) -> Dict[str, float]:
    """按基金类型统计当前市值占比。"""
    type_market_values: Dict[str, float] = {}
    total_market_value = sum(item.market_value for item in snapshots)

    for item in snapshots:
        type_market_values[item.fund_type] = (
            type_market_values.get(item.fund_type, 0.0) + item.market_value
        )

    type_allocation: Dict[str, float] = {}
    for fund_type, market_value in type_market_values.items():
        type_allocation[fund_type] = (
            market_value / total_market_value if total_market_value else 0.0
        )

    return type_allocation


def calculate_totals(snapshots: List[FundSnapshot]) -> dict:
    """计算组合汇总、配置结构和集中度指标。"""
    total_cost = sum(item.units * item.cost_nav for item in snapshots)
    total_market_value = sum(item.market_value for item in snapshots)
    total_profit = total_market_value - total_cost
    total_profit_rate = (total_profit / total_cost) if total_cost else 0.0

    type_allocation = calculate_type_allocation(snapshots)
    max_fund_weight = max((item.weight for item in snapshots), default=0.0)
    max_type_weight = max(type_allocation.values(), default=0.0)

    return {
        "total_cost": total_cost,
        "total_market_value": total_market_value,
        "total_profit": total_profit,
        "total_profit_rate": total_profit_rate,
        "type_allocation": type_allocation,
        "max_fund_weight": max_fund_weight,
        "max_type_weight": max_type_weight,
    }
