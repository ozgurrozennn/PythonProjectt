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
    
    # Uzunluk skoru
    if length >= 16:
        score += 3
    elif length >= 12:
        score += 2
    elif length >= 8:
        score += 1
    
    # Karakter türü kontrolleri
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 2
    
    # Güç seviyesini belirle
    if score <= 3:
        level = "🔴 Zayıf"
    elif score <= 5:
        level = "🟡 Orta"
    elif score <= 7:
        level = "🟢 Güçlü"
    else:
        level = "🟢 Çok Güçlü"
    
    return score, level

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

# Özel CSS - Matrix/Dijital Şelale efekti
st.markdown("""
<style>
    .password-container {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        border: 2px solid #00ff41;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        }
        to {
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.6);
        }
    }
    
    .password-text {
        font-family: 'Courier New', monospace;
        font-size: 20px;
        font-weight: bold;
        color: #00ff41;
        text-shadow: 0 0 10px #00ff41;
        letter-spacing: 3px;
        word-break: break-all;
        animation: flicker 0.5s infinite alternate;
    }
    
    @keyframes flicker {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.8;
        }
    }
    
    .timestamp {
        font-family: 'Courier New', monospace;
        font-size: 14px;
        color: #00ff41;
        opacity: 0.7;
        margin-top: 5px;
    }
    
    .strength-info {
        font-family: 'Courier New', monospace;
        font-size: 14px;
        color: #00ff41;
        margin-top: 10px;
    }
    
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff41, transparent);
        margin: 10px 0;
        animation: slide 2s linear infinite;
    }
    
    @keyframes slide {
        0% {
            background-position: -100% 0;
        }
        100% {
            background-position: 100% 0;
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
    
    if st.button("Kontrol Et"):
        if password:
            score, level = analyze_password(password)
            st.success(f"**Sonuç:** {level}  |  **Skor:** {score}/8")
        else:
            st.warning("⚠️ Lütfen önce bir şifre girin.")

# === ŞİFRE OLUŞTURMA MODU ===
elif mode == "Şifre Oluştur":
    st.subheader("🎲 Otomatik Şifre Oluşturucu")
    
    strength = st.selectbox("Şifre gücünü seçin:", ["Zayıf", "Orta", "Güçlü", "Çok Güçlü"])
    amount = st.slider("Kaç adet şifre oluşturmak istiyorsunuz?", 1, 10, 3)
    
    if st.button("Oluştur"):
        progress = st.progress(0)
        placeholders = [st.empty() for _ in range(amount)]
        
        # Animasyonlu sahte şifreler
        for i in range(10):
            for p in placeholders:
                fake = generate_password(strength)
                p.markdown(f"""
                <div class="password-container">
                    <div class="password-text">{fake}</div>
                </div>
                """, unsafe_allow_html=True)
            progress.progress((i + 1) * 10)
            time.sleep(0.1)
        
        progress.empty()
        for p in placeholders:
            p.empty()
        
        # Yeni şifreler oluştur ve kaydet
        st.session_state.passwords = []
        
        for i in range(amount):
            password = generate_password(strength)
            score, level = analyze_password(password)
            creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.passwords.append({
                'password': password,
                'score': score,
                'level': level,
                'timestamp': creation_time
            })
    
    # Oluşturulan şifreleri göster
    if st.session_state.passwords:
        st.markdown("### ✅ Oluşturulan Şifreler:")
        
        for idx, pwd_data in enumerate(st.session_state.passwords, 1):
            password = pwd_data['password']
            score = pwd_data['score']
            level = pwd_data['level']
            timestamp = pwd_data['timestamp']
            
            st.markdown(f"""
            <div class="password-container">
                <div style="color: #00ff41; font-size: 16px; margin-bottom: 10px;">
                    🔐 Şifre #{idx}
                </div>
                <div class="password-text">{password}</div>
                <div class="divider"></div>
                <div class="timestamp">
                    🕒 Oluşturulma Zamanı: {timestamp}
                </div>
                <div class="strength-info">
                    💪 Güç: {level}  |  📊 Skor: {score}/8
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
