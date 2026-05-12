"""学习中心 - 金融知识库（支持三语切换）"""
import sys
from pathlib import Path

import streamlit as st

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent.parent))
from modules.i18n import t, render_language_selector

st.set_page_config(
    page_title="Learning Center",
    page_icon="📚",
    layout="wide",
)

# 初始化
if "completed" not in st.session_state:
    st.session_state.completed = set()

# 三语知识库
KNOWLEDGE_BASE = {
    "zh_CN": {
        "title": "📚 金融知识库",
        "subtitle": "**系统学习金融市场核心概念**",
        "progress": "📊 学习进度",
        "completed_text": "已完成",
        "mark_done": "✅ 完成",
        "relearn": "重新学习",
        "definition": "定义",
        "indicators": "指标",
        "principles": "原则",
        "methods": "方法",
        "application": "💡 实战应用",
        "case": "📚 案例",
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
        "concepts": {
            "流动性": {
                "name": "流动性",
                "定义": "资产快速转换为现金而不显著影响价格的能力",
                "指标": ["成交量", "成交额", "买卖价差", "市场深度"],
                "应用": "通过成交额过滤阈值筛选高流动性交易对",
                "案例": "2020年3月流动性危机，比特币24小时暴跌50%"
            },
            "波动率": {
                "name": "波动率",
                "定义": "衡量资产价格变动的剧烈程度",
                "指标": ["历史波动率", "年化波动率", "ATR"],
                "应用": "年化波动率>60%标记为极高风险",
                "案例": "2020年3月VIX从15飙升至82"
            },
            "量价关系": {
                "name": "量价关系",
                "定义": "价格变动与成交量之间的关系",
                "原则": ["放量上涨=强势", "缩量上涨=弱势", "放量下跌=恐慌"],
                "应用": "波动状态列自动识别量价关系",
                "案例": "2021年5月比特币从64000跌至30000"
            },
            "异常检测": {
                "name": "异常检测",
                "定义": "识别偏离正常模式的数据点",
                "方法": ["Z-Score", "移动平均偏离", "布林带"],
                "应用": "告警功能使用Z-Score识别异常",
                "案例": "2021年狗狗币单日涨幅超100%"
            }
        }
    },
    "zh_TW": {
        "title": "📚 金融知識庫",
        "subtitle": "**系統學習金融市場核心概念**",
        "progress": "📊 學習進度",
        "completed_text": "已完成",
        "mark_done": "✅ 完成",
        "relearn": "重新學習",
        "definition": "定義",
        "indicators": "指標",
        "principles": "原則",
        "methods": "方法",
        "application": "💡 實戰應用",
        "case": "📚 案例",
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
        "concepts": {
            "流动性": {
                "name": "流動性",
                "定義": "資產快速轉換為現金而不顯著影響價格的能力",
                "指標": ["成交量", "成交額", "買賣價差", "市場深度"],
                "應用": "通過成交額過濾閾值篩選高流動性交易對",
                "案例": "2020年3月流動性危機，比特幣24小時暴跌50%"
            },
            "波动率": {
                "name": "波動率",
                "定義": "衡量資產價格變動的劇烈程度",
                "指標": ["歷史波動率", "年化波動率", "ATR"],
                "應用": "年化波動率>60%標記為極高風險",
                "案例": "2020年3月VIX從15飆升至82"
            },
            "量价关系": {
                "name": "量價關係",
                "定義": "價格變動與成交量之間的關係",
                "原則": ["放量上漲=強勢", "縮量上漲=弱勢", "放量下跌=恐慌"],
                "應用": "波動狀態列自動識別量價關係",
                "案例": "2021年5月比特幣從64000跌至30000"
            },
            "异常检测": {
                "name": "異常檢測",
                "定義": "識別偏離正常模式的數據點",
                "方法": ["Z-Score", "移動平均偏離", "布林帶"],
                "應用": "告警功能使用Z-Score識別異常",
                "案例": "2021年狗狗幣單日漲幅超100%"
            }
        }
    },
    "en_US": {
        "title": "📚 Financial Knowledge Base",
        "subtitle": "**Systematically learn core financial market concepts**",
        "progress": "📊 Learning Progress",
        "completed_text": "Completed",
        "mark_done": "✅ Complete",
        "relearn": "Relearn",
        "definition": "Definition",
        "indicators": "Indicators",
        "principles": "Principles",
        "methods": "Methods",
        "application": "💡 Practical Application",
        "case": "📚 Case Study",
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
        "concepts": {
            "流动性": {
                "name": "Liquidity",
                "Definition": "The ability of an asset to be quickly converted to cash without significantly affecting its price",
                "Indicators": ["Volume", "Turnover", "Bid-Ask Spread", "Market Depth"],
                "Application": "Filter high-liquidity pairs using volume threshold",
                "Case": "March 2020 liquidity crisis, Bitcoin crashed 50% in 24h"
            },
            "波动率": {
                "name": "Volatility",
                "Definition": "Measures the intensity of asset price changes",
                "Indicators": ["Historical Volatility", "Annualized Volatility", "ATR"],
                "Application": "Annualized Vol > 60% marked as extreme risk",
                "Case": "March 2020 VIX surged from 15 to 82"
            },
            "量价关系": {
                "name": "Volume-Price Relationship",
                "Definition": "The relationship between price changes and trading volume",
                "Principles": ["Volume Surge = Strong", "Volume Shrink = Weak", "Volume Drop = Panic"],
                "Application": "Volume Status column automatically identifies volume-price relationship",
                "Case": "May 2021 Bitcoin dropped from 64000 to 30000"
            },
            "异常检测": {
                "name": "Anomaly Detection",
                "Definition": "Identify data points that deviate from normal patterns",
                "Methods": ["Z-Score", "Moving Average Deviation", "Bollinger Bands"],
                "Application": "Alert function uses Z-Score to identify anomalies",
                "Case": "2021 Dogecoin single-day surge over 100%"
            }
        }
    }
}


