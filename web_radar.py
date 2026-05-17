"""
╔══════════════════════════════════════════════════════════════╗
║         BIST QUANTUM PRO MAX — KOMUTA MERKEZİ               ║
║  Çalıştır:  streamlit run bist_promax.py                    ║
║  Kur:       pip install streamlit yfinance plotly pandas     ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from datetime import datetime

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

/* Genel metin */
h1, h2, h3, h4, p, span, div, label {
    font-family: 'Share Tech Mono', monospace !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #050505 !important;
    border-right: 1px solid #00FF0033 !important;
}
[data-testid="stSidebar"] * { color: #00FF00 !important; }

/* Butonlar */
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

/* Metrikler */
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
[data-testid="stMetricDelta"] { font-size: 0.7rem !important; }

/* Selectbox */
.stSelectbox > div > div {
    background: #050505 !important;
    border: 1px solid #00FF0044 !important;
    color: #00FF00 !important;
    border-radius: 4px !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Slider */
.stSlider > div > div > div { background: #003300 !important; }
.stSlider > div > div > div > div { background: #00FF00 !important; }

/* Tabs */
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

/* DataFrame */
[data-testid="stDataFrame"] {
    border: 1px solid #00FF0044 !important;
    border-radius: 4px !important;
}
.stDataFrame * { font-family: 'Share Tech Mono', monospace !important; }

/* Text input */
.stTextInput > div > div > input {
    background: #050505 !important;
    border: 1px solid #00FF0044 !important;
    color: #00FF00 !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 4px !important;
}

/* Progress */
.stProgress > div > div > div { background: #00FF00 !important; }

/* Expander */
[data-testid="stExpander"] {
    background: #050505 !important;
    border: 1px solid #00FF0033 !important;
    border-radius: 4px !important;
}

/* Success/Error/Warning */
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
.stInfo {
    background: #000811 !important;
    border: 1px solid #00FFFF44 !important;
    color: #00FFFF !important;
}

/* Divider */
hr { border-color: #00FF0033 !important; }

/* Header gizle */
#MainMenu, footer, header { visibility: hidden; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { background: #003300; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #00FF00; }

/* Spin animasyonu */
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
@keyframes scanline {
    0%   { transform: translateY(-100%); }
    100% { transform: translateY(100vh); }
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# BIST ÜNİVERSİ
# ─────────────────────────────────────────────────────────────
UNIVERSE = {
    "AKBNK.IS": "Bankacılık",  "GARAN.IS": "Bankacılık",
    "YKBNK.IS": "Bankacılık",  "SAHOL.IS": "Holding",
    "FROTO.IS": "Otomotiv",    "TOASO.IS": "Otomotiv",
    "ASELS.IS": "Savunma",     "VESTL.IS": "Elektronik",
    "TUPRS.IS": "Enerji",      "PETKM.IS": "Petrokimya",
    "SASA.IS":  "Kimya",       "EREGL.IS": "Demir-Çelik",
    "KRDMD.IS": "Demir-Çelik", "BIMAS.IS": "Perakende",
    "ULKER.IS": "Gıda",        "KCHOL.IS": "Holding",
    "DOHOL.IS": "Holding",     "SISE.IS":  "Cam",
    "HEKTS.IS": "Sağlık",      "TCELL.IS": "Telekom",
    "TTKOM.IS": "Telekom",     "THYAO.IS": "Havacılık",
    "PGSUS.IS": "Havacılık",   "TAVHL.IS": "Havalimanı",
}

# ─────────────────────────────────────────────────────────────
# TEKNİK GÖSTERGELER — 7'Lİ MOTOR
# ─────────────────────────────────────────────────────────────

def ema(s, span):
    return s.ewm(span=span, adjust=False).mean()

def calc_rsi(s, period=14):
    delta = s.diff()
    gain  = delta.clip(lower=0)
    loss  = (-delta).clip(lower=0)
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
        (low  - close.shift()).abs()
    ], axis=1).max(axis=1)
    return tr.ewm(com=period-1, adjust=False).mean()

def calc_obv(close, volume):
    direction = np.sign(close.diff()).fillna(0)
    return (direction * volume).cumsum()

def calc_stochastic(high, low, close, k=14, d=3):
    lowest  = low.rolling(k).min()
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

    close  = df["Close"].squeeze()
    high   = df["High"].squeeze()
    low    = df["Low"].squeeze()
    volume = df["Volume"].squeeze()
    price  = float(close.iloc[-1])

    # ── 1. RSI
    rsi_s = calc_rsi(close)
    rsi_v = float(rsi_s.iloc[-1])
    rsi_p = float(rsi_s.iloc[-4])

    # ── 2. EMA Trend
    e9   = float(ema(close, 9).iloc[-1])
    e21  = float(ema(close, 21).iloc[-1])
    e50  = float(ema(close, 50).iloc[-1]) if len(close) >= 50 else None
    e200 = float(ema(close,200).iloc[-1]) if len(close) >= 100 else None

    # ── 3. MACD
    ml, sl, hist = calc_macd(close)
    macd_h    = float(hist.iloc[-1])
    macd_p    = float(hist.iloc[-2])
    macd_cross = float(hist.iloc[-2]) < 0 and macd_h > 0

    # ── 4. Bollinger
    bb_up, bb_mid, bb_dn = calc_bollinger(close)
    bb_pos = float((price - float(bb_dn.iloc[-1])) /
                   (float(bb_up.iloc[-1]) - float(bb_dn.iloc[-1]) + 1e-10))

    # ── 5. ATR
    atr_v   = float(calc_atr(high, low, close).iloc[-1])
    atr_pct = atr_v / price * 100

    # ── 6. OBV
    obv_s  = calc_obv(close, volume)
    obv_em = ema(obv_s, 20)
    obv_up = float(obv_s.iloc[-1]) > float(obv_em.iloc[-1])

    # ── 7. Stochastic
    sk, sd  = calc_stochastic(high, low, close)
    stoch_k = float(sk.iloc[-1])
    stoch_d = float(sd.iloc[-1])

    # ── Getiri
    ret_1w = (price / float(close.iloc[-5])  - 1)*100 if len(close) >= 5  else 0
    ret_1m = (price / float(close.iloc[-21]) - 1)*100 if len(close) >= 21 else 0
    ret_3m = (price / float(close.iloc[-63]) - 1)*100 if len(close) >= 63 else 0

    high52 = float(high.max())
    low52  = float(low.min())

    # ── KOMPOZİT SKOR (100 puan bazlı)
    scores = {}

    # RSI (max ±25)
    if   rsi_v < 25: scores["RSI"] = 25
    elif rsi_v < 35: scores["RSI"] = 18
    elif rsi_v < 45: scores["RSI"] = 10
    elif rsi_v < 55: scores["RSI"] = 4
    elif rsi_v < 65: scores["RSI"] = 0
    elif rsi_v < 75: scores["RSI"] = -8
    else:            scores["RSI"] = -18
    if rsi_v > rsi_p: scores["RSI"] += 3

    # EMA (max 25)
    ema_pts = 0
    if price > e9:                    ema_pts += 5
    if price > e21:                   ema_pts += 7
    if e9 > e21:                      ema_pts += 5
    if e50  and price > e50:          ema_pts += 5
    if e200 and price > e200:         ema_pts += 3
    scores["EMA"] = ema_pts

    # MACD (max ±20)
    if macd_cross:                            scores["MACD"] = 20
    elif macd_h > 0 and macd_h > macd_p:     scores["MACD"] = 14
    elif macd_h > 0:                          scores["MACD"] = 7
    elif macd_h < 0 and macd_h < macd_p:     scores["MACD"] = -14
    else:                                     scores["MACD"] = -5

    # Bollinger (max ±14)
    if   bb_pos < 0.1: scores["BOLLINGER"] = 14
    elif bb_pos < 0.3: scores["BOLLINGER"] = 9
    elif bb_pos < 0.5: scores["BOLLINGER"] = 4
    elif bb_pos < 0.7: scores["BOLLINGER"] = 0
    elif bb_pos < 0.9: scores["BOLLINGER"] = -5
    else:              scores["BOLLINGER"] = -12

    # Stochastic (max ±10)
    if   stoch_k < 20 and stoch_k > stoch_d: scores["STOCH"] = 10
    elif stoch_k < 20:                        scores["STOCH"] = 5
    elif stoch_k > 80 and stoch_k < stoch_d: scores["STOCH"] = -10
    elif stoch_k > 80:                        scores["STOCH"] = -5
    else:                                     scores["STOCH"] = 2

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

    total      = sum(scores.values())
    confidence = min(100, max(0, (total + 30) / 1.5))

    stop  = price - atr_v * 2
    tgt1  = price + atr_v * 3
    tgt2  = price + atr_v * 5
    rr    = (tgt1 - price) / (price - stop + 1e-10)

    pivot = (float(high.iloc[-5:].max()) + float(low.iloc[-5:].min()) + price) / 3
    r1 = 2*pivot - float(low.iloc[-5:].min())
    s1 = 2*pivot - float(high.iloc[-5:].max())
    r2 = pivot + (float(high.iloc[-5:].max()) - float(low.iloc[-5:].min()))
    s2 = pivot - (float(high.iloc[-5:].max()) - float(low.iloc[-5:].min()))

    return {
        "sym":        sym,
        "price":      round(price, 2),
        "score":      round(total, 1),
        "confidence": round(confidence, 1),
        "scores":     {k: round(v, 1) for k, v in scores.items()},
        "rsi":        round(rsi_v, 1),
        "macd_hist":  round(macd_h, 4),
        "macd_cross": macd_cross,
        "macd_dir":   "POZİTİF" if macd_h > 0 else "NEGATİF",
        "bb_pos":     round(bb_pos * 100, 1),
        "stoch_k":    round(stoch_k, 1),
        "stoch_d":    round(stoch_d, 1),
        "atr_pct":    round(atr_pct, 2),
        "obv_up":     obv_up,
        "ema_pts":    ema_pts,
        "ret_1w":     round(ret_1w, 2),
        "ret_1m":     round(ret_1m, 2),
        "ret_3m":     round(ret_3m, 2),
        "high_52":    round(high52, 2),
        "low_52":     round(low52, 2),
        "from_high":  round((price/high52-1)*100, 2),
        "from_low":   round((price/low52-1)*100, 2),
        "stop":       round(stop, 2),
        "target1":    round(tgt1, 2),
        "target2":    round(tgt2, 2),
        "rr":         round(rr, 2),
        "pivot":      round(pivot, 2),
        "r1": round(r1,2), "r2": round(r2,2),
        "s1": round(s1,2), "s2": round(s2,2),
        "close_s": close, "high_s": high,
        "low_s": low, "vol_s": volume,
    }

def signal(score):
    if score >= 55:  return "⚡ GÜÇLÜ AL",   "#00FF00", "🟢▲▲"
    if score >= 35:  return "📈 AL",          "#00CC00", "🟢▲"
    if score >= 15:  return "🔼 ZAYIF AL",   "#00FF88", "🟡▲"
    if score >= -10: return "🔄 NÖTR",        "#FFFF00", "🟡▬"
    if score >= -30: return "🔽 ZAYIF SAT",  "#FF8800", "🔴▼"
    if score >= -50: return "📉 SAT",         "#FF4444", "🔴▼"
    return               "🚨 GÜÇLÜ SAT",  "#FF0000", "🔴▼▼"

# ─────────────────────────────────────────────────────────────
# YORUM MOTORU
# ─────────────────────────────────────────────────────────────

def generate_comment(r):
    sig, _, _ = signal(r["score"])
    lines = []
    sym = r["sym"].replace(".IS","")

    lines.append(f"**{sym}** hissesi {r['price']:.2f} TL seviyesinde işlem görüyor.")

    # RSI
    if r["rsi"] > 70:
        lines.append(f"RSI {r['rsi']} ile aşırı alım bölgesinde — kısa vadede kar realizasyonu riski yüksek.")
    elif r["rsi"] < 30:
        lines.append(f"RSI {r['rsi']} ile dip bölgesinde sıkıştı — güçlü bir tepki alımı gelebilir.")
    else:
        lines.append(f"RSI {r['rsi']} dengeli bölgede seyrediyor.")

    # MACD
    if r["macd_cross"]:
        lines.append("🔥 MACD boğa kesişimi gerçekleşti — güçlü yükseliş sinyali!")
    elif r["macd_dir"] == "POZİTİF":
        lines.append("MACD pozitif bölgede, momentum yukarı yönlü devam ediyor.")
    else:
        lines.append("MACD negatif — trendin dönmesi için güçlü hacim beklenmeli.")

    # Bollinger
    if r["bb_pos"] < 20:
        lines.append("Fiyat Bollinger alt bandına yakın — fırsat bölgesi.")
    elif r["bb_pos"] > 80:
        lines.append("Fiyat Bollinger üst bandında — aşırı gerilme, düzeltme olabilir.")

    # OBV + Hacim
    if r["obv_up"]:
        lines.append("OBV yükseliyor: kurumsal alım baskısı mevcut.")
    else:
        lines.append("OBV düşüyor: akıllı para henüz pozisyon almıyor.")

    # EMA
    if r["ema_pts"] >= 20:
        lines.append(f"EMA trend {r['ema_pts']}/25 — tüm hareketli ortalamalar yukarı yönlü.")
    elif r["ema_pts"] <= 5:
        lines.append(f"EMA trend {r['ema_pts']}/25 — fiyat tüm ortalamaların altında, zayıf yapı.")

    # Risk/Ödül
    lines.append(f"\n🎯 **KOMPOZİT SKOR: {r['score']:+.1f} | GÜVENİLİRLİK: %{r['confidence']:.0f}**")
    lines.append(f"🛑 Stop: {r['stop']:.2f} TL | Hedef 1: {r['target1']:.2f} TL | R/Ödül: {r['rr']:.2f}x")
    lines.append(f"\n**Sistem Kararı: {sig}**")

    return "\n\n".join(lines)

# ─────────────────────────────────────────────────────────────
# GRAFİK FONKSİYONLARI — Siyah/Yeşil Tema
# ─────────────────────────────────────────────────────────────

PLOT_BG   = "#000000"
PLOT_PAPER= "#050505"
GRID_COL  = "#001100"
TEXT_COL  = "#006600"
GREEN     = "#00FF00"
RED       = "#FF0000"
YELLOW    = "#FFFF00"
CYAN      = "#00FFFF"
# Alpha varyantları (string birleştirme yerine sabit değer)
GREEN88   = "rgba(0,255,0,0.53)"
GREEN66   = "rgba(0,255,0,0.4)"
GREEN44   = "rgba(0,255,0,0.27)"
RED88     = "rgba(255,0,0,0.53)"
RED66     = "rgba(255,0,0,0.4)"
RED44     = "rgba(255,0,0,0.27)"

def plot_layout(fig, height=600):
    fig.update_layout(
        height=height,
        paper_bgcolor=PLOT_PAPER,
        plot_bgcolor=PLOT_BG,
        font=dict(family="Share Tech Mono", color=TEXT_COL, size=10),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        legend=dict(
            bgcolor="#050505", bordercolor="#003300",
            font=dict(size=9, color=GREEN),
            orientation="h", y=1.02, x=0
        ),
    )
    for axis in [fig.update_xaxes, fig.update_yaxes]:
        axis(showgrid=True, gridcolor=GRID_COL,
             showline=True, linecolor="#003300",
             tickfont=dict(color=TEXT_COL))
    return fig

def make_chart(r):
    close  = r["close_s"]
    high   = r["high_s"]
    low    = r["low_s"]
    volume = r["vol_s"]

    e9_s  = ema(close, 9)
    e21_s = ema(close, 21)
    e50_s = ema(close, 50)
    bb_up, bb_mid, bb_dn = calc_bollinger(close)
    rsi_s = calc_rsi(close)
    ml, sl_line, hist_s = calc_macd(close)
    sk, sd_line = calc_stochastic(high, low, close)

    fig = make_subplots(
        rows=5, cols=1, shared_xaxes=True,
        row_heights=[0.42, 0.14, 0.14, 0.14, 0.16],
        vertical_spacing=0.018,
        subplot_titles=["", "HACİM", "RSI", "STOCH", "MACD"]
    )

    # Mum
    fig.add_trace(go.Candlestick(
        x=close.index, open=r["close_s"], high=high, low=low, close=close,
        increasing_fillcolor=GREEN, increasing_line_color=GREEN,
        decreasing_fillcolor=RED,   decreasing_line_color=RED,
        name="FİYAT", showlegend=False
    ), row=1, col=1)

    for s_data, col, nm in [
        (e9_s, CYAN,   "EMA9"),
        (e21_s,"#FF8800","EMA21"),
        (e50_s,"#FF00FF","EMA50")
    ]:
        fig.add_trace(go.Scatter(
            x=close.index, y=s_data,
            line=dict(color=col, width=1.2),
            name=nm, opacity=0.9
        ), row=1, col=1)

    fig.add_trace(go.Scatter(x=close.index, y=bb_up,
        line=dict(color="rgba(0,255,0,0.2)", width=1, dash="dot"),
        name="BB", showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=close.index, y=bb_dn,
        line=dict(color="rgba(0,255,0,0.2)", width=1, dash="dot"),
        fill="tonexty", fillcolor="rgba(0,255,0,0.04)",
        showlegend=False), row=1, col=1)

    # Hacim
    vol_colors = [GREEN if float(close.iloc[i]) >= float(close.iloc[i-1])
                  else RED for i in range(len(close))]
    fig.add_trace(go.Bar(x=close.index, y=volume,
        marker_color=vol_colors, showlegend=False), row=2, col=1)

    # RSI
    fig.add_trace(go.Scatter(x=close.index, y=rsi_s,
        line=dict(color=GREEN, width=1.5),
        name="RSI", showlegend=False), row=3, col=1)
    fig.add_shape(type="line", x0=close.index[0], x1=close.index[-1], y0=70, y1=70,
        line=dict(color="rgba(255,0,0,0.5)", dash="dot", width=1), row=3, col=1)
    fig.add_shape(type="line", x0=close.index[0], x1=close.index[-1], y0=30, y1=30,
        line=dict(color="rgba(0,255,0,0.5)", dash="dot", width=1), row=3, col=1)
    fig.add_hrect(y0=30, y1=70, fillcolor="rgba(0,255,0,0.02)", line_width=0, row=3, col=1)

    # Stochastic
    fig.add_trace(go.Scatter(x=close.index, y=sk,
        line=dict(color=CYAN, width=1.2),
        name="STOCH K", showlegend=False), row=4, col=1)
    fig.add_trace(go.Scatter(x=close.index, y=sd_line,
        line=dict(color=YELLOW, width=1),
        name="STOCH D", showlegend=False), row=4, col=1)
    fig.add_shape(type="line", x0=close.index[0], x1=close.index[-1], y0=80, y1=80,
        line=dict(color="rgba(255,0,0,0.4)", dash="dot", width=1), row=4, col=1)
    fig.add_shape(type="line", x0=close.index[0], x1=close.index[-1], y0=20, y1=20,
        line=dict(color="rgba(0,255,0,0.4)", dash="dot", width=1), row=4, col=1)

    # MACD
    hist_colors = [GREEN if float(v) >= 0 else RED for v in hist_s]
    fig.add_trace(go.Bar(x=close.index, y=hist_s,
        marker_color=hist_colors, showlegend=False), row=5, col=1)
    fig.add_trace(go.Scatter(x=close.index, y=ml,
        line=dict(color=CYAN, width=1.2), name="MACD", showlegend=False), row=5, col=1)
    fig.add_trace(go.Scatter(x=close.index, y=sl_line,
        line=dict(color=YELLOW, width=1), name="SİNYAL", showlegend=False), row=5, col=1)

    for i in range(1, 6):
        fig.update_xaxes(showgrid=True, gridcolor=GRID_COL,
                         showline=True, linecolor="#003300",
                         tickfont=dict(color=TEXT_COL), row=i, col=1)
        fig.update_yaxes(showgrid=True, gridcolor=GRID_COL,
                         showline=True, linecolor="#003300",
                         tickfont=dict(color=TEXT_COL), row=i, col=1)

    fig.update_layout(
        height=680, paper_bgcolor=PLOT_PAPER, plot_bgcolor=PLOT_BG,
        font=dict(family="Share Tech Mono", color=TEXT_COL, size=10),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        legend=dict(bgcolor="#050505", bordercolor="#003300",
                    font=dict(size=9, color=GREEN),
                    orientation="h", y=1.02, x=0)
    )
    return fig

def make_radar(scores):
    cats = list(scores.keys())
    maxv = {"RSI":25,"EMA":25,"MACD":20,"BOLLINGER":14,"STOCH":10,"OBV":8,"MOMENTUM":15}
    norm = [max(0, min(100, (v + abs(min(maxv.values(),default=1))) /
                       (maxv.get(k,20) + abs(min(maxv.values(),default=1))) * 100))
            for k, v in scores.items()]
    fig = go.Figure(go.Scatterpolar(
        r=norm+[norm[0]], theta=cats+[cats[0]],
        fill="toself",
        fillcolor="rgba(0,255,0,0.08)",
        line=dict(color=GREEN, width=2),
        marker=dict(color=GREEN, size=6)
    ))
    fig.update_layout(
        polar=dict(
            bgcolor=PLOT_BG,
            radialaxis=dict(visible=True, range=[0,100],
                gridcolor=GRID_COL, linecolor=GRID_COL,
                tickfont=dict(size=8, color=TEXT_COL)),
            angularaxis=dict(gridcolor=GRID_COL, linecolor=GRID_COL,
                tickfont=dict(size=9, color=GREEN))
        ),
        paper_bgcolor=PLOT_PAPER,
        height=280, margin=dict(l=20,r=20,t=20,b=20),
        showlegend=False,
    )
    return fig

def make_sector_bar(results):
    df = pd.DataFrame([{"sector": r["sector"], "score": r["score"]} for r in results])
    grp = df.groupby("sector")["score"].mean().sort_values(ascending=True).reset_index()
    colors = [GREEN if v > 15 else YELLOW if v > -10 else RED for v in grp["score"]]
    fig = go.Figure(go.Bar(
        x=grp["score"], y=grp["sector"], orientation="h",
        marker_color=colors, marker_line_width=0,
        text=[f"{v:+.1f}" for v in grp["score"]],
        textposition="auto",
        textfont=dict(size=10, family="Share Tech Mono", color="#000000")
    ))
    fig.update_layout(
        paper_bgcolor=PLOT_PAPER, plot_bgcolor=PLOT_BG,
        font=dict(family="Share Tech Mono", color=TEXT_COL, size=10),
        height=280, margin=dict(l=10,r=10,t=10,b=10),
        xaxis=dict(showgrid=True, gridcolor=GRID_COL,
                   zeroline=True, zerolinecolor="#003300"),
        yaxis=dict(showgrid=False, tickfont=dict(color=GREEN)),
    )
    return fig

def make_bubble(results):
    df = pd.DataFrame(results)
    colors = [signal(s)[1] for s in df["score"]]
    fig = go.Figure(go.Scatter(
        x=df["rsi"], y=df["score"],
        mode="markers+text",
        marker=dict(size=df["confidence"]/3+8,
                    color=colors, opacity=0.85,
                    line=dict(color="#000000", width=1)),
        text=[s.replace(".IS","") for s in df["sym"]],
        textposition="top center",
        textfont=dict(size=8, color=GREEN, family="Share Tech Mono"),
        hovertemplate="<b>%{text}</b><br>RSI: %{x:.1f}<br>Skor: %{y:.1f}<extra></extra>"
    ))
    fig.add_shape(type="line", x0=70, x1=70, y0=-90, y1=90,
        line=dict(color="rgba(255,0,0,0.4)", dash="dot", width=1))
    fig.add_shape(type="line", x0=30, x1=30, y0=-90, y1=90,
        line=dict(color="rgba(0,255,0,0.4)", dash="dot", width=1))
    fig.add_shape(type="line", x0=0, x1=100, y0=15, y1=15,
        line=dict(color="rgba(0,255,0,0.25)", dash="dot", width=1))
    fig.add_shape(type="line", x0=0, x1=100, y0=-10, y1=-10,
        line=dict(color="rgba(255,0,0,0.25)", dash="dot", width=1))
    fig.update_layout(
        paper_bgcolor=PLOT_PAPER, plot_bgcolor=PLOT_BG,
        font=dict(family="Share Tech Mono", color=TEXT_COL, size=10),
        height=340, margin=dict(l=10,r=10,t=10,b=10),
        xaxis=dict(title="RSI", showgrid=True, gridcolor=GRID_COL,
                   tickfont=dict(color=GREEN)),
        yaxis=dict(title="SKOR", showgrid=True, gridcolor=GRID_COL,
                   tickfont=dict(color=GREEN)),
    )
    return fig

# ─────────────────────────────────────────────────────────────
# VERİ ÇEKME (Önbellekli)
# ─────────────────────────────────────────────────────────────

@st.cache_data(ttl=300, show_spinner=False)
def fetch_all(period="6mo"):
    try:
        return yf.download(list(UNIVERSE.keys()), period=period,
                           progress=False, auto_adjust=True)
    except:
        return None

@st.cache_data(ttl=300, show_spinner=False)
def fetch_single(sym, period="6mo"):
    try:
        df = yf.Ticker(sym).history(period=period, auto_adjust=True)
        return df if not df.empty else None
    except:
        return None

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px;'>
        <div style='font-family:Orbitron,monospace; font-size:18px;
                    font-weight:900; color:#00FF00;
                    text-shadow:0 0 10px #00FF00;
                    letter-spacing:3px;'>◆ BIST QUANTUM</div>
        <div style='font-size:9px; color:#006600;
                    letter-spacing:4px; margin-top:4px;'>
            PRO MAX EDITION
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    period = st.selectbox("📅 PERİYOT",
        ["3mo","6mo","1y","2y"], index=1,
        format_func=lambda x: {"3mo":"3 AY","6mo":"6 AY","1y":"1 YIL","2y":"2 YIL"}[x])

    sector_filter = st.selectbox("🏭 SEKTÖR",
        ["TÜMÜ"] + sorted(set(UNIVERSE.values())))

    score_min = st.slider("🎯 MİN. SKOR", -80, 80, -80)

    st.divider()

    custom = st.text_input("🔍 HİSSE ARA", "").upper().strip()
    if custom and not custom.endswith(".IS"):
        custom += ".IS"

    st.divider()

    run_scan = st.button("⚡ BULUT RADARINI ATEŞLE")

    st.markdown("""
    <div style='font-size:9px; color:#003300; text-align:center; margin-top:16px;'>
        RSI · EMA · MACD<br>
        BOLLINGER · ATR<br>
        OBV · STOCHASTIC<br><br>
        Veri: Yahoo Finance<br>
        Cache: 5 dk
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# BAŞLIK
# ─────────────────────────────────────────────────────────────

