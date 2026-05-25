"""fund-monitor 入口脚本。"""

from calculator import build_snapshots, calculate_totals
from data_loader import load_funds
from mock_nav_provider import get_mock_nav_data
from position_calculator import build_positions
from real_nav_provider import get_real_nav_data
from report_generator import generate_report_markdown, save_report
from transaction_loader import load_transactions


def main() -> None:
    """执行一次基金监控日报生成流程。"""
    funds = load_funds("data/funds.csv")
    transactions = load_transactions("data/transactions.csv")
    positions = build_positions(funds, transactions)

    # 优先尝试真实接口，失败则整体回退到模拟数据。
    try:
        real_cache: dict[str, dict] = {}
        for position in positions:
            real_cache[position.code] = get_real_nav_data(position.code)

        def nav_provider(code: str) -> dict:
            return real_cache[code]

        data_source_note = "当前使用真实基金净值数据"
        data_source_label = "真实基金净值接口"
    except Exception:
        nav_provider = get_mock_nav_data
        data_source_note = "当前真实接口失败，已切换为模拟数据"
        data_source_label = "模拟数据"

    snapshots = build_snapshots(positions, nav_provider=nav_provider)
    totals = calculate_totals(snapshots)
    totals["data_source_note"] = data_source_note
    totals["data_source_label"] = data_source_label

    report_content = generate_report_markdown(snapshots, totals)
    report_path = save_report(report_content)

    print("日报已生成：", report_path)


if __name__ == "__main__":
    main()
