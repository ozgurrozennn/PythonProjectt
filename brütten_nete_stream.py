import streamlit as st
import pandas as pd

st.title("Bordro Hesaplama")

# Girişler
brüt_ücret = st.number_input("Brüt Ücret (TL)")

bordro = st.checkbox("Bordro ", )

hesapla_btn = st.button(" Hesapla")

if hesapla_btn and brüt_ücret > 0:
    # 2025 Asgari Ücret
    asgari_ucret_brut = 26_005.50

    # Asgari ücret kesintileri
    asgari_sgk = asgari_ucret_brut * 0.14
    asgari_issizlik = asgari_ucret_brut * 0.01
    asgari_damga_vergisi = asgari_ucret_brut * 0.00759

    # Asgari ücret gelir matrahı
    asgari_gelir_matrahi = asgari_ucret_brut - (asgari_sgk + asgari_issizlik)

    # Asgari ücret gelir vergisi (ilk dilim %15)
    asgari_gelir_vergisi = asgari_gelir_matrahi * 0.15

    # Asgari ücret net hesaplama
    asgari_net = asgari_ucret_brut - (asgari_sgk + asgari_issizlik + asgari_gelir_vergisi + asgari_damga_vergisi)

    # İstisnalar
    asgari_ucret_gelir_vergisi_istisnasi = asgari_gelir_vergisi
    asgari_ucret_damga_vergisi_istisnasi = asgari_damga_vergisi

    # Sabit oranlar
    sgk_oranı = 0.14
    işsizlik_sigorta_primi = 0.01
    damga_vergisi = 0.00759

    # Vergi dilimleri
    vergi1 = 158_000 * 0.15
    vergi2 = (330_000 - 158_000) * 0.20
    vergi3 = (1_200_000 - 330_000) * 0.27
    vergi4 = (4_300_000 - 1_200_000) * 0.35
    vergi5 = (800_000 - 330_000) * 0.27
    vergi6 = (4_300_000 - 800_000) * 0.35

    # Kesintiler
    sgk_işçi = brüt_ücret * sgk_oranı
    işsizlik_işçi = brüt_ücret * işsizlik_sigorta_primi
    damga_vergisi_tutarı = brüt_ücret * damga_vergisi
    gelir_matrahı = brüt_ücret - (sgk_işçi + işsizlik_işçi)

    # Hesaplamalar
    toplam_net = 0
    toplam_vergi = 0
    kümülatif_matrah = 0
    sonuclar = []

    for ay in range(1, 13):
        kümülatif_matrah += gelir_matrahı

        # Vergi hesaplama
        if bordro:
            if kümülatif_matrah < 158_000:
                kümülatif_vergi = kümülatif_matrah * 0.15
            elif kümülatif_matrah < 330_000:
                kümülatif_vergi = vergi1 + ((kümülatif_matrah - 158_000) * 0.20)
            elif kümülatif_matrah < 1_200_000:
                kümülatif_vergi = vergi1 + vergi2 + ((kümülatif_matrah - 330_000) * 0.27)
            elif kümülatif_matrah < 4_300_000:
                kümülatif_vergi = vergi1 + vergi2 + vergi3 + ((kümülatif_matrah - 1_200_000) * 0.35)
            else:
                kümülatif_vergi = vergi1 + vergi2 + vergi3 + vergi4 + ((kümülatif_matrah - 4_300_000) * 0.40)
        else:
            if kümülatif_matrah < 158_000:
                kümülatif_vergi = kümülatif_matrah * 0.15
            elif kümülatif_matrah < 330_000:
                kümülatif_vergi = vergi1 + ((kümülatif_matrah - 158_000) * 0.20)
            elif kümülatif_matrah < 800_000:
                kümülatif_vergi = vergi1 + vergi2 + ((kümülatif_matrah - 330_000) * 0.27)
            elif kümülatif_matrah < 4_300_000:
                kümülatif_vergi = vergi1 + vergi2 + vergi5 + ((kümülatif_matrah - 800_000) * 0.35)
            else:
                kümülatif_vergi = vergi1 + vergi2 + vergi5 + vergi6 + ((kümülatif_matrah - 4_300_000) * 0.40)

        if ay == 1:
            aylık_gelir_vergisi = kümülatif_vergi
        else:
            aylık_gelir_vergisi = kümülatif_vergi - toplam_vergi

        # İstisna uygulaması
        gelir_vergisi_istisna_sonrası = max(0, aylık_gelir_vergisi - asgari_ucret_gelir_vergisi_istisnasi)
        damga_vergisi_istisna_sonrası = max(0, damga_vergisi_tutarı - asgari_ucret_damga_vergisi_istisnasi)

        toplam_vergi = kümülatif_vergi

        # Net ücret hesaplama
        aylık_net = brüt_ücret - (
                    sgk_işçi + işsizlik_işçi + gelir_vergisi_istisna_sonrası + damga_vergisi_istisna_sonrası)
        toplam_net += aylık_net

        sonuclar.append({
            'Ay': ay,
            'Brüt Ücret': brüt_ücret,
            'SGK': sgk_işçi,
            'İşsizlik': işsizlik_işçi,
            'Gelir Vergisi': aylık_gelir_vergisi,
            'GV İstisnası': asgari_ucret_gelir_vergisi_istisnasi,
            'Ödenecek GV': gelir_vergisi_istisna_sonrası,
            'Damga Vergisi': damga_vergisi_tutarı,
            'DV İstisnası': asgari_ucret_damga_vergisi_istisnasi,
            'Ödenecek DV': damga_vergisi_istisna_sonrası,
            'Net Ücret': aylık_net
        })


    # Sonuçları göster
    df = pd.DataFrame(sonuclar)

    st.dataframe(
        df.style.format({
            'Brüt Ücret': '{:,.2f} ₺',
            'SGK': '{:,.2f} ₺',
            'İşsizlik': '{:,.2f} ₺',
            'Gelir Vergisi': '{:,.2f} ₺',
            'GV İstisnası': '{:,.2f} ₺',
            'Ödenecek GV': '{:,.2f} ₺',
            'Damga Vergisi': '{:,.2f} ₺',
            'DV İstisnası': '{:,.2f} ₺',
            'Ödenecek DV': '{:,.2f} ₺',
            'Net Ücret': '{:,.2f} ₺'
        }),

    )

