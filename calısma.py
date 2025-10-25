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
        level = "Zayıf"
    elif score <= 5:
        level = "Orta"
    elif score <= 7:
        level = "Güçlü"
    else:
        level = "Çok Güçlü"
    
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

# Siyah arka plan + yeşil dijital tema
st.markdown("""
<style>
    /* Siyah arka plan */
    .stApp {
        background: #000000;
    }
    
    /* Tüm metinler yeşil */
    .stApp, .stMarkdown, p, span, div, label {
        color: #00ff41 !important;
    }
    
    /* Başlıklar */
    h1, h2, h3, h4, h5, h6 {
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Progress bar */
    div[data-testid="stProgressBar"] > div > div {
        background: #00ff41 !important;
        box-shadow: 0 0 15px #00ff41 !important;
    }
    
    div[data-testid="stProgressBar"] > div {
        background-color: rgba(0, 255, 65, 0.2) !important;
        border: 2px solid #00ff41 !important;
        border-radius: 10px !important;
    }
    
    div[data-testid="stProgressBar"] p {
        color: #00ff41 !important;
        font-weight: bold !important;
    }
    
    /* Mesaj kutuları */
    div[data-testid="stAlert"] {
        background: rgba(0, 20, 0, 0.6) !important;
        border: 2px solid #00ff41 !important;
        border-radius: 10px !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Butonlar */
    button[kind="primary"] {
        background: linear-gradient(135deg, #00ff41 0%, #00e676 100%) !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.5) !important;
        font-family: 'Courier New', monospace !important;
    }
    
    button[kind="primary"]:hover {
        box-shadow: 0 0 30px rgba(0, 255, 65, 0.8) !important;
        transform: scale(1.02) !important;
    }
    
    /* Input alanları */
    input {
        background-color: rgba(0, 20, 0, 0.6) !important;
        border: 2px solid #00ff41 !important;
        color: #00ff41 !important;
        border-radius: 10px !important;
        font-family: 'Courier New', monospace !important;
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
    
    /* Horizontal rule */
    hr {
        border-color: #00ff41 !important;
        box-shadow: 0 0 10px #00ff41 !important;
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
    
    if st.button("🔎 Kontrol Et", use_container_width=True, type="primary"):
        if password:
            score, level = analyze_password(password)
            
            # Container kullanarak HTML render et
            with st.container():
                st.markdown(f"""
                <div style='background: #000000; 
                            border: 3px solid #00ff41; 
                            border-radius: 15px; 
                            padding: 30px; 
                            margin: 20px 0;
                            box-shadow: 0 0 30px rgba(0, 255, 65, 0.5);'>
                    
                    <div style='background: rgba(0, 20, 0, 0.8); 
                                border: 2px solid #00ff41; 
                                border-radius: 10px; 
                                padding: 25px; 
                                margin: 15px 0;
                                box-shadow: inset 0 0 20px rgba(0, 255, 65, 0.2);'>
                        <p style='color: #00ff41; 
                                  font-family: Courier New, monospace; 
                                  font-size: 32px; 
                                  font-weight: bold; 
                                  letter-spacing: 8px; 
                                  text-align: center;
                                  text-shadow: 0 0 15px #00ff41, 0 0 25px #00ff41;
                                  margin: 0;'>
                            {password}
                        </p>
                    </div>
                    
                    <div style='text-align: center; margin-top: 25px;'>
                        <div style='color: #00ff41; 
                                    font-family: Courier New, monospace; 
                                    font-size: 28px; 
                                    font-weight: bold;
                                    text-shadow: 0 0 15px #00ff41;'>
                            Seviye: {level}
                        </div>
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
    
    if st.button("⚡ Oluştur", use_container_width=True, type="primary"):
        progress_bar = st.progress(0)
        
        # Animasyon için placeholder'lar oluştur
        animation_placeholders = []
        for i in range(amount):
            animation_placeholders.append(st.empty())
        
        # Animasyonlu şifre oluşturma gösterimi
        for frame in range(20):
            for placeholder in animation_placeholders:
                fake_password = generate_password(strength)
                placeholder.markdown(f"""
                <div style='background: rgba(0, 20, 0, 0.8); 
                            border: 3px solid #00ff41; 
                            border-radius: 10px; 
                            padding: 20px; 
                            margin: 10px 0;
                            box-shadow: 0 0 30px rgba(0, 255, 65, 0.6);'>
                    <p style='color: #00ff41; 
                              font-family: Courier New, monospace; 
                              font-size: 22px; 
                              font-weight: bold; 
                              letter-spacing: 6px; 
                              text-align: center;
                              text-shadow: 0 0 15px #00ff41;
                              margin: 0;'>
                        {fake_password}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            progress_bar.progress((frame + 1) * 5, text=f"⚡ Şifreler oluşturuluyor... {(frame + 1) * 5}%")
            time.sleep(0.08)
        
        # Animasyonu temizle
        progress_bar.empty()
        for placeholder in animation_placeholders:
            placeholder.empty()
        
        # Gerçek şifreleri oluştur ve kaydet
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
        
        st.success("✅ Şifreler başarıyla oluşturuldu!")
    
    # Oluşturulan şifreleri göster
    if st.session_state.passwords:
        st.markdown("---")
        st.markdown("### ✅ Oluşturulan Şifreler")
        
        for idx, pwd_data in enumerate(st.session_state.passwords, 1):
            password = pwd_data['password']
            score = pwd_data['score']
            level = pwd_data['level']
            timestamp = pwd_data['timestamp']
            
            # Her şifre için container kullan
            with st.container():
                st.markdown(f"""
                <div style='background: #000000; 
                            border: 3px solid #00ff41; 
                            border-radius: 15px; 
                            padding: 25px; 
                            margin: 20px 0;
                            box-shadow: 0 0 30px rgba(0, 255, 65, 0.5);'>
                    
                    <div style='text-align: center; margin-bottom: 20px;'>
                        <span style='color: #00ff41; 
                                     font-family: Courier New, monospace; 
                                     font-size: 22px; 
                                     font-weight: bold;
                                     text-shadow: 0 0 10px #00ff41;'>
                            🔐 Şifre #{idx}
                        </span>
                    </div>
                    
                    <div style='background: rgba(0, 20, 0, 0.8); 
                                border: 2px solid #00ff41; 
                                border-radius: 10px; 
                                padding: 20px; 
                                margin: 15px 0;
                                box-shadow: inset 0 0 20px rgba(0, 255, 65, 0.2);'>
                        <p style='color: #00ff41; 
                                  font-family: Courier New, monospace; 
                                  font-size: 28px; 
                                  font-weight: bold; 
                                  letter-spacing: 8px; 
                                  text-align: center;
                                  text-shadow: 0 0 15px #00ff41, 0 0 25px #00ff41;
                                  margin: 0;'>
                            {password}
                        </p>
                    </div>
                    
                    <div style='display: flex; justify-content: space-around; margin: 20px 0;'>
                        <div style='text-align: center;'>
                            <div style='color: #00ff41; font-family: Courier New; font-size: 14px; opacity: 0.8;'>Seviye</div>
                            <div style='color: #00ff41; font-family: Courier New; font-size: 24px; font-weight: bold; text-shadow: 0 0 10px #00ff41;'>{level}</div>
                        </div>
                        <div style='text-align: center;'>
                            <div style='color: #00ff41; font-family: Courier New; font-size: 14px; opacity: 0.8;'>Uzunluk</div>
                            <div style='color: #00ff41; font-family: Courier New; font-size: 24px; font-weight: bold; text-shadow: 0 0 10px #00ff41;'>{len(password)}</div>
                        </div>
                    </div>
                    
                    <div style='text-align: center; margin-top: 15px;'>
                        <span style='color: #00ff41; 
                                     font-family: Courier New, monospace; 
                                     font-size: 13px; 
                                     opacity: 0.8;'>
                            🕒 {timestamp}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
