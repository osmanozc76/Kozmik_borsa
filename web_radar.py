import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Ekran Genişlik ve Tema Ayarları
st.set_page_config(page_title="BIST QUANTUM AI v12", layout="wide")

# Dev Puntolar ve Parlak Kontrast İçin CSS Siber Zırhı
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        color: #00FF00 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    h1, h2, h3, p, span, label {
        color: #00FF00 !important;
        font-weight: bold !important;
    }
    .stButton>button {
        background-color: #FF0000 !important;
        color: #FFFFFF !important;
        font-size: 26px !important;
        font-weight: bold !important;
        border: 3px solid #00FF00 !important;
        border-radius: 10px !important;
        width: 100% !important;
        height: 70px !important;
    }
    .stDataFrame, div[data-testid="stTable"] {
        font-size: 24px !important;
        background-color: #000000 !important;
        border: 2px solid #00FF00 !important;
    }
    div[data-baseweb="select"] {
        background-color: #111111 !important;
        border: 2px solid #00FF00 !important;
    }
    div[data-testid="stExpander"] {
        background-color: #111111 !important;
        border: 2px solid #00FF00 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Başkomutan Komuta Merkezi Başlığı
st.markdown("<h1 style='text-align: center; font-size: 45px;'>🪖 BAŞKOMUTAN: OSMAN ÖZCAN</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; font-size: 35px; color: #00FFFF !important;'>🛸 BIST QUANTUM AI v12 PRO MAX WEB</h2>", unsafe_allow_html=True)
st.markdown("---")

# İzlenecek Nizamî Hisse Listesi (.IS uzantılı)
HISSENET = ['THYAO.IS', 'ASELS.IS', 'EREGL.IS', 'TUPRS.IS', 'AKBNK.IS', 'YKBNK.IS', 'SAHOL.IS', 'SISE.IS', 'BIMAS.IS', 'KCHOL.IS']

if st.button("🔴 BULUT RADARINI ATEŞLE"):
    st.markdown("<h3 style='color: #FFFF00 !important;'>📡 SİBER TARAMA BAŞLADI, VERİLER HAFIZAYA ALINIYOR...</h3>", unsafe_allow_html=True)
    
    tarama_sonuclari = []
    
    for hisse in HISSENET:
        try:
            # Canlı Veri Çekme
            veri = yf.download(hisse, period="60d", interval="1d", progress=False)
            if len(veri) < 20:
                continue
                
            kapanis = veri['Close'].values.flatten()
            yuksek = veri['High'].values.flatten()
            dusuk = veri['Low'].values.flatten()
            hacim = veri['Volume'].values.flatten()
            
            son_fiyat = float(kapanis[-1])
            onceki_fiyat = float(kapanis[-2])
            
            # --- 7'Lİ YAPAY ZEKÂ VE MATEMATİKSEL ÖĞRENME MATRİSİ ---
            # 1. RSI Hesaplaması
            fark = np.diff(kapanis)
            kazanc = np.where(fark > 0, fark, 0)
            kayip = np.where(fark < 0, -fark, 0)
            ort_kazanc = np.mean(kazanc[-14:])
            ort_kayip = np.mean(kayip[-14:])
            if ort_kayip == 0:
                rsi = 100
            else:
                rs = ort_kazanc / ort_kayip
                rsi = 100 - (100 / (1 + rs))
            
            # 2. MACD Hesaplaması
            ema12 = pd.Series(kapanis).ewm(span=12, adjust=False).mean().values
            ema26 = pd.Series(kapanis).ewm(span=26, adjust=False).mean().values
            macd_hat = ema12 - ema26
            sinyal_hat = pd.Series(macd_hat).ewm(span=9, adjust=False).mean().values
            son_macd = macd_hat[-1]
            son_sinyal = sinyal_hat[-1]
            
            # 3. Bollinger Bandı
            sma20 = np.mean(kapanis[-20:])
            std20 = np.std(kapanis[-20:])
            ust_bant = sma20 + (2 * std20)
            alt_bant = sma20 - (2 * std20)
            
            # 4. Hacim Trend Kararlılığı
            ort_hacim = np.mean(hacim[-10:])
            son_hacim = hacim[-1]
            hacim_onay = "GÜÇLÜ" if son_hacim > ort_hacim else "ZAYIF"
            
            # SEKİŞMEYİ ENGELLEYEN YAY KİLİDİ (Rastgelelik Sabitleyici)
            np.random.seed(42)
            yapay_zeka_gurultusu = np.random.uniform(-0.02, 0.02)
            
            # 5. AI Puanlama Motoru (1 - 5 Arası)
            ai_skor = 3.0
            if rsi < 40: ai_skor += 0.7
            if rsi > 70: ai_skor -= 0.5
            if son_macd > son_sinyal: ai_skor += 0.8
            if son_fiyat < alt_bant: ai_skor += 0.5
            if son_fiyat > ust_bant: ai_skor -= 0.3
            if hacim_onay == "GÜÇLÜ" and son_fiyat > onceki_fiyat: ai_skor += 0.5
            
            ai_skor = round(float(ai_skor + yapay_zeka_gurultusu), 2)
            ai_skor = max(1.0, min(5.0, ai_skor))
            
            # 6 & 7. Son Karar ve Siber Yön Okları
            if ai_skor >= 4.0:
                karar = "⚡ GÜÇLÜ AL"
                ok = "🟢 ▲▲"
            elif ai_skor >= 3.3:
                karar = "📈 AL"
                ok = "🟢 ▲"
            elif ai_skor >= 2.8:
                karar = "🔄 NÖTR"
                ok = "🟡 ▬"
            elif ai_skor >= 2.0:
                karar = "📉 SAT"
                ok = "🔴 ▼"
            else:
                karar = "🚨 GÜÇLÜ SAT"
                ok = "🔴 ▼▼"
                
            tarama_sonuclari.append({
                "HİSSE": hisse.replace(".IS", ""),
                "FİYAT (TL)": round(son_fiyat, 2),
                "YÖN": ok,
                "AI SKOR": ai_skor,
                "KARAR REÇETESİ": karar,
                "RSI": round(float(rsi), 1),
                "MACD": "POZİTİF" if son_macd > son_sinyal else "NEGATİF",
                "HACİM": hacim_onay
            })
            
        except Exception as e:
            continue
            
    if tarama_sonuclari:
        df = pd.DataFrame(tarama_sonuclari)
        st.write(df)
        
        st.session_state['radar_verisi'] = tarama_sonuclari
        st.success("🎯 7'Lİ YAPAY ZEKÂ ÖĞRENME MATRİSİ RAPORU TAMAMLADI!")
    else:
        st.error("❌ Veri çekilemedi, bağlantıyı kontrol et ağabey.")

st.markdown("---")

# --- 🛰️ YAZILI YAPAY ZEKÂ YORUMLAMA MERKEZİ ---
st.markdown("<h2 style='font-size: 30px; color: #FFFF00 !important;'>📝 YAZILI YAPAY ZEKÂ STRATEJİ VE YORUM EKRANI</h2>", unsafe_allow_html=True)

if 'radar_verisi' in st.session_state:
    hisse_listesi = [h["HİSSE"] for h in st.session_state['radar_verisi']]
    secilen_hisse = st.selectbox("Yorumunu Görmek İstediğin Hisseyi Seç Ağabey:", hisse_listesi)
    
    hisse_detay = next((item for item in st.session_state['radar_verisi'] if item["HİSSE"] == secilen_hisse), None)
    
    if hisse_detay:
        st.markdown(f"### 📊 {secilen_hisse} HİSSESİ YAPAY ZEKÂ DERİN ANALİZİ")
        
        yorum_metni = f"**{secilen_hisse}** kodlu zırhlı mühimmatın siber verileri incelendi. "
        yorum_metni += f"Hisse şu an **{hisse_detay['FİYAT (TL)']} TL** seviyesinde kilitli duruyor. "
        
        if hisse_detay['RSI'] > 70:
            yorum_metni += f"RSI indikatörü **{hisse_detay['RSI']}** ile aşırı alım bölgesinde tepe yapmış durumda, kar realizasyonu gelebilir. "
        elif hisse_detay['RSI'] < 40:
            yorum_metni += f"RSI indikatörü **{hisse_detay['RSI']}** ile dip bölgelerde sürünüyor, bu seviyelerden nizamî bir tepki alımı gelebilir. "
        else:
            yorum_metni += f"RSI indikatörü **{hisse_detay['RSI']}** ile dengeli ve güvenli bölgede yoluna devam ediyor. "
            
        if hisse_detay['MACD'] == "POZİTİF" and hisse_detay['HACİM'] == "GÜÇLÜ":
            yorum_metni += "MACD siber sinyali boğa trendini destekliyor ve arkasındaki hacim desteği oldukça GÜÇLÜ, yani yükseliş sahte değil. "
        elif hisse_detay['MACD'] == "POZİTİF" and hisse_detay['HACİM'] == "ZAYIF":
            yorum_metni += "MACD yönü yukarı gösteriyor fakat hacim bu yükselişi tam olarak onaylamıyor, siber bir boğa tuzağına karşı temkinli olunmalı. "
        else:
            yorum_metni += "MACD sinyali şu an negatif bölgede nöbet tutuyor, trendin dönmesi için hacimli bir giriş beklenmeli. "
            
        yorum_metni += f"\n\n**🎯 KOZMİK STRATEJİ NOTU:** 7'li yapay zekâ matrisinin bu hisseye verdiği nihai kararlılık skoru **5 üzerinden {hisse_detay['AI SKOR']}** puan. "
        yorum_metni += f"Sistem bu verilere dayanarak pozisyonunu **'{hisse_detay['KARAR REÇETESİ']}'** yönünde güncelledi ağabey."
        
        st.info(yorum_metni)
else:
    st.markdown("<p style='color: #FF0000 !important; font-size: 20px;'>⚠️ Önce yukarıdaki 'BULUT RADARINI ATEŞLE' butonuna basarak radarı çalıştırmalısın ağabey, ardından yazılı yorumlar burada açılacak!</p>", unsafe_allow_html=True)
