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

# Özel CSS - Dijital Matrix Efekti
st.markdown("""
<style>
    /* Ana Arka Plan */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    /* Dijital Konteyner */
    .digital-container {
        background: linear-gradient(135deg, rgba(10, 14, 39, 0.95) 0%, rgba(26, 31, 58, 0.95) 100%);
        border: 3px solid;
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 0 50px rgba(0, 255, 65, 0.5), inset 0 0 30px rgba(0, 255, 65, 0.1);
        animation: borderGlow 3s ease-in-out infinite alternate;
        position: relative;
        overflow: hidden;
    }
    
    .digital-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent 30%, rgba(0, 255, 65, 0.08) 50%, transparent 70%);
        animation: scanLine 4s linear infinite;
    }
    
    @keyframes scanLine {
        0% {
            transform: translateX(-100%) translateY(-100%) rotate(45deg);
        }
        100% {
            transform: translateX(100%) translateY(100%) rotate(45deg);
        }
    }
    
    @keyframes borderGlow {
        0%, 100% {
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.3), inset 0 0 20px rgba(0, 255, 65, 0.1);
        }
        50% {
            box-shadow: 0 0 60px rgba(0, 255, 65, 0.7), inset 0 0 40px rgba(0, 255, 65, 0.2);
        }
    }
    
    /* Dijital Başlık */
    .digital-header {
        font-family: 'Courier New', monospace;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        padding: 15px;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 10px;
        text-shadow: 0 0 20px currentColor, 0 0 40px currentColor;
        animation: textPulse 2s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }
    
    @keyframes textPulse {
        0%, 100% {
            transform: scale(1);
            opacity: 0.9;
        }
        50% {
            transform: scale(1.02);
            opacity: 1;
        }
    }
    
    /* Dijital Şifre Gösterimi */
    .digital-password {
        font-family: 'Courier New', monospace;
        font-size: 36px;
        font-weight: 900;
        text-align: center;
        letter-spacing: 10px;
        padding: 25px;
        margin: 20px 0;
        background: rgba(0, 0, 0, 0.6);
        border-radius: 15px;
        border: 2px solid currentColor;
        text-shadow: 0 0 15px currentColor, 0 0 30px currentColor, 0 0 45px currentColor;
        animation: flicker 0.4s infinite alternate;
        position: relative;
        z-index: 1;
    }
    
    @keyframes flicker {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.92;
        }
    }
    
    /* Skor Çubuğu */
    .score-container {
        position: relative;
        height: 40px;
        background: rgba(0, 0, 0, 0.6);
        border-radius: 20px;
        border: 2px solid rgba(0, 255, 65, 0.3);
        overflow: hidden;
        margin: 25px 0;
        z-index: 1;
    }
    
    .score-fill {
        height: 100%;
        border-radius: 18px;
        transition: width 2s ease;
        box-shadow: 0 0 30px currentColor, inset 0 0 20px rgba(255, 255, 255, 0.3);
        animation: scorePulse 2s ease-in-out infinite;
        position: relative;
    }
    
    .score-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        animation: scoreShine 3s linear infinite;
    }
    
    @keyframes scorePulse {
        0%, 100% {
            opacity: 0.9;
        }
        50% {
            opacity: 1;
        }
    }
    
    @keyframes scoreShine {
        0% {
            left: -100%;
        }
        100% {
            left: 200%;
        }
    }
    
    /* Sonuç Kartı */
    .result-card {
        background: rgba(0, 0, 0, 0.5);
        border: 2px solid currentColor;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.3), inset 0 0 20px rgba(0, 0, 0, 0.5);
        position: relative;
        z-index: 1;
    }
    
    .result-level {
        font-family: 'Courier New', monospace;
        font-size: 42px;
        font-weight: bold;
        margin: 15px 0;
        text-shadow: 0 0 20px currentColor, 0 0 40px currentColor;
        animation: levelPulse 1.5s ease-in-out infinite;
    }
    
    @keyframes levelPulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    /* Geri Bildirim Kutusu */
    .feedback-box {
        background: rgba(0, 0, 0, 0.5);
        border-left: 4px solid currentColor;
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        font-family: 'Courier New', monospace;
        position: relative;
        z-index: 1;
    }
    
    .feedback-item {
        padding: 8px 0;
        font-size: 15px;
        letter-spacing: 1px;
    }
    
    /* Öneri Kutusu */
    .recommendation-box {
        background: rgba(0, 0, 0, 0.6);
        border: 2px dashed currentColor;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        font-style: italic;
        animation: recommendBlink 3s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }
    
    @keyframes recommendBlink {
        0%, 100% {
            opacity: 0.9;
        }
        50% {
            opacity: 1;
        }
    }
    
    /* Bilgi Satırı */
    .info-row {
        display: flex;
        justify-content: space-between;
        margin: 15px 0;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        opacity: 0.8;
        position: relative;
        z-index: 1;
    }
    
    /* Ayırıcı Çizgi */
    .digital-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, currentColor, transparent);
        margin: 20px 0;
        border-radius: 2px;
        box-shadow: 0 0 10px currentColor;
        animation: dividerFlow 3s linear infinite;
        position: relative;
        z-index: 1;
    }
    
    @keyframes dividerFlow {
        0% {
            opacity: 0.5;
        }
        50% {
            opacity: 1;
        }
        100% {
            opacity: 0.5;
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
    
    if st.button("🔎 Analiz Et", use_container_width=True):
        if password:
            score, level, color, feedback, recommendation = analyze_password(password)
            percentage = (score / 8) * 100
            
            # Dijital Sonuç Gösterimi
            st.markdown(f"""
            <div class="digital-container" style="border-color: {color};">
                <div class="digital-header" style="color: {color};">
                    🔐 ŞİFRE ANALİZ SONUCU
                </div>
                
                <div class="digital-password" style="color: {color};">
                    {'●' * len(password)}
                </div>
                
                <div class="score-container">
                    <div class="score-fill" style="width: {percentage}%; background: {color};"></div>
                </div>
                
                <div style="text-align: center; font-family: 'Courier New', monospace; color: {color}; font-size: 16px; margin: 10px 0; position: relative; z-index: 1;">
                    📊 GÜÇ SKORU: {score}/8 ({percentage:.0f}%)
                </div>
                
                <div class="digital-divider" style="background: linear-gradient(90deg, transparent, {color}, transparent);"></div>
                
                <div class="result-card" style="border-color: {color}; color: {color};">
                    <div class="result-level" style="color: {color};">
                        {level}
                    </div>
                </div>
                
                <div class="feedback-box" style="border-color: {color}; color: {color};">
                    <div style="font-weight: bold; font-size: 16px; margin-bottom: 12px;">📋 ANALİZ DETAYLARI</div>
                    {''.join([f'<div class="feedback-item">{item}</div>' for item in feedback])}
                </div>
                
                <div class="recommendation-box" style="border-color: {color}; color: {color};">
                    💡 {recommendation}
                </div>
                
                <div class="digital-divider" style="background: linear-gradient(90deg, transparent, {color}, transparent);"></div>
                
                <div class="info-row" style="color: {color};">
                    <span>🕒 Kontrol: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>
                    <span>📏 Uzunluk: {len(password)} karakter</span>
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
        # Animasyon
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f"⚡ Şifreler oluşturuluyor... {i + 1}%")
            time.sleep(0.015)
        
        progress_bar.empty()
        status_text.empty()
        
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
        
        st.success("✅ Şifreler başarıyla oluşturuldu!")
    
    # Oluşturulan şifreleri göster
    if st.session_state.passwords:
        st.markdown("---")
        st.markdown("### ✅ Oluşturulan Şifreler:")
        
        for idx, pwd_data in enumerate(st.session_state.passwords, 1):
            password = pwd_data['password']
            score = pwd_data['score']
            level = pwd_data['level']
            color = pwd_data['color']
            timestamp = pwd_data['timestamp']
            percentage = (score / 8) * 100
            
            st.markdown(f"""
            <div class="digital-container" style="border-color: {color};">
                <div class="digital-header" style="color: {color};">
                    🔐 ŞİFRE #{idx}
                </div>
                
                <div class="digital-password" style="color: {color}; font-size: 28px;">
                    {password}
                </div>
                
                <div class="score-container">
                    <div class="score-fill" style="width: {percentage}%; background: {color};"></div>
                </div>
                
                <div class="digital-divider" style="background: linear-gradient(90deg, transparent, {color}, transparent);"></div>
                
                <div class="info-row" style="color: {color};">
                    <span>💪 {level}</span>
                    <span>📊 {score}/8 ({percentage:.0f}%)</span>
                </div>
                
                <div class="info-row" style="color: {color};">
                    <span>🕒 {timestamp}</span>
                    <span>📏 {len(password)} karakter</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
