"""
╔══════════════════════════════════════════════════════════════╗
║       BIST QUANTUM ANALYZER — AI PRO EDITION v12 WEB         ║
║  Sistem Sahibi: OSMAN ÖZCAN                                  ║
║  (Streamlit Cloud Bulut Sunucuları İçin Güçlendirilmiş Sürüm)║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import time

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# 1. BULUT UYUMLU MOBİL TASARIM AYARLARI
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="BIST Quantum AI v12 Web", page_icon="◆", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace !important;
    background-color: #040814 !important;
    color: #ffffff !important;
}
.stApp { background: #040814; }

.title-box { 
    text-align: center; 
    padding: 25px 10px; 
    margin-bottom: 30px; 
    border-bottom: 3px solid #00ff88;
}
.main-title {
    color: #00e5ff !important;
    font-size: 34px !important;
    font-weight: 700 !important;
    letter-spacing: -1px;
    margin: 0 !important;
    text-shadow: 0 0 15px rgba(0,229,255,0.4);
}
.sub-title {
    color: #00ff88 !important;
    font-size: 18px !important;
    font-weight: bold !important;
    margin-top: 15px !important;
    line-height: 1.4;
}

.stButton > button {
    background: linear-gradient(135deg, #00ff88, #00aa55) !important;
    border: none !important;
    color: black !important;
    font-weight: bold !important;
    font-size: 22px !important;
    border-radius: 10px !important;
    width: 100%;
    padding: 16px !important;
    box-shadow: 0 4px 15px rgba(0,255,136,0.3);
}

.cyber-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 15px;
    background-color: #0b1126;
    border: 2px solid #1e293b;
}
.cyber-table th {
    background-color: #121b3a;
    color: #00e5ff;
    padding: 14px 10px;
    font-weight: bold;
    border-bottom: 2px solid #00ff88;
}
.cyber-table td {
    padding: 14px 10px;
    border-bottom: 1px solid #1e293b;
    color: #ffffff;
    font-weight: 500;
}
.badge-score { background: #00ff8822; color: #00ff88; padding: 4px 8px; border-radius: 4px; font-weight: bold; border: 1px solid #00ff88; }
.badge-prob { background: #00e5ff22; color: #00e5ff; padding: 4px 8px; border-radius: 4px; font-weight: bold; border: 1px solid #00e5ff; }

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='title-box'>
    <h1 class='main-title'>◆ BIST QUANTUM AI v12 WEB</h1>
    <p class='sub-title'>Yerel Yapay Zekâ Tabanlı Algoritmik Karar Destek Terminali<br>Başkomutan: OSMAN ÖZCAN</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 2. BIST EVRENİ Tanımlaması
# ─────────────────────────────────────────────────────────────
UNIVERSE = {
    "AKBNK.IS": "Bankacılık",  "GARAN.IS": "Bankacılık",
    "YKBNK.IS": "Bankacılık",  "SAHOL.IS": "Holding",
    "FROTO.IS": "Otomotiv",    "TOASO.IS": "Otomotiv",
    "ASELS.IS": "Savunma",     "TUPRS.IS": "Enerji",
    "PETKM.IS": "Petrokimya",  "SASA.IS":  "Kimya",
    "EREGL.IS": "Demir-Çelik", "KRDMD.IS": "Demir-Çelik",
    "BIMAS.IS": "Perakende",   "KCHOL.IS": "Holding",
    "SISE.IS":  "Cam",         "TCELL.IS": "Telekom",
    "TTKOM.IS": "Telekom",     "THYAO.IS": "Havacılık",
    "PGSUS.IS": "Havacılık"
}

# ─────────────────────────────────────────────────────────────
# 3. KENDİ KENDİNE ÖĞRENEN QUANTUM MOTORU
# ─────────────────────────────────────────────────────────────
class QuantumAIv12:
    def __init__(self):
        self.weights = np.array([0.12, 0.18, 0.15, 0.10, 0.20, 0.15, 0.10])
        self.bias = 0.0
        self.lr = 0.003

    def predict(self, features):
        z = np.dot(features, self.weights) + self.bias
        return 1 / (1 + np.exp(-np.clip(z, -15, 15)))

    def train(self, features, label):
        pred = self.predict(features)
        error = label - pred
        self.weights += self.lr * error * np.array(features)
        self.bias += self.lr * error

@st.cache_resource
def init_ai(): return QuantumAIv12()
ai = init_ai()

# İndikatör Hesaplama Fonksiyonları
def ema(s, span): return s.ewm(span=span, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)
    avg_gain = gain.ewm(com=period-1, adjust=False).mean()
    avg_loss = loss.ewm(com=period-1, adjust=False).mean()
    return 100 - (100 / (1 + (avg_gain / (avg_loss + 1e-10))))

def atr(high, low, close, period=14):
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def macd(series):
    fast = ema(series, 12)
    slow = ema(series, 26)
    macd_line = fast - slow
    signal = ema(macd_line, 9)
    return macd_line, signal

def calc_bollinger(series, period=20):
    mid = series.rolling(period).mean()
    std = series.rolling(period).std()
    return mid + (2 * std), mid, mid - (2 * std)

def analyze_stock(symbol, df):
    if df is None or len(df) < 50: return None
    try:
        close = df["Close"].squeeze()
        high = df["High"].squeeze()
        low = df["Low"].squeeze()
        volume = df["Volume"].squeeze()
        price = float(close.iloc[-1])

        ema20 = ema(close, 20)
        ema50 = ema(close, 50)
        rsi_series = rsi(close)
        macd_line, _ = macd(close)
        atr_series = atr(high, low, close)
        
        ret5 = (close.iloc[-1] - close.iloc[-5]) / close.iloc[-5]
        volatility = close.pct_change().rolling(20).std().iloc[-1]
        momentum = close.pct_change(10).iloc[-1]
        vol_ratio = volume.iloc[-1] / (volume.iloc[-20:].mean() + 1e-9)

        features = [rsi_series.iloc[-1]/100.0, price/(ema20.iloc[-1]+1e-9), price/(ema50.iloc[-1]+1e-9), min(vol_ratio/5.0, 1.0), ret5, momentum, macd_line.iloc[-1]/(price+1e-9)]
        prob = ai.predict(features)
        ai.train(features, 1 if close.pct_change().shift(-1).iloc[-2] > 0 else 0)

        score = 0
        if rsi_series.iloc[-1] < 35: score += 15
        if ema20.iloc[-1] > ema50.iloc[-1]: score += 15
        if momentum > 0: score += 10
        if macd_line.iloc[-1] > 0: score += 15
        if vol_ratio > 1.3: score += 10

        final_score = max(0, min(100, int((prob * 60) + score)))

        return {
            "symbol": symbol, "price": round(price, 2), "score": final_score, "ai_prob": round(prob * 100, 1),
            "rsi": round(rsi_series.iloc[-1], 1), "target": round(price + (atr_series.iloc[-1] * 3), 2),
            "stop": round(price - (atr_series.iloc[-1] * 2), 2), "close": close
        }
    except:
        return None

# ─────────────────────────────────────────────────────────────
# 4. BULUT SUNUCULARI İÇİN GÜÇLENDİRİLMİŞ VERİ ÇEKME SİSTEMİ
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def fetch_data_safe():
    symbols = list(UNIVERSE.keys())
    data_dict = {}
    for sym in symbols:
        try:
            ticker = yf.Ticker(sym)
            df = ticker.history(period="1y", auto_adjust=True)
            if not df.empty:
                data_dict[sym] = df
            time.sleep(0.2) # Sunucu koruma gecikmesi (Yahoo Kalkanı)
        except:
            continue
    return data_dict

# ─────────────────────────────────────────────────────────────
# ARAYÜZ SEKMELERİ
# ─────────────────────────────────────────────────────────────
page1, page2 = st.tabs(["📊 STRATEJİK RADAR", "🎯 DERİN GRAFİK ANALİZİ"])

with page1:
    st.sidebar.header("Quantum Web Kontrol")
    sector_filter = st.sidebar.selectbox("Sektör Filtresi", ["HEPSİ"] + sorted(list(set(UNIVERSE.values()))))

    if st.button("🔴 BULUT RADARINI ATEŞLE"):
        with st.spinner("Siber veri kanalları taranıyor..."):
            raw_data = fetch_data_safe()
            results = []
            
            for symbol, sector in UNIVERSE.items():
                if sector_filter != "HEPSİ" and sector != sector_filter: continue
                if symbol in raw_data:
                    res = analyze_stock(symbol, raw_data[symbol])
                    if res:
                        res["sector"] = sector
                        results.append(res)
            
            if results:
                st.session_state["web_results"] = sorted(results, key=lambda x: x["score"], reverse=True)
            else:
                st.error("Veri çekme hattında geçici kesinti oluştu, lütfen az sonra tekrar deneyin ağabey.")

    if "web_results" in st.session_state:
        res = st.session_state["web_results"]
        html_table = "<div style='overflow-x:auto;'><table class='cyber-table'>"
        html_table += "<tr><th>HİSSE</th><th>FİYAT</th><th>Y.Z. PROB</th><th>SKOR</th><th>RSI</th><th>NİZAMÎ HEDEF</th><th>STOP</th></tr>"
        for r in res:
            html_table += f"<tr><td><b>{r['symbol'].replace('.IS', '')}</b></td><td>{r['price']} TL</td><td><span class='badge-prob'>%{r['ai_prob']}</span></td><td><span class='badge-score'>{r['score']}</span></td><td>{r['rsi']}</td><td>{r['target']}</td><td>{r['stop']}</td></tr>"
        html_table += "</table></div>"
        st.markdown(html_table, unsafe_allow_html=True)

with page2:
    if "web_results" not in st.session_state:
        st.info("⚠️ Grafikleri aktif etmek için önce Stratejik Radar sayfasında radarı ateşlemelisin ağabey.")
    else:
        res = st.session_state["web_results"]
        selected = st.selectbox("Hisseyi Seçin:", [r["symbol"].replace(".IS", "") for r in res])
        sel_data = [x for x in res if x["symbol"].replace(".IS", "") == selected][0]
        close = sel_data["close"]
        
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3], vertical_spacing=0.03)
        fig.add_trace(go.Scatter(x=close.index, y=close, mode="lines", line=dict(color="#00ff88", width=2), name="Fiyat"), row=1, col=1)
        fig.add_trace(go.Scatter(x=close.index, y=ema(close, 20), line=dict(color="#fbbf24", width=1.5), name="EMA20"), row=1, col=1)
        fig.add_trace(go.Scatter(x=close.index, y=rsi(close), line=dict(color="#00e5ff", width=1.5), name="RSI"), row=2, col=1)
        fig.update_layout(height=500, paper_bgcolor="#040814", plot_bgcolor="#080b18", font=dict(family="JetBrains Mono", color="#ffffff"), xaxis_rangeslider_visible=False, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
      
