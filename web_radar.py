"""
╔══════════════════════════════════════════════════════════════╗
║           BIST WEB RADAR - Gerçek Zamanlı İzleme              ║
║  Çalıştır: streamlit run web_radar.py                          ║
║  Kur: pip install streamlit yfinance plotly pandas numpy     ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# ─────────────────────────────────────────────────────────────
# SAYFA AYARLARI
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BIST WEB RADAR",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# BIST HİSSELERİ (İzlenecek hisseler)
# ─────────────────────────────────────────────────────────────
WATCHLIST = {
    "AKBNK.IS": "Akbank",
    "GARAN.IS": "Garanti BBVA",
    "YKBNK.IS": "Yapı Kredi",
    "ISCTR.IS": "İş Bankası",
    "TUPRS.IS": "Tüpraş",
    "PETKM.IS": "Petkim",
    "THYAO.IS": "THY",
    "TCELL.IS": "Turkcell",
    "SAHOL.IS": "Sabancı Holding",
    "KCHOL.IS": "Koç Holding",
    "DOHOL.IS": "Doğan Holding",
    "VESTL.IS": "Vestel",
    "ASELS.IS": "Aselsan",
    "FROTO.IS": "Ford Otosan",
    "TOASO.IS": "Tofaş",
    "EREGL.IS": "Erdemir",
    "KRDMD.IS": "Kardemir",
    "BIMAS.IS": "BIM",
    "ULKER.IS": "Ülker",
    "HEKTS.IS": "Hektaş",
    "SISE.IS": "Şişecam",
    "PGSUS.IS": "Pegasus",
    "TAVHL.IS": "TAV Havalimanları",
}

# ─────────────────────────────────────────────────────────────
# TEKNİK GÖSTERGELER
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
    return mid + nstd * std, mid, mid - nstd * std

# ─────────────────────────────────────────────────────────────
# VERİ ÇEKME FONKSİYONU
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)  # 5 dakika önbellek
def get_data(sym, period="5d", interval="15m"):
    try:
        stock = yf.Ticker(sym)
        df = stock.history(period=period, interval=interval)
        return df
    except Exception as e:
        st.error(f"⚠️ {sym} için veri çekme hatası: {e}")
        return None

# ─────────────────────────────────────────────────────────────
# ANALİZ FONKSİYONU
# ─────────────────────────────────────────────────────────────
def analyze(df, sym):
    if df is None or df.empty or len(df) < 20:
        return None

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    price = close.iloc[-1]

    # RSI
    rsi = calc_rsi(close).iloc[-1]

    # EMA
    e9 = ema(close, 9).iloc[-1]
    e21 = ema(close, 21).iloc[-1]

    # MACD
    ml, sl, hist = calc_macd(close)
    macd_h = hist.iloc[-1]

    # Bollinger Bands
    bb_up, bb_mid, bb_dn = calc_bollinger(close)
    bb_pos = (price - bb_dn.iloc[-1]) / (bb_up.iloc[-1] - bb_dn.iloc[-1] + 1e-10) * 100

    # Stochastic
    lowest = low.rolling(14).min()
    highest = high.rolling(14).max()
    stoch_k = 100 * (close.iloc[-1] - lowest.iloc[-1]) / (highest.iloc[-1] - lowest.iloc[-1] + 1e-10)
    stoch_d = stoch_k.rolling(3).mean().iloc[-1]

    # Sinyal hesapla (Kompozit Skor)
    score = 0
    if rsi < 30: score += 10
    elif rsi > 70: score -= 10
    if price > e9: score += 5
    if price > e21: score += 5
    if macd_h > 0: score += 5
    if bb_pos < 20: score += 5
    elif bb_pos > 80: score -= 5
    if stoch_k < 20: score += 5
    elif stoch_k > 80: score -= 5

    # Sinyal belirle
    if score >= 20: signal = "⚡ GÜÇLÜ AL"
    elif score >= 10: signal = "📈 AL"
    elif score >= 0: signal = "🔄 NÖTR"
    elif score >= -10: signal = "🔽 ZAYIF SAT"
    else: signal = "📉 SAT"

    return {
        "sym": sym,
        "price": round(price, 2),
        "rsi": round(rsi, 1),
        "ema9": round(e9, 2),
        "ema21": round(e21, 2),
        "macd": round(macd_h, 4),
        "bb_pos": round(bb_pos, 1),
        "stoch_k": round(stoch_k, 1),
        "stoch_d": round(stoch_d, 1),
        "signal": signal,
        "score": score,
    }

# ─────────────────────────────────────────────────────────────
# ANA UYGULAMA
# ─────────────────────────────────────────────────────────────
st.title("📡 BIST WEB RADAR")
st.markdown("""
---
**Gerçek zamanlı hisse izleme ve teknik analiz aracı.**
*Seçtiğiniz hisselerin fiyatlarını, teknik göstergelerini ve sinyallerini izleyin.*
---
""")

# Sidebar
st.sidebar.header("⚙️ Ayarlar")
selected_syms = st.sidebar.multiselect(
    "📌 İzlenecek Hisseler",
    options=list(WATCHLIST.keys()),
    default=["AKBNK.IS", "GARAN.IS", "YKBNK.IS", "TUPRS.IS", "THYAO.IS"],
    format_func=lambda x: f"{x.replace('.IS', '')} ({WATCHLIST[x]})"
)
period = st.sidebar.selectbox("📅 Zaman Aralığı", ["1d", "5d", "1mo", "3mo", "1y"])
interval = st.sidebar.selectbox("⏱️ Güncelleme Aralığı", ["15m", "1h", "1d"])

# Veri çek ve analiz et
results = []
for sym in selected_syms:
    with st.spinner(f"{sym} verileri çekiliyor..."):
        df = get_data(sym, period=period, interval=interval)
        if df is not None:
            result = analyze(df, sym)
            if result:
                results.append(result)

# Sonuçları göster
if results:
    # Sinyal özeti
    st.markdown("### 🚨 **Sinyal Özeti**")
    buy_signals = [r for r in results if "AL" in r["signal"]]
    sell_signals = [r for r in results if "SAT" in r["signal"]]
    neutral_signals = [r for r in results if r["signal"] == "🔄 NÖTR"]

    col1, col2, col3 = st.columns(3)
    col1.metric("⚡ AL Sinyali", len(buy_signals))
    col2.metric("🔄 NÖTR", len(neutral_signals))
    col3.metric("📉 SAT Sinyali", len(sell_signals))

    # Detaylı tablo
    st.markdown("### 📊 **Detaylı Analiz**")
    df_results = pd.DataFrame(results)
    df_results = df_results[["sym", "price", "rsi", "ema9", "ema21", "macd", "bb_pos", "stoch_k", "signal", "score"]]
    df_results.columns = ["Hisse", "Fiyat (TL)", "RSI", "EMA9", "EMA21", "MACD", "Bollinger %", "Stoch %K", "Sinyal", "Skor"]
    st.dataframe(df_results, use_container_width=True)

    # Uyarılar
    st.markdown("### 🔔 **Uyarılar**")
    for result in results:
        if "GÜÇLÜ AL" in result["signal"]:
            st.success(f"🚀 **{result['sym'].replace('.IS', '')}**: {result['signal']} | Fiyat: {result['price']} TL | RSI: {result['rsi']} | Skor: {result['score']}")
        elif "AL" in result["signal"]:
            st.info(f"📈 **{result['sym'].replace('.IS', '')}**: {result['signal']} | Fiyat: {result['price']} TL | RSI: {result['rsi']}")
        elif "SAT" in result["signal"]:
            st.error(f"🔻 **{result['sym'].replace('.IS', '')}**: {result['signal']} | Fiyat: {result['price']} TL | RSI: {result['rsi']}")

    # Grafikler
    st.markdown("### 📈 **Grafikler**")
    for sym in selected_syms:
        df = get_data(sym, period=period, interval=interval)
        if df is not None:
            with st.expander(f"📊 {sym.replace('.IS', '')} - {WATCHLIST[sym]}"):
                fig = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.05,
                    subplot_titles=(f"{sym} Fiyat ve EMA", "RSI ve MACD"),
                    row_heights=[0.7, 0.3]
                )

                # Mum grafiği ve EMA
                fig.add_trace(
                    go.Candlestick(
                        x=df.index,
                        open=df["Open"],
                        high=df["High"],
                        low=df["Low"],
                        close=df["Close"],
                        name="Fiyat",
                        increasing_line_color="#00FF00",
                        decreasing_line_color="#FF0000"
                    ),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Scatter(x=df.index, y=ema(df["Close"], 9), line=dict(color="blue", width=1), name="EMA9"),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Scatter(x=df.index, y=ema(df["Close"], 21), line=dict(color="orange", width=1), name="EMA21"),
                    row=1, col=1
                )

                # RSI
                rsi = calc_rsi(df["Close"])
                fig.add_trace(
                    go.Scatter(x=df.index, y=rsi, line=dict(color="purple", width=1), name="RSI"),
                    row=2, col=1
                )
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

                # MACD
                ml, sl, hist = calc_macd(df["Close"])
                fig.add_trace(
                    go.Scatter(x=df.index, y=hist, line=dict(color="cyan", width=1), name="MACD Hist"),
                    row=2, col=1
                )

                fig.update_layout(
                    height=600,
                    template="plotly_dark",
                    xaxis_rangeslider_visible=False,
                    showlegend=True
                )
                st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ Lütfen izlenecek hisseleri seçin.")
