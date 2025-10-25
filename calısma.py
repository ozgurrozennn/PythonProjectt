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

# Basit arka plan CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    /* Metinleri yeşil yap */
    .stMarkdown, .stText {
        color: #00ff41 !important;
    }
    
    /* Code blokları için */
    code {
        color: #00ff41 !important;
        background-color: rgba(0, 0, 0, 0.5) !important;
        padding: 10px !important;
        border-radius: 5px !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 3px !important;
        font-size: 18px !important;
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
            score, level, feedback, recommendation = analyze_password(password)
            percentage = (score / 8) * 100
            
            # Boşluk
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Başlık
            st.markdown("## 🔐 ŞİFRE ANALİZ SONUCU")
            st.markdown("---")
            
            # Şifre maskesi (code bloğu olarak)
            st.code("●" * len(password), language="text")
            
            # Progress bar
            st.progress(percentage / 100)
            
            # Sonuç metrikleri
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Seviye", level)
            with col2:
                st.metric("Skor", f"{score}/8")
            with col3:
                st.metric("Yüzde", f"{percentage:.0f}%")
            
            st.markdown("---")
            
            # Analiz detayları
            st.markdown("### 📋 Analiz Detayları")
            for item in feedback:
                if "✓" in item:
                    st.success(item)
                elif "✗" in item:
                    st.error(item)
                else:
                    st.warning(item)
            
            st.markdown("---")
            
            # Öneri
            st.info(f"💡 **Öneri:** {recommendation}")
            
            # Bilgiler
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
            score, level, feedback, recommendation = analyze_password(password)
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
            percentage = (score / 8) * 100
            
            with st.expander(f"🔐 Şifre #{idx} - {level}", expanded=True):
                # Şifre gösterimi
                st.code(password, language="text")
                
                # Progress bar
                st.progress(percentage / 100)
                
                # Bilgiler
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Seviye", level)
                with col2:
                    st.metric("Skor", f"{score}/8")
                with col3:
                    st.metric("Uzunluk", f"{len(password)}")
                
                st.caption(f"🕒 Oluşturulma: {timestamp}")
