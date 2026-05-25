"""fund-monitor MVP 入口脚本。

第一阶段目标：先搭建基金监控日报框架（MVP），
使用模拟数据走通“读取 -> 计算 -> 生成日报”的流程。
后续会接入真实基金净值数据接口并替换模拟数据。
"""

from data_loader import load_positions
from calculator import build_snapshots, calculate_totals
from report_generator import generate_report_markdown, save_report


def main() -> None:
    """执行一次基金监控日报生成流程。"""
    # 注意：当前 data/funds.csv 为模拟示例数据，不代表真实持仓。
    positions = load_positions("data/funds.csv")
    snapshots = build_snapshots(positions)
    totals = calculate_totals(snapshots)

    report_content = generate_report_markdown(snapshots, totals)
    report_path = save_report(report_content)

    print("日报已生成：", report_path)


if __name__ == "__main__":
    main()
