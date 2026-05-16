import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# SAYFA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="BIST QUANTUM PRO MAX",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS (AYNEN KORUNDU)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700;900&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #000000 !important;
    color: #00FF00 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

h1,h2,h3,h4,p,span,div,label {
    font-family: 'Share Tech Mono', monospace !important;
}

.stButton > button {
    background: #000 !important;
    color: #00FF00 !important;
    border: 2px solid #00FF00 !important;
    font-family: 'Orbitron' !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# UNIVERSE
# ─────────────────────────────────────────────
UNIVERSE = {
    "AKBNK.IS": "Bankacılık",
    "GARAN.IS": "Bankacılık",
    "ASELS.IS": "Savunma",
    "TUPRS.IS": "Enerji",
    "BIMAS.IS": "Perakende",
    "THYAO.IS": "Havacılık"
}

# ─────────────────────────────────────────────
# BENCHMARK (YENİ)
# ─────────────────────────────────────────────
XU100 = "^XU100.IS"

def get_benchmark():
    df = yf.download(XU100, period="1y", interval="1d", progress=False)
    if df is None or df.empty:
        return None
    return df["Close"]

# ─────────────────────────────────────────────
# INDICATORS
# ─────────────────────────────────────────────
def ema(s, n):
    return s.ewm(span=n).mean()

def rsi(s, n=14):
    d = s.diff()
    up = d.clip(lower=0)
    dn = -d.clip(upper=0)
    rs = up.ewm(alpha=1/n).mean() / (dn.ewm(alpha=1/n).mean() + 1e-10)
    return 100 - (100/(1+rs))

def macd(s):
    m = ema(s,12) - ema(s,26)
    sig = ema(m,9)
    return m, sig, m-sig

def boll(s):
    mid = s.rolling(20).mean()
    std = s.rolling(20).std()
    return mid+2*std, mid, mid-2*std

# ─────────────────────────────────────────────
# MARKET REGIME (YENİ)
# ─────────────────────────────────────────────
def market_regime(close):
    if len(close) < 100:
        return "UNKNOWN"
    short = close.rolling(20).mean().iloc[-1]
    long = close.rolling(100).mean().iloc[-1]

    if short > long:
        return "BULL"
    elif short < long:
        return "BEAR"
    return "SIDEWAYS"

# ─────────────────────────────────────────────
# RELATIVE STRENGTH (YENİ)
# ─────────────────────────────────────────────
def rs(stock, bench):
    s = stock.pct_change(20)
    b = bench.pct_change(20)
    return (s / (b + 1e-10)).iloc[-1]

# ─────────────────────────────────────────────
# ANALYZE (GÜNCELLENDİ)
# ─────────────────────────────────────────────
def analyze(df):

    close = df["Close"]

    price = close.iloc[-1]

    rsi_v = rsi(close).iloc[-1]
    macd_v, sig_v, hist = macd(close)

    bb_u, bb_m, bb_l = boll(close)

    scores = {}

    # RSI
    scores["RSI"] = 20 if rsi_v < 30 else -10 if rsi_v > 70 else 5

    # MACD
    scores["MACD"] = 15 if hist.iloc[-1] > 0 else -10

    # TREND
    scores["EMA"] = 10 if price > ema(close,20).iloc[-1] else -5

    total = sum(scores.values())

    confidence = min(100, max(0, (total+30)*2))

    stop = price * 0.97
    target = price * 1.05

    bench = get_benchmark()

    rs_val = 1
    regime = "UNKNOWN"

    if bench is not None:
        rs_val = rs(close, bench)
        regime = market_regime(close)

        if rs_val > 1.05:
            scores["RS"] = 10
        elif rs_val < 0.95:
            scores["RS"] = -5

    total = sum(scores.values())

    return {
        "price": price,
        "score": total,
        "confidence": confidence,
        "rsi": rsi_v,
        "macd": hist.iloc[-1],
        "rs": rs_val,
        "regime": regime,
        "stop": stop,
        "target": target,
        "close": close,
        "bb_u": bb_u,
        "bb_l": bb_l,
        "ema20": ema(close,20)
    }

# ─────────────────────────────────────────────
# SIGNAL
# ─────────────────────────────────────────────
def signal(score):
    if score > 40:
        return "GÜÇLÜ AL"
    elif score > 20:
        return "AL"
    elif score > 0:
        return "NÖTR"
    elif score > -20:
        return "SAT"
    return "GÜÇLÜ SAT"

# ─────────────────────────────────────────────
# CHART
# ─────────────────────────────────────────────
def chart(r):

    fig = go.Figure()

    fig.add_trace(go.Scatter(y=r["close"], name="Price"))
    fig.add_trace(go.Scatter(y=r["ema20"], name="EMA20"))
    fig.add_trace(go.Scatter(y=r["bb_u"], name="BB Upper"))
    fig.add_trace(go.Scatter(y=r["bb_l"], name="BB Lower"))

    return fig

# ─────────────────────────────────────────────
# APP
# ─────────────────────────────────────────────
st.title("🛸 BIST QUANTUM PRO MAX")

sym = st.selectbox("Hisse", list(UNIVERSE.keys()))

if st.button("ANALİZ ET"):

    df = yf.download(sym, period="1y")

    r = analyze(df)

    st.metric("Fiyat", round(r["price"],2))
    st.metric("Skor", r["score"])
    st.metric("Güven", f"%{r['confidence']}")

    st.write("RS:", r["rs"])
    st.write("Regime:", r["regime"])

    st.write("Sinyal:", signal(r["score"]))

    st.plotly_chart(chart(r), use_container_width=True)