st.markdown(f"""
<div style='text-align:center; padding:10px 0 4px;'>
    <div style='font-family:Orbitron,monospace; font-size:32px; font-weight:900;
                color:#00FF00; text-shadow:0 0 20px #00FF00, 0 0 40px #00FF0044;
                letter-spacing:4px;'>
        🛸 BIST QUANTUM PRO MAX
    </div>
    <div style='font-size:11px; color:#006600; letter-spacing:3px; margin-top:6px;'>
        7 TEKNİK GÖSTERGE · KOMPOZİT SKOR · RİSK/ÖDÜL · PİVOT · YAZILI STRATEJİ
    </div>
    <div style='font-size:9px; color:#003300; margin-top:4px;'>
        {datetime.now().strftime("%d.%m.%Y %H:%M")} · {len(UNIVERSE)} HİSSE TAKİP EDİLİYOR
    </div>
</div>
<hr style='border-color:#003300; margin:10px 0;'/>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# TARAMA
# ─────────────────────────────────────────────────────────────

if "results" not in st.session_state or run_scan:
    st.markdown("""
    <div style='text-align:center; color:#FFFF00; font-size:13px;
                letter-spacing:2px; padding:8px;'>
        📡 SİBER TARAMA BAŞLADI... VERİLER HAFIZAYA ALINIYOR...
    </div>
    """, unsafe_allow_html=True)

    with st.spinner(""):
        raw  = fetch_all(period)
        results, failed = [], []

        if raw is not None:
            bar = st.progress(0)
            for i, (sym, sector) in enumerate(UNIVERSE.items()):
                try:
                    if ("Close", sym) in raw.columns:
                        df_tmp = pd.DataFrame({
                            "Close":  raw["Close"][sym],
                            "High":   raw["High"][sym],
                            "Low":    raw["Low"][sym],
                            "Volume": raw["Volume"][sym],
                            "Open":   raw["Open"][sym],
                        }).dropna()
                    elif sym in raw["Close"].columns:
                        df_tmp = pd.DataFrame({
                            "Close":  raw["Close"][sym],
                            "High":   raw["High"][sym],
                            "Low":    raw["Low"][sym],
                            "Volume": raw["Volume"][sym],
                            "Open":   raw["Open"][sym],
                        }).dropna()
                    else:
                        failed.append(sym); continue

                    r = analyze(sym, df_tmp)
                    if r:
                        r["sector"] = sector
                        results.append(r)
                    else:
                        failed.append(sym)
                except:
                    failed.append(sym)
                bar.progress((i+1)/len(UNIVERSE))
            bar.empty()

    st.session_state["results"] = results
    st.session_state["failed"]  = failed

    if results:
        st.success(f"🎯 7'Lİ MOTOR TARAMAYI TAMAMLADI! {len(results)} hisse analiz edildi.")
    else:
        st.error("❌ Veri çekilemedi. İnternet bağlantısını kontrol et.")

results = st.session_state.get("results", [])
failed  = st.session_state.get("failed", [])

if not results:
    st.warning("⚡ Başlamak için sol menüden 'BULUT RADARINI ATEŞLE' butonuna bas.")
    st.stop()

# Filtrele
filtered = [r for r in results
            if (sector_filter == "TÜMÜ" or r.get("sector") == sector_filter)
            and r["score"] >= score_min]
filtered.sort(key=lambda x: x["score"], reverse=True)

# ─────────────────────────────────────────────────────────────
# ÖZET METRİKLER
# ─────────────────────────────────────────────────────────────

bull  = sum(1 for r in results if r["score"] >= 15)
bear  = sum(1 for r in results if r["score"] <= -10)
avg_s = np.mean([r["score"] for r in results])
best  = max(results, key=lambda x: x["score"])
worst = min(results, key=lambda x: x["score"])

c1,c2,c3,c4,c5,c6 = st.columns(6)
with c1: st.metric("📊 TARANAN",    len(results))
with c2: st.metric("🟢 AL SİNYALİ", bull, f"%{bull/len(results)*100:.0f}")
with c3: st.metric("🔴 SAT SİNYALİ",bear)
with c4: st.metric("📈 PİYASA SKOR",f"{avg_s:+.1f}")
with c5: st.metric("🏆 EN GÜÇLÜ",   best["sym"].replace(".IS",""), f"{best['score']:+.1f}")
with c6: st.metric("⚠️ EN ZAYIF",   worst["sym"].replace(".IS",""),f"{worst['score']:+.1f}")

st.divider()

# ─────────────────────────────────────────────────────────────
# SEKMELER
# ─────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋  RADAR TABLOSU",
    "📊  GRAFİK MERKEZİ",
    "🏭  SEKTÖR ANALİZİ",
    "🔍  YAZILI STRATEJİ",
    "⚙️  BACKTESTING",
    "📰  KAP HABERLERİ",
])

# ── TAB 1: Tablo
with tab1:
    tcol1, tcol2 = st.columns([3,1])
    with tcol1:
        rows = []
        for r in filtered:
            sig, col, ok = signal(r["score"])
            rows.append({
                "HİSSE":     r["sym"].replace(".IS",""),
                "SEKTÖR":    r.get("sector",""),
                "FİYAT ₺":  r["price"],
                "SKOR":      r["score"],
                "GÜVEN %":  r["confidence"],
                "RSI":       r["rsi"],
                "EMA":       f"{r['ema_pts']}/5",
                "STOCH K":  r["stoch_k"],
                "OBV":       "↑" if r["obv_up"] else "↓",
                "MACD":      r["macd_dir"],
                "1H %":      r["ret_1w"],
                "1A %":      r["ret_1m"],
                "R/ÖDÜL":   r["rr"],
                "YÖN":       ok,
                "KARAR":     sig,
            })
        df_t = pd.DataFrame(rows)
        st.dataframe(df_t, use_container_width=True, height=500,
            column_config={
                "SKOR":     st.column_config.NumberColumn(format="%+.1f"),
                "GÜVEN %": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%.1f%%"),
                "FİYAT ₺": st.column_config.NumberColumn(format="%.2f"),
                "RSI":      st.column_config.NumberColumn(format="%.1f"),
                "1H %":     st.column_config.NumberColumn(format="%+.2f%%"),
                "1A %":     st.column_config.NumberColumn(format="%+.2f%%"),
                "R/ÖDÜL":  st.column_config.NumberColumn(format="%.2fx"),
            }, hide_index=True)

    with tcol2:
        st.markdown("""
        <div style='font-family:Orbitron,monospace; font-size:12px;
                    color:#00FF00; letter-spacing:2px; margin-bottom:10px;'>
            ⚡ TOP 5 AL
        </div>""", unsafe_allow_html=True)
        for r in filtered[:5]:
            sig, col, ok = signal(r["score"])
            st.markdown(f"""
            <div style='background:#050505; border:1px solid {col}55;
                        border-left:3px solid {col}; border-radius:4px;
                        padding:8px 10px; margin-bottom:6px;'>
                <div style='font-family:Orbitron,monospace; font-weight:700;
                            color:#FFFFFF; font-size:13px;'>
                    {r["sym"].replace(".IS","")}
                </div>
                <div style='font-size:9px; color:#006600;'>{r.get("sector","")}</div>
                <div style='color:{col}; font-size:11px; font-weight:700;
                            text-shadow:0 0 6px {col}88;'>{sig}</div>
                <div style='font-size:9px; color:#666;'>
                    {r["score"]:+.1f} puan · %{r["confidence"]:.0f} güven
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div style='font-family:Orbitron,monospace; font-size:11px;
                    color:#FF4444; letter-spacing:2px;
                    margin:14px 0 8px;'>⚠️ DİKKAT ET</div>""",
            unsafe_allow_html=True)
        for r in sorted(filtered, key=lambda x: x["score"])[:3]:
            sig, col, ok = signal(r["score"])
            st.markdown(f"""
            <div style='background:#050505; border:1px solid {col}44;
                        border-left:3px solid {col}; border-radius:4px;
                        padding:6px 10px; margin-bottom:5px;'>
                <div style='color:#FFFFFF; font-size:12px; font-weight:700;'>
                    {r["sym"].replace(".IS","")}
                </div>
                <div style='color:{col}; font-size:10px;'>
                    {sig} · {r["score"]:+.1f}
                </div>
            </div>""", unsafe_allow_html=True)

