"""模拟净值数据来源。"""

from typing import Dict, Tuple


def get_mock_nav_map() -> Dict[str, Dict[str, float]]:
    """返回模拟的基金代码 -> 净值数据（昨日/当前）。"""
    return {
        "513100": {"previous_nav": 1.0120, "current_nav": 1.0340},
        "161125": {"previous_nav": 1.0850, "current_nav": 1.0710},
        "518880": {"previous_nav": 1.2200, "current_nav": 1.2500},
        "000216": {"previous_nav": 1.2400, "current_nav": 1.2150},
    }


def get_mock_nav_pair(code: str, fallback_nav: float = 1.00) -> Tuple[float, float]:
    """根据基金代码获取（当前净值, 昨日净值）。"""
    nav_map = get_mock_nav_map()
    nav_data = nav_map.get(code)
    if not nav_data:
        return fallback_nav, fallback_nav
    return nav_data["current_nav"], nav_data["previous_nav"]


def get_mock_nav_data(code: str, fallback_nav: float = 1.00) -> dict:
    """返回与真实接口一致结构的模拟净值数据。"""
    current_nav, previous_nav = get_mock_nav_pair(code, fallback_nav=fallback_nav)
    daily_change_rate = (
        (current_nav - previous_nav) / previous_nav if previous_nav else 0.0
    )

    return {
        "current_nav": current_nav,
        "previous_nav": previous_nav,
        "nav_date": "模拟数据",
        "daily_growth_rate": daily_change_rate,
        "subscribe_status": "未知",
        "redeem_status": "未知",
    }
