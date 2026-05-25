"""根据交易流水计算持仓。"""

from typing import Dict, List

from models import FundMeta, FundPosition, Transaction


def build_positions(funds: List[FundMeta], transactions: List[Transaction]) -> List[FundPosition]:
    """根据基金基础信息和交易流水生成持仓列表。"""
    # 先初始化每只基金，确保无交易记录也会输出观察基金。
    state: Dict[str, dict] = {
        fund.code: {
            "name": fund.name,
            "fund_type": fund.fund_type,
            "units": 0.0,
            "total_cost": 0.0,
        }
        for fund in funds
    }

    for tx in transactions:
        if tx.code not in state:
            # 不在基金池中的交易跳过。
            continue

        if tx.nav <= 0:
            continue

        record = state[tx.code]

        if tx.action == "buy":
            buy_units = (tx.amount - tx.fee) / tx.nav
            if buy_units <= 0:
                continue
            record["units"] += buy_units
            record["total_cost"] += tx.amount

        elif tx.action == "sell":
            if record["units"] <= 0:
                continue

            sell_units = tx.amount / tx.nav
            if sell_units <= 0:
                continue

            current_units = record["units"]
            avg_cost_nav = (record["total_cost"] / current_units) if current_units else 0.0

            actual_sell_units = sell_units if sell_units <= current_units else current_units
            reduce_cost = actual_sell_units * avg_cost_nav

            record["units"] = current_units - actual_sell_units
            record["total_cost"] = max(record["total_cost"] - reduce_cost, 0.0)

    positions: List[FundPosition] = []
    for fund in funds:
        record = state[fund.code]
        units = record["units"]
        total_cost = record["total_cost"]
        cost_nav = (total_cost / units) if units > 0 else 0.0

        positions.append(
            FundPosition(
                code=fund.code,
                name=fund.name,
                fund_type=fund.fund_type,
                units=units,
                cost_nav=cost_nav,
            )
        )

    return positions