def get_current_lang():
    """获取当前语言"""
    if "language" not in st.session_state:
        st.session_state.language = "zh_CN"
    return st.session_state.language


def get_content():
    """获取当前语言的内容"""
    lang = get_current_lang()
    return KNOWLEDGE_BASE.get(lang, KNOWLEDGE_BASE["zh_CN"])


# 侧边栏 - 语言选择器
with st.sidebar:
    render_language_selector()
    st.divider()

    content = get_content()

    st.markdown(f"### {content['progress']}")
    concepts_dict = content["concepts"]
    total = len(concepts_dict)
    done = len(st.session_state.completed)
    pct = int(done / total * 100) if total > 0 else 0
    st.progress(pct / 100)
    st.write(f"{done}/{total} {content['completed_text']} ({pct}%)")

# 获取当前语言内容
content = get_content()

# 标题
st.title(content["title"])
st.markdown(content["subtitle"])

# 主内容
for concept_key, data in content["concepts"].items():
    is_done = concept_key in st.session_state.completed
    concept_name = data["name"]

    with st.expander(f"{'✅' if is_done else '📖'} {concept_name}", expanded=not is_done):
        # 获取定义（根据语言用不同的键）
        lang = get_current_lang()
        if lang == "en_US":
            def_key = "Definition"
            indicators_key = "Indicators"
            principles_key = "Principles"
            methods_key = "Methods"
            application_key = "Application"
            case_key = "Case"
        elif lang == "zh_TW":
            def_key = "定義"
            indicators_key = "指標"
            principles_key = "原則"
            methods_key = "方法"
            application_key = "應用"
            case_key = "案例"
        else:  # zh_CN
            def_key = "定义"
            indicators_key = "指标"
            principles_key = "原则"
            methods_key = "方法"
            application_key = "应用"
            case_key = "案例"

        # 显示定义
        st.markdown(f"**{content['definition']}**: {data[def_key]}")

        # 显示指标/原则/方法
        for key, label_key in [(indicators_key, 'indicators'),
                                (principles_key, 'principles'),
                                (methods_key, 'methods')]:
            if key in data:
                st.markdown(f"**{content[label_key]}**: {', '.join(data[key])}")

        # 实战应用
        st.info(f"**{content['application']}**: {data[application_key]}")

        # 案例
        st.success(f"**{content['case']}**: {data[case_key]}")

        # 完成按钮
        col1, col2 = st.columns([1, 4])
        with col1:
            if is_done:
                if st.button(content['relearn'], key=f"redo_{concept_key}"):
                    st.session_state.completed.discard(concept_key)
                    st.rerun()
            else:
                if st.button(content['mark_done'], key=f"done_{concept_key}"):
                    st.session_state.completed.add(concept_key)
                    st.rerun()

st.divider()

# 学习建议
st.markdown(content['suggestions_title'])
for suggestion in content['suggestions']:
    st.markdown(suggestion)

st.markdown(content['next_title'])
for step in content['next_steps']:
    st.markdown(step)
