"""学习中心 - 金融知识库（完整支持三语切换）"""
import sys
from pathlib import Path

import streamlit as st

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent.parent))
from modules.i18n import render_language_selector

st.set_page_config(
    page_title="Learning Center",
    page_icon="📚",
    layout="wide",
)

# 初始化
if "completed" not in st.session_state:
    st.session_state.completed = set()
if "language" not in st.session_state:
    st.session_state.language = "zh_CN"


# UI 文字翻译
UI_TEXT = {
    "zh_CN": {
        "title": "📚 金融知识库",
        "subtitle": "**系统学习金融市场核心概念**",
        "progress": "📊 学习进度",
        "completed_text": "已完成",
        "mark_done": "✅ 完成",
        "relearn": "重新学习",
        "definition_label": "定义",
        "indicators_label": "指标",
        "principles_label": "原则",
        "methods_label": "方法",
        "application_label": "💡 实战应用",
        "case_label": "📚 案例",
        "suggestions_title": "### 💡 学习建议",
        "suggestions": [
            "1. 理论结合实践 - 学习后到市场扫描页面观察真实数据",
            "2. 完成所有概念学习",
            "3. 定期复习巩固"
        ],
        "next_title": "### 🎯 下一步",
        "next_steps": [
            "- 📊 前往市场扫描应用所学知识",
            "- 📝 完成知识测验(即将推出)"
        ],
    },
    "zh_TW": {
        "title": "📚 金融知識庫",
        "subtitle": "**系統學習金融市場核心概念**",
        "progress": "📊 學習進度",
        "completed_text": "已完成",
        "mark_done": "✅ 完成",
        "relearn": "重新學習",
        "definition_label": "定義",
        "indicators_label": "指標",
        "principles_label": "原則",
        "methods_label": "方法",
        "application_label": "💡 實戰應用",
        "case_label": "📚 案例",
        "suggestions_title": "### 💡 學習建議",
        "suggestions": [
            "1. 理論結合實踐 - 學習後到市場掃描頁面觀察真實數據",
            "2. 完成所有概念學習",
            "3. 定期複習鞏固"
        ],
        "next_title": "### 🎯 下一步",
        "next_steps": [
            "- 📊 前往市場掃描應用所學知識",
            "- 📝 完成知識測驗(即將推出)"
        ],
    },
    "en_US": {
        "title": "📚 Financial Knowledge Base",
        "subtitle": "**Systematically learn core financial market concepts**",
        "progress": "📊 Learning Progress",
        "completed_text": "Completed",
        "mark_done": "✅ Complete",
        "relearn": "Relearn",
        "definition_label": "Definition",
        "indicators_label": "Indicators",
        "principles_label": "Principles",
        "methods_label": "Methods",
        "application_label": "💡 Practical Application",
        "case_label": "📚 Case Study",
        "suggestions_title": "### 💡 Learning Tips",
        "suggestions": [
            "1. Combine theory with practice - Apply concepts to real market data",
            "2. Complete all concept learning",
            "3. Review regularly to reinforce knowledge"
        ],
        "next_title": "### 🎯 Next Steps",
        "next_steps": [
            "- 📊 Go to Market Scan to apply what you learned",
            "- 📝 Complete Knowledge Test (Coming Soon)"
        ],
    }
}


