import streamlit as st
import random
import string
import time
from datetime import datetime

# === Yardımcı Fonksiyonlar ===
def analyze_password(password):
    """Şifrenin gücünü analiz eder."""
    score = 0
    length = len(password)
    feedback = []
    
    # Uzunluk skoru
    if length >= 16:
        score += 3
        feedback.append("✓ Mükemmel uzunluk")
    elif length >= 12:
        score += 2
        feedback.append("✓ İyi uzunluk")
    elif length >= 8:
        score += 1
        feedback.append("⚠ Orta uzunluk")
    else:
        feedback.append("✗ Çok kısa")
    
    # Karakter türü kontrolleri
    if any(c.islower() for c in password):
        score += 1
        feedback.append("✓ Küçük harf")
    else:
        feedback.append("✗ Küçük harf yok")
        
    if any(c.isupper() for c in password):
        score += 1
        feedback.append("✓ Büyük harf")
    else:
        feedback.append("✗ Büyük harf yok")
        
    if any(c.isdigit() for c in password):
        score += 1
        feedback.append("✓ Rakam")
    else:
        feedback.append("✗ Rakam yok")
        
    if any(c in string.punctuation for c in password):
        score += 2
        feedback.append("✓ Özel karakter")
    else:
        feedback.append("✗ Özel karakter yok")
    
    # Güç seviyesini belirle
    if score <= 3:
        level = "🔴 Zayıf"
        recommendation = "Bu şifre çok zayıf! Daha uzun ve karmaşık bir şifre kullanın."
    elif score <= 5:
        level = "🟡 Orta"
        recommendation = "Bu şifre orta seviyede. Özel karakterler ekleyerek güçlendirebilirsiniz."
    elif score <= 7:
        level = "🟢 Güçlü"
        recommendation = "Bu şifre güçlü! Güvenle kullanabilirsiniz."
    else:
        level = "🟢 Çok Güçlü"
        recommendation = "Mükemmel! Bu şifre çok güçlü ve güvenli."
    
    return score, level, feedback, recommendation

def generate_password(strength_level):
    """Seçilen güç seviyesine göre şifre oluşturur."""
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation
    
    if strength_level == "Zayıf":
        length = 8
        pool = lower + upper + digits
    elif strength_level == "Orta":
        length = 12
        pool = lower + upper + digits + symbols
    elif strength_level == "Güçlü":
        length = 16
        pool = lower + upper + digits + symbols
    else:  # Çok Güçlü
        length = 20
        pool = lower + upper + digits + symbols
    
    return ''.join(random.choice(pool) for _ in range(length))

# === Streamlit UI ===
st.set_page_config(page_title="🔐 Güçlü Şifre Aracı", page_icon="🔐", layout="centered")

