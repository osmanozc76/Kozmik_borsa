import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings("ignore")

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BIST QUANTUM PRO MAX",
    page_icon="🛸",
    layout="wide"
)

# ============================================================
# CYBER UI
# ============================================================

st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"]{
    background-color:#000000;
    color:#00FF00;
}

.stApp{
    background-color:#000000;
}

h1,h2,h3,h4,p,span,div,label{
    color:#00FF00 !important;
}

[data-testid="stSidebar"]{
    background:#050505;
}

.stButton>button{
    background:black;
    color:#00FF00;
    border:1px solid #00FF00;
}

.stDataFrame{
    border:1px solid #00FF00;
}

#MainMenu, footer, header{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# UNIVERSE
# ============================================================

UNIVERSE = {
    "AKBNK.IS": "Bank",
    "GARAN.IS": "Bank",
    "YKBNK.IS": "Bank",
    "ASELS.IS": "Defense",
    "THYAO.IS": "Airlines",
    "SISE.IS": "Glass",
    "EREGL.IS": "Steel",
    "KCHOL.IS": "Holding",
    "SAHOL.IS": "Holding",
    "BIMAS.IS": "Retail",
    "TUPRS.IS": "Energy",
    "FROTO.IS": "Auto",
    "TOASO.IS": "Auto",
}

# ============================================================
# DATA LOADER
# ============================================================

@st.cache_data(ttl=300)
def load_data(symbol, period="1y", interval="1d"):

    try:

        df = yf.download(
            symbol,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=True,
            threads=False
        )

        if df is None or df.empty:
            return None

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        required = ["Open", "High", "Low", "Close", "Volume"]

        for col in required:
            if col not in df.columns:
                return None

        df.dropna(inplace=True)

        return df

    except:
        return None

# ============================================================
# INDICATORS
# ============================================================

def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def calc_rsi(series, period=14):

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)

    avg_gain = gain.ewm(com=period-1, adjust=False).mean()
    avg_loss = loss.ewm(com=period-1, adjust=False).mean()

    rs = avg_gain / (avg_loss + 1e-10)

    return 100 - (100 / (1 + rs))

def calc_macd(series):

    fast = ema(series, 12)
    slow = ema(series, 26)

    macd = fast - slow
    signal = ema(macd, 9)

    hist = macd - signal

    return macd, signal, hist

def calc_bollinger(series, window=20):

    mid = series.rolling(window).mean()
    std = series.rolling(window).std()

    upper = mid + std * 2
    lower = mid - std * 2

    return upper, mid, lower

def calc_atr(high, low, close, period=14):

    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    return tr.rolling(period).mean()

def calc_adx(high, low, close, period=14):

    plus_dm = high.diff()
    minus_dm = low.diff() * -1

    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm < 0] = 0

    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(period).mean()

    plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(period).mean() / atr)

    dx = (
        abs(plus_di - minus_di)
        / (plus_di + minus_di + 1e-10)
    ) * 100

    adx = dx.rolling(period).mean()

    return adx

def calc_relative_strength(stock_close, benchmark_close):

    stock_ret = stock_close.pct_change(20)
    benchmark_ret = benchmark_close.pct_change(20)

    rs = (1 + stock_ret) / (1 + benchmark_ret)

    return rs

# ============================================================
# MARKET REGIME
# ============================================================

def detect_market_regime(close):

    ema50 = ema(close, 50)
    ema200 = ema(close, 200)

    if float(ema50.iloc[-1]) > float(ema200.iloc[-1]):
        return "BULL"

    return "BEAR"

# ============================================================
# BACKTEST
# ============================================================

def run_backtest(df):

    close = df["Close"]

    rsi = calc_rsi(close)

    e9 = ema(close, 9)
    e21 = ema(close, 21)

    buy_signal = (
        (rsi < 35)
        & (e9 > e21)
    )

    trades = []

    for i in range(len(df)-5):

        if buy_signal.iloc[i]:

            entry = float(close.iloc[i])
            exitp = float(close.iloc[i+5])

            pnl = ((exitp / entry) - 1) * 100

            trades.append(pnl)

    if len(trades) == 0:

        return {
            "win_rate": 0,
            "avg_return": 0,
            "trades": 0
        }

    wins = [x for x in trades if x > 0]

    return {
        "win_rate": round(len(wins)/len(trades)*100, 2),
        "avg_return": round(np.mean(trades), 2),
        "trades": len(trades)
    }

