"""学习中心 - 金融知识库"""
import streamlit as st

st.set_page_config(
    page_title="学习中心",
    page_icon="📚",
    layout="wide",
)

st.title("📚 金融知识库")
st.markdown("**系统学习金融市场核心概念**")

# 初始化
if "completed" not in st.session_state:
    st.session_state.completed = set()

# 知识库
concepts = {
    "流动性": {
        "定义": "资产快速转换为现金而不显著影响价格的能力",
        "指标": ["成交量", "成交额", "买卖价差", "市场深度"],
        "应用": "通过成交额过滤阈值筛选高流动性交易对",
        "案例": "2020年3月流动性危机，比特币24小时暴跌50%"
    },
    "波动率": {
        "定义": "衡量资产价格变动的剧烈程度",
        "指标": ["历史波动率", "年化波动率", "ATR"],
        "应用": "年化波动率>60%标记为极高风险",
        "案例": "2020年3月VIX从15飙升至82"
    },
    "量价关系": {
        "定义": "价格变动与成交量之间的关系",
        "原则": ["放量上涨=强势", "缩量上涨=弱势", "放量下跌=恐慌"],
        "应用": "波动状态列自动识别量价关系",
        "案例": "2021年5月比特币从64000跌至30000"
    },
    "异常检测": {
        "定义": "识别偏离正常模式的数据点",
        "方法": ["Z-Score", "移动平均偏离", "布林带"],
        "应用": "告警功能使用Z-Score识别异常",
        "案例": "2021年狗狗币单日涨幅超100%"
    }
}

# 侧边栏
with st.sidebar:
    st.markdown("### 📊 学习进度")
    total = len(concepts)
    done = len(st.session_state.completed)
    pct = int(done / total * 100) if total > 0 else 0
    st.progress(pct / 100)
    st.write(f"{done}/{total} 已完成 ({pct}%)")

# 主内容
for name, data in concepts.items():
    is_done = name in st.session_state.completed
    
    with st.expander(f"{'✅' if is_done else '📖'} {name}", expanded=not is_done):
        st.markdown(f"**定义**: {data['定义']}")
        
        for key in ['指标', '原则', '方法']:
            if key in data:
                st.markdown(f"**{key}**: {', '.join(data[key])}")
        
        st.info(f"💡 **实战应用**: {data['应用']}")
        st.success(f"📚 **案例**: {data['案例']}")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if is_done:
                if st.button("重新学习", key=f"redo_{name}"):
                    st.session_state.completed.discard(name)
                    st.rerun()
            else:
                if st.button("✅ 完成", key=f"done_{name}"):
                    st.session_state.completed.add(name)
                    st.rerun()

st.divider()
st.markdown("""
### 💡 学习建议
1. 理论结合实践 - 学习后到市场扫描页面观察真实数据
2. 完成所有概念学习
3. 定期复习巩固

### 🎯 下一步
- 📊 前往市场扫描应用所学知识
- 📝 完成知识测验(即将推出)
""")
