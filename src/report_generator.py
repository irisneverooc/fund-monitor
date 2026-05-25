"""Markdown 日报生成。"""

from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from models import FundSnapshot


def _build_observation_note(item: FundSnapshot) -> str:
    """根据单只基金收益率与日涨跌幅生成观察提示。"""
    if item.daily_change_rate > 0.02:
        daily_note = "今日上涨明显"
    elif item.daily_change_rate < -0.02:
        daily_note = "今日下跌明显"
    else:
        daily_note = "日内波动正常"

    if item.units == 0:
        return f"{daily_note}。当前为观察基金（未持仓），用于跟踪走势。"
    if item.profit_rate > 0.05:
        return f"{daily_note}。已有浮盈，可继续观察，避免冲动加仓。"
    if item.profit_rate < -0.05:
        return f"{daily_note}。出现浮亏，可检查是否仍符合长期配置逻辑。"
    return f"{daily_note}。波动正常，按计划观察。"


def _build_trade_watch_note(item: FundSnapshot) -> str:
    """根据持仓收益率生成交易观察提醒。"""
    if item.profit_rate <= -0.15:
        return "进入加仓观察区：当前相对成本跌幅较大，可结合长期配置计划、资金安排和基金基本面判断是否分批加仓。"
    if item.profit_rate >= 0.20:
        return "进入止盈/减仓观察区：当前已有较明显浮盈，可结合目标仓位和后续计划判断是否部分止盈或减仓。"
    return "未触发加仓或减仓观察阈值，继续按计划观察。"


def _find_max_type(type_allocation: dict) -> Tuple[str, float]:
    """找到占比最高的基金类型。"""
    if not type_allocation:
        return "", 0.0
    fund_type = max(type_allocation, key=type_allocation.get)
    return fund_type, type_allocation[fund_type]


def _build_nav_date_summary(snapshots: List[FundSnapshot]) -> str:
    """生成净值日期说明（单日或区间）。"""
    nav_dates = sorted({item.nav_date for item in snapshots if item.nav_date})
    if not nav_dates:
        return "未知"

    # 模拟数据或非标准日期场景：直接展示唯一集合。
    if any(not date[:4].isdigit() for date in nav_dates):
        return "、".join(nav_dates)

    if len(nav_dates) == 1:
        return nav_dates[0]

    return f"{nav_dates[0]} 至 {nav_dates[-1]}"


