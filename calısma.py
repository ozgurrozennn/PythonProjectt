import streamlit as st
import random
import string
import time

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
st.title("🔐 Güçlü Şifre Aracı")
st.markdown("---")

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
                p.code("*" * len(fake), language="text")
            progress.progress((i + 1) * 10)
            time.sleep(0.1)
        
        progress.empty()
        for p in placeholders:
            p.empty()
        
        st.markdown("### ✅ Oluşturulan Şifreler:")
        
        # Session state'de şifreleri sakla
        if 'passwords' not in st.session_state:
            st.session_state.passwords = []
        
        st.session_state.passwords = []
        for i in range(amount):
            password = generate_password(strength)
            score, level = analyze_password(password)
            st.session_state.passwords.append({
                'password': password,
                'score': score,
                'level': level,
                'index': i
            })
        
        # Her şifre için ayrı göster/gizle ve kopyala butonu
        for pwd_data in st.session_state.passwords:
            i = pwd_data['index']
            password = pwd_data['password']
            score = pwd_data['score']
            level = pwd_data['level']
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                # Şifre gösterme durumunu kontrol et
                show_key = f'show_pwd_{i}'
                if show_key not in st.session_state:
                    st.session_state[show_key] = False
                
                if st.session_state[show_key]:
                    st.code(password, language="text")
                else:
                    st.code("*" * len(password), language="text")
            
            with col2:
                if st.button("👁️ Göster" if not st.session_state[show_key] else "🙈 Gizle", key=f'btn_{i}'):
                    st.session_state[show_key] = not st.session_state[show_key]
                    st.rerun()
            
            with col3:
                # Kopyalama için metin göster
                if st.session_state[show_key]:
                    st.button("📋 Kopyala", key=f'copy_{i}', help="Şifreyi manuel olarak kopyalayın")
            
            st.write(f"**Güç:** {level}  |  **Skor:** {score}/8")
            st.markdown("---")
