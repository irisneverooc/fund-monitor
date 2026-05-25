"""模拟净值数据来源。

本模块只用于 MVP 阶段演示，暂不调用真实基金接口。
后续计划：在 v0.3 接入真实净值接口后，替换本模块逻辑。
"""

from typing import Dict


def get_mock_nav_map() -> Dict[str, float]:
    """返回模拟的基金代码 -> 当前净值。"""
    return {
        "161725": 1.12,
        "110022": 2.18,
        "000217": 1.26,
    }


def get_mock_nav(code: str, fallback_nav: float = 1.00) -> float:
    """根据基金代码获取模拟净值，不存在时使用默认值。"""
    nav_map = get_mock_nav_map()
    return nav_map.get(code, fallback_nav)
