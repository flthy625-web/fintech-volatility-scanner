# 📈 Fintech 市场波动扫描器

> 一个面向金融科技学习的实验工具，帮助工商管理专业学生理解加密货币市场的流动性、价格发现机制和量价关系。

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 项目简介

这是一个专为 **FinTech 教育** 设计的市场波动监测工具，通过实时数据分析帮助学生：

- 📊 **理解市场流动性**：通过成交量、成交额、成交笔数等指标，直观感受市场的活跃程度
- 💹 **观察价格发现机制**：实时监控价格变动、振幅、涨跌幅，理解供需如何影响价格
- 🔍 **识别量价关系**：通过"放量上涨"、"缩量背离"等状态，学习技术分析的核心概念
- ⚡ **体验市场异常**：自动识别剧烈波动、高振幅等异常市场行为

### 🎓 教育价值

#### 1. **流动性理解**
- **成交额过滤**：通过调节阈值（100万-10000万 USDT），学生可以观察不同流动性水平的市场特征
- **成交笔数分析**：理解交易频率与市场活跃度的关系
- **平均每笔成交额**：识别大单交易与散户交易的区别

#### 2. **价格发现机制**
- **24h 涨跌幅**：观察价格如何在供需作用下波动
- **高低价区间**：理解价格在一定范围内的震荡与突破
- **实时排序**：看到资金如何流向不同资产，形成价格差异

#### 3. **量价关系分析**
- **放量上涨** 🚀：价格上涨 + 成交量放大 = 强势信号（买方力量强）
- **缩量背离** ⚠️：价格上涨 + 成交量萎缩 = 风险信号（上涨动能不足）
- **放量下跌** 📉：价格下跌 + 成交量放大 = 恐慌抛售
- **剧烈波动** ⚡：短时间内大幅波动，反映市场情绪剧烈变化

#### 4. **风险管理意识**
- **波动率监控**：通过年化波动率、ATR、最大回撤等指标，理解风险度量
- **异常预警**：Z-Score 异常检测，识别偏离正常分布的极端行情
- **多资产对比**：通过相关性矩阵，理解资产间的联动关系

---

## ✨ 核心功能

### 1. 📊 多资产波动扫描
- 支持美股科技、指数、加密货币、外汇、大宗商品等多类资产
- 实时计算年化波动率、ATR%、最大回撤、Z-Score
- 波动等级自动分类（低/中/高/极高）

### 2. 💰 Binance USDT 交易对监控
- **自动数据源切换**：Binance API（优先）→ CoinGecko API（备用）
- **智能过滤**：可调节成交额阈值（100万-10000万 USDT）
- **量价状态分析**：
  - 🚀 放量上涨：涨幅 > 10% 且成交量 > 中位数 1.5 倍
  - ⚠️ 缩量背离：涨幅 > 5% 但成交量 < 中位数 0.7 倍
  - 📉 放量下跌：跌幅 > 10% 且成交量 > 中位数 1.5 倍
  - ⚡ 剧烈波动：涨跌幅绝对值 > 15%
  - 🌊 高振幅：24h 振幅 > 20%

### 3. 📈 可视化分析
- **K线图 + 滚动波动率**：双图联动展示价格走势与波动变化
- **相关性热力图**：展示不同资产间https://github.com/flthy625-web/fintech-volatility-scanner.git
cd fintech-volatility-scar
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动应用**
```bash
streamlit run app.py
```

4. **访问应用**
- 浏览器会自动打开 `http://localhost:8501`
- 如果没有自动打开，手动访问该地址

---

## 📖 使用指南

### 基础操作

#### 1. 配置扫描参数（左侧边栏）

**资产预设**
- 选择预设组合：美股科技、美股指数、加密货币、外汇、大宗商品
- 或自定义标的列表（逗号或换行分隔）

**时间窗口**
- 1个月、3个月、6个月、1年、2年、5年

**告警阈值**
- 年化波动率阈值：5%-150%
- Z-Score 阈值：1.0-4.0

**Binance 过滤配置**
- 成交额过滤阈值：100万-10000万 USDT
- 💡 建议：500万（平衡流动性和数量）

