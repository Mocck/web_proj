# crypto_quant_trading.md

# 虚拟货币量化交易指南

本文件介绍虚拟货币量化交易的基础概念、策略、工具和注意事项，适合用于 RAG 知识库。

---

## 1. 量化交易概念
- **定义**：使用计算机程序基于历史数据和算法进行自动化交易。
- **目标**：最大化收益、控制风险、实现高频或低频交易策略。
- **特点**：数据驱动、可回测、策略可复制。

## 2. 交易市场
- **现货市场（Spot）**：实际买卖加密货币。
- **衍生品市场（Futures / Perpetual）**：杠杆交易、空头和多头策略。
- **DEX（去中心化交易所）**：如 Uniswap、Sushiswap，基于 AMM 模型。

## 3. 常见量化策略

### 3.1 趋势跟踪（Trend Following）
- 基于价格趋势判断买卖时机。
- 常用指标：移动平均线（MA）、指数移动平均线（EMA）、MACD。

### 3.2 均值回归（Mean Reversion）
- 假设价格会回归均值。
- 常用指标：布林带（Bollinger Bands）、RSI、标准差。

### 3.3 市场中性（Market Neutral）
- 对冲市场方向风险。
- 示例：多空配对交易（Pairs Trading）。

### 3.4 高频交易（HFT）
- 低延迟、高频率下单。
- 对系统性能要求高，需要专用硬件和算法优化。

## 4. 数据获取与处理
- **交易所 API**：如 Binance、Coinbase Pro、OKX 等。
- **链上数据**：通过 Web3、The Graph 获取链上交易、资金流信息。
- **数据清洗**：处理缺失值、异常值、时间对齐。

## 5. 回测与模拟
- **回测（Backtesting）**：使用历史数据验证策略有效性。
- **模拟交易（Paper Trading）**：在真实市场环境下测试策略而不涉及真实资金。
- 常用工具：Backtrader、Zipline、Freqtrade。

## 6. 风险管理
- **仓位控制**：每笔交易资金比例限制。
- **止损止盈**：固定或动态止损止盈策略。
- **杠杆风险**：控制杠杆倍数，避免爆仓。
- **多策略组合**：降低单一策略失败风险。

## 7. 工具与技术栈
- **编程语言**：Python、JavaScript
- **数据分析库**：Pandas、NumPy、TA-Lib
- **交易库**：CCXT（多交易所接口）、Web3.py（链上数据）
- **可视化**：Matplotlib、Plotly

## 8. 自动化交易系统架构
1. 数据采集模块
2. 策略计算模块
3. 风控与仓位管理模块
4. 下单执行模块
5. 日志与监控模块

## 9. 注意事项
- 市场波动性大，历史收益不代表未来收益
- 关注交易所安全和 API 限制
- 合理设计交易策略，避免过拟合
- 法律合规：了解所在地区加密货币交易规定

# 常见量化策略及 Python 实现

## 1. 趋势跟踪策略（Trend Following）
### 策略说明
- 基于价格趋势判断买卖时机。
- 常用指标：移动平均线（MA）、指数移动平均线（EMA）、MACD。

### Python 示例（均线交叉策略）
```python
import pandas as pd
import numpy as np

# 假设有历史数据 df 包含 'close'
data = pd.read_csv('btc_prices.csv', parse_dates=['timestamp'])
data.set_index('timestamp', inplace=True)

# 短期和长期均线
short_window = 10
long_window = 50

data['SMA_short'] = data['close'].rolling(short_window).mean()
data['SMA_long'] = data['close'].rolling(long_window).mean()

# 生成信号
data['signal'] = 0
data['signal'][short_window:] = np.where(
    data['SMA_short'][short_window:] > data['SMA_long'][short_window:], 1, -1
)

# 输出信号
print(data[['close', 'SMA_short', 'SMA_long', 'signal']].tail())
```

---

## 2. 均值回归策略（Mean Reversion）
### 策略说明
- 假设价格会回归均值，当价格偏离均值过大时买入或卖出。
- 常用指标：布林带（Bollinger Bands）、RSI。

### Python 示例（布林带策略）
```python
import pandas as pd
import numpy as np

# 数据
data = pd.read_csv('btc_prices.csv', parse_dates=['timestamp'])
data.set_index('timestamp', inplace=True)

# 布林带计算
window = 20
data['MA'] = data['close'].rolling(window).mean()
data['STD'] = data['close'].rolling(window).std()
data['Upper'] = data['MA'] + 2*data['STD']
data['Lower'] = data['MA'] - 2*data['STD']

# 生成信号
data['signal'] = 0
data['signal'] = np.where(data['close'] < data['Lower'], 1, np.where(data['close'] > data['Upper'], -1, 0))

print(data[['close','MA','Upper','Lower','signal']].tail())
```

---

## 3. 市场中性策略（Market Neutral）
### 策略说明
- 对冲市场方向风险，通过多空组合降低整体波动。
- 示例：配对交易（Pairs Trading），选择相关性高的两只资产，价格偏离时进行买卖。

### Python 示例（配对交易）
```python
import pandas as pd

# 假设有两只相关资产的价格数据
asset1 = pd.read_csv('asset1.csv', parse_dates=['timestamp']).set_index('timestamp')
asset2 = pd.read_csv('asset2.csv', parse_dates=['timestamp']).set_index('timestamp')

spread = asset1['close'] - asset2['close']
spread_mean = spread.mean()
spread_std = spread.std()

# 当价差高于均值+2*std 卖出，低于均值-2*std 买入
signal = pd.Series(0, index=spread.index)
signal[spread > spread_mean + 2*spread_std] = -1
signal[spread < spread_mean - 2*spread_std] = 1

print(signal.tail())
```

---

## 4. 动量策略（Momentum）
### 策略说明
- 基于过去价格表现预测未来趋势。
- 常用指标：RSI, ROC（Rate of Change）。

### Python 示例（动量策略）
```python
import pandas as pd

data = pd.read_csv('btc_prices.csv', parse_dates=['timestamp']).set_index('timestamp')
data['ROC'] = data['close'].pct_change(periods=10)

# 当 ROC > 0 买入，ROC < 0 卖出
data['signal'] = 0
data['signal'] = np.where(data['ROC'] > 0, 1, -1)

print(data[['close','ROC','signal']].tail())
```

---

## 5. 风险管理
- 仓位控制：单笔交易不超过总资金的 x%
- 止损止盈：动态设置止损止盈
- 多策略组合：降低单一策略失败风险

---

## 6. 工具推荐
- **Python 库**：Pandas、NumPy、TA-Lib、CCXT、Backtrader、Freqtrade
- **数据源**：Binance、Coinbase Pro、OKX API，链上数据 Web3



