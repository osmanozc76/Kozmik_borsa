"""
╔══════════════════════════════════════════════════════════════╗
║         BIST QUANTUM PRO MAX — ALTIN VURUŞU EDİSYONU         ║
║  Çalıştır:  streamlit run bist_promax.py                    ║
║  Kur:       pip install streamlit yfinance plotly pandas    ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# SAYFA AYARLARI
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BIST QUANTUM PRO MAX",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# SİBER KOMUTA CSS — Siyah/Yeşil + Pro Detay
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700;900&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #000000 !important;
    color: #00FF00 !important;
    font-family: 'Share Tech Mono', 'Courier New', monospace !important;
}

h1, h2, h3, h4, p, span, div, label {
    font-family: 'Share Tech Mono', monospace !important;
}

[data-testid="stSidebar"] {
    background: #050505 !important;
    border-right: 1px solid #00FF0033 !important;
}
[data-testid="stSidebar"] * { color: #00FF00 !important; }

.stButton > button {
    background: #000 !important;
    color: #00FF00 !important;
    border: 2px solid #00FF00 !important;
    border-radius: 4px !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    width: 100% !important;
    padding: 12px !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
    box-shadow: 0 0 10px #00FF0033 !important;
}
.stButton > button:hover {
    background: #00FF0011 !important;
    box-shadow: 0 0 20px #00FF0066 !important;
}

[data-testid="stMetric"] {
    background: #050505 !important;
    border: 1px solid #00FF0044 !important;
    border-radius: 4px !important;
    padding: 10px !important;
}
[data-testid="stMetricValue"] {
    color: #00FF00 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1.3rem !important;
}
[data-testid="stMetricLabel"] {
    color: #006600 !important;
    font-size: 0.65rem !important;
    letter-spacing: 2px !important;
}

.stSelectbox > div > div, .stMultiSelect > div > div {
    background: #050505 !important;
    border: 1px solid #00FF0044 !important;
    color: #00FF00 !important;
    border-radius: 4px !important;
    font-family: 'Share Tech Mono', monospace !important;
}

.stSlider > div > div > div { background: #003300 !important; }
.stSlider > div > div > div > div { background: #00FF00 !important; }

[data-baseweb="tab-list"] {
    background: #050505 !important;
    border: 1px solid #00FF0033 !important;
    border-radius: 4px !important;
}
[data-baseweb="tab"] {
    color: #006600 !important;
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 1px !important;
}
[aria-selected="true"] {
    color: #00FF00 !important;
    border-bottom: 2px solid #00FF00 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #00FF0044 !important;
    border-radius: 4px !important;
}
.stDataFrame * { font-family: 'Share Tech Mono', monospace !important; }

.stTextInput > div > div > input {
    background: #050505 !important;
    border: 1px solid #00FF0044 !important;
    color: #00FF00 !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 4px !important;
}

.stProgress > div > div > div { background: #00FF00 !important; }

[data-testid="stExpander"] {
    background: #050505 !important;
    border: 1px solid #00FF0033 !important;
    border-radius: 4px !important;
}

.stSuccess {
    background: #001100 !important;
    border: 1px solid #00FF0066 !important;
    color: #00FF00 !important;
    border-radius: 4px !important;
}
.stError {
    background: #110000 !important;
    border: 1px solid #FF000066 !important;
    color: #FF4444 !important;
}
.stWarning {
    background: #111100 !important;
    border: 1px solid #FFFF0044 !important;
    color: #FFFF00 !important;
}

hr { border-color: #00FF0033 !important; }
#MainMenu, footer, header { visibility: hidden; }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { background: #003300; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #00FF00; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# BIST ÜNİVERSİ (Örnek hisseler, istediğin gibi genişlet)
# ─────────────────────────────────────────────────────────────
UNIVERSE = {
    "AKBNK.IS": "Bankacılık",   "GARAN.IS": "Bankacılık",   "YKBNK.IS": "Bankacılık",
    "ISCTR.IS": "Bankacılık",   "HALKB.IS": "Bankacılık",   "QNBFB.IS": "Bankacılık",
    "SAHOL.IS": "Holding",      "KCHOL.IS": "Holding",      "DOHOL.IS": "Holding",
    "SABAN.IS": "Holding",      "TUPRS.IS": "Enerji",       "PETKM.IS": "Petrokimya",
    "AEFES.IS": "İçecek",       "EKGYO.IS": "Gayrimenkul",  "VESTL.IS": "Elektronik",
    "ASELS.IS": "Savunma",      "TAI.IS": "Savunma",        "FROTO.IS": "Otomotiv",
    "TOASO.IS": "Otomotiv",     "TCELL.IS": "Telekom",      "TTKOM.IS": "Telekom",
    "THYAO.IS": "Havacılık",    "PGSUS.IS": "Havacılık",    "TAVHL.IS": "Havalimanı",
    "BIMAS.IS": "Perakende",    "ULKER.IS": "Gıda",         "HEKTS.IS": "Sağlık",
    "SISE.IS": "Cam",           "EREGL.IS": "Demir-Çelik",  "KRDMD.IS": "Demir-Çelik",
    "ARCLK.IS": "Çimento",      "ODAS.IS": "Lojistik",      "NETAS.IS": "Teknoloji",
}

# ─────────────────────────────────────────────────────────────
# TEKNİK GÖSTERGELER — 7'Lİ MOTOR
# ─────────────────────────────────────────────────────────────
def ema(s, span):
    return s.ewm(span=span, adjust=False).mean()

def calc_rsi(s, period=14):
    delta = s.diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)
    ag = gain.ewm(com=period-1, adjust=False).mean()
    al = loss.ewm(com=period-1, adjust=False).mean()
    rs = ag / (al + 1e-10)
    return 100 - (100 / (1 + rs))

def calc_macd(s, fast=12, slow=26, signal=9):
    fe = s.ewm(span=fast, adjust=False).mean()
    se = s.ewm(span=slow, adjust=False).mean()
    ml = fe - se
    sl = ml.ewm(span=signal, adjust=False).mean()
    return ml, sl, ml - sl

def calc_bollinger(s, window=20, nstd=2):
    mid = s.rolling(window).mean()
    std = s.rolling(window).std()
    return mid + nstd*std, mid, mid - nstd*std

def calc_atr(high, low, close, period=14):
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)
    return tr.ewm(com=period-1, adjust=False).mean()

def calc_obv(close, volume):
    direction = np.sign(close.diff()).fillna(0)
    return (direction * volume).cumsum()

def calc_stochastic(high, low, close, k=14, d=3):
    lowest = low.rolling(k).min()
    highest = high.rolling(k).max()
    pct_k = 100 * (close - lowest) / (highest - lowest + 1e-10)
    pct_d = pct_k.rolling(d).mean()
    return pct_k, pct_d

# ─────────────────────────────────────────────────────────────
# ANA ANALİZ MOTORU
# ─────────────────────────────────────────────────────────────
def analyze(sym, df):
    if df is None or df.empty or len(df) < 30:
        return None

    close = df["Close"].squeeze()
    high = df["High"].squeeze()
    low = df["Low"].squeeze()
    volume = df["Volume"].squeeze()
    price = float(close.iloc[-1])

    # 1. RSI
    rsi_s = calc_rsi(close)
    rsi_v = float(rsi_s.iloc[-1])
    rsi_p = float(rsi_s.iloc[-4]) if len(rsi_s) >= 4 else rsi_v

    # 2. EMA Trend
    e9 = float(ema(close, 9).iloc[-1])
    e21 = float(ema(close, 21).iloc[-1])
    e50 = float(ema(close, 50).iloc[-1]) if len(close) >= 50 else None
    e200 = float(ema(close, 200).iloc[-1]) if len(close) >= 200 else None

    # 3. MACD
    ml, sl_line, hist_s = calc_macd(close)
    macd_h = float(hist_s.iloc[-1])
    macd_p = float(hist_s.iloc[-2]) if len(hist_s) >= 2 else macd_h
    macd_cross = macd_p < 0 and macd_h > 0

    # 4. Bollinger
    bb_up, bb_mid, bb_dn = calc_bollinger(close)
    bb_pos = float((price - float(bb_dn.iloc[-1])) / (float(bb_up.iloc[-1]) - float(bb_dn.iloc[-1]) + 1e-10))

    # 5. ATR
    atr_v = float(calc_atr(high, low, close).iloc[-1])
    atr_pct = atr_v / price * 100

    # 6. OBV
    obv_s = calc_obv(close, volume)
    obv_em = ema(obv_s, 20)
    obv_up = float(obv_s.iloc[-1]) > float(obv_em.iloc[-1]) if len(obv_s) >= 20 else False

    # 7. Stochastic
    sk, sd_line = calc_stochastic(high, low, close)
    stoch_k = float(sk.iloc[-1])
    stoch_d = float(sd_line.iloc[-1])

    # Getiri
    ret_1w = (price / float(close.iloc[-5]) - 1)*100 if len(close) >= 5 else 0
    ret_1m = (price / float(close.iloc[-21]) - 1)*100 if len(close) >= 21 else 0
    ret_3m = (price / float(close.iloc[-63]) - 1)*100 if len(close) >= 63 else 0

    high52 = float(high.max())
    low52 = float(low.min())

    # KOMPOZİT SKOR (100 puan bazlı)
    scores = {}

    # RSI (max ±25)
    if rsi_v < 25: scores["RSI"] = 25
    elif rsi_v < 35: scores["RSI"] = 18
    elif rsi_v < 45: scores["RSI"] = 10
    elif rsi_v < 55: scores["RSI"] = 4
    elif rsi_v < 65: scores["RSI"] = 0
    elif rsi_v < 75: scores["RSI"] = -8
    else: scores["RSI"] = -18
    if rsi_v > rsi_p: scores["RSI"] += 3

    # EMA (max 25)
    ema_pts = 0
    if price > e9: ema_pts += 5
    if price > e21: ema_pts += 7
    if e9 > e21: ema_pts += 5
    if e50 and price > e50: ema_pts += 5
    if e200 and price > e200: ema_pts += 3
    scores["EMA"] = ema_pts

    # MACD (max ±20)
    if macd_cross: scores["MACD"] = 20
    elif macd_h > 0 and macd_h > macd_p: scores["MACD"] = 14
    elif macd_h > 0: scores["MACD"] = 7
    elif macd_h < 0 and macd_h < macd_p: scores["MACD"] = -14
    else: scores["MACD"] = -5

    # Bollinger (max ±14)
    if bb_pos < 0.1: scores["BOLLINGER"] = 14
    elif bb_pos < 0.3: scores["BOLLINGER"] = 9
    elif bb_pos < 0.5: scores["BOLLINGER"] = 4
    elif bb_pos < 0.7: scores["BOLLINGER"] = 0
    elif bb_pos < 0.9: scores["BOLLINGER"] = -5
    else: scores["BOLLINGER"] = -12

    # Stochastic (max ±10)
    if stoch_k < 20 and stoch_k > stoch_d: scores["STOCH"] = 10
    elif stoch_k < 20: scores["STOCH"] = 5
    elif stoch_k > 80 and stoch_k < stoch_d: scores["STOCH"] = -10
    elif stoch_k > 80: scores["STOCH"] = -5
    else: scores["STOCH"] = 2

    # OBV (max ±8)
    scores["OBV"] = 8 if obv_up else -5

    # Momentum (max 15)
    mom = 0
    if ret_1w > 0: mom += 3
    if ret_1m > 5: mom += 5
    elif ret_1m > 0: mom += 2
    if ret_3m > 10: mom += 5
    elif ret_3m > 0: mom += 2
    scores["MOMENTUM"] = mom

    total = sum(scores.values())
    confidence = min(100, max(0, (total + 30) / 1.5))

    # Stop-loss ve hedefler
    stop = price - atr_v * 2
    tgt1 = price + atr_v * 3
    tgt2 = price + atr_v * 5
    rr = (tgt1 - price) / (price - stop + 1e-10) if (price - stop) != 0 else 0

    # Pivot noktaları
    pivot = (float(high.iloc[-5:].max()) + float(low.iloc[-5:].min()) + price) / 3
    r1 = 2 * pivot - float(low.iloc[-5:].min())
    s1 = 2 * pivot - float(high.iloc[-5:].max())
    r2 = pivot + (float(high.iloc[-5:].max()) - float(low.iloc[-5:].min()))
    s2 = pivot - (float(high.iloc[-5:].max()) - float(low.iloc[-5:].min()))

    return {
        "sym": sym,
        "price": round(price, 2),
        "score": round(total, 1),
        "confidence": round(confidence, 1),
        "scores": {k: round(v, 1) for k, v in scores.items()},
        "rsi": round(rsi_v, 1),
        "macd_hist": round(macd_h, 4),
        "macd_cross": macd_cross,
        "macd_dir": "POZİTİF" if macd_h > 0 else "NEGATİF",
        "bb_pos": round(bb_pos * 100, 1),
        "stoch_k": round(stoch_k, 1),
        "stoch_d": round(stoch_d, 1),
        "atr_pct": round(atr_pct, 2),
        "obv_up": obv_up,
        "ema_pts": ema_pts,
        "ret_1w": round(ret_1w, 2),
        "ret_1m": round(ret_1m, 2),
        "ret_3m": round(ret_3m, 2),
        "high_52": round(high52, 2),
        "low_52": round(low52, 2),
        "from_high": round((price / high52 - 1) * 100, 2),
        "from_low": round((price / low52 - 1) * 100, 2),
        "stop": round(stop, 2),
        "target1": round(tgt1, 2),
        "target2": round(tgt2, 2),
        "rr": round(rr, 2),
        "pivot": round(pivot, 2),
        "r1": round(r1, 2), "r2": round(r2, 2),
        "s1": round(s1, 2), "s2": round(s2, 2),
        "close_s": close, "high_s": high,
        "low_s": low, "vol_s": volume,
    }

# ─────────────────────────────────────────────────────────────
# SİNYAL SİSTEMİ
# ─────────────────────────────────────────────────────────────
def signal(score):
    if score >= 55: return "⚡ GÜÇLÜ AL", "#00FF00", "🟢▲▲"
    if score >= 35: return "📈 AL", "#00CC00", "🟢▲"
    if score >= 15: return "🔼 ZAYIF AL", "#00FF88", "🟡▲"
    if score >= -10: return "🔄 NÖTR", "#FFFF00", "🟡▬"
    if score >= -30: return "🔽 ZAYIF SAT", "#FF8800", "🔴▼"
    if score >= -50: return "📉 SAT", "#FF4444", "🔴▼"
    return "🚨 GÜÇLÜ SAT", "#FF0000", "🔴▼▼"

# ─────────────────────────────────────────────────────────────
# YORUM MOTORU
# ────────────────────────────────────────────────────────