#### 2. 获取 Binance 数据

点击主界面的 **📊 获取 Binance USDT 交易对** 按钮：
- 自动尝试 Binance API（4个端点）
- 如遇地区限制，自动切换到 CoinGecko API
- 显示统计概览：交易对数量、涨跌分布、放量上涨/缩量背离数量

#### 3. 数据筛选与排序

**排序选项**
- 保持默认（涨幅从高到低）
- 24h 振幅%
- 24h 成交额(USDT)
- 最新价

**进一步筛选**
- 全部
- 仅上涨
- 仅下跌
- 振幅 > 5%
- 振幅 > 10%

#### 4. 查看详细分析

**扫描全景**
- 多资产对比表格
- 下载 CSV 数据

**单标的详情**
- K线图 + 滚动波动率
- 选择具体标的查看

**相关性矩阵**
- 标的间收益率相关性热力图

**告警**
- 触发阈值的标的列表
- 详细告警原因

#### 5. 实时扫描（可选）

点击 **🔴 开始实时扫描**：
- 设置刷新间隔（10-300秒）
- 自动更新数据
- 显示扫描次数
- 点击 **⏸️ 停止扫描** 结束

---

## 🎓 教学场景示例

### 场景 1：理解流动性分层

**操作步骤**：
1. 设置成交额阈值为 **100万 USDT**，观察交易对数量
2. 逐步提高到 **500万**、**1000万**、**5000万**
3. 观察每个阈值下的交易对数量变化

**学习要点**：
- 流动性越高的市场，参与者越多，价格发现越有效
- 小市值币种流动取 Binance 数据
2. 查看 **波动状态** 列
3. 找到标记为 **⚠️ 缩量背离** 的币种

**学习要点**：
- 价格上涨但成交量萎缩，说明买方力量减弱
- 可能是趋势末期，存在回调风险
- 对比 **🚀 放量上涨** 的币种，理解健康上涨的特征

### 场景 3：观察市场恐慌

**操作步骤**：
1. 筛选 **仅下跌** 的币种
2. 观察 **波动状态** 是否为 **📉 放量下跌**
3. 查看 **24h 振幅%** 和 **涨跌%**

**学习要点**：
- 放量下跌通常伴随恐慌性抛售
- 高振幅反映市场情绪剧烈波动
- 理解市场情绪如何影响价格

### 场景 4：相关性分析

**操作步骤**：
1. 选择多个标的（如 BTC、ETH、BNB）
2. 切换到 **相关性矩阵** 标签
3. 观察热力图中的颜色深浅

**学习要点**：
- 相关性接近 1：两个资产同涨同跌
- 相关性接近 -1：两个资产反向波动
- 相关性接近 0：两个资产独立变动
- 理解资产配置中的分散化原理

---

## 🛠️ 技术架构

### 数据源
- **Yahoo Finance**：股票、指数、外汇、大宗商品历史数据
- **Binance API**：加密货币实时 24h 数据（优先）
- **CoinGecko API**：加密货币备用数据源（无地区限制）

### 核心技术栈
- **Streamlit**：Web 应用框架
- **Pandas & NumPy**：数据处理与计算
- **Plotly**：交互式图表
- **yfinance**：金融数据获取
- **Requests**：API 调用

### 关键算法

#### 1. 历史波动率（HV）
```python
returns = price.pct_change()
hv_annualized = returns.std() * sqrt(trading_periods) * 100
```

#### 2. 平均真实波幅（ATR%）
```python
tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
atr = tr.rolling(14).mean()
atr_pct = atr / close * 100
```

#### 3. 最大回撤
```python
cummax = close.cummax()
drawdown = (close / cummax - 1) * 100
max_drawdown = drawdown.min()
```

#### 4. Z-Score 异常检测
```python
recent_return = returns.iloc[-1]
std = returns.iloc[-60:].std()
zscore = recent_return / std
```