# ============================================================
# ANALYZE ENGINE
# ============================================================

def analyze(symbol, df, xu100_df=None):

    if df is None or len(df) < 100:
        return None

    open_s = df["Open"].astype(float)

    high = df["High"].astype(float)
    low = df["Low"].astype(float)
    close = df["Close"].astype(float)
    volume = df["Volume"].astype(float)

    price = float(close.iloc[-1])

    rsi = calc_rsi(close)
    rsi_val = float(rsi.dropna().iloc[-1])

    macd, signal_line, hist = calc_macd(close)
    macd_hist = float(hist.dropna().iloc[-1])

    e9 = ema(close, 9)
    e21 = ema(close, 21)
    e50 = ema(close, 50)
    e200 = ema(close, 200)

    bb_up, bb_mid, bb_low = calc_bollinger(close)

    atr = calc_atr(high, low, close)
    atr_val = float(atr.dropna().iloc[-1])

    adx = calc_adx(high, low, close)
    adx_val = float(adx.dropna().iloc[-1])

    regime = detect_market_regime(close)

    score = 0

    # RSI

    if rsi_val < 30:
        score += 20

    elif rsi_val < 40:
        score += 10

    elif rsi_val > 70:
        score -= 20

    # EMA

    if price > float(e9.iloc[-1]):
        score += 5

    if price > float(e21.iloc[-1]):
        score += 10

    if float(e9.iloc[-1]) > float(e21.iloc[-1]):
        score += 10

    if float(e50.iloc[-1]) > float(e200.iloc[-1]):
        score += 10

    # MACD

    if macd_hist > 0:
        score += 10
    else:
        score -= 10

    # ADX

    if adx_val > 25:
        score += 10

    # RELATIVE STRENGTH

    rs_val = 1.0

    if xu100_df is not None:

        rs = calc_relative_strength(
            close,
            xu100_df["Close"]
        )

        rs_val = float(rs.dropna().iloc[-1])

        if rs_val > 1.05:
            score += 10

        elif rs_val < 1:
            score -= 5

    # REGIME

    if regime == "BULL":
        score *= 1.1
    else:
        score *= 0.9

    confidence = min(
        100,
        max(0, (score + 30) / 1.5)
    )

    stop = price - atr_val * 2
    target = price + atr_val * 3

    backtest = run_backtest(df)

    return {

        "symbol": symbol,

        "price": round(price, 2),

        "score": round(score, 2),

        "confidence": round(confidence, 2),

        "rsi": round(rsi_val, 2),

        "adx": round(adx_val, 2),

        "relative_strength": round(rs_val, 3),

        "regime": regime,

        "target": round(target, 2),

        "stop": round(stop, 2),

        "backtest": backtest,

        "open_s": open_s,

        "high": high,

        "low": low,

        "close": close,

        "volume": volume,

        "e9": e9,

        "e21": e21,

        "e50": e50,

        "bb_up": bb_up,

        "bb_low": bb_low,

        "rsi_s": rsi,

        "macd_hist_s": hist
    }

# ============================================================
# SIGNAL
# ============================================================

def signal(score):

    if score >= 50:
        return "⚡ GÜÇLÜ AL"

    if score >= 25:
        return "📈 AL"

    if score >= 0:
        return "🔄 NÖTR"

    return "📉 SAT"

# ============================================================
# CHART
# ============================================================

