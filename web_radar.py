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
        line=dict(color="#00FF0033", width=1, dash="dot"),
        name="BB", showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=close.index, y=bb_dn,
        line=dict(color="#00FF0033", width=1, dash="dot"),
        fill="tonexty", fillcolor="#00FF000A",
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
    fig.add_hline(y=70, line_dash="dot", line_color=RED+"88",    row=3, col=1)
    fig.add_hline(y=30, line_dash="dot", line_color=GREEN+"88",  row=3, col=1)
    fig.add_hrect(y0=30, y1=70, fillcolor="#00FF0006", line_width=0, row=3, col=1)

    # Stochastic
    fig.add_trace(go.Scatter(x=close.index, y=sk,
        line=dict(color=CYAN, width=1.2),
        name="STOCH K", showlegend=False), row=4, col=1)
    fig.add_trace(go.Scatter(x=close.index, y=sd_line,
        line=dict(color=YELLOW, width=1),
        name="STOCH D", showlegend=False), row=4, col=1)
    fig.add_hline(y=80, line_dash="dot", line_color=RED+"66",   row=4, col=1)
    fig.add_hline(y=20, line_dash="dot", line_color=GREEN+"66", row=4, col=1)

    # MACD
    hist_colors = [GREEN if float(v) >= 0 else RED for v in hist_s]
    fig.add_trace(go.Bar(x