def generate_report_markdown(snapshots: List[FundSnapshot], totals: dict) -> str:
    """生成基金监控日报的 Markdown 文本。"""
    report_date = datetime.now().strftime("%Y-%m-%d")
    data_source_note = totals.get("data_source_note", "当前净值为模拟数据")
    data_source_label = totals.get("data_source_label", "模拟数据")
    nav_date_summary = _build_nav_date_summary(snapshots)

    lines = [
        f"# 基金监控日报（生成日期：{report_date}）",
        "",
        "## 数据说明",
        f"- 报告生成日期：{report_date}",
        (f"- 净值数据日期：{nav_date_summary}" if "至" not in nav_date_summary else f"- 净值数据日期范围：{nav_date_summary}"),
        f"- 数据来源：{data_source_label}",
        "- 说明：QDII 等海外基金净值可能存在 1-2 个交易日延迟，请以基金平台最终展示为准。",
        "",
        "## 组合总览",
        f"- 总成本：{totals['total_cost']:.2f}",
        f"- 总市值：{totals['total_market_value']:.2f}",
        f"- 总收益：{totals['total_profit']:.2f}",
        f"- 总收益率：{totals['total_profit_rate'] * 100:.2f}%",
        "",
        "## 持仓明细",
        "",
        "| 基金代码 | 基金名称 | 基金类型 | 持仓状态 | 持有份额 | 净值日期 | 成本净值 | 昨日净值 | 当前净值 | 日涨跌幅 | 当前市值 | 持仓收益 | 收益率 | 持仓占比 |",
        "|---|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for item in snapshots:
        position_status = "观察基金" if item.units == 0 else "持有中"
        lines.append(
            "| {code} | {name} | {fund_type} | {position_status} | {units:.2f} | {nav_date} | {cost_nav:.4f} | {previous_nav:.4f} | {current_nav:.4f} | {daily_change_rate:.2f}% | {market_value:.2f} | {profit:.2f} | {profit_rate:.2f}% | {weight:.2f}% |".format(
                code=item.code,
                name=item.name,
                fund_type=item.fund_type,
                position_status=position_status,
                units=item.units,
                nav_date=item.nav_date,
                cost_nav=item.cost_nav,
                previous_nav=item.previous_nav,
                current_nav=item.current_nav,
                daily_change_rate=item.daily_change_rate * 100,
                market_value=item.market_value,
                profit=item.profit,
                profit_rate=item.profit_rate * 100,
                weight=item.weight * 100,
            )
        )

    lines.extend(["", "## 今日观察"])
    for item in snapshots:
        observe_note = _build_observation_note(item)
        lines.append(
            f"- {item.name}（{item.code}）：当前收益率 {item.profit_rate * 100:.2f}%，持仓占比 {item.weight * 100:.2f}%，日涨跌幅 {item.daily_change_rate * 100:.2f}%。{observe_note}"
        )

    lines.extend(["", "## 交易观察提醒"])
    for item in snapshots:
        trade_watch_note = _build_trade_watch_note(item)
        lines.append(
            f"- {item.name}（{item.code}）：当前收益率 {item.profit_rate * 100:.2f}%，{trade_watch_note}"
        )

    lines.extend(["", "## 配置结构"])
    for fund_type, ratio in totals["type_allocation"].items():
        lines.append(f"- {fund_type}：{ratio * 100:.2f}%")

    lines.extend(["", "## 组合建议"])
    total_profit_rate = totals["total_profit_rate"]
    if total_profit_rate > 0:
        lines.append("- 组合当前浮盈，继续按计划观察。")
    elif total_profit_rate < 0:
        lines.append("- 组合当前浮亏，避免情绪化操作。")
    else:
        lines.append("- 组合当前基本持平。")

    if totals["max_fund_weight"] > 0.5:
        lines.append("- 单只基金占比较高，注意集中度风险。")
    else:
        max_type, max_ratio = _find_max_type(totals["type_allocation"])
        if max_ratio > 0.6:
            lines.append(
                f"- {max_type}类基金占比 {max_ratio * 100:.2f}%，超过 60%，注意单一资产类别集中度风险。"
            )
        else:
            lines.append("- 组合配置相对分散。")

    lines.extend(["", "## 风险提示"])
    if total_profit_rate > 0:
        lines.append("- 当前组合处于浮盈状态，但模拟数据不代表未来收益。")
    elif total_profit_rate < 0:
        lines.append("- 当前组合处于浮亏状态，避免因短期波动做情绪化决策。")
    else:
        lines.append("- 当前组合收益基本持平，继续按计划跟踪观察。")
    lines.append("- 本项目仅用于 Python 数据分析练习，不构成投资建议。")

    lines.extend(
        [
            "",
            "## 说明",
            f"- {data_source_note}",
            "- 真实接口可能存在数据延迟（QDII 基金尤为常见）。",
            "- 支持通过 data/funds.csv 自定义个人基金池（含观察基金）。",
            "- 本报告仅用于个人学习与记录，不构成投资建议。",
        ]
    )

    return "\n".join(lines)


def save_report(content: str, output_dir: str = "reports") -> Path:
    """保存 Markdown 日报到 reports 目录。"""
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)

    report_date = datetime.now().strftime("%Y%m%d")
    file_path = folder / f"daily_report_{report_date}.md"
    file_path.write_text(content, encoding="utf-8")
    return file_path