# 概念数据 - 使用英文 key，每种语言都有完整翻译
CONCEPTS = {
    "liquidity": {
        "zh_CN": {
            "name": "流动性",
            "definition": "资产快速转换为现金而不显著影响价格的能力",
            "indicators": ["成交量", "成交额", "买卖价差", "市场深度"],
            "application": "通过成交额过滤阈值筛选高流动性交易对",
            "case": "2020年3月流动性危机，比特币24小时暴跌50%"
        },
        "zh_TW": {
            "name": "流動性",
            "definition": "資產快速轉換為現金而不顯著影響價格的能力",
            "indicators": ["成交量", "成交額", "買賣價差", "市場深度"],
            "application": "通過成交額過濾閾值篩選高流動性交易對",
            "case": "2020年3月流動性危機，比特幣24小時暴跌50%"
        },
        "en_US": {
            "name": "Liquidity",
            "definition": "The ability of an asset to be quickly converted to cash without significantly affecting its price",
            "indicators": ["Volume", "Turnover", "Bid-Ask Spread", "Market Depth"],
            "application": "Filter high-liquidity pairs using volume threshold",
            "case": "March 2020 liquidity crisis: Bitcoin crashed 50% in 24 hours"
        }
    },
    "volatility": {
        "zh_CN": {
            "name": "波动率",
            "definition": "衡量资产价格变动的剧烈程度",
            "indicators": ["历史波动率", "年化波动率", "ATR"],
            "application": "年化波动率>60%标记为极高风险",
            "case": "2020年3月VIX从15飙升至82"
        },
        "zh_TW": {
            "name": "波動率",
            "definition": "衡量資產價格變動的劇烈程度",
            "indicators": ["歷史波動率", "年化波動率", "ATR"],
            "application": "年化波動率>60%標記為極高風險",
            "case": "2020年3月VIX從15飆升至82"
        },
        "en_US": {
            "name": "Volatility",
            "definition": "Measures the intensity of asset price fluctuations",
            "indicators": ["Historical Volatility", "Annualized Volatility", "ATR"],
            "application": "Annualized volatility > 60% is marked as extreme risk",
            "case": "March 2020: VIX surged from 15 to 82"
        }
    },
    "volume_price": {
        "zh_CN": {
            "name": "量价关系",
            "definition": "价格变动与成交量之间的关系",
            "principles": ["放量上涨=强势", "缩量上涨=弱势", "放量下跌=恐慌"],
            "application": "波动状态列自动识别量价关系",
            "case": "2021年5月比特币从64000跌至30000"
        },
        "zh_TW": {
            "name": "量價關係",
            "definition": "價格變動與成交量之間的關係",
            "principles": ["放量上漲=強勢", "縮量上漲=弱勢", "放量下跌=恐慌"],
            "application": "波動狀態列自動識別量價關係",
            "case": "2021年5月比特幣從64000跌至30000"
        },
        "en_US": {
            "name": "Volume-Price Relationship",
            "definition": "The relationship between price changes and trading volume",
            "principles": ["Volume Surge + Rise = Strong", "Volume Shrink + Rise = Weak", "Volume Surge + Drop = Panic"],
            "application": "Volume Status column automatically identifies volume-price relationships",
            "case": "May 2021: Bitcoin dropped from 64,000 to 30,000"
        }
    },
    "anomaly": {
        "zh_CN": {
            "name": "异常检测",
            "definition": "识别偏离正常模式的数据点",
            "methods": ["Z-Score", "移动平均偏离", "布林带"],
            "application": "告警功能使用Z-Score识别异常",
            "case": "2021年狗狗币单日涨幅超100%"
        },
        "zh_TW": {
            "name": "異常檢測",
            "definition": "識別偏離正常模式的數據點",
            "methods": ["Z-Score", "移動平均偏離", "布林帶"],
            "application": "告警功能使用Z-Score識別異常",
            "case": "2021年狗狗幣單日漲幅超100%"
        },
        "en_US": {
            "name": "Anomaly Detection",
            "definition": "Identify data points that deviate from normal patterns",
            "methods": ["Z-Score", "Moving Average Deviation", "Bollinger Bands"],
            "application": "Alert system uses Z-Score to identify anomalies",
            "case": "2021: Dogecoin single-day surge over 100%"
        }
    }
}


def get_lang():
    """获取当前语言"""
    return st.session_state.get("language", "zh_CN")


# ==========  侧边栏 - 语言选择器 ==========
with st.sidebar:
    render_language_selector()
    st.divider()

    # 获取当前语言的 UI 文字
    lang = get_lang()
    ui = UI_TEXT[lang]

    st.markdown(f"### {ui['progress']}")
    total = len(CONCEPTS)
    done = len(st.session_state.completed)
    pct = int(done / total * 100) if total > 0 else 0
    st.progress(pct / 100)
    st.write(f"{done}/{total} {ui['completed_text']} ({pct}%)")


# ========== 主内容区 ==========
lang = get_lang()
ui = UI_TEXT[lang]

# 标题
st.title(ui["title"])
st.markdown(ui["subtitle"])

# 渲染每个概念
for concept_key, concept_translations in CONCEPTS.items():
    # 获取当前语言的概念数据
    data = concept_translations[lang]

    is_done = concept_key in st.session_state.completed
    concept_name = data["name"]

    with st.expander(f"{'✅' if is_done else '📖'} {concept_name}", expanded=not is_done):
        # 显示定义
        st.markdown(f"**{ui['definition_label']}**: {data['definition']}")

        # 显示指标（如果存在）
        if "indicators" in data:
            st.markdown(f"**{ui['indicators_label']}**: {', '.join(data['indicators'])}")

        # 显示原则（如果存在）
        if "principles" in data:
            st.markdown(f"**{ui['principles_label']}**: {', '.join(data['principles'])}")

        # 显示方法（如果存在）
        if "methods" in data:
            st.markdown(f"**{ui['methods_label']}**: {', '.join(data['methods'])}")

        # 实战应用
        st.info(f"**{ui['application_label']}**: {data['application']}")

        # 案例
        st.success(f"**{ui['case_label']}**: {data['case']}")

        # 完成按钮
        col1, col2 = st.columns([1, 4])
        with col1:
            if is_done:
                if st.button(ui['relearn'], key=f"redo_{concept_key}"):
                    st.session_state.completed.discard(concept_key)
                    st.rerun()
            else:
                if st.button(ui['mark_done'], key=f"done_{concept_key}"):
                    st.session_state.completed.add(concept_key)
                    st.rerun()

# 底部建议和下一步
st.divider()

st.markdown(ui['suggestions_title'])
for suggestion in ui['suggestions']:
    st.markdown(suggestion)

st.markdown(ui['next_title'])
for step in ui['next_steps']:
    st.markdown(step)
