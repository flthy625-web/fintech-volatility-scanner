"""学习中心 - 金融知识库"""
import streamlit as st
import json
from part Path

st.set_page_config(
    page_title="学习中心 - 金融科学教育",
    page_icon="📚",
    layout="wide",
)

# 自定义样式
st.markdown("""
<style>
    .concept-card {
        background: linear-gradient(135deg, rgba(94, 234, 212, 0.1), rgba(96, 165, 250, 0.05));
        border: 1px solid rgba(94, 234, 212, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .concept-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #5eead4;
        margin-bottom: 0.5rem;
    }
    .concept-definition {
        font-size: 1rem;
        color: #e6ecff;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    .concept-section {
        margin-top: 1rem;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #60a5fa;
        margin-bottom: 0.5rem;
    }
    .example-box {
        background: rgba(96, 165, 250, 0.1);
        border-left: 3px solid #60a5fa;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    .progress-bar {
        background: rgba(94, 234, 212, 0.2);
        border-radius: 10px;
        height: 20px;
        margin: 0.5rem 0;
    }
    .progress-fill {
        background: linear-gradient(90deg, #5eead4, #60a5fa);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.title("📚 金融知识库")
st.markdown("**系统学习金融市场核心概念，理论与实践相结合**")

# 初始化 session state
if "completed_concepts" not in st.session_state:
    st.session_state.completed_concepts = set()

# 知识库内容
KNOWLEDGE_BASE = {
    "初级概念": {
        "流动性 (Liquidity)": {
            "定义": "流动性是指资产能够快速转换为现金而不显著影响其价格的能力。高流动性意味着市场中有足够的买家和卖家，交易可以迅速完成。",
            "衡量指标": [
                "**成交量**：单位时间内的交易数量",
                "**成交额**：单位时间内的交易金额",
                "**买卖价差**：买入价和卖出价之间的差距",
                "**市场深度**：不同价格水平上的订单数量",
                "**成交笔数**：交易的频率"
            ],
            "实战应用": "在本应用中，我们通过「成交额过滤阈值」来筛选高流动性的交易对。成交额越大，说明市场越活跃，价格发现越有效。",
            "案例": "**2020年3月流动性危机**：疫情爆发初期，市场恐慌导致流动性枯竭，即使是比特币这样的主流资产也出现了大幅滑点，24小时内暴跌50%。",
            "思考题": "为什么小市值币种的流动性通常较差？这对投资者有什么影响？"
        },
        "波动率 (Volatility)": {
            "定义": "波动率衡量资产价格变动的剧烈程度。高波动率意味着价格变化幅度大，风险和机会并存。",
            "计算方法": [
                "**历史波动率 (HV)**：基于过去价格数据计算的标准差",
                "**年化波动率**：HV × √交易周期数 × 100%",
                "**ATR (平均真实波幅)**：考虑跳空的波动率指标",
                "**隐含波动率 (IV)**：从期权价格反推的市场预期波动率"
            ],
            "实战应用": "本应用计算的「年化波动率」帮助你识别高风险/高收益的资产。波动率 > 60% 通常被标记为「极高」风险。",
            "案例": "**VIX 恐慌指数**：2020年3月，VIX 从15飙升至82，创历史新高，反映市场极度恐慌。",
            "思考题": "为什么加密货币的波动率通常远高于股票？"
        },
        "价格发现 (Price Discovery)": {
            "定义": "价格发现是市场通过供需关系确定资产公允价值的过       "**市场结构**：集中式 vs 去中心化交易所"
            ],
            "实战应用": "观察「24h涨跌%」排序，可以看到资金如何在不同资产间流动，哪些资产正在被市场重新定价。",
            "案例": "**比特币减半行情**：每次减半后，市场需要6-12个月重新发现比特币的价值，价格通常大幅上涨。",
 ，是技术分析的核心原理之一。健康的价格趋势通常伴随着成交量的配合。",
            "核心原则": [
                "**放量上涨**：价格↑ + 成交量↑ = 强势信号（买方力量强）",
                "**缩量上涨**：价格↑ + 成交量↓ = 弱势信号（上涨动能不足）",
                "**放量下跌**：价格↓ + 成交量↑ = 恐慌抛售",
                "**缩量下跌**：价格↓ + 成交量↓ = 下跌动能减弱",
                "**量价背离**：价格创新高但成交量萎缩 = 趋势可能反转"
            ],
            "实战应用": "本应用的「波动状态」列自动识别量价关系：🚀放量上涨、⚠️缩量背离、📉放量下跌等。",
            "案例": "**2021年5月比特币暴跌**：价格从64000跌至30000，伴随巨大成交量，典型的恐慌性抛售。",
            "思考题": "为什么「缩量背离」是危险信号？"
        },
        "市场深度 (Market Depth)": {
            "定义": "市场深度指不同价格水平上的买卖订单数量。深度越好，大单交易对价格的冲击越小。",
            "衡量方法": [
                "**订单簿分析**：买卖盘口的订单分布",
                "**平均每笔成交额**：成交额 / 成交笔数",
                "**滑点测试**：大单成交的价格偏离",
                "**买卖价差**：Bid-Ask Spread"
            ],
            "实战应用": "本应用计算「平均每笔(USDT)」，数值越大说明大单交易，市场深度越好。",
            "案例": "**闪崩事件**：2017年6月，以太坊在 GDAX 交易所瞬间从319美元跌至0.1美元，原因是市场深度不足。",
            "思考题": "为什么大资金更关注市场深度而不是价格？"
        },
        "相关性 (Correlation)": {
            "定义": "相关性衡量两个资产价格变动的同步程度。相关系数范围从-1到+1。",
            "相关系数解读": [
                "**+1**：完全正相关（同涨同跌）",
                "**和风险分散。",
            "案例": "**比特币与山寨币**：牛市中相关性通常 > 0.8，熊市中相关性下降，山寨币跌幅更大。",
            "思考题": "为什么分散投资要选择低相关性的资产？"
        }
    },
    "高级概念": {
        "异常检测 (Anomaly Detection)": {
            "定义": "异常检测识别偏离正常模式的数据点，用于发现市场异常行为和潜在机会。",
            "常用方法": [
                "**Z-Score**：衡量数据点偏离均值的标准差倍数",
                "**移动平均偏离**：价格偏离均线的程度",
                "**布林带突破**：价格突破统计区间",
                "**成交量异常**：成交量突然放大或萎缩"
            ],
            "Z-Score 解读": [
                "|Z| < 1：正常波动（68%概率）",
                "|Z| = 1-2：较大波动（率）",
                "|Z| = 2-3：异常波动（4%概率）",
                "|Z| > 3：极端异常（0.3%概率）"
            ],
            "实战应用": "本应用的「告警」功能使用 Z-Score 识别异常波动，|Z-Score| ≥ 2 会触发预警。",
            "案例": "**2021年狗狗币暴涨**：在马斯克喊单后，狗狗币单日涨幅超过100%，Z-Score > 5，属于极端异常。",
            "思考题": "为什么极端异常既是机会也是风险？"
        },
        "风险管理 (Risk Management)": {
            "定义": "风险管理是识别、评估和控Value at Risk)**：给定置信度下的最大可能损失",
                "**仓位管理**：单笔交易占总资金的比例",
                "**止损止盈**：预设的退出点位"
            ],
            "实战应用": "本应用显示「最大回撤%」，帮助你评估资产的历史风险。回撤 > -30% 通常被认为是高风险。",
            "案例": "**2022年 LUNA 崩盘**：从119美元跌至0.00001美元，最大回撤 -99.99%，投资者血本无归。",
            "思考题": "为什么专业交易者更关注风险而不是收益？"
        },
        "市场微观结构 (Market Microstructure)": {
            "定义": "市场微观结构研究交易机制如何影响价格形成过程，包括订单类型、交易规则、做市商行为等。",
            "关键要素": [
                "**订单类型**：市价单 vs 限价单",
                "**订单簿动态**：订单的提交、撤销、成交",
                "**做市商**：提供流动性的专业机构",
                "**交易成本**：手续费、滑点、价差",
                "**信息称**：不同参与信息优势"
            ],
            "实战应用": "通过「成T)**：利用微秒级速度优势，在订单簿中抢先成交，每笔利润极小但交易频率极高。",
            "思考题": "为什么交易所的撮合机制会影响价格公平性？"
        }
    }
}

# 侧边栏 - 学习进度
with st.sidebar:
    st.markdown("### 📊 学习进度")

    total_concepts = sum(len(concepts) for concepts in KNOWLEDGE_BASE.values())
  e="width: {progress}%"></div>
    </div>
    <p style="text-align: center; color: #5eead4; font-weight: 600;">
        {completed} / {total_concepts} 已完成 ({progress:.0f}%)
    </p>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 🎯 学习路径")
    st.info("""
    **建议学习顺序：**
    1. 初级概念（必修）
    2. 中级概念（进阶）
    3. 高级概念（深入）

    💡 每个概念学习后，记得点击「✅ 标记为已学习」
    """)

# 主内容区
tab_beginner, tab_intermediate, tab_advanced = st.tabs(["🌱 初级概念", "📈 中级概念", "🚀 高级概念"])

def render_concept(concept_name, concept_data, level):
    """渲染单个概念卡片"""
    is_completed = f"{level}_{concept_name}" in st.session_state.completed_concepts

    st.markdown(f"""
    <div class="concept-card">
        <div class="concept-title">
            {'✅ ' if is_completed else '📖 '}{concept_name}
        </div>
        <div class="concept-definition">
            {concept_data['定义']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 详细内容
    col1, col2 = st.columns([2, 1])

    with col1:
        # 核心内容
        if '衡量指标' in concept_data:
            st.markdown('<div class="section-title">📊 衡量指标</div>', unsafe_allow_html=True)
            for indicator in concept_data['衡量指标']:
                st.markdown(f"- {indicator}")

        if '计算方法' in concept_data:
            st.markdown('<div class="section-title">🧮 计算方法</div>', unsafe_allow_html=True)
            for method in concept_data['计算方法']:
                st.markdown(f"- {method}")

        if '核心原则' in concept_data:
            st.markdown('<div class="section-title">💡 核心原则</div>', unsafe_allow_html=True)
            for principle in concept_data['核心原则']:
                st.markdown(f"- {principle}")

        if '影响因素' in concept_data:
            st.markdown('<div class="section-title">🔍 影响因素</div>', unsafe_allow_html=True)
            for factor in concept_data['影响因素']:
                st.markdown(f"- {factor}")

        if '衡量方法' in concept_data:
            st.markdown('<div class="section-title">📏 衡量方法</div>', unsafe_allow_html=True)
            for method in concept_data['衡量方法']:
                st.markdown(f"- {method}")

        if '常用方法' in concept_data:
            st.markdown('<div class="section-title">🛠️ 常用方法</div>', unsafe_allow_html=True)
            for method in concept_data['常用方法']:
                st.markdown(f"- {method}")

        if 'Z-Score 解读' in concept_data:
            st.markdown('<div class="section-title">📊 Z-Score 解读</div>', unsafe_allow_html=True)
            for interpretation in concept_data['Z-Score 解读']:
                st.markdown(f"- {interpretation}")

        if '核心指标' in concept_data:
            st.markdown('<div class="section-title">📈 核心指标</div>', unsafe_allow_html=True)
            for indicator in concept_data['核心指标']:
                st.markdown(f"- {indiccept_data:
            st.markdown('<div class="section-title">📊 相关系数解读</div>', unsafe_allow_html=True)
            for interpretation in concept_data['相关系数解读']:
                st.markdown(f"- {interpretation}")

        if '关键要素' in concept_data:
            st.markdown('<div class="section-title">🔑 关键要素</div>', unsafe_allow_html=True)
            for element in concept_data['关键要素']:
                st.markdown(f"- t.markdown(f'<div class="example-box">{concept_data["实战应用"]}</div>', unsafe_allow_html=True)

        # 案例
        if '案例' in concept_data:
            st.markdown('<div class="section-title">📚 真实案例</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="example-box">{concept_data["案例"]}</div>', unsafe_allow_html=True)

        # 思考题
        if '思考题' in concept_data:
            st.markdown('<div class="section-title">🤔 思考题</div>', unsafe_allow_html=True)
            st.warning(concept_data['思考题'])

    # 标记按钮
    c st.button("↩️ 重新学习", key=f"unmark_{level}_{concept_name}"):
                st.session_state.completed_concepts.discard(f"{level}_{concept_name}")
                st.rerun()
        else:
            if st.button("✅ 标记为已学习", key=f"mark_{level}_{concept_name}", type="primary"):
                st.session_state.completed_concepts.add(f"{level}_{concept_name}")
                st.success(f"太棒了！你已完成「{concept_name}」的学习！")
                st.rerun()

    st.divider()

# 渲染各级别概念
with tab_beginner:
    st.markdown("### 🌱 初级概念 - 金融市场基础")
    st.info("💡 这些是理解金融顺序学习。")

    for concept_name, concept_data in KNOWLEDGE_BASE["初级概念"].items():
        render_concept(concept_name, concept_data, "初级")

with tab_intermediate:
    st.markdown("### 📈 中级概念 - 深入市场分析")
    st.info("💡 在掌握初级概念后，这些中级概念将帮助你进行更深入的市场分析。")

    for concept_name, concept_data in KNOWLEDGE_BASE["中级概念"].items():
        render_concept(concept_name, concept_data, "中级")

with tab_advanced:
    st.markdown("### 🚀 高级概念 - 专业级分析")
    st.info("💡 这些高级概念是专业交易者和量化分析师的必备知识。")

    for concept_name, concept_data in KNOWLEDGE_BASE["高级概念"].items():
        render_concept(concept_name, coata, "高级")

# 底部提示
st.divider()
st.markdown("""
### 💡 学习建议

1. **理论结合实践**：学习概念后，立即到「市场扫描」页面观察真实数据
2. **做好笔记**：记录你的理解和疑问
3. **完成思考题**：每个概念都有思考题，帮助加深理解
4. **定期复习**：金融概念需要反复理解和应用

### 🎯 下一步

- 📝 前往「知识测验」检验学习成果
- 📊 前往「市场扫描」应用所学知识
- 🎮 前往「模拟交易」实战练习（即将推出）
""")
