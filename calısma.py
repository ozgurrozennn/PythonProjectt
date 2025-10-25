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
        color = "#ff4444"
        recommendation = "Bu şifre çok zayıf! Daha uzun ve karmaşık bir şifre kullanın."
    elif score <= 5:
        level = "🟡 Orta"
        color = "#ffaa00"
        recommendation = "Bu şifre orta seviyede. Özel karakterler ekleyerek güçlendirebilirsiniz."
    elif score <= 7:
        level = "🟢 Güçlü"
        color = "#00ff41"
        recommendation = "Bu şifre güçlü! Güvenle kullanabilirsiniz."
    else:
        level = "🟢 Çok Güçlü"
        color = "#00ff41"
        recommendation = "Mükemmel! Bu şifre çok güçlü ve güvenli."
    
    return score, level, color, feedback, recommendation

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
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .password-container {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        border: 2px solid #00ff41;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.4);
        animation: glow 2s ease-in-out infinite alternate;
        position: relative;
        overflow: hidden;
    }
    
    .password-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 255, 65, 0.1), transparent);
        animation: scan 3s linear infinite;
    }
    
    @keyframes scan {
        0% {
            transform: translateX(-100%) translateY(-100%) rotate(45deg);
        }
        100% {
            transform: translateX(100%) translateY(100%) rotate(45deg);
        }
    }
    
    .check-container {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.4);
        animation: glow 2s ease-in-out infinite alternate;
        position: relative;
        overflow: hidden;
    }
    
    .check-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0, 255, 65, 0.05), transparent);
        animation: scan 4s linear infinite;
    }
    
    @keyframes glow {
        from {
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        }
        to {
            box-shadow: 0 0 40px rgba(0, 255, 65, 0.6);
        }
    }
    
    .password-text {
        font-family: 'Courier New', monospace;
        font-size: 22px;
        font-weight: bold;
        color: #00ff41;
        text-shadow: 0 0 15px #00ff41;
        letter-spacing: 4px;
        word-break: break-all;
        animation: flicker 0.5s infinite alternate;
        position: relative;
        z-index: 1;
    }
    
    .check-password-text {
        font-family: 'Orbitron', monospace;
        font-size: 32px;
        font-weight: 900;
        text-shadow: 0 0 20px currentColor, 0 0 40px currentColor;
        letter-spacing: 8px;
        word-break: break-all;
        animation: flicker 0.3s infinite alternate, pulse-text 2s ease-in-out infinite;
        text-align: center;
        margin: 25px 0;
        position: relative;
        z-index: 1;
    }
    
    @keyframes pulse-text {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes flicker {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.85;
        }
    }
    
    .strength-info {
        font-family: 'Courier New', monospace;
        font-size: 14px;
        color: #00ff41;
        margin-top: 10px;
        position: relative;
        z-index: 1;
    }
    
    .check-result {
        font-family: 'Orbitron', monospace;
        font-size: 18px;
        text-align: center;
        margin: 20px 0;
        padding: 20px;
        border-radius: 10px;
        background: rgba(0, 255, 65, 0.1);
        border: 1px solid currentColor;
        position: relative;
        z-index: 1;
    }
    
    .feedback-list {
        font-family: 'Courier New', monospace;
        font-size: 14px;
        text-align: left;
        margin: 15px 0;
        padding: 15px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 8px;
        border-left: 3px solid currentColor;
        position: relative;
        z-index: 1;
    }
    
    .recommendation {
        font-family: 'Courier New', monospace;
        font-size: 13px;
        text-align: center;
        margin: 15px 0;
        padding: 12px;
        background: rgba(0, 0, 0, 0.4);
        border-radius: 8px;
        font-style: italic;
        position: relative;
        z-index: 1;
    }
    
    .divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #00ff41, transparent);
        margin: 15px 0;
        animation: slide 2s linear infinite;
        position: relative;
        z-index: 1;
    }
    
    @keyframes slide {
        0% {
            background-position: -200% 0;
        }
        100% {
            background-position: 200% 0;
        }
    }
    
    .score-bar {
        height: 35px;
        border-radius: 20px;
        background: linear-gradient(90deg, #1a1f3a 0%, #2a3f5a 100%);
        position: relative;
        overflow: hidden;
        margin: 25px 0;
        border: 2px solid rgba(0, 255, 65, 0.3);
        z-index: 1;
    }
    
    .score-indicator {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        background: linear-gradient(90deg, #ff4444, #ffaa00, #00ff41);
        transition: width 1.5s ease;
        animation: pulse-bar 2s infinite;
        box-shadow: 0 0 20px currentColor;
    }
    
    @keyframes pulse-bar {
        0%, 100% {
            opacity: 0.8;
        }
        50% {
            opacity: 1;
        }
    }
    
    .header-text {
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        text-align: center;
        font-size: 20px;
        margin-bottom: 15px;
        text-shadow: 0 0 10px currentColor;
        position: relative;
        z-index: 1;
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
    
    if st.button("🔎 Analiz Et", use_container_width=True):
        if password:
            score, level, color, feedback, recommendation = analyze_password(password)
            percentage = (score / 8) * 100
            
            # Dijital şelale efektiyle sonuç gösterimi
            st.markdown(f"""
            <div class="check-container" style="border: 3px solid {color};">
                <div class="header-text" style="color: {color};">
                    🔐 ŞİFRE ANALİZ SONUCU
                </div>
                <div class="divider" style="background: linear-gradient(90deg, transparent, {color}, transparent);"></div>
                
                <div class="check-password-text" style="color: {color};">
                    {'●' * len(password)}
                </div>
                
                <div class="score-bar">
                    <div class="score-indicator" style="width: {percentage}%; background: {color};"></div>
                </div>
                
                <div class="check-result" style="color: {color}; background: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.15); border-color: {color};">
                    <div style="font-size: 28px; margin: 10px 0; font-weight: bold;">
                        {level}
                    </div>
                    <div style="font-size: 18px; opacity: 0.9;">
                        📊 Skor: {score}/8 ({percentage:.0f}%)
                    </div>
                </div>
                
                <div class="feedback-list" style="color: {color}; border-color: {color};">
                    <div style="font-weight: bold; margin-bottom: 8px;">📋 Analiz Detayları:</div>
                    {'<br>'.join(feedback)}
                </div>
                
                <div class="recommendation" style="color: {color};">
                    💡 {recommendation}
                </div>
                
                <div class="divider" style="background: linear-gradient(90deg, transparent, {color}, transparent);"></div>
                
                <div style="color: {color}; font-family: 'Courier New', monospace; font-size: 14px; text-align: center; margin-top: 15px; position: relative; z-index: 1;">
                    🕒 Kontrol Zamanı: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                </div>
                
                <div style="color: {color}; font-family: 'Courier New', monospace; font-size: 13px; text-align: center; margin-top: 10px; opacity: 0.7; position: relative; z-index: 1;">
                    📏 Uzunluk: {len(password)} karakter
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.warning("⚠️ Lütfen önce bir şifre girin.")

# === ŞİFRE OLUŞTURMA MODU ===
elif mode == "Şifre Oluştur":
    st.subheader("🎲 Otomatik Şifre Oluşturucu")
    
    strength = st.selectbox("Şifre gücünü seçin:", ["Zayıf", "Orta", "Güçlü", "Çok Güçlü"])
    amount = st.slider("Kaç adet şifre oluşturmak istiyorsunuz?", 1, 10, 3)
    
    if st.button("⚡ Oluştur", use_container_width=True):
        progress = st.progress(0)
        placeholders = [st.empty() for _ in range(amount)]
        
        # Animasyonlu sahte şifreler
        for i in range(12):
            for p in placeholders:
                fake = generate_password(strength)
                p.markdown(f"""
                <div class="password-container">
                    <div class="password-text">{fake}</div>
                </div>
                """, unsafe_allow_html=True)
            progress.progress((i + 1) * 8)
            time.sleep(0.08)
        
        progress.empty()
        for p in placeholders:
            p.empty()
        
        # Yeni şifreler oluştur ve kaydet
        st.session_state.passwords = []
        
        for i in range(amount):
            password = generate_password(strength)
            score, level, color, feedback, recommendation = analyze_password(password)
            creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.passwords.append({
                'password': password,
                'score': score,
                'level': level,
                'color': color,
                'timestamp': creation_time
            })
    
    # Oluşturulan şifreleri göster
    if st.session_state.passwords:
        st.markdown("### ✅ Oluşturulan Şifreler:")
        
        for idx, pwd_data in enumerate(st.session_state.passwords, 1):
            password = pwd_data['password']
            score = pwd_data['score']
            level = pwd_data['level']
            color = pwd_data['color']
            timestamp = pwd_data['timestamp']
            percentage = (score / 8) * 100
            
            st.markdown(f"""
            <div class="password-container" style="border-color: {color};">
                <div class="header-text" style="color: {color};">
                    🔐 Şifre #{idx}
                </div>
                <div class="password-text" style="color: {color}; text-shadow: 0 0 15px {color};">{password}</div>
                
                <div class="score-bar" style="margin-top: 15px;">
                    <div class="score-indicator" style="width: {percentage}%; background: {color};"></div>
                </div>
                
                <div class="divider" style="background: linear-gradient(90deg, transparent, {color}, transparent);"></div>
                <div style="color: {color}; font-family: 'Courier New', monospace; font-size: 14px; opacity: 0.8; position: relative; z-index: 1;">
                    🕒 Oluşturulma: {timestamp}
                </div>
                <div class="strength-info" style="color: {color};">
                    💪 Güç: {level}  |  📊 Skor: {score}/8 ({percentage:.0f}%)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