# ── TAB 2: Grafik
with tab2:
    st.markdown("""
    <div style='font-size:11px; color:#006600; letter-spacing:2px; margin-bottom:8px;'>
        RSI × KOMPOZİT SKOR HARİTASI
    </div>""", unsafe_allow_html=True)
    st.plotly_chart(make_bubble(results), use_container_width=True, key="bubble")

    st.divider()

    gcol1, gcol2 = st.columns([2,1])
    with gcol1:
        sel_sym = st.selectbox("🎯 HİSSE SEÇ",
            [r["sym"] for r in sorted(results, key=lambda x: x["score"], reverse=True)],
            format_func=lambda x: x.replace(".IS",""))
    with gcol2:
        g_period = st.selectbox("📅",
            ["1mo","3mo","6mo","1y"], index=1,
            format_func=lambda x: {"1mo":"1 AY","3mo":"3 AY","6mo":"6 AY","1y":"1 YIL"}[x],
            key="g_p")

    sel = next((r for r in results if r["sym"] == sel_sym), None)
    if sel:
        sig, col, ok = signal(sel["score"])
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("FİYAT", f"{sel['price']:.2f} ₺")
        m2.metric("KARAR", f"{ok} {sig.split()[-1]}")
        m3.metric("SKOR",  f"{sel['score']:+.1f}")
        m4.metric("GÜVEN", f"%{sel['confidence']:.1f}")

        df_g = fetch_single(sel_sym, g_period)
        if df_g is not None and not df_g.empty:
            st.plotly_chart(make_chart(sel), use_container_width=True, key="chart_sel")
        else:
            st.error("Grafik verisi alınamadı.")

        rcol1, rcol2 = st.columns(2)
        with rcol1:
            st.markdown("""<div style='font-size:10px;color:#006600;
                letter-spacing:2px;margin-bottom:4px;'>SKOR RADAR</div>""",
                unsafe_allow_html=True)
            st.plotly_chart(make_radar(sel["scores"]), use_container_width=True, key="radar_sel")
        with rcol2:
            st.markdown("""<div style='font-size:10px;color:#006600;
                letter-spacing:2px;margin-bottom:8px;'>RİSK / ÖDÜL</div>""",
                unsafe_allow_html=True)
            st.markdown(f"""
            <div style='background:#050505; border:1px solid #003300;
                        border-radius:4px; padding:14px; font-size:12px;'>
                <div style='color:#FF4444; margin-bottom:6px;'>
                    🛑 STOP LOSS: {sel["stop"]:.2f} ₺</div>
                <div style='color:#00CC00; margin-bottom:6px;'>
                    🎯 HEDEF 1: {sel["target1"]:.2f} ₺</div>
                <div style='color:#00FF00; margin-bottom:10px;'>
                    🎯 HEDEF 2: {sel["target2"]:.2f} ₺</div>
                <div style='color:#00FFFF; font-size:15px; font-weight:700;
                            text-shadow:0 0 8px #00FFFF88;'>
                    R/ÖDÜL: {sel["rr"]:.2f}x</div>
            </div>""", unsafe_allow_html=True)

            st.markdown("""<div style='font-size:10px;color:#006600;
                letter-spacing:2px;margin:12px 0 6px;'>PİVOT SEVİYELER</div>""",
                unsafe_allow_html=True)
            for label, val, clr in [
                ("DİRENÇ 2", sel["r2"], "#FF6666"),
                ("DİRENÇ 1", sel["r1"], "#FF9999"),
                ("PİVOT",   sel["pivot"],"#FFFF00"),
                ("DESTEK 1",sel["s1"],  "#99FF99"),
                ("DESTEK 2",sel["s2"],  "#00FF00"),
            ]:
                marker = " ◄ YAKIN" if abs(val - sel["price"])/sel["price"] < 0.02 else ""
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;
                            padding:4px 0;border-bottom:1px solid #001100;font-size:10px;'>
                    <span style='color:#006600;'>{label}</span>
                    <span style='color:{clr};font-weight:700;'>{val:.2f}{marker}</span>
                </div>""", unsafe_allow_html=True)

# ── TAB 3: Sektör
with tab3:
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("""<div style='font-size:10px;color:#006600;
            letter-spacing:2px;margin-bottom:4px;'>SEKTÖR SKOR ORTALAMALARI</div>""",
            unsafe_allow_html=True)
        st.plotly_chart(make_sector_bar(results), use_container_width=True, key="sector_bar")
    with sc2:
        st.markdown("""<div style='font-size:10px;color:#006600;
            letter-spacing:2px;margin-bottom:4px;'>SİNYAL DAĞILIMI</div>""",
            unsafe_allow_html=True)
        sig_c = {"GÜÇLÜ AL":0,"AL":0,"ZAYIF AL":0,"NÖTR":0,
                  "ZAYIF SAT":0,"SAT":0,"GÜÇLÜ SAT":0}
        for r in results:
            s, _, _ = signal(r["score"])
            lbl = s.split()[-1] if "GÜÇLÜ" not in s else " ".join(s.split()[-2:])
            key = s.replace("⚡ ","").replace("📈 ","").replace("🔼 ","") \
                   .replace("🔄 ","").replace("🔽 ","").replace("📉 ","").replace("🚨 ","")
            if key in sig_c: sig_c[key] += 1
        pie = go.Figure(go.Pie(
            labels=list(sig_c.keys()),
            values=list(sig_c.values()),
            marker_colors=["#00FF00","#00CC00","#009900",
                           "#FFFF00","#FF8800","#FF4444","#FF0000"],
            hole=0.5,
            textfont=dict(family="Share Tech Mono", size=9, color="#000"),
        ))
        pie.update_layout(
            paper_bgcolor=PLOT_PAPER,
            font=dict(color=GREEN, family="Share Tech Mono"),
            height=260, margin=dict(l=10,r=10,t=10,b=10),
            legend=dict(font=dict(size=9, color=GREEN))
        )
        st.plotly_chart(pie, use_container_width=True, key="pie_chart")

    sector_rows = {}
    for r in results:
        s = r.get("sector","?")
        if s not in sector_rows:
            sector_rows[s] = []
        sector_rows[s].append(r["score"])

    rows_s = []
    for s, v in sector_rows.items():
        avg = np.mean(v)
        sig_s, _, ok_s = signal(avg)
        rows_s.append({
            "SEKTÖR": s, "HİSSE": len(v),
            "ORT. SKOR": round(avg,1),
            "MAX": round(max(v),1), "MIN": round(min(v),1),
            "DURUM": f"{ok_s} {sig_s.split()[-1]}"
        })
    rows_s.sort(key=lambda x: x["ORT. SKOR"], reverse=True)
    st.dataframe(pd.DataFrame(rows_s), use_container_width=True, hide_index=True)

