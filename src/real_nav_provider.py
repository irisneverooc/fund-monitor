"""真实基金净值数据提供器（AkShare）。"""

from typing import Any


def _to_float(value: Any, default: float = 0.0) -> float:
    """把值安全转换为 float。"""
    if value is None:
        return default
    text = str(value).strip().replace("%", "")
    if text == "":
        return default
    return float(text)


def _get_trade_status(ak, code: str) -> tuple[str, str]:
    """获取申购状态和赎回状态。"""
    try:
        df = ak.fund_purchase_em()
        if df is None or df.empty:
            return "未知", "未知"

        code_col = "基金代码" if "基金代码" in df.columns else None
        if not code_col:
            return "未知", "未知"

        matched = df[df[code_col].astype(str).str.strip() == code]
        if matched.empty:
            return "未知", "未知"

        row = matched.iloc[0]
        subscribe_status = row.get("申购状态", "未知")
        redeem_status = row.get("赎回状态", "未知")
        return str(subscribe_status), str(redeem_status)
    except Exception:
        return "未知", "未知"


def get_real_nav_data(code: str) -> dict:
    """按基金代码获取真实净值数据。"""
    try:
        import akshare as ak
    except Exception as e:
        raise RuntimeError(f"未安装或无法导入 akshare: {e}")

    df = ak.fund_open_fund_info_em(symbol=code, indicator="单位净值走势")
    if df is None or df.empty:
        raise ValueError("接口返回为空")

    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) >= 2 else latest

    nav_date = latest.get("净值日期", latest.get("x", "未知"))
    current_nav = _to_float(latest.get("单位净值", latest.get("y", 0.0)))
    previous_nav = _to_float(previous.get("单位净值", previous.get("y", current_nav)))

    raw_growth = latest.get("日增长率", "")
    if str(raw_growth).strip() == "":
        daily_growth_rate = (
            (current_nav - previous_nav) / previous_nav if previous_nav else 0.0
        )
    else:
        daily_growth_rate = _to_float(raw_growth) / 100.0

    subscribe_status, redeem_status = _get_trade_status(ak, code)

    return {
        "current_nav": current_nav,
        "previous_nav": previous_nav,
        "nav_date": str(nav_date),
        "daily_growth_rate": daily_growth_rate,
        "subscribe_status": subscribe_status,
        "redeem_status": redeem_status,
    }