#### 5. 量价状态判断
```python
avg_trade_size = quote_volume / trades_count
median_trade_size = median(all_avg_trade_sizes)

if price_change > 10% and avg_trade_size > median * 1.5:
    status = "放量上涨"
elif price_change > 5% and avg_trade_size < median * 0.7:
    status = "缩量背离"
```

---

## 📊 数据说明

#成交额(USDT) | 24小时成交的 USDT 总额 | USDT |
| 成交笔数 | 24小时内的交易次数 | 笔 |
| 平均每笔(USDT) | 成交额 / 成交笔数 | USDT |
| 波动状态 | 量价关系分析结果 | 标签 |

### 波动状态定义

| 状态 | 触发条件 | 市场含义 |
|------|---------|---------|
| 🚀 放量上涨 | 涨幅 > 10% 且 平均每笔 > 中位数 × 1.5 | 强势上涨，资金大量流入 |
| ⚠️ 缩量背离 | 涨幅 > 5% 但 平均每笔 < 中位数 × 0.7 | 上涨动能不足，可能回调 |
| 📉 放量下跌 | 跌幅 > 10% 且 平均每笔 > 中位数 × 1.5 | 恐慌抛售，大量资金流出 |
| 🔻 缩量下跌 | 跌幅 > 5% 但 平均每笔 < 中位数 × 0.7 | 下跌但抛压不大 |
| ⚡ 剧烈波动 | \|涨跌幅\| > 15% | 极端行情，情绪剧烈 |
| 🌊 高振幅 | 24h振幅 > 20% | 价格大幅震荡 |
| ➖ 正常 | 其他情况 | 常规波动 |

---

## ⚠️ 免责声明

**本工具仅供教育和学习使用，不构成任何投资建议。**

- 📚 **教育目的**：帮助学生理解金融市场的运作机制
- **：所有数据和分析仅供参考，不应作为投资决策依据
- ⚡ **市场风险**：加密货币市场波动极大，投资需谨慎
- 🔍 **数据延迟**：实时数据可能存在延迟，不保证绝对准确性
- 💼 **自负盈亏**：任何基于本工具的投资决策，风险自担

---

## 🐛 常见问题

### Q1: Binance API 无法访问（HTTP 451）？
**A**: 这是地区限制问题。应用会自动切换到 CoinGecko API（无地区限制）。你也可以：
- 使用 VPN 切换到其他地区
- 部署到 Streamlit Cloud（云端服务器通常无限制）

### Q2: 数据加载很慢？
**A**: 
- 降低成交额阈值，减少数据量
- 检查网络连接
- 等待缓存生效（60秒 TTL）

### Q3: 为什么有些币种没有数据？
**A**: 
- 成交额低于设定阈值被过滤
- 数据源暂时不可用
- 币种已下架或暂停交易

### Q4: 如何理解"放量上涨"和"缩量背离"？
**A**: 
- **放量上涨**：价格上涨 + 成交量大 = 买方力量强，趋势可能持续
- **缩量背离**：价格上涨 + 成交量小 = 买方力量弱，可能是假突破

### Q5: Z-Score 是什么？
**A**: 
- 衡量当前价格变动偏离正常分布的程度
- |Z-Score| > 2：异常波动（约 5% 概率）
- |Z-Score| > 3：极端异常（约 0.3% 概率）

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境设置
```bash
# 克隆仓库
git clone https://github.com/flthy625-web/fintech-volatility-scanner.git
cd fintech-volatility-scanner

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run app.py
```

### 提交规范
- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具链相关

---

## 📄 许目采用 [MIT License](LICENSE) 开源协议。

---

## 👨‍💻 作者

**flthy625-web**

- GitHub: [@flthy625-web](https://github.com/flthy625-web)
- 项目链接: [fintech-volatility-scanner](https://github.com/flthy625-web/fintech-volatility-scanner)

---

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - 优秀的 Pyt 提交 [GitHub Issue](https://github.com/flthy625-web/fintech-volatility-scanner/issues)
- 💬 发起 [GitHub Discussion](https://github.com/flthy625-web/fintech-volatility-scanner/discussions)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star！**

Made with ❤️ for FinTech Education

</div>