def make_chart(r):

    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.5,0.15,0.15,0.2]
    )

    fig.add_trace(

        go.Candlestick(

            x=r["close"].index,

            open=r["open_s"],

            high=r["high"],

            low=r["low"],

            close=r["close"],

            name="PRICE"

        ),

        row=1,
        col=1
    )

    fig.add_trace(

        go.Scatter(
            x=r["close"].index,
            y=r["e9"],
            name="EMA9"
        ),

        row=1,
        col=1
    )

    fig.add_trace(

        go.Scatter(
            x=r["close"].index,
            y=r["e21"],
            name="EMA21"
        ),

        row=1,
        col=1
    )

    fig.add_trace(

        go.Bar(
            x=r["close"].index,
            y=r["volume"],
            name="VOLUME"
        ),

        row=2,
        col=1
    )

    fig.add_trace(

        go.Scatter(
            x=r["close"].index,
            y=r["rsi_s"],
            name="RSI"
        ),

        row=3,
        col=1
    )

    fig.add_trace(

        go.Bar(
            x=r["close"].index,
            y=r["macd_hist_s"],
            name="MACD HIST"
        ),

        row=4,
        col=1
    )

    fig.update_layout(

        height=900,

        paper_bgcolor="black",

        plot_bgcolor="black",

        font=dict(color="#00FF00"),

        xaxis_rangeslider_visible=False
    )

    return fig

# ============================================================
# HEADER
# ============================================================

st.title("🛸 BIST QUANTUM PRO MAX")

# ============================================================
# LOAD XU100
# ============================================================

xu100_df = load_data("XU100.IS")

# ============================================================
# MARKET SCAN
# ============================================================

results = []

with st.spinner("QUANTUM ENGINE SCANNING..."):

    for symbol in UNIVERSE:

        df = load_data(symbol)

        if df is not None:

            result = analyze(
                symbol,
                df,
                xu100_df
            )

            if result:
                results.append(result)

# ============================================================
# EMPTY CHECK
# ============================================================

if len(results) == 0:

    st.error("Veri alınamadı")

    st.stop()

# ============================================================
# TABLE
# ============================================================

scan_df = pd.DataFrame([

    {

        "SYMBOL": r["symbol"],

        "PRICE": r["price"],

        "SCORE": r["score"],

        "CONF": r["confidence"],

        "RSI": r["rsi"],

        "ADX": r["adx"],

        "RS": r["relative_strength"],

        "SIGNAL": signal(r["score"])

    }

    for r in results

])

scan_df = scan_df.sort_values(
    "SCORE",
    ascending=False
)

# ============================================================
# MARKET PANEL
# ============================================================

bullish = len(scan_df[scan_df["SCORE"] > 20])

bearish = len(scan_df[scan_df["SCORE"] < 0])

c1, c2, c3 = st.columns(3)

c1.metric("BULLISH", bullish)

c2.metric("BEARISH", bearish)

c3.metric("TOTAL", len(scan_df))

# ============================================================
# TABLE VIEW
# ============================================================

st.dataframe(
    scan_df,
    use_container_width=True
)

# ============================================================
# DETAIL PANEL
# ============================================================

st.subheader("📡 HİSSE DETAY ANALİZİ")

selected = st.selectbox(
    "HİSSE SEÇ",
    scan_df["SYMBOL"].tolist()
)

selected_result = None

for r in results:

    if r["symbol"] == selected:

        selected_result = r

        break

if selected_result:

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "FİYAT",
        selected_result["price"]
    )

    c2.metric(
        "SKOR",
        selected_result["score"]
    )

    c3.metric(
        "RSI",
        selected_result["rsi"]
    )

    c4.metric(
        "ADX",
        selected_result["adx"]
    )

    st.success(
        signal(selected_result["score"])
    )

    st.write(
        f"REGIME: {selected_result['regime']}"
    )

    st.write(
        f"STOP: {selected_result['stop']}"
    )

    st.write(
        f"TARGET: {selected_result['target']}"
    )

    bt = selected_result["backtest"]

    st.info(

        f"BACKTEST → "
        f"WIN RATE: %{bt['win_rate']} | "
        f"AVG RETURN: %{bt['avg_return']} | "
        f"TRADES: {bt['trades']}"
    )

    fig = make_chart(selected_result)

    st.plotly_chart(
        fig,
        use_container_width=True
    )
