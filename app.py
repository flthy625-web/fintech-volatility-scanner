"""Fintech 市场波动扫描器 - Streamlit 应用主入口"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Iterable

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st
import yfinance as yf
from plotly.subplots import make_subplots

# ---------------------------------------------------------------------------
# 页面与全局样式
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Fintech 市场波动扫描器",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    :root {
        --surface-0: #0b1020;
        --surface-1: #111832;
        --surface-2: #1a2347;
        --text-primary: #e6ecff;
        --text-muted: #8a95c4;
        --accent: #5eead4;
        --accent-warn: #fbbf24;
        --accent-danger: #f87171;
        --accent-calm: #60a5fa;
    }

    html, body, [class*="stApp"] {
        background: radial-gradient(
                circle at top left,
                #1a2347 0%,
                var(--surface-0) 45%,
                #05070f 100%
            );
        color: var(--text-primary);
    }

    .block-container { padding-top: 2.2rem; padding-bottom: 3rem; }

    .hero-wrap {
        border: 1px solid rgba(94, 234, 212, 0.18);
        background: linear-gradient(135deg, rgba(94, 234, 212, 0.08), rgba(96, 165, 250, 0.04));
        border-radius: 18px;
        padding: 1.6rem 2rem;
        margin-bottom: 1.6rem;
        box-shadow: 0 20px 60px -30px rgba(94, 234, 212, 0.45);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin: 0;
        background: linear-gradient(90deg, #5eead4, #60a5fa 60%, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        color: var(--text-muted);
        font-size: 0.95rem;
        margin-top: 0.4rem;
    }
    .hero-chips { margin-top: 0.9rem; display: flex; gap: 0.5rem; flex-wrap: wrap; }
    .chip {
        background: rgba(94, 234, 212, 0.12);
        border: 1px solid rgba(94, 234, 212, 0.35);
        color: var(--accent);
        padding: 0.2rem 0.7rem;
        border-radius: 999px;
        font-size: 0.75rem;
        letter-spacing: 0.4px;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        height: 100%;
    }
    .metric-label {
        color: var(--text-muted);
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value { font-size: 1.55rem; font-weight: 700; margin-top: 0.25rem; }
    .metric-delta-up { color: var(--accent); font-size: 0.9rem; }
    .metric-delta-down { color: var(--accent-danger); font-size: 0.9rem; }
    .metric-delta-flat { color: var(--text-muted); font-size: 0.9rem; }

    .section-title {
        font-size: 1.05rem;
        font-weight: 600;
        margin: 1.8rem 0 0.8rem;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-title::before {
        content: "";
        width: 6px;
        height: 18px;
        border-radius: 3px;
        background: linear-gradient(180deg, var(--accent), var(--accent-calm));
    }

    /* 侧边栏 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0e1530 0%, #070a18 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    section[data-testid="stSidebar"] * { color: var(--text-primary); }

    /* 表格 */
    .stDataFrame { border-radius: 12px; overflow: hidden; }

    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 资产预设
# ---------------------------------------------------------------------------

PRESETS: dict[str, list[str]] = {
    "美股科技": ["AAPL", "MSFT", "NVDA", "GOOGL", "META", "AMZN", "TSLA"],
    "美股指数": ["^GSPC", "^IXIC", "^DJI", "^RUT", "^VIX"],
    "加密货币": ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD"],
    "外汇": ["EURUSD=X", "USDJPY=X", "GBPUSD=X", "USDCNY=X", "AUDUSD=X"],
    "大宗商品": ["GC=F", "SI=F", "CL=F", "NG=F", "HG=F"],
}

TIMEFRAMES: dict[str, tuple[str, str]] = {
    "1 个月": ("1mo", "1d"),
    "3 个月": ("3mo", "1d"),
    "6 个月": ("6mo", "1d"),
    "1 年": ("1y", "1d"),
    "2 年": ("2y", "1wk"),
    "5 年": ("5y", "1wk"),
}

# 实时扫描配置
REALTIME_REFRESH_INTERVAL = 30  # 秒

# Binance API 配置
BINANCE_API_BASE = "https://api.binance.com"
BINANCE_24H_TICKER = f"{BINANCE_API_BASE}/api/v3/ticker/24hr"


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------


@dataclass
class VolStats:
    symbol: str
    last_price: float
    pct_change_1d: float
    pct_change_period: float
    hv_annualized: float
    atr_pct: float
    max_drawdown: float
    zscore: float
    bucket: str  # 低 / 中 / 高 / 极高


@dataclass
class BinanceTicker:
    symbol: str
    last_price: float
    price_change_pct: float
    high_24h: float
    low_24h: float
    volume_24h: float
    quote_volume_24h: float
    trades_count: int


# ---------------------------------------------------------------------------
# 数据获取与计算
# ---------------------------------------------------------------------------


@st.cache_data(ttl=300, show_spinner=False)
def load_history(symbol: str, period: str, interval: str) -> pd.DataFrame:
    """拉取历史行情，失败返回空表而非抛出。"""
    try:
        df = yf.download(
            symbol,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=True,
            threads=False,
        )
    except Exception:
        return pd.DataFrame()
    if df is None or df.empty:
        return pd.DataFrame()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.dropna(how="all").copy()
    df.index = pd.to_datetime(df.index)
    return df


def _trading_periods_per_year(interval: str) -> int:
    return {"1d": 252, "1wk": 52, "1mo": 12}.get(interval, 252)


def compute_stats(symbol: str, df: pd.DataFrame, interval: str) -> VolStats | None:
    if df.empty or "Close" not in df.columns or len(df) < 5:
        return None

    close = df["Close"].astype(float)
    returns = close.pct_change().dropna()
    if returns.empty:
        return None

    periods = _trading_periods_per_year(interval)
    hv = float(returns.std() * math.sqrt(periods) * 100)

    # ATR%
    high = df["High"].astype(float)
    low = df["Low"].astype(float)
    prev_close = close.shift(1)
    tr = pd.concat(
        [(high - low), (high - prev_close).abs(), (low - prev_close).abs()], axis=1
    ).max(axis=1)
    atr = tr.rolling(14).mean().iloc[-1]
    atr_pct = float(atr / close.iloc[-1] * 100) if close.iloc[-1] else 0.0

    # 回撤
    cummax = close.cummax()
    drawdown = (close / cummax - 1.0) * 100
    max_dd = float(drawdown.min())

    # z-score（以最近一根 vs. 过去 60 根标准差）
    window = min(60, max(20, len(returns) - 1))
    recent = returns.iloc[-1]
    std = returns.iloc[-window:].std()
    zscore = float(recent / std) if std and not np.isnan(std) else 0.0

    pct_1d = float(returns.iloc[-1] * 100)
    pct_period = float((close.iloc[-1] / close.iloc[0] - 1) * 100)

    bucket = _bucket_hv(hv)

    return VolStats(
        symbol=symbol,
        last_price=float(close.iloc[-1]),
        pct_change_1d=pct_1d,
        pct_change_period=pct_period,
        hv_annualized=hv,
        atr_pct=atr_pct,
        max_drawdown=max_dd,
        zscore=zscore,
        bucket=bucket,
    )


def _bucket_hv(hv: float) -> str:
    if hv < 15:
        return "低"
    if hv < 30:
        return "中"
    if hv < 60:
        return "高"
    return "极高"


def scan_universe(
    symbols: Iterable[str], period: str, interval: str
) -> tuple[list[VolStats], dict[str, pd.DataFrame]]:
    results: list[VolStats] = []
    histories: dict[str, pd.DataFrame] = {}
    for sym in symbols:
        hist = load_history(sym, period, interval)
        histories[sym] = hist
        stats = compute_stats(sym, hist, interval)
        if stats is not None:
            results.append(stats)
    return results, histories


# ---------------------------------------------------------------------------
# Binance API 数据获取
# ---------------------------------------------------------------------------


@st.cache_data(ttl=60, show_spinner=False)
def fetch_binance_usdt_pairs() -> list[BinanceTicker]:
    """获取所有 USDT 交易对的 24h 数据"""
    try:
        response = requests.get(BINANCE_24H_TICKER, timeout=10)
        response.raise_for_status()
        data = response.json()

        tickers: list[BinanceTicker] = []
        for item in data:
            symbol = item.get("symbol", "")
            # 只保留 USDT 交易对
            if not symbol.endswith("USDT"):
                continue

            try:
                ticker = BinanceTicker(
                    symbol=symbol,
                    last_price=float(item.get("lastPrice", 0)),
                    price_change_pct=float(item.get("priceChangePercent", 0)),
                    high_24h=float(item.get("highPrice", 0)),
                    low_24h=float(item.get("lowPrice", 0)),
                    volume_24h=float(item.get("volume", 0)),
                    quote_volume_24h=float(item.get("quoteVolume", 0)),
                    trades_count=int(item.get("count", 0)),
                )
                tickers.append(ticker)
            except (ValueError, TypeError):
                continue

        return tickers
    except requests.RequestException as e:
        st.error(f"Binance API 请求失败: {e}")
        return []


def build_binance_table(tickers: list[BinanceTicker]) -> pd.DataFrame:
    """构建 Binance USDT 交易对数据表"""
    # 计算所有交易对的平均每笔成交额，用于判断量能
    avg_trade_sizes = [
        t.quote_volume_24h / t.trades_count if t.trades_count > 0 else 0
        for t in tickers
    ]
    median_trade_size = np.median([x for x in avg_trade_sizes if x > 0]) if avg_trade_sizes else 0

    rows = []
    for t in tickers:
        # 计算该交易对的平均每笔成交额
        avg_trade_size = t.quote_volume_24h / t.trades_count if t.trades_count > 0 else 0

        # 计算 24h 振幅
        amplitude = (t.high_24h - t.low_24h) / t.low_24h * 100 if t.low_24h > 0 else 0

        # 判断波动状态
        volume_status = ""
        if t.price_change_pct > 10 and avg_trade_size > median_trade_size * 1.5:
            volume_status = "🚀 放量上涨"
        elif t.price_change_pct > 5 and avg_trade_size < median_trade_size * 0.7:
            volume_status = "⚠️ 缩量背离"
        elif t.price_change_pct < -10 and avg_trade_size > median_trade_size * 1.5:
            volume_status = "📉 放量下跌"
        elif t.price_change_pct < -5 and avg_trade_size < median_trade_size * 0.7:
            volume_status = "🔻 缩量下跌"
        elif abs(t.price_change_pct) > 15:
            volume_status = "⚡ 剧烈波动"
        elif amplitude > 20:
            volume_status = "🌊 高振幅"
        else:
            volume_status = "➖ 正常"

        rows.append({
            "交易对": t.symbol,
            "最新价": t.last_price,
            "24h涨跌%": round(t.price_change_pct, 2),
            "24h最高": t.high_24h,
            "24h最低": t.low_24h,
            "24h振幅%": round(amplitude, 2),
            "24h成交量": round(t.volume_24h, 2),
            "24h成交额(USDT)": round(t.quote_volume_24h, 2),
            "成交笔数": t.trades_count,
            "平均每笔(USDT)": round(avg_trade_size, 2),
            "波动状态": volume_status,
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# UI 组件
# ---------------------------------------------------------------------------


def render_hero(symbol_count: int, timeframe_label: str, is_realtime: bool = False) -> None:
    realtime_indicator = ""
    if is_realtime:
        realtime_indicator = '<span class="chip" style="background: rgba(248, 113, 113, 0.22); border-color: #f87171; color: #f87171; animation: pulse 2s infinite;">🔴 实时扫描中</span>'

    st.markdown(
        f"""
        <div class="hero-wrap">
            <p class="hero-title">Fintech 市场波动扫描器</p>
            <p class="hero-subtitle">
                基于历史波动率、ATR、回撤与异常 z-score 的多资产实时扫描面板。
                数据源 Yahoo Finance，每 5 分钟缓存一次。
            </p>
            <div class="hero-chips">
                <span class="chip">已加载 {symbol_count} 个标的</span>
                <span class="chip">观察窗口 · {timeframe_label}</span>
                <span "chip">更新时间 · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
                {realtime_indicator}
            </div>
        </div>
        <style>
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.6; }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label: str, value: str, delta: str = "", trend: str = "flat") -> str:
    cls = {
        "up": "metric-delta-up",
        "down": "metric-delta-down",
        "flat": "metric-delta-flat",
    }[trend]
    delta_html = f'<div class="{cls}">{delta}</div>' if delta else ""
    return f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
    """


def render_summary_cards(stats_list: list[VolStats]) -> None:
    if not stats_list:
        st.info("暂无可用数据，请调整标的或时间窗口后重试。")
        return

    avg_hv = np.mean([s.hv_annualized for s in stats_list])
    avg_dd = np.mean([s.max_drawdown for s in stats_list])
    top_mover = max(stats_list, key=lambda s: abs(s.pct_change_1d))
    extreme = [s for s in stats_list if abs(s.zscore) >= 2]

    cards = [
        render_metric_card(
            "平均年化波动率",
            f"{avg_hv:.1f}%",
            f"{len(stats_list)} 个标的均值",
            "flat",
        ),
        render_metric_card(
            "平均最大回撤",
            f"{avg_dd:.1f}%",
            "基于区间收盘价",
            "down" if avg_dd < -5 else "flat",
        ),
        render_metric_card(
            "单日最大变动",
            f"{top_mover.pct_change_1d:+.2f}%",
            top_mover.symbol,
            "up" if top_mover.pct_change_1d >= 0 else "down",
        ),
        render_metric_card(
            "异常波动标的",
            f"{len(extreme)}",
            "|z-score| ≥ 2",
            "down" if extreme else "flat",
        ),
    ]

    cols = st.columns(4, gap="medium")
    for col, html in zip(cols, cards):
        with col:
            st.markdown(html, unsafe_allow_html=True)


def build_scanner_table(stats_list: list[VolStats]) -> pd.DataFrame:
    rows = [
        {
            "标的": s.symbol,
            "最新价": round(s.last_price, 4),
            "日涨跌%": round(s.pct_change_1d, 2),
            "区间涨跌%": round(s.pct_change_period, 2),
            "年化波动率%": round(s.hv_annualized, 2),
            "ATR%": round(s.atr_pct, 2),
            "最大回撤%": round(s.max_drawdown, 2),
            "Z-Score": round(s.zscore, 2),
            "波动等级": s.bucket,
        }
        for s in stats_list
    ]
    return pd.DataFrame(rows)


def render_scanner_table(df: pd.DataFrame) -> None:
    if df.empty:
        return

    def _color_bucket(val: str) -> str:
        palette = {
            "低": "background-color: rgba(94, 234, 212, 0.18); color: #5eead4;",
            "中": "background-color: rgba(96, 165, 250, 0.18); color: #60a5fa;",
            "高": "background-color: rgba(251, 191, 36, 0.20); color: #fbbf24;",
            "极高": "background-color: rgba(248, 113, 113, 0.22); color: #f87171;",
        }
        return palette.get(val, "")

    styled = (
        df.style.map(_color_bucket, subset=["波动等级"])
        .background_gradient(
            subset=["年化波动率%", "ATR%"], cmap="YlOrRd", vmin=0
        )
        .format(
            {
                "最新价": "{:,.4f}",
                "日涨跌%": "{:+.2f}",
                "区间涨跌%": "{:+.2f}",
                "年化波动率%": "{:.2f}",
                "ATR%": "{:.2f}",
                "最大回撤%": "{:.2f}",
                "Z-Score": "{:+.2f}",
            }
        )
    )
    st.dataframe(styled, use_container_width=True, height=min(520, 60 + 36 * len(df)))


def render_volatility_chart(
    symbol: str, df: pd.DataFrame, interval: str
) -> None:
    if df.empty:
        st.warning(f"{symbol} 没有可用的历史数据。")
        return

    close = df["Close"].astype(float)
    returns = close.pct_change()
    periods = _trading_periods_per_year(interval)
    rolling_hv = returns.rolling(20).std() * math.sqrt(periods) * 100

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights=[0.62, 0.38],
        subplot_titles=(f"{symbol} · 价格走势", "20 周期年化波动率 (%)"),
    )

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name=symbol,
            increasing_line_color="#5eead4",
            decreasing_line_color="#f87171",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=rolling_hv.index,
            y=rolling_hv,
            mode="lines",
            line=dict(color="#60a5fa", width=2),
            fill="tozeroy",
            fillcolor="rgba(96, 165, 250, 0.18)",
            name="年化 HV",
        ),
        row=2,
        col=1,
    )

    fig.update_layout(
        template="plotly_dark",
        height=560,
        margin=dict(l=20, r=20, t=50, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6ecff"),
        showlegend=False,
        xaxis_rangeslider_visible=False,
    )
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)")
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)")
    st.plotly_chart(fig, use_container_width=True)


def render_correlation_heatmap(histories: dict[str, pd.DataFrame]) -> None:
    closes: dict[str, pd.Series] = {}
    for sym, df in histories.items():
        if not df.empty and "Close" in df.columns:
            closes[sym] = df["Close"].astype(float).pct_change()

    if len(closes) < 2:
        st.info("至少需要 2 个有效标的才能生成相关性矩阵。")
        return

    corr = pd.DataFrame(closes).dropna(how="all").corr()
    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.index,
            colorscale="RdBu",
            zmid=0,
            zmin=-1,
            zmax=1,
            text=np.round(corr.values, 2),
            texttemplate="%{text}",
            textfont=dict(size=11),
            hovertemplate="%{y} ↔ %{x}<br>ρ = %{z:.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        template="plotly_dark",
        height=max(360, 40 * len(corr)),
        margin=dict(l=20, r=20, t=10, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e6ecff"),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_alerts(
    stats_list: list[VolStats], hv_threshold: float, z_threshold: float
) -> None:
    triggered = [
        s
        for s in stats_list
        if s.hv_annualized >= hv_threshold or abs(s.zscore) >= z_threshold
    ]
    if not triggered:
        st.success("当前条件下暂无触发告警的标的。")
        return

    for s in sorted(triggered, key=lambda x: -abs(x.zscore)):
        reasons = []
        if s.hv_annualized >= hv_threshold:
            reasons.append(f"年化波动率 {s.hv_annualized:.1f}% ≥ {hv_threshold:.0f}%")
        if abs(s.zscore) >= z_threshold:
            reasons.append(f"z-score {s.zscore:+.2f}")
        severity = "error" if s.bucket == "极高" or abs(s.zscore) >= 3 else "warning"
        message = f"**{s.symbol}** · {s.bucket}波动 · " + " · ".join(reasons)
        if severity == "error":
            st.error(message)
        else:
            st.warning(message)


def render_binance_table(df: pd.DataFrame) -> None:
    """渲染 Binance USDT 交易对数据表"""
    if df.empty:
        st.info("暂无 Binance 数据")
        return

    def _color_change(val: float) -> str:
        if val > 0:
            return "color: #5eead4;"
        elif val < 0:
            return "color: #f87171;"
        return "color: #8a95c4;"

    def _color_status(val: str) -> str:
        if "放量上涨" in val:
            return "background-color: rgba(94, 234, 212, 0.25); color: #5eead4; font-weight: 600;"
        elif "缩量背离" in val:
            return "background-color: rgba(251, 191, 36, 0.25); color: #fbbf24; font-weight: 600;"
        elif "放量下跌" in val:
            return "background-color: rgba(248, 113, 113, 0.25); color: #f87171; font-weight: 600;"
        elif "剧烈波动" in val:
            return "background-color: rgba(167, 139, 250, 0.25); color: #a78bfa; font-weight: 600;"
        elif "高振幅" in val:
            return "background-color: rgba(96, 165, 250, 0.25); color: #60a5fa; font-weight: 600;"
        return "color: #8a95c4;"

    styled = (
        df.style.map(_color_change, subset=["24h涨跌%"])
        .map(_color_status, subset=["波动状态"])
        .background_gradient(subset=["24h振幅%"], cmap="YlOrRd", vmin=0)
        .format(
            {
                "最新价": "{:,.8f}",
                "24h涨跌%": "{:+.2f}",
                "24h最高": "{:,.8f}",
                "24h最低": "{:,.8f}",
                "24h振幅%": "{:.2f}",
                "24h成交量": "{:,.2f}",
                "24h成交额(USDT)": "{:,.2f}",
                "成交笔数": "{:,}",
                "平均每笔(USDT)": "{:,.2f}",
            }
        )
    )
    st.dataframe(styled, use_container_width=True, height=600)


# ---------------------------------------------------------------------------
# 侧边栏
# ---------------------------------------------------------------------------


def render_sidebar() -> dict:
    with st.sidebar:
        st.markdown("### 扫描配置")

        preset_name = st.selectbox(
            "资产预设",
            options=list(PRESETS.keys()),
            index=0,
            help="选择预设标的组合，或在下方自行编辑列表。",
        )
        default_symbols = ", ".join(PRESETS[preset_name])
        symbols_raw = st.text_area(
            "标的列表（逗号或换行分隔）",
            value=default_symbols,
            height=110,
        )

        timeframe_label = st.selectbox(
            "时间窗口",
            options=list(TIMEFRAMES.keys()),
            index=2,
        )

        st.divider()
        st.markdown("### 告警阈值")
        hv_threshold = st.slider(
            "年化波动率阈值 (%)", min_value=5, max_value=150, value=40, step=5
        )
        z_threshold = st.slider(
            "|Z-Score| 阈值", min_value=1.0, max_value=4.0, value=2.0, step=0.5
        )

        st.divider()
        st.markdown("### 实时扫描")

        # 初始化 session state
        if "realtime_scanning" not in st.session_state:
            st.session_state.realtime_scanning = False
        if "scan_count" not in st.session_state:
            st.session_state.scan_count = 0

        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "🔴 开始实时扫描" if not st.session_state.realtime_scanning else "⏸️ 停止扫描",
                use_container_width=True,
                type="primary" if not st.session_state.realtime_scanning else "secondary",
            ):
                st.session_state.realtime_scanning = not st.session_state.realtime_scanning
                if st.session_state.realtime_scanning:
                    st.session_state.scan_count = 0
                    st.cache_data.clear()
                st.rerun()

        with col2:
            refresh = st.button("🔄 手动刷新", use_container_width=True)
            if refresh:
                st.cache_data.clear()
                st.rerun()

        if st.session_state.realtime_scanning:
            refresh_interval = st.slider(
                "刷新间隔（秒）",
                min_value=10,
                max_value=300,
                value=REALTIME_REFRESH_INTERVAL,
                step=10,
                help="实时扫描的数据刷新间隔",
            )
            st.info(f"⏱️ 已扫描 {st.session_state.scan_count} 次 · 每 {refresh_interval} 秒自动刷新")
        else:
            refresh_interval = REALTIME_REFRESH_INTERVAL

        st.caption("数据来源：Yahoo Finance · 仅供研究参考，不构成投资建议。")

    symbols = [
        s.strip().upper()
        for s in symbols_raw.replace("\n", ",").split(",")
        if s.strip()
    ]
    # 去重且保留顺序
    seen: set[str] = set()
    unique_symbols = [s for s in symbols if not (s in seen or seen.add(s))]

    period, interval = TIMEFRAMES[timeframe_label]
    return {
        "symbols": unique_symbols,
        "period": period,
        "interval": interval,
        "timeframe_label": timeframe_label,
        "hv_threshold": hv_threshold,
        "z_threshold": z_threshold,
        "refresh_interval": refresh_interval,
    }


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------


def main() -> None:
    config = render_sidebar()

    # 实时扫描逻辑
    is_realtime = st.session_state.get("realtime_scanning", False)
    render_hero(len(config["symbols"]), config["timeframe_label"], is_realtime)

    if not config["symbols"]:
        st.warning("请在左侧输入至少一个有效标的。")
        return

    with st.spinner("正在拉取并计算各标的波动指标…"):
        stats_list, histories = scan_universe(
            config["symbols"], config["period"], config["interval"]
        )

    # 实时扫描自动刷新
    if is_realtime:
        st.session_state.scan_count += 1
        time.sleep(config["refresh_interval"])
        st.cache_data.clear()
        st.rerun()

    render_summary_cards(stats_list)

    # Binance 数据获取按钮
    st.divider()
    col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 6])
    with col_btn1:
        if st.button("📊 获取 Binance USDT 交易对", use_container_width=True, type="primary"):
            st.session_state.show_binance = True
            st.session_state.binance_data = None  # 清除旧数据
    with col_btn2:
        if st.button("🔄 刷新 Binance 数据", use_container_width=True):
            st.cache_data.clear()
            st.session_state.binance_data = None

    # 显示 Binance 数据
    if st.session_state.get("show_binance", False):
        st.markdown('<div class="section-title">Binance USDT 交易对 24h 数据</div>', unsafe_allow_html=True)

        with st.spinner("正在从 Binance API 获取数据..."):
            if st.session_state.get("binance_data") is None:
                tickers = fetch_binance_usdt_pairs()
                st.session_state.binance_data = tickers
            else:
                tickers = st.session_state.binance_data

        if tickers:
            # 核心过滤：仅保留 24h 成交额 > 500 万 USDT 的交易对
            tickers = [t for t in tickers if t.quote_volume_24h > 5_000_000]

            # 按涨幅从高到低排序
            tickers = sorted(tickers, key=lambda t: t.price_change_pct, reverse=True)

            # 计算波动状态统计（需要先构建表格来获取状态）
            temp_df = build_binance_table(tickers)
            volume_surge_count = len(temp_df[temp_df["波动状态"].str.contains("放量上涨", na=False)])
            divergence_count = len(temp_df[temp_df["波动状态"].str.contains("缩量背离", na=False)])

            # 统计信息
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("交易对数量", f"{len(tickers)}", "成交额 > 500万")
            with col2:
                gainers = len([t for t in tickers if t.price_change_pct > 0])
                st.metric("上涨", f"{gainers}", f"{gainers/len(tickers)*100:.1f}%" if tickers else "0%")
            with col3:
                losers = len([t for t in tickers if t.price_change_pct < 0])
                st.metric("下跌", f"{losers}", f"{losers/len(tickers)*100:.1f}%" if tickers else "0%")
            with col4:
                st.metric("🚀 放量上涨", f"{volume_surge_count}", "强势信号")
            with col5:
                st.metric("⚠️ 缩量背离", f"{divergence_count}", "风险信号")

            # 排序选项
            st.info("💡 默认已按 24h 涨幅从高到低排序，且仅显示成交额 > 500 万 USDT 的交易对")
            sort_col1, sort_col2 = st.columns([3, 7])
            with sort_col1:
                sort_by = st.selectbox(
                    "重新排序",
                    ["保持默认(涨幅)", "24h振幅%", "24h成交额(USDT)", "最新价"],
                    index=0,
                )
            with sort_col2:
                filter_option = st.radio(
                    "进一步筛选",
                    ["全部", "仅上涨", "仅下跌", "振幅>5%", "振幅>10%"],
                    horizontal=True,
                )

            # 数据筛选
            filtered_tickers = tickers.copy()
            if filter_option == "仅上涨":
                filtered_tickers = [t for t in filtered_tickers if t.price_change_pct > 0]
            elif filter_option == "仅下跌":
                filtered_tickers = [t for t in filtered_tickers if t.price_change_pct < 0]
            elif filter_option == "振幅>5%":
                filtered_tickers = [
                    t for t in filtered_tickers
                    if (t.high_24h - t.low_24h) / t.low_24h * 100 > 5
                ]
            elif filter_option == "振幅>10%":
                filtered_tickers = [
                    t for t in filtered_tickers
                    if (t.high_24h - t.low_24h) / t.low_24h * 100 > 10
                ]

            # 构建表格
            df_binance = build_binance_table(filtered_tickers)
            if not df_binance.empty:
                # 重新排序（如果用户选择了其他排序方式）
                if sort_by != "保持默认(涨幅)":
                    sort_column = sort_by
                    ascending = sort_by == "最新价"
                    df_binance = df_binance.sort_values(sort_column, ascending=ascending)
                # 否则保持原有的按涨幅排序（已在 tickers 中完成）

                render_binance_table(df_binance)

                # 下载按钮
                st.download_button(
                    "下载 Binance 数据 CSV",
                    data=df_binance.to_csv(index=False).encode("utf-8-sig"),
                    file_name=f"binance_usdt_{datetime.now():%Y%m%d_%H%M}.csv",
                    mime="text/csv",
                )
            else:
                st.info("没有符合筛选条件的数据")
        else:
            st.error("无法获取 Binance 数据，请检查网络连接或稍后重试")

    st.divider()

    tab_scan, tab_detail, tab_corr, tab_alerts = st.tabs(
        ["扫描全景", "单标的详情", "相关性矩阵", "告警"]
    )

    with tab_scan:
        st.markdown('<div class="section-title">多资产波动扫描</div>', unsafe_allow_html=True)
        table = build_scanner_table(stats_list)
        if table.empty:
            st.info("没有成功获取到任何标的数据。")
        else:
            render_scanner_table(table.sort_values("年化波动率%", ascending=False))
            st.download_button(
                "下载当前扫描结果 CSV",
                data=table.to_csv(index=False).encode("utf-8-sig"),
                file_name=f"vol_scan_{datetime.now():%Y%m%d_%H%M}.csv",
                mime="text/csv",
            )

    with tab_detail:
        st.markdown('<div class="section-title">单标的走势与滚动波动率</div>', unsafe_allow_html=True)
        available = [s.symbol for s in stats_list]
        if not available:
            st.info("无可用标的。")
        else:
            chosen = st.selectbox("选择标的", options=available, index=0)
            render_volatility_chart(chosen, histories.get(chosen, pd.DataFrame()), config["interval"])

    with tab_corr:
        st.markdown('<div class="section-title">标的收益率相关性</div>', unsafe_allow_html=True)
        render_correlation_heatmap(histories)

    with tab_alerts:
        st.markdown('<div class="section-title">阈值告警</div>', unsafe_allow_html=True)
        render_alerts(stats_list, config["hv_threshold"], config["z_threshold"])


if __name__ == "__main__":
    main()