# ── TAB 4: Yazılı Strateji
with tab4:
    st.markdown("""
    <div style='font-family:Orbitron,monospace; font-size:14px; color:#00FF00;
                letter-spacing:3px; margin-bottom:12px;'>
        📝 YAZILI STRATEJİ VE DERİN ANALİZ MERKEZİ
    </div>""", unsafe_allow_html=True)

    wcol1, wcol2 = st.columns([1,2])
    with wcol1:
        w_sym = st.selectbox("🎯 HİSSE SEÇ",
            [r["sym"] for r in sorted(results, key=lambda x: x["score"], reverse=True)],
            format_func=lambda x: x.replace(".IS",""),
            key="w_sym")
        if custom:
            w_sym = custom

    w_res = next((r for r in results if r["sym"] == w_sym), None)

    if not w_res and custom:
        with st.spinner("Veri çekiliyor..."):
            df_w = fetch_single(custom, period)
        if df_w is not None:
            w_res = analyze(custom, df_w)
            if w_res:
                w_res["sector"] = UNIVERSE.get(custom, "Bilinmiyor")

    if w_res:
        sig_w, col_w, ok_w = signal(w_res["score"])

        with wcol1:
            st.markdown(f"""
            <div style='background:#050505; border:2px solid {col_w}55;
                        border-left:4px solid {col_w}; border-radius:4px;
                        padding:16px; margin-top:8px;'>
                <div style='font-family:Orbitron,monospace; font-size:20px;
                            font-weight:900; color:#FFFFFF;'>
                    {w_res["sym"].replace(".IS","")}
                </div>
                <div style='font-size:9px; color:#006600; margin-bottom:10px;'>
                    {w_res.get("sector","")}</div>
                <div style='font-size:26px; font-weight:700; color:#FFFFFF;'>
                    {w_res["price"]:.2f} TL</div>
                <div style='font-size:14px; font-weight:700; color:{col_w};
                            text-shadow:0 0 10px {col_w}99; margin-top:4px;'>
                    {sig_w}</div>
                <hr style='border-color:#003300; margin:10px 0;'/>
                <div style='font-size:11px;'>
                    <span style='color:#006600;'>SKOR&nbsp;&nbsp;</span>
                    <span style='color:{col_w}; font-weight:700;'>
                        {w_res["score"]:+.1f}</span><br>
                    <span style='color:#006600;'>GÜVEN </span>
                    <span style='color:{col_w}; font-weight:700;'>
                        %{w_res["confidence"]:.1f}</span><br>
                    <span style='color:#006600;'>R/ÖDÜL</span>
                    <span style='color:#00FFFF; font-weight:700;'>
                        {w_res["rr"]:.2f}x</span>
                </div>
            </div>""", unsafe_allow_html=True)

            # Gösterge tablosu
            st.markdown("""
            <div style='font-size:9px;color:#006600;letter-spacing:2px;
                        margin:14px 0 6px;'>7'Lİ GÖSTERGE MATRISI</div>""",
                unsafe_allow_html=True)
            for label, val, note, clr in [
                ("RSI (14)",    w_res["rsi"],
                 "AŞIRI ALIM" if w_res["rsi"]>70 else "AŞIRI SATIM" if w_res["rsi"]<30 else "DENGE",
                 "#FF4444" if w_res["rsi"]>70 else "#00FF00" if w_res["rsi"]<30 else "#FFFF00"),
                ("BOLLINGER",   f"%{w_res['bb_pos']:.1f}",
                 "ALT BAND" if w_res["bb_pos"]<20 else "ÜST BAND" if w_res["bb_pos"]>80 else "ORTA",
                 "#00FF00" if w_res["bb_pos"]<20 else "#FF4444" if w_res["bb_pos"]>80 else "#FFFF00"),
                ("STOCH K",     w_res["stoch_k"], "", "#00FFFF"),
                ("EMA TREND",   f"{w_res['ema_pts']}/5", "", "#00CC00"),
                ("ATR %",       f"%{w_res['atr_pct']:.2f}", "OYNAKLIK", "#FF8800"),
                ("OBV",         "↑ YUKARI" if w_res["obv_up"] else "↓ AŞAĞI", "",
                 "#00FF00" if w_res["obv_up"] else "#FF4444"),
                ("MACD",        w_res["macd_dir"],
                 "KESİŞİM!" if w_res["macd_cross"] else "",
                 "#00FF00" if w_res["macd_dir"]=="POZİTİF" else "#FF4444"),
            ]:
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;align-items:center;
                            padding:5px 0;border-bottom:1px solid #001100;font-size:10px;'>
                    <span style='color:#006600;'>{label}</span>
                    <div style='text-align:right;'>
                        <span style='color:{clr};font-weight:700;'>{val}</span>
                        {'<br><span style="font-size:8px;color:#004400;">'+note+'</span>' if note else ''}
                    </div>
                </div>""", unsafe_allow_html=True)

        with wcol2:
            # Yazılı yorum
            comment = generate_comment(w_res)
            st.markdown(f"""
            <div style='background:#050505; border:1px solid #006600;
                        border-radius:4px; padding:16px; margin-bottom:12px;'>
                <div style='font-family:Orbitron,monospace; font-size:10px;
                            color:#006600; letter-spacing:2px; margin-bottom:10px;'>
                    ◆ YAPAY ZEKÂ DERİN ANALİZ RAPORU
                </div>
                <div style='color:#00FF00; font-size:12px; line-height:1.8;'>
                    {comment.replace(chr(10), "<br>")}
                </div>
            </div>""", unsafe_allow_html=True)

            # Skor radar
            st.plotly_chart(make_radar(w_res["scores"]), use_container_width=True, key="radar_detail")

            # Risk/ödül + pivot
            p1, p2 = st.columns(2)
            with p1:
                st.markdown("""
                <div style='font-size:9px;color:#006600;letter-spacing:2px;
                            margin-bottom:6px;'>RİSK / ÖDÜL</div>""",
                    unsafe_allow_html=True)
                st.markdown(f"""
                <div style='background:#050505;border:1px solid #003300;
                            border-radius:4px;padding:12px;font-size:11px;'>
                    <div style='color:#FF4444;margin-bottom:5px;'>
                        🛑 STOP: {w_res["stop"]:.2f} ₺</div>
                    <div style='color:#00CC00;margin-bottom:5px;'>
                        🎯 H1: {w_res["target1"]:.2f} ₺</div>
                    <div style='color:#00FF00;margin-bottom:8px;'>
                        🎯 H2: {w_res["target2"]:.2f} ₺</div>
                    <div style='color:#00FFFF;font-size:14px;font-weight:700;
                                text-shadow:0 0 8px #00FFFF66;'>
                        R/Ö: {w_res["rr"]:.2f}x</div>
                </div>""", unsafe_allow_html=True)
            with p2:
                st.markdown("""
                <div style='font-size:9px;color:#006600;letter-spacing:2px;
                            margin-bottom:6px;'>PİVOT SEVİYELER</div>""",
                    unsafe_allow_html=True)
                for lbl, val, clr in [
                    ("R2", w_res["r2"],"#FF6666"),
                    ("R1", w_res["r1"],"#FF9999"),
                    ("PVT",w_res["pivot"],"#FFFF00"),
                    ("S1", w_res["s1"],"#99FF99"),
                    ("S2", w_res["s2"],"#00FF00"),
                ]:
                    m = " ◄" if abs(val-w_res["price"])/w_res["price"] < 0.02 else ""
                    st.markdown(f"""
                    <div style='display:flex;justify-content:space-between;
                                padding:4px 0;border-bottom:1px solid #001100;font-size:10px;'>
                        <span style='color:#006600;'>{lbl}</span>
                        <span style='color:{clr};font-weight:700;'>{val:.2f}{m}</span>
                    </div>""", unsafe_allow_html=True)