# Matrix yeşili CSS - Siyah arka plan + Animasyonlar
st.markdown("""
<style>
    /* Siyah arka plan */
    .stApp {
        background: #000000;
        position: relative;
        overflow: hidden;
    }
    
    /* Matrix yağmuru animasyonu */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(transparent 0%, rgba(0, 255, 65, 0.05) 50%, transparent 100%),
            linear-gradient(90deg, transparent 0%, rgba(0, 255, 65, 0.05) 50%, transparent 100%);
        background-size: 50px 50px;
        animation: matrixRain 20s linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes matrixRain {
        0% {
            background-position: 0 0, 0 0;
        }
        100% {
            background-position: 50px 1000px, 1000px 50px;
        }
    }
    
    /* Tüm içerik üstte */
    .block-container {
        position: relative;
        z-index: 1;
    }
    
    /* Tüm metinler yeşil */
    .stApp, .stMarkdown, p, span, div, label {
        color: #00ff41 !important;
    }
    
    /* Başlıklar - Hareketli glow */
    h1, h2, h3, h4, h5, h6 {
        color: #00ff41 !important;
        text-shadow: 0 0 15px #00ff41, 0 0 25px #00ff41 !important;
        font-family: 'Courier New', monospace !important;
        animation: textGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes textGlow {
        0% {
            text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41;
        }
        100% {
            text-shadow: 0 0 20px #00ff41, 0 0 40px #00ff41, 0 0 60px #00ff41;
        }
    }
    
    /* Code blokları - Hareketli dijital görünüm */
    div[data-testid="stCodeBlock"] {
        background: rgba(0, 20, 0, 0.8) !important;
        border: 3px solid #00ff41 !important;
        border-radius: 15px !important;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.5), inset 0 0 20px rgba(0, 255, 65, 0.1) !important;
        padding: 20px !important;
        position: relative;
        overflow: hidden;
        animation: borderPulse 3s ease-in-out infinite;
    }
    
    @keyframes borderPulse {
        0%, 100% {
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.3), inset 0 0 10px rgba(0, 255, 65, 0.1);
        }
        50% {
            box-shadow: 0 0 50px rgba(0, 255, 65, 0.8), inset 0 0 30px rgba(0, 255, 65, 0.3);
        }
    }
    
    /* Code bloğunda tarama çizgisi */
    div[data-testid="stCodeBlock"]::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(0, 255, 65, 0.1) 45%,
            rgba(0, 255, 65, 0.3) 50%,
            rgba(0, 255, 65, 0.1) 55%,
            transparent 70%
        );
        animation: scanLine 4s linear infinite;
    }
    
    @keyframes scanLine {
        0% {
            transform: translate(-100%, -100%) rotate(45deg);
        }
        100% {
            transform: translate(100%, 100%) rotate(45deg);
        }
    }
    
    div[data-testid="stCodeBlock"] code {
        color: #00ff41 !important;
        background: transparent !important;
        padding: 20px !important;
        border-radius: 10px !important;
        font-family: 'Courier New', monospace !important;
        font-size: 24px !important;
        font-weight: bold !important;
        letter-spacing: 8px !important;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 30px #00ff41 !important;
        animation: textFlicker 0.5s infinite alternate;
        position: relative;
        z-index: 1;
    }
    
    @keyframes textFlicker {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.9;
        }
    }
    
    /* Progress bar - Hareketli */
    div[data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #00ff41, #00e676, #00ff41) !important;
        background-size: 200% 100% !important;
        box-shadow: 0 0 25px #00ff41 !important;
        animation: progressFlow 2s linear infinite;
    }
    
    @keyframes progressFlow {
        0% {
            background-position: 0% 50%;
        }
        100% {
            background-position: 200% 50%;
        }
    }
    
    div[data-testid="stProgressBar"] > div {
        background-color: rgba(0, 255, 65, 0.2) !important;
        border: 2px solid #00ff41 !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.3) !important;
    }
    
    div[data-testid="stProgressBar"] p {
        color: #00ff41 !important;
        font-weight: bold !important;
        text-shadow: 0 0 10px #00ff41 !important;
    }
    
    /* Metric kartları - Hareketli */
    div[data-testid="stMetric"] {
        background: rgba(0, 20, 0, 0.6) !important;
        border: 2px solid #00ff41 !important;
        border-radius: 15px !important;
        padding: 15px !important;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.4) !important;
        animation: metricGlow 3s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes metricGlow {
        0%, 100% {
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
        }
        50% {
            box-shadow: 0 0 35px rgba(0, 255, 65, 0.7);
        }
    }
    
    /* Metric'te tarama efekti */
    div[data-testid="stMetric"]::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -100%;
        width: 50%;
        height: 200%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 65, 0.3), transparent);
        animation: metricScan 3s linear infinite;
    }
    
    @keyframes metricScan {
        0% {
            left: -100%;
        }
        100% {
            left: 200%;
        }
    }
    
    div[data-testid="stMetric"] label {
        color: #00ff41 !important;
        font-weight: bold !important;
        font-family: 'Courier New', monospace !important;
        position: relative;
        z-index: 1;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #00ff41 !important;
        font-size: 28px !important;
        font-weight: bold !important;
        text-shadow: 0 0 10px #00ff41 !important;
        font-family: 'Courier New', monospace !important;
        position: relative;
        z-index: 1;
    }
    
    /* Mesaj kutuları */
    div[data-testid="stAlert"] {
        background: rgba(0, 20, 0, 0.6) !important;
        border: 2px solid #00ff41 !important;
        border-radius: 10px !important;
        font-family: 'Courier New', monospace !important;
        animation: alertPulse 2s ease-in-out infinite;
    }
    
    @keyframes alertPulse {
        0%, 100% {
            border-color: #00ff41;
        }
        50% {
            border-color: #00e676;
        }
    }
    
    /* Expander - Hareketli Matrix kutu */
    div[data-testid="stExpander"] {
        background: rgba(0, 20, 0, 0.6) !important;
        border: 3px solid #00ff41 !important;
        border-radius: 15px !important;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.4) !important;
        margin: 15px 0 !important;
        position: relative;
        overflow: hidden;
        animation: expanderGlow 4s ease-in-out infinite;
    }
    
    @keyframes expanderGlow {
        0%, 100% {
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        }
        50% {
            box-shadow: 0 0 50px rgba(0, 255, 65, 0.7);
        }
    }
    
    /* Expander'da dijital çizgiler */
    div[data-testid="stExpander"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff41, transparent);
        animation: lineFlow 3s linear infinite;
    }
    
    @keyframes lineFlow {
        0% {
            left: -100%;
        }
        100% {
            left: 200%;
        }
    }
    
    div[data-testid="stExpander"] summary {
        color: #00ff41 !important;
        font-weight: bold !important;
        font-size: 18px !important;
        text-shadow: 0 0 10px #00ff41 !important;
        font-family: 'Courier New', monospace !important;
        position: relative;
        z-index: 1;
    }
    
    /* Caption */
    .stCaption {
        color: #00ff41 !important;
        font-family: 'Courier New', monospace !important;
        opacity: 0.8 !important;
    }
    
    /* Butonlar - Hareketli */
    button[kind="primary"] {
        background: linear-gradient(135deg, #00ff41 0%, #00e676 50%, #00ff41 100%) !important;
        background-size: 200% 100% !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 0 25px rgba(0, 255, 65, 0.6) !important;
        font-family: 'Courier New', monospace !important;
        animation: buttonGlow 3s ease-in-out infinite, buttonSlide 2s linear infinite;
    }
    
    @keyframes buttonGlow {
        0%, 100% {
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
        }
        50% {
            box-shadow: 0 0 40px rgba(0, 255, 65, 0.9);
        }
    }
    
    @keyframes buttonSlide {
        0% {
            background-position: 0% 50%;
        }
        100% {
            background-position: 200% 50%;
        }
    }
    
    button[kind="primary"]:hover {
        box-shadow: 0 0 50px rgba(0, 255, 65, 1) !important;
        transform: scale(1.05) !important;
    }
    
    /* Input alanları */
    input {
        background-color: rgba(0, 20, 0, 0.6) !important;
        border: 2px solid #00ff41 !important;
        color: #00ff41 !important;
        border-radius: 10px !important;
        font-family: 'Courier New', monospace !important;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.3) !important;
    }
    
    input:focus {
        box-shadow: 0 0 25px rgba(0, 255, 65, 0.6) !important;
    }
    
    input::placeholder {
        color: rgba(0, 255, 65, 0.5) !important;
    }
    
    /* Select box */
    div[data-baseweb="select"] {
        background-color: rgba(0, 20, 0, 0.6) !important;
        border: 2px solid #00ff41 !important;
        border-radius: 10px !important;
    }
    
    /* Horizontal rule - Hareketli */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #00ff41, transparent) !important;
        box-shadow: 0 0 10px #00ff41 !important;
        animation: hrPulse 2s ease-in-out infinite;
    }
    
    @keyframes hrPulse {
        0%, 100% {
            opacity: 0.6;
        }
        50% {
            opacity: 1;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("🔐 Güçlü Şifre Aracı")
st.markdown("---")

# Session state başlangıç
if 'passwords' not in st.session_state:
    st.session_state.passwords = []

# Mod seçimi
mode = st.selectbox("Bir seçenek belirleyin:", ["Şifre Gücünü Kontrol Et", "Şifre Oluştur"])

# === ŞİFRE KONTROL MODU ===
if mode == "Şifre Gücünü Kontrol Et":
    st.subheader("🔍 Şifre Gücü Kontrolü")
    password = st.text_input("Şifrenizi girin:", type="password", placeholder="Şifrenizi buraya yazın...")
    
    if st.button("🔎 Analiz Et", use_container_width=True, type="primary"):
        if password:
            score, level, feedback, recommendation = analyze_password(password)
            percentage = (score / 8) * 100
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("## 🔐 ŞİFRE ANALİZ SONUCU")
            st.markdown("---")
            
            st.code("●" * len(password), language="text")
            st.progress(percentage / 100, text=f"Güç Skoru: {percentage:.0f}%")
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Seviye", level)
            with col2:
                st.metric("Skor", f"{score}/8")
            with col3:
                st.metric("Yüzde", f"{percentage:.0f}%")
            
            st.markdown("---")
            st.markdown("### 📋 Analiz Detayları")
            for item in feedback:
                if "✓" in item:
                    st.success(item)
                elif "✗" in item:
                    st.error(item)
                else:
                    st.warning(item)
            
            st.markdown("---")
            st.info(f"💡 **Öneri:** {recommendation}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"🕒 Kontrol Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            with col2:
                st.caption(f"📏 Uzunluk: {len(password)} karakter")
            
        else:
            st.warning("⚠️ Lütfen önce bir şifre girin.")

# === ŞİFRE OLUŞTURMA MODU ===
elif mode == "Şifre Oluştur":
    st.subheader("🎲 Otomatik Şifre Oluşturucu")
    
    strength = st.selectbox("Şifre gücünü seçin:", ["Zayıf", "Orta", "Güçlü", "Çok Güçlü"])
    amount = st.slider("Kaç adet şifre oluşturmak istiyorsunuz?", 1, 10, 3)
    
    if st.button("⚡ Oluştur", use_container_width=True, type="primary"):
        progress_bar = st.progress(0)
        
        for i in range(100):
            progress_bar.progress(i + 1, text=f"⚡ Şifreler oluşturuluyor... {i + 1}%")
            time.sleep(0.015)
        
        progress_bar.empty()
        
        st.session_state.passwords = []
        
        for i in range(amount):
            password = generate_password(strength)
            score, level, feedback, recommendation = analyze_password(password)
            creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.passwords.append({
                'password': password,
                'score': score,
                'level': level,
                'timestamp': creation_time
            })
        
        st.success("✅ Şifreler başarıyla oluşturuldu!")
    
    if st.session_state.passwords:
        st.markdown("---")
        st.markdown("### ✅ Oluşturulan Şifreler")
        
        for idx, pwd_data in enumerate(st.session_state.passwords, 1):
            password = pwd_data['password']
            score = pwd_data['score']
            level = pwd_data['level']
            timestamp = pwd_data['timestamp']
            percentage = (score / 8) * 100
            
            with st.expander(f"🔐 Şifre #{idx} - {level}", expanded=True):
                st.code(password, language="text")
                st.progress(percentage / 100, text=f"Güç: {percentage:.0f}%")
                st.markdown("<br>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Seviye", level)
                with col2:
                    st.metric("Skor", f"{score}/8")
                with col3:
                    st.metric("Uzunluk", f"{len(password)}")
                
                st.caption(f"🕒 Oluşturulma: {timestamp}")
