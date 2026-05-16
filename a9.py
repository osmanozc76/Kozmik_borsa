"""
╔══════════════════════════════════════════════════════════════╗
║       BIST QUANTUM ANALYZER — STREAMLIT ULTRA EDITION        ║
║  Geliştirici / Sistem Sahibi: OSMAN ÖZCAN                    ║
║  Çalıştırmak için:  streamlit run a9.py                     ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# SAYFA AYARLARI
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BIST Quantum Analyzer — Osman Özcan",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS — Karanlık, keskin, profesyonel tema
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght=300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace !important;
    background-color: #070a18 !important;
    color: #c0d4f0 !important;
}

.stApp { background: #070a18; }

/* Üst İmza Paneli */
.osman-signature {
    background: linear-gradient(90deg, #1a2550 0%, #0d1130 100%);
    border-left: 5px solid #00e5ff;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(0, 229, 255, 0.05);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0e22 0%, #080b1a 100%) !important;
    border-right: 1px solid #1a2240 !important;
}

/* Metrikler */
[data-testid="stMetric"] {
    background: #0d1130;
    border: 1px solid #1a2550;
    border-radius: 10px;
    padding: 12px 16px !important;
}
[data-testid="stMetricValue"] { color: #00e5ff !important; font-size: 1.4rem !important; }
[data-testid="stMetricLabel"] { color: #4466aa !important; font-size: 0.7rem !important; letter-spacing: 1px; }

/* Saf HTML Tablo Özelleştirmesi */
table {
    width: 100% !important;
    background-color: #0d1130 !important;
    border: 1px solid #1a2550 !important;
    border-radius: 8px !important;
    color: #c0d4f0 !important;
    border-collapse: collapse !important;
    margin: 10px 0 !important;
}
th {
    background-color: #1a2550 !important;
    color: #00e5ff !important;
    font-weight: 600 !important;
    border-bottom: 2px solid #00e5ff !important;
}
td, th {
    padding: 12px 10px !important;
    text-align: left !important;
    border-bottom: 1px solid #161f42 !important;
}
tr:hover {
    background-color: #111740 !important;
}

/* Selectbox & inputs */
.stSelectbox > div > div {
    background: #0d1130 !important;
    border: 1px solid #1a2550 !important;
    border-radius: 8px !important;
    color: #c0d4f0 !important;
}

#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-thumb { background: #1e2a5a; border-radius: 2px; }
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
# TEKNİK MATEMATİKSEL FONKSİYONLAR
# ─────────────────────────────────────────────────────────────
def ema(s, span): return s.ewm(span=span, adjust=False).mean()

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
    mid  = s.rolling(window).mean()
    std  = s.rolling(window).std()
    return mid + nstd*std, mid, mid - nstd*std

def calc_atr(high, low, close, period=14):
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
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
# COGNITIVE QUANTUM MATRİS MOTORU
# ─────────────────────────────────────────────────────────────
def analyze_stock(sym, df):
    if df is None or df.empty or len(df) < 30:
        return None

    close  = df["Close"].squeeze().astype(float)
    high   = df["High"].squeeze().astype(float)
    low    = df["Low"].squeeze().astype(float)
    volume = df["Volume"].squeeze().astype(float)
    price  = float(close.iloc[-1])

    rsi_s  = calc_rsi(close)
    rsi_v  = float(rsi_s.iloc[-1])
    rsi_p  = float(rsi_s.iloc[-4])

    e9   = float(ema(close, 9).iloc[-1])
    e21  = float(ema(close, 21).iloc[-1])
    e50  = float(ema(close, 50).iloc[-1]) if len(close) >= 50 else price
    e200 = float(ema(close, 200).iloc[-1]) if len(close) >= 100 else price

    ml, sl, hist = calc_macd(close)
    macd_h  = float(hist.iloc[-1])
    macd_p  = float(hist.iloc[-2])
    macd_cross = (float(hist.iloc[-2]) < 0 and macd_h > 0)

    bb_up, bb_mid, bb_dn = calc_bollinger(close)
    bb_pos = float((price - bb_dn.iloc[-1]) / (bb_up.iloc[-1] - bb_dn.iloc[-1] + 1e-10))

    atr_v   = float(calc_atr(high, low, close).iloc[-1])
    atr_pct = atr_v / price * 100

    obv_s   = calc_obv(close, volume)
    obv_ema = ema(obv_s, 20)
    obv_up  = float(obv_s.iloc[-1]) > float(obv_ema.iloc[-1])

    sk, sd = calc_stochastic(high, low, close)
    stoch_k = float(sk.iloc[-1])
    stoch_d = float(sd.iloc[-1])

    ret_1m = (price / float(close.iloc[-21]) - 1) * 100 if len(close) >= 21 else 0

    high52 = float(high.max())
    low52  = float(low.min())

    scores = {}
    if rsi_v < 25:    scores["RSI"] = 25
    elif rsi_v < 35:  scores["RSI"] = 18
    elif rsi_v < 45:  scores["RSI"] = 10
    elif rsi_v < 55:  scores["RSI"] = 4
    elif rsi_v < 65:  scores["RSI"] = 0
    elif rsi_v < 75:  scores["RSI"] = -8
    else:             scores["RSI"] = -18

    ema_pts = 0
    if price > e9:   ema_pts += 5
    if price > e21:  ema_pts += 7
    if e9 > e21:     ema_pts += 5
    if price > e50:  ema_pts += 5
    if price > e200: ema_pts += 3
    scores["EMA"] = ema_pts

    if macd_cross:          scores["MACD"] = 20
    elif macd_h > 0 and macd_h > macd_p: scores["MACD"] = 14
    elif macd_h > 0:        scores["MACD"] = 7
    elif macd_h < 0 and macd_h < macd_p: scores["MACD"] = -14
    else:                   scores["MACD"] = -5

    if bb_pos < 0.1:    scores["Bollinger"] = 14
    elif bb_pos < 0.3:  scores["Bollinger"] = 9
    elif bb_pos < 0.5:  scores["Bollinger"] = 4
    else:               scores["Bollinger"] = -5

    scores["Stochastic"] = 8 if (stoch_k < 20 and stoch_k > stoch_d) else 2
    scores["OBV"] = 8 if obv_up else -5
    scores["Momentum"] = 5 if ret_1m > 0 else -3

    total = sum(scores.values())
    confidence = min(100, max(0, (total + 30) / 1.5))

    stop = price - atr_v * 2
    tgt1 = price + atr_v * 3
    tgt2 = price + atr_v * 5

    pivot  = (high.iloc[-5:].max() + low.iloc[-5:].min() + price) / 3
    r1, s1 = 2*pivot - low.iloc[-5:].min(), 2*pivot - high.iloc[-5:].max()

    return {
        "sym":        sym,
        "sector":     UNIVERSE.get(sym, "Genel"),
        "price":      round(price, 2),
        "score":      round(total, 1),
        "confidence": round(confidence, 1),
        "scores":     scores,
        "rsi":        round(rsi_v, 1),
        "macd_hist":  round(macd_h, 4),
        "bb_pos":     round(bb_pos * 100, 1),
        "atr_pct":    round(atr_pct, 2),
        "high_52":    round(high52, 2),
        "low_52":     round(low52, 2),
        "stop":       round(stop, 2),
        "target1":    round(tgt1, 2),
        "target2":    round(tgt2, 2),
        "pivot":      round(pivot, 2),
        "r1": round(r1,2), "s1": round(s1,2),
        "close_series": close, "volume_series": volume,
        "high_series": high, "low_series": low
    }

def signal_info(score):
    if score >= 40:  return "GÜÇLÜ AL",  "#00ff88", "🟢"
    if score >= 15:  return "AL",         "#4ade80", "🟢"
    if score >= -5:  return "NÖTR",       "#fbbf24", "🟡"
    if score >= -25: return "SAT",        "#fb923c", "🔴"
    return "GÜÇLÜ SAT", "#ff2255", "🔴"

# ─────────────────────────────────────────────────────────────
# GRAFİK YAPILARI
# ─────────────────────────────────────────────────────────────
def make_candlestick_chart(r, df):
    close = r["close_series"]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3], vertical_spacing=0.03)
    fig.add_trace(go.Candlestick(
        x=close.index, open=df["Open"].squeeze(), high=df["High"].squeeze(), low=df["Low"].squeeze(), close=close,
        increasing_line_color="#00ff88", decreasing_line_color="#ff4466", name="Fiyat"
    ), row=1, col=1)
    fig.add_trace(go.Bar(x=close.index, y=r["volume_series"], marker_color="#4466aa", name="Hacim"), row=2, col=1)
    fig.update_layout(height=450, paper_bgcolor="#0a0e22", plot_bgcolor="#080b18", font=dict(family="JetBrains Mono", color="#8899bb"), xaxis_rangeslider_visible=False, margin=dict(l=10,r=10,t=10,b=10))
    return fig

# ─────────────────────────────────────────────────────────────
# ANA AKIŞ - ENGINE
# ─────────────────────────────────────────────────────────────
# Şık Osman Özcan İmza Katmanı
st.markdown(f"""
<div class="osman-signature">
    <span style="color:#00e5ff; font-weight:bold; font-size:1.2rem;">◆ BIST QUANTUM TERMINAL v9</span><br>
    <span style="color:#8899bb; font-size:0.85rem;">Sistem Sahibi & Baş Analist: </span>
    <span style="color:#ffffff; font-weight:600; font-size:0.95rem; letter-spacing:1px;">OSMAN ÖZCAN</span>