# ── TAB 5: BACKTESTING
with tab5:
    st.markdown("""
    <div style='font-family:Orbitron,monospace; font-size:14px; color:#00FF00;
                letter-spacing:3px; margin-bottom:12px;'>
        ⚙️ BACKTESTING — SİNYAL PERFORMANS TESTİ
    </div>
    <div style='font-size:10px; color:#006600; margin-bottom:16px;'>
        Composite skor eşiği üzerindeki hisseler tarihsel olarak ne kazandırdı?
    </div>""", unsafe_allow_html=True)

    bc1, bc2, bc3 = st.columns(3)
    with bc1:
        bt_sym = st.selectbox("📌 HİSSE",
            [r["sym"] for r in sorted(results, key=lambda x: x["score"], reverse=True)],
            format_func=lambda x: x.replace(".IS",""), key="bt_sym")
    with bc2:
        bt_period = st.selectbox("📅 GEÇMİŞ PERİYOT",
            ["6mo","1y","2y"], index=1,
            format_func=lambda x: {"6mo":"6 AY","1y":"1 YIL","2y":"2 YIL"}[x],
            key="bt_period")
    with bc3:
        bt_threshold = st.slider("🎯 AL EŞİĞİ (Skor)", 0, 60, 20, key="bt_thresh")

    run_bt = st.button("⚡ BACKTESTI ÇALIŞTIR", key="bt_run")

    if run_bt:
        with st.spinner("Tarihsel veri analiz ediliyor..."):
            df_bt = fetch_single(bt_sym, bt_period)

        if df_bt is None or len(df_bt) < 60:
            st.error("Yetersiz veri.")
        else:
            close_bt = df_bt["Close"].squeeze()
            high_bt  = df_bt["High"].squeeze()
            low_bt   = df_bt["Low"].squeeze()
            vol_bt   = df_bt["Volume"].squeeze()

            # Her gün için skor hesapla (rolling 30 günlük pencere)
            scores_hist, dates_hist = [], []
            hold_days = 10  # Sinyal sonrası kaç gün tut

            signals_bt = []
            for i in range(30, len(close_bt) - hold_days):
                window = df_bt.iloc[i-30:i].copy()
                r_tmp = analyze(bt_sym, window)
                if r_tmp:
                    scores_hist.append(r_tmp["score"])
                    dates_hist.append(close_bt.index[i])
                    if r_tmp["score"] >= bt_threshold:
                        entry = float(close_bt.iloc[i])
                        exit_ = float(close_bt.iloc[i + hold_days])
                        ret   = (exit_ / entry - 1) * 100
                        signals_bt.append({
                            "Tarih":    close_bt.index[i].strftime("%d.%m.%Y"),
                            "Giriş ₺": round(entry, 2),
                            "Çıkış ₺": round(exit_, 2),
                            "Skor":    round(r_tmp["score"], 1),
                            f"{hold_days}G %": round(ret, 2),
                            "Sonuç":   "✅ KAR" if ret > 0 else "❌ ZARAR",
                        })

            if not signals_bt:
                st.warning(f"Bu eşikte ({bt_threshold}) sinyal üretilmedi. Eşiği düşür.")
            else:
                df_sig = pd.DataFrame(signals_bt)
                win_rate = (df_sig["Sonuç"] == "✅ KAR").mean() * 100
                avg_ret  = df_sig[f"{hold_days}G %"].mean()
                total    = df_sig[f"{hold_days}G %"].sum()
                best     = df_sig[f"{hold_days}G %"].max()
                worst    = df_sig[f"{hold_days}G %"].min()

                # Özet metrikler
                bm1, bm2, bm3, bm4, bm5 = st.columns(5)
                bm1.metric("📊 Sinyal Sayısı", len(df_sig))
                bm2.metric("🎯 Kazanma Oranı", f"%{win_rate:.1f}")
                bm3.metric("📈 Ort. Getiri", f"%{avg_ret:.2f}")
                bm4.metric("🏆 En İyi", f"%{best:.2f}")
                bm5.metric("⚠️ En Kötü", f"%{worst:.2f}")

                st.divider()

                # Skor zaman serisi grafiği
                if scores_hist:
                    fig_bt = go.Figure()
                    fig_bt.add_trace(go.Scatter(
                        x=dates_hist, y=scores_hist,
                        line=dict(color="#00FF00", width=1.5),
                        fill="tozeroy", fillcolor="rgba(0,255,0,0.05)",
                        name="Composite Skor"
                    ))
                    fig_bt.add_shape(type="line",
                        x0=dates_hist[0], x1=dates_hist[-1],
                        y0=bt_threshold, y1=bt_threshold,
                        line=dict(color="rgba(255,255,0,0.6)", dash="dot", width=1))

                    # Sinyal noktaları
                    sig_dates = [s["Tarih"] for s in signals_bt]
                    sig_scores= [s["Skor"]  for s in signals_bt]
                    sig_rets  = [s[f"{hold_days}G %"] for s in signals_bt]
                    sig_colors= ["rgba(0,255,0,0.8)" if r > 0 else "rgba(255,0,0,0.8)"
                                 for r in sig_rets]
                    fig_bt.add_trace(go.Scatter(
                        x=sig_dates, y=sig_scores,
                        mode="markers",
                        marker=dict(color=sig_colors, size=8, symbol="triangle-up"),
                        name="Sinyal Noktaları",
                        hovertemplate="<b>%{x}</b><br>Skor: %{y}<extra></extra>"
                    ))
                    fig_bt.update_layout(
                        height=300,
                        paper_bgcolor="#050505", plot_bgcolor="#000000",
                        font=dict(family="Share Tech Mono", color="#006600", size=10),
                        margin=dict(l=10,r=10,t=30,b=10),
                        xaxis=dict(showgrid=True, gridcolor="#001100"),
                        yaxis=dict(showgrid=True, gridcolor="#001100"),
                        title=dict(text=f"{bt_sym.replace('.IS','')} — Skor Geçmişi",
                                   font=dict(color="#00FF00", size=11))
                    )
                    st.plotly_chart(fig_bt, use_container_width=True, key="bt_score_chart")

                # Getiri dağılımı
                fig_ret = go.Figure()
                colors_ret = ["rgba(0,255,0,0.7)" if v > 0 else "rgba(255,0,0,0.7)"
                              for v in df_sig[f"{hold_days}G %"]]
                fig_ret.add_trace(go.Bar(
                    x=df_sig["Tarih"],
                    y=df_sig[f"{hold_days}G %"],
                    marker_color=colors_ret,
                    text=[f"%{v:.1f}" for v in df_sig[f"{hold_days}G %"]],
                    textposition="auto",
                    textfont=dict(size=9, color="#000000")
                ))
                fig_ret.add_shape(type="line",
                    x0=0, x1=len(df_sig)-1, y0=0, y1=0,
                    line=dict(color="rgba(255,255,255,0.3)", width=1))
                fig_ret.update_layout(
                    height=250,
                    paper_bgcolor="#050505", plot_bgcolor="#000000",
                    font=dict(family="Share Tech Mono", color="#006600", size=10),
                    margin=dict(l=10,r=10,t=30,b=10),
                    xaxis=dict(showgrid=False, tickangle=45),
                    yaxis=dict(showgrid=True, gridcolor="#001100",
                               tickformat=".1f", ticksuffix="%"),
                    title=dict(text=f"{hold_days} Günlük Getiri Dağılımı",
                               font=dict(color="#00FF00", size=11))
                )
                st.plotly_chart(fig_ret, use_container_width=True, key="bt_ret_chart")

                # Sinyal tablosu
                st.markdown("""<div style='font-size:9px;color:#006600;
                    letter-spacing:2px;margin:10px 0 6px;'>
                    TÜM SİNYAL GEÇMİŞİ</div>""", unsafe_allow_html=True)
                st.dataframe(df_sig, use_container_width=True, hide_index=True,
                    column_config={
                        f"{hold_days}G %": st.column_config.NumberColumn(format="%+.2f%%"),
                        "Skor": st.column_config.NumberColumn(format="%+.1f"),
                    })

                # Özet yorum
                if win_rate >= 60:
                    yorum = f"✅ Bu sistem {bt_sym.replace('.IS','')} için GÜVENİLİR. %{win_rate:.0f} kazanma oranı ile sinyaller çalışıyor."
                elif win_rate >= 45:
                    yorum = f"🟡 Orta performans. %{win_rate:.0f} kazanma oranı — risk yönetimi ile kullanılabilir."
                else:
                    yorum = f"❌ Bu hissede sistem ZAYIF çalışıyor. %{win_rate:.0f} kazanma oranı yetersiz, eşiği artır."
                st.info(yorum)

