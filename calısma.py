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

# Basit siyah arka plan + yeşil dijital tema (animasyon yok)
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
    
    /* Code blokları - Dijital görünüm */
    div[data-testid="stCodeBlock"] {
        background: rgba(0, 20, 0, 0.6) !important;
        border: 2px solid #00ff41 !important;
        border-radius: 10px !important;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.3) !important;
        padding: 20px !important;
    }
    
    div[data-testid="stCodeBlock"] code {
        color: #00ff41 !important;
        background: transparent !important;
        padding: 15px !important;
        font-family: 'Courier New', monospace !important;
        font-size: 22px !important;
        font-weight: bold !important;
        letter-spacing: 6px !important;
        text-shadow: 0 0 8px #00ff41 !important;
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
    
    /* Metric kartları */
    div[data-testid="stMetric"] {
        background: rgba(0, 20, 0, 0.6) !important;
        border: 2px solid #00ff41 !important;
        border-radius: 10px !important;
        padding: 15px !important;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.3) !important;
    }
    
    div[data-testid="stMetric"] label {
        color: #00ff41 !important;
        font-weight: bold !important;
        font-family: 'Courier New', monospace !important;
    }
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #00ff41 !important;
        font-size: 26px !important;
        font-weight: bold !important;
        text-shadow: 0 0 8px #00ff41 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Mesaj kutuları */
    div[data-testid="stAlert"] {
        background: rgba(0, 20, 0, 0.6) !important;
        border: 2px solid #00ff41 !important;
        border-radius: 10px !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Expander kutuları */
    div[data-testid="stExpander"] {
        background: rgba(0, 20, 0, 0.6) !important;
        border: 2px solid #00ff41 !important;
        border-radius: 10px !important;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.3) !important;
        margin: 15px 0 !important;
    }
    
    div[data-testid="stExpander"] summary {
        color: #00ff41 !important;
        font-weight: bold !important;
        font-size: 18px !important;
        text-shadow: 0 0 8px #00ff41 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Caption */
    .stCaption {
        color: #00ff41 !important;
        font-family: 'Courier New', monospace !important;
        opacity: 0.8 !important;
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
    
    /* SADECE ANİMASYON SIRASINDA KULLANILAN SINIF */
    .generating-animation {
        animation: digitalFlicker 0.1s infinite, borderPulse 0.5s ease-in-out infinite !important;
    }
    
    @keyframes digitalFlicker {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.85;
        }
    }
    
    @keyframes borderPulse {
        0%, 100% {
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
        }
        50% {
            box-shadow: 0 0 40px rgba(0, 255, 65, 1);
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
        
        # Animasyon için placeholder'lar oluştur
        animation_placeholders = []
        for i in range(amount):
            animation_placeholders.append(st.empty())
        
        # Animasyonlu şifre oluşturma gösterimi
        for frame in range(20):  # 20 kare animasyon
            for placeholder in animation_placeholders:
                # Her karede rastgele şifre göster (hızlı değişim)
                fake_password = generate_password(strength)
                placeholder.markdown(f"""
                <div style='background: rgba(0, 20, 0, 0.8); 
                            border: 3px solid #00ff41; 
                            border-radius: 10px; 
                            padding: 20px; 
                            margin: 10px 0;
                            box-shadow: 0 0 30px rgba(0, 255, 65, 0.6);
                            animation: digitalFlicker 0.1s infinite, borderPulse 0.3s ease-in-out infinite;'>
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
            time.sleep(0.08)  # Hızlı değişim
        
        # Animasyonu temizle
        progress_bar.empty()
        for placeholder in animation_placeholders:
            placeholder.empty()
        
        # Gerçek şifreleri oluştur ve kaydet
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
    
    # Oluşturulan şifreleri göster (statik, animasyon yok)
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
