# fund-monitor

一个面向个人投资学习的 Python 项目：记录交易流水，自动计算基金持仓，并生成**个人基金监控日报**（规则化日报）。

## 重要说明

- 当前项目已支持真实基金净值读取；当真实接口失败时，会自动回退到模拟数据，保证日报可生成。
- 报告明确区分“生成日期”和“净值数据日期（或日期范围）”，便于识别 QDII 等基金的净值延迟。
- 接口数据可能存在延迟（尤其是 QDII 基金），请以基金公司/官方渠道披露为准。
- 当前项目输出仅用于学习与记录，不构成任何投资建议。

## 新增能力：交易流水自动计算持仓

项目现在通过 `data/transactions.csv` 的买入/卖出记录，自动计算每只基金的：
- 持有份额 `units`
- 平均成本净值 `cost_nav`

你不再需要手动维护 `funds.csv` 中的 `units` 和 `cost_nav`。

## 数据文件

### `data/funds.csv`
只保留基金基础信息：

```csv
code,name,fund_type
017641,摩根标普500指数(QDII)A,海外指数
```

### `data/transactions.csv`
交易流水字段：

```csv
date,code,action,amount,nav,fee
2026-05-20,270042,buy,300,1.5200,0
```

- `action=buy`：买入
- `action=sell`：卖出

## 持仓计算规则

- 买入份额：`(amount - fee) / nav`
- 卖出份额：`amount / nav`
- 卖出后按当前平均成本等比例减少成本
- 份额不会被减到负数
- 在 `funds.csv` 中存在但无交易记录的基金，会在日报中显示为“观察基金”

## 项目结构（核心）

```text
src/
├─ data_loader.py           # 基金基础信息读取
├─ transaction_loader.py    # 交易流水读取
├─ position_calculator.py   # 交易流水 -> 持仓计算
├─ real_nav_provider.py     # 真实净值提供器（AkShare）
├─ mock_nav_provider.py     # 模拟净值提供器
├─ calculator.py            # 收益计算与配置分析
├─ report_generator.py      # 报告生成
└─ main.py                  # 程序入口
```

## 如何运行

```bash
python src/main.py
```

## 依赖安装

```bash
pip install -r requirements.txt
```
