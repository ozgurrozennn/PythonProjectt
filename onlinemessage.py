"""
STREAMLIT İSTEMCİ - P2P Mesajlaşma
Tarayıcıda çalışır, Terminal sunucuya mesaj gönderir
"""

import streamlit as st
import socket
import time

# Sayfa ayarları
st.set_page_config(
    page_title="P2P Chat",
    page_icon="💬",
    layout="centered"
)

# CSS Stilleri
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .chat-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        margin: 20px 0;
    }
    .sent-msg {
        background-color: #DCF8C6;
        padding: 10px 15px;
        border-radius: 15px 15px 5px 15px;
        margin: 10px 0;
        text-align: right;
    }
    .received-msg {
        background-color: #E8E8E8;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Başlık
st.title("💬 P2P Mesajlaşma")
st.caption("Terminal ↔️ Streamlit")

# Session State Başlat
if 'bagli' not in st.session_state:
    st.session_state.bagli = False
if 'socket' not in st.session_state:
    st.session_state.socket = None
if 'mesajlar' not in st.session_state:
    st.session_state.mesajlar = []

# BÖLÜM 1: BAĞLANTI
st.header("1️⃣ Bağlantı Kur")

if not st.session_state.bagli:
    col1, col2 = st.columns([3, 1])

    with col1:
        ip_adresi = st.text_input(
            "IP Adresi",
            value="localhost",
            placeholder="localhost veya 127.0.0.1"
        )

    with col2:
        port = st.number_input(
            "Port",
            value=5555,
            min_value=1000,
            max_value=9999
        )

    if st.button("🔗 BAĞLAN", type="primary", use_container_width=True):
        with st.spinner("Bağlanıyor..."):
            try:
                # Socket oluştur
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)

                # Bağlan
                s.connect((ip_adresi, int(port)))

                # Kaydet
                st.session_state.socket = s
                st.session_state.bagli = True

                st.success("✅ BAŞARIYLA BAĞLANDI!")
                st.balloons()
                time.sleep(1)
                st.rerun()

            except socket.timeout:
                st.error("⏱️ Zaman Aşımı! Sunucu cevap vermiyor.")
                st.info("💡 Kontrol: Terminal'de sunucu çalışıyor mu?")

            except ConnectionRefusedError:
                st.error("❌ Bağlantı Reddedildi!")
                st.info("💡 Kontrol:\n- Terminal'de `python p2p_sunucu.py` çalıştır\n- Port numarası doğru mu?")

            except Exception as e:
                st.error(f"❌ Hata: {e}")

    st.divider()
    st.info("ℹ️ **Nasıl Başlatılır?**\n1. Terminal aç\n2. `python p2p_sunucu.py` çalıştır\n3. Burada 'BAĞLAN' butonuna bas")

else:
    # Bağlı durumu
    st.success("✅ BAĞLI")

    if st.button("❌ Bağlantıyı Kes"):
        if st.session_state.socket:
            st.session_state.socket.close()
        st.session_state.bagli = False
        st.session_state.socket = None
        st.session_state.mesajlar = []
        st.rerun()

    st.divider()

    # BÖLÜM 2: MESAJLAŞMA
    st.header("2️⃣ Mesajlaşma")

    # Mesaj kutusu
    chat_container = st.container()

    with chat_container:
        if len(st.session_state.mesajlar) == 0:
            st.info("👋 Mesajlaşmaya başla!")
        else:
            for mesaj in st.session_state.mesajlar:
                if mesaj['tip'] == 'gonderilen':
                    st.markdown(f"""
                    <div class='sent-msg'>
                        <strong>🟢 Sen:</strong> {mesaj['icerik']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='received-msg'>
                        <strong>🔵 Terminal:</strong> {mesaj['icerik']}
                    </div>
                    """, unsafe_allow_html=True)

    st.divider()

    # Mesaj gönderme formu
    with st.form("mesaj_form", clear_on_submit=True):
        yeni_mesaj = st.text_input(
            "Mesajını yaz:",
            placeholder="Mesajını buraya yaz..."
        )

        gonder_btn = st.form_submit_button(
            "📤 GÖNDER",
            type="primary",
            use_container_width=True
        )

        if gonder_btn and yeni_mesaj:
            try:
                # Mesajı gönder
                st.session_state.socket.send(yeni_mesaj.encode('utf-8'))

                # Listeye ekle
                st.session_state.mesajlar.append({
                    'tip': 'gonderilen',
                    'icerik': yeni_mesaj
                })

                st.success("✅ Gönderildi!")

                # Cevap bekle
                with st.spinner("💬 Cevap bekleniyor... (60 saniye)"):
                    st.session_state.socket.settimeout(60)
                    cevap = st.session_state.socket.recv(1024).decode('utf-8')

                    if cevap:
                        st.session_state.mesajlar.append({
                            'tip': 'gelen',
                            'icerik': cevap
                        })
                        st.success("📨 Cevap geldi!")

                time.sleep(0.5)
                st.rerun()

            except socket.timeout:
                st.warning("⏱️ Cevap bekleme süresi doldu")

            except Exception as e:
                st.error(f"❌ Hata: {e}")
                st.session_state.bagli = False

# Alt bilgi
st.divider()
st.caption("Made with ❤️ using Streamlit")