# ── TAB 6: KAP HABERLERİ
with tab6:
    st.markdown("""
    <div style='font-family:Orbitron,monospace; font-size:14px; color:#00FF00;
                letter-spacing:3px; margin-bottom:12px;'>
        📰 KAP — KAMUYU AYDINLATMA PLATFORMU
    </div>
    <div style='font-size:10px; color:#006600; margin-bottom:16px;'>
        Şirket bildirimleri, özel durum açıklamaları ve finansal tablolar
    </div>""", unsafe_allow_html=True)

    kc1, kc2 = st.columns([1, 2])
    with kc1:
        kap_sym = st.selectbox("📌 HİSSE SEÇ",
            [r["sym"] for r in sorted(results, key=lambda x: x["score"], reverse=True)],
            format_func=lambda x: x.replace(".IS",""), key="kap_sym")
        kap_code = kap_sym.replace(".IS","").upper()

        st.markdown(f"""
        <div style='background:#050505; border:1px solid #003300;
                    border-radius:6px; padding:14px; margin-top:10px;'>
            <div style='font-family:Orbitron,monospace; font-size:11px;
                        color:#00FF00; margin-bottom:10px;'>
                🔗 KAP LİNKLERİ — {kap_code}
            </div>
            <div style='font-size:11px; line-height:2.2;'>
                <a href='https://www.kap.org.tr/tr/search?keywords={kap_code}'
                   target='_blank'
                   style='color:#00FFFF; text-decoration:none;'>
                    📋 Tüm Bildirimler →
                </a><br>
                <a href='https://www.kap.org.tr/tr/search?keywords={kap_code}&disclosureTypes=FR'
                   target='_blank'
                   style='color:#00FFFF; text-decoration:none;'>
                    💰 Finansal Raporlar →
                </a><br>
                <a href='https://www.kap.org.tr/tr/search?keywords={kap_code}&disclosureTypes=ODA'
                   target='_blank'
                   style='color:#00FFFF; text-decoration:none;'>
                    ⚡ Özel Durum Açıklamaları →
                </a><br>
                <a href='https://www.kap.org.tr/tr/search?keywords={kap_code}&disclosureTypes=DDN'
                   target='_blank'
                   style='color:#00FFFF; text-decoration:none;'>
                    💵 Temettü Bildirimleri →
                </a><br>
                <a href='https://finance.yahoo.com/quote/{kap_sym}/news'
                   target='_blank'
                   style='color:#FFFF00; text-decoration:none;'>
                    📰 Yahoo Finance Haberleri →
                </a><br>
                <a href='https://www.isyatirim.com.tr/analiz-ve-raporlar/hisse?hisse={kap_code}'
                   target='_blank'
                   style='color:#FFFF00; text-decoration:none;'>
                    📊 İş Yatırım Analiz →
                </a>
            </div>
        </div>""", unsafe_allow_html=True)

        # Mevcut analiz özeti
        kap_res = next((r for r in results if r["sym"] == kap_sym), None)
        if kap_res:
            sig_k, col_k, ok_k = signal(kap_res["score"])
            st.markdown(f"""
            <div style='background:#050505; border:1px solid {col_k}44;
                        border-left:3px solid {col_k}; border-radius:6px;
                        padding:12px; margin-top:10px; font-size:11px;'>
                <div style='font-family:Orbitron,monospace; font-size:10px;
                            color:#006600; margin-bottom:8px;'>
                    GÜNCEL TEKNİK DURUM
                </div>
                <div style='color:#fff; margin-bottom:4px;'>
                    {kap_code} · {kap_res["price"]:.2f} ₺
                </div>
                <div style='color:{col_k}; font-weight:700;'>{sig_k}</div>
                <div style='color:#666; font-size:10px; margin-top:4px;'>
                    Skor: {kap_res["score"]:+.1f} · RSI: {kap_res["rsi"]} ·
                    EMA: {kap_res["ema_pts"]}/5
                </div>
                <div style='color:#006600; font-size:9px; margin-top:6px;'>
                    Stop: {kap_res["stop"]:.2f} ₺ · Hedef: {kap_res["target1"]:.2f} ₺
                </div>
            </div>""", unsafe_allow_html=True)

    with kc2:
        st.markdown(f"""
        <div style='background:#050505; border:1px solid #003300;
                    border-radius:6px; padding:16px;'>
            <div style='font-family:Orbitron,monospace; font-size:11px;
                        color:#00FF00; margin-bottom:12px;'>
                📡 KAP NASIL KULLANILIR?
            </div>
            <div style='font-size:11px; color:#00CC00; line-height:2.0;'>
                <b style='color:#FFFF00;'>1. Özel Durum Açıklamaları (ODA)</b><br>
                &nbsp;&nbsp;Şirketten gelen ani haberler burada. Birleşme, satın alma,<br>
                &nbsp;&nbsp;sözleşme, yönetim değişikliği — fiyatı anlık etkiler.<br><br>

                <b style='color:#FFFF00;'>2. Finansal Raporlar (FR)</b><br>
                &nbsp;&nbsp;3 ayda bir yayınlanır. Kâr/zarar, borç, büyüme burada.<br>
                &nbsp;&nbsp;Beklentinin üstü → fiyat yükselir. Altı → düşer.<br><br>

                <b style='color:#FFFF00;'>3. Temettü Bildirimleri (DDN)</b><br>
                &nbsp;&nbsp;Şirket kâr payı dağıtacaksa burada açıklanır.<br>
                &nbsp;&nbsp;Temettü verimi yüksekse uzun vadeli cazip olabilir.<br><br>

                <b style='color:#00FF00;'>💡 PRO STRATEJİ:</b><br>
                &nbsp;&nbsp;Teknik analiz (bu sistem) + KAP haberi birlikte değerlendir.<br>
                &nbsp;&nbsp;Sistem AL diyor + pozitif KAP haberi var → GÜÇLÜ sinyal.<br>
                &nbsp;&nbsp;Sistem AL diyor + negatif KAP haberi var → BEKLE.
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div style='background:#050505; border:1px solid #003300;
                    border-radius:6px; padding:16px; margin-top:12px;'>
            <div style='font-family:Orbitron,monospace; font-size:11px;
                        color:#00FF00; margin-bottom:12px;'>
                🏦 TÜM HİSSELER HIZLI KAP ERİŞİM
            </div>""", unsafe_allow_html=True)

        for r in sorted(results, key=lambda x: x["score"], reverse=True):
            code = r["sym"].replace(".IS","")
            sig_r, col_r, ok_r = signal(r["score"])
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center;
                        padding:6px 0; border-bottom:1px solid #001100; font-size:10px;'>
                <span style='color:#00FF00; font-weight:700; min-width:60px;'>{code}</span>
                <span style='color:{col_r}; min-width:80px;'>{sig_r.split()[-1]}</span>
                <span style='color:#006600;'>{r["score"]:+.1f}</span>
                <a href='https://www.kap.org.tr/tr/search?keywords={code}'
                   target='_blank'
                   style='color:#00FFFF; text-decoration:none; font-size:9px;'>
                    KAP →
                </a>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.divider()
st.markdown(f"""
<div style='text-align:center;font-size:9px;color:#003300;padding:8px;font-family:Share Tech Mono;'>
    BIST QUANTUM PRO MAX · {datetime.now().strftime("%d.%m.%Y %H:%M")} ·
    VERI: YAHOO FINANCE · YATIRIM TAVSİYESİ DEĞİLDİR
</div>
""", unsafe_allow_html=True)
