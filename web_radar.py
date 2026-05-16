import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(page_title="BIST QUANTUM PRO MAX", page_icon="🛸", layout="wide")

# ─────────────────────────────────────────────────────────────
# BIST EVRENİ
# ─────────────────────────────────────────────────────────────
UNIVERSE = {
    "AKBNK.IS": "Bankacılık","GARAN.IS": "Bankacılık","YKBNK.IS": "Bankacılık",
    "SAHOL.IS": "Holding","FROTO.IS": "Otomotiv","TOASO.IS": "Otomotiv",
    "ASELS.IS": "Savunma","VESTL.IS": "Elektronik","TUPRS.IS": "Enerji",
    "PETKM.IS": "Petrokimya","SASA.IS": "Kimya","EREGL.IS": "Demir-Çelik",
    "KRDMD.IS": "Demir-Çelik","BIMAS.IS": "Perakende","ULKER.IS": "Gıda",
    "KCHOL.IS": "Holding","DOHOL.IS": "Holding","SISE.IS": "Cam",
    "HEKTS.IS": "Sağlık","TCELL.IS": "Telekom","TTKOM.IS": "Telekom",
    "THYAO.IS": "Havacılık","PGSUS.IS": "Havacılık","TAVHL.IS": "Havalimanı",
}

# ─────────────────────────────────────────────────────────────
# İNDİKATÖRLER
# ─────────────────────────────────────────────────────────────
def ema(s, span): return s.ewm(span=span, adjust=False).mean()
def calc_rsi(s, period=14):
    delta = s.diff(); gain = delta.clip(lower=0); loss = (-delta).clip(lower=0)
    ag = gain.ewm(com=period-1, adjust=False).mean(); al = loss.ewm(com=period-1, adjust=False).mean()
    return 100 - (100 / (1 + ag/(al+1e-10)))
def calc_macd(s, fast=12, slow=26, signal=9):
    fe, se = s.ewm(span=fast, adjust=False).mean(), s.ewm(span=slow, adjust=False).mean()
    ml = fe - se; sl = ml.ewm(span=signal, adjust=False).mean()
    return ml, sl, ml-sl
def calc_bollinger(s, window=20, nstd=2):
    mid, std = s.rolling(window).mean(), s.rolling(window).std()
    return mid+nstd*std, mid, mid-nstd*std

# ─────────────────────────────────────────────────────────────
# ANALİZ MOTORU
# ─────────────────────────────────────────────────────────────
def analyze(sym, df):
    if df is None or df.empty or len(df) < 30: return None
    close, high, low, volume = df["Close"], df["High"], df["Low"], df["Volume"]
    price = float(close.iloc[-1])
    rsi_v = float(calc_rsi(close).iloc[-1])
    ml, sl, hist = calc_macd(close); macd_h = float(hist.iloc[-1])
    bb_up, bb_mid, bb_dn = calc_bollinger(close)
    bb_pos = (price - bb_dn.iloc[-1])/(bb_up.iloc[-1]-bb_dn.iloc[-1]+1e-10)
    score = 0
    if rsi_v < 35: score += 15
    if macd_h > 0: score += 10
    if bb_pos < 0.2: score += 10
    return {"sym": sym,"price": round(price,2),"score": score,"rsi": round(rsi_v,1),"macd": macd_h,"bb_pos": round(bb_pos*100,1)}

# ─────────────────────────────────────────────────────────────
# VERİ ÇEKME
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def fetch_data():
    return yf.download(list(UNIVERSE.keys()), period="6mo", auto_adjust=True, progress=False)

# ─────────────────────────────────────────────────────────────
# ANA ÇALIŞMA
# ─────────────────────────────────────────────────────────────
raw = fetch_data()
if st.button("🔴 QUANTUM RADAR SCAN"):
    results = []
    for sym, sector in UNIVERSE.items():
        try:
            df = pd.DataFrame({
                "Close": raw["Close"][sym],"High": raw["High"][sym],
                "Low": raw["Low"][sym],"Volume": raw["Volume"][sym]
            }).dropna()
            res = analyze(sym, df)
            if res: res["sector"] = sector; results.append(res)
        except: continue
    if results:
        results = sorted(results, key=lambda x: x["score"], reverse=True)
        df = pd.DataFrame(results)
        st.write(df)
        st.success("🎯 Tarama tamamlandı, en güçlü hisseler bulundu!")

        # Top 5 Kartları
        st.markdown("---")
        st.subheader("🏆 En Güçlü 5 Hisse")
        top5 = results[:5]
        cols = st.columns(5)
        for i, r in enumerate(top5):
            cols[i].metric(r["sym"].replace(".IS",""), f"{r['price']} TL", f"Skor: {r['score']}")
