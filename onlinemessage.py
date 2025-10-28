"""
GRUP CHAT İSTEMCİ - Streamlit
Herkes aynı sohbete katılır, WhatsApp gibi grup sohbeti
"""

import streamlit as st
import socket
import time
try:
    import threading
except ImportError:
    st.error("Threading modülü bulunamadı!")
    st.stop()

st.set_page_config(page_title="Grup Chat", page_icon="👥", layout="centered")

# CSS - WhatsApp tarzı
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
    }
    
    .chat-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        max-height: 400px;
        overflow-y: auto;
        margin: 20px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .mesaj-benim {
        background: #DCF8C6;
        padding: 10px 15px;
        border-radius: 15px 15px 5px 15px;
        margin: 8px 0;
        margin-left: 30%;
        text-align: right;
    }
    
    .mesaj-diger {
        background: #E8E8E8;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 5px;
        margin: 8px 0;
        margin-right: 30%;
    }
    
    .sistem-mesaji {
        background: #FFF9C4;
        padding: 8px;
        border-radius: 10px;
        margin: 8px 0;
        text-align: center;
        font-size: 12px;
        color: #666;
    }
    
    h1 {
        color: white !important;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Session State
if 'bagli' not in st.session_state:
    st.session_state.bagli = False
if 'socket' not in st.session_state:
    st.session_state.socket = None
if 'mesajlar' not in st.session_state:
    st.session_state.mesajlar = []
if 'isim' not in st.session_state:
    st.session_state.isim = ""
if 'dinleme_thread' not in st.session_state:
    st.session_state.dinleme_thread = None

def mesaj_dinle():
    """Arka planda sürekli mesaj dinle"""
    while st.session_state.bagli:
        try:
            st.session_state.socket.settimeout(1)
            mesaj = st.session_state.socket.recv(1024).decode('utf-8')
            
            if mesaj and mesaj != "ISIM_SOR":
                # Sistem mesajı mı?
                if mesaj.startswith("📢"):
                    st.session_state.mesajlar.append({
                        'tip': 'sistem',
                        'icerik': mesaj
                    })
                else:
                    st.session_state.mesajlar.append({
                        'tip': 'gelen',
                        'icerik': mesaj
                    })
        except socket.timeout:
            continue
        except:
            st.session_state.bagli = False
            break

# Başlık
st.title("👥 Grup Chat")
st.caption("WhatsApp tarzı grup sohbeti")

# BAĞLANTI BÖLÜMÜ
if not st.session_state.bagli:
    st.header("🔗 Sohbete Katıl")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        isim = st.text_input("👤 Adın:", placeholder="Ahmet, Mehmet...")
    
    with col2:
        ip = st.text_input("📍 Sunucu IP:", value="localhost")
    
    if st.button("🚀 KATIL", type="primary", use_container_width=True):
        if not isim:
            st.error("❌ Lütfen bir isim gir!")
        else:
            try:
                # Bağlan
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((ip, 5555))
                
                # İsim soran mesajı al
                ilk_mesaj = s.recv(1024).decode('utf-8')
                if ilk_mesaj == "ISIM_SOR":
                    # İsmi gönder
                    s.send(isim.encode('utf-8'))
                
                st.session_state.socket = s
                st.session_state.isim = isim
                st.session_state.bagli = True
                
                # Dinleme thread'i başlat
                thread = threading.Thread(target=mesaj_dinle, daemon=True)
                thread.start()
                st.session_state.dinleme_thread = thread
                
                st.success(f"✅ Hoş geldin {isim}!")
                st.balloons()
                time.sleep(1)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Bağlantı hatası: {e}")
                st.info("💡 Sunucu çalışıyor mu? `python grup_chat_sunucu.py`")

else:
    # BAĞLI DURUM
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.success(f"✅ Bağlısın: **{st.session_state.isim}**")
    with col2:
        st.info(f"💬 Mesaj sayısı: {len(st.session_state.mesajlar)}")
    with col3:
        if st.button("🚪 Çık"):
            if st.session_state.socket:
                st.session_state.socket.close()
            st.session_state.bagli = False
            st.session_state.mesajlar = []
            st.rerun()
    
    st.divider()
    
    # MESAJLAR
    st.header("💬 Sohbet")
    
    # Mesajları göster
    chat_html = '<div class="chat-container">'
    
    if len(st.session_state.mesajlar) == 0:
        chat_html += '<p style="text-align:center; color:#999;">Henüz mesaj yok. İlk mesajı sen at! 👋</p>'
    else:
        for msg in st.session_state.mesajlar:
            if msg['tip'] == 'sistem':
                chat_html += f'<div class="sistem-mesaji">{msg["icerik"]}</div>'
            elif msg['tip'] == 'gonderilen':
                chat_html += f'<div class="mesaj-benim"><strong>Sen:</strong> {msg["icerik"]}</div>'
            else:
                chat_html += f'<div class="mesaj-diger">{msg["icerik"]}</div>'
    
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)
    
    # Otomatik yenileme
    if st.button("🔄 Yenile"):
        st.rerun()
    
    st.divider()
    
    # MESAJ GÖNDER
    with st.form("mesaj_form", clear_on_submit=True):
        mesaj = st.text_input("✍️ Mesajını yaz:", placeholder="Mesajını buraya yaz...")
        gonder = st.form_submit_button("📤 GÖNDER", type="primary", use_container_width=True)
        
        if gonder and mesaj:
            try:
                st.session_state.socket.send(mesaj.encode('utf-8'))
                st.session_state.mesajlar.append({
                    'tip': 'gonderilen',
                    'icerik': mesaj
                })
                st.success("✅ Gönderildi!")
                time.sleep(0.3)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Hata: {e}")
                st.session_state.bagli = False
    
    # Otomatik yenileme timer
    st.caption("💡 Yeni mesajlar için sayfa otomatik yenileniyor...")
    time.sleep(2)
    st.rerun()

# Alt bilgi
st.divider()
st.caption("Made with ❤️ - Grup Chat Uygulaması")