</div>
""", unsafe_allow_html=True)

st.caption(f"Veri Güncelleme: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Multi-Index Safe Engine")

with st.sidebar:
    st.header("⚙ AYARLAR")
    time_period = st.selectbox("Analiz Zaman Dilimi", ["3mo", "6mo", "1y"], index=0)
    st.markdown("---")
    st.markdown("**Sinyal Kılavuzu:**\n\n🟢 Güçlü Al / Al\n\n🟡 Nötr\n\n🔴 Sat / Güçlü Sat")

with st.spinner("BIST Piyasa Katmanları Çözümleniyor..."):
    tickers = list(UNIVERSE.keys())
    try:
        raw_data = yf.download(tickers, period=time_period, progress=False, group_by="ticker")
    except Exception as e:
        st.error(f"Yahoo Finance Bağlantı Hatası: {e}")
        raw_data = None

if raw_data is not None and not raw_data.empty:
    results = []
    
    for tk in tickers:
        try:
            if tk in raw_data.columns.levels[0] if isinstance(raw_data.columns, pd.MultiIndex) else tk in raw_data.columns:
                sub_df = raw_data[tk].dropna() if isinstance(raw_data.columns, pd.MultiIndex) else raw_data.dropna()
                res = analyze_stock(tk, sub_df)
                if res:
                    results.append(res)
        except:
            continue

    if results:
        results_df = pd.DataFrame(results).sort_values(by="score", ascending=False)
        
        tab1, tab2 = st.tabs(["📊 CANLI TARAMA PANELİ", "🎯 TEKİL HİSSE DERİNLİK"])
        
        with tab1:
            st.subheader("Algoritmik Skor Matrisi")
            
            html_table = "<table><thead><tr><th>Hisse</th><th>Sektör</th><th>Fiyat (TL)</th><th>Kuantum Skoru</th><th>Güven Oranı</th><th>RSI (14)</th><th>Sinyal</th></tr></thead><tbody>"
            for _, row in results_df.iterrows():
                lbl, clr, ico = signal_info(row['score'])
                html_table += f"<tr><td><b>{row['sym'].replace('.IS','')}</b></td><td>{row['sector']}</td><td>{row['price']}</td><td>{row['score']}</td><td>%{row['confidence']}</td><td>{row['rsi']}</td><td style='color:{clr}; font-weight:bold;'>{ico} {lbl}</td></tr>"
            html_table += "</tbody></table>"
            
            st.markdown(html_table, unsafe_allow_html=True)
            
        with tab2:
            selected_sym = st.selectbox("Hisse Seçiniz:", results_df["sym"].tolist())
            hisse_data = results_df[results_df["sym"] == selected_sym].iloc[0]
            
            selected_df = raw_data[selected_sym].dropna() if isinstance(raw_data.columns, pd.MultiIndex) else raw_data.dropna()
            sig_lbl, sig_clr, sig_ico = signal_info(hisse_data["score"])
            
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Son Fiyat", f"{hisse_data['price']} TL")
            col_m2.metric("Kuantum Sinyali", sig_lbl, delta=f"{hisse_data['score']} Puan")
            col_m3.metric("RSI (14)", hisse_data["rsi"])
            
            st.plotly_chart(make_candlestick_chart(hisse_data, selected_df), use_container_width=True)
            
            st.subheader("Algoritmik Al-Sat Seviyeleri")
            b1, b2 = st.columns(2)
            with b1:
                st.markdown(f"🎯 **Kısa Vade Hedef:** `{hisse_data['target1']} TL`")
                st.markdown(f"🚀 **Orta Vade Hedef:** `{hisse_data['target2']} TL`")
                st.markdown(f"🛑 **Sistem Stop-Loss:** `{hisse_data['stop']} TL`")
            with b2:
                st.markdown(f"🎛 **Pivot Seviyesi:** `{hisse_data['pivot']} TL`")
                st.markdown(f"📈 **Direnç Seviyesi (R1):** `{hisse_data['r1']} TL`")
                st.markdown(f"📉 **Destek Seviyesi (S1):** `{hisse_data['s1']} TL`")
    else:
        st.error("Veriler parse edilemedi. Lütfen sayfayı yenileyin.")
else:
    st.error("BIST Veri hatası! İnternet bağlantınızı kontrol edin.")
