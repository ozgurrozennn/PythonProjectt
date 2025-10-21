import streamlit as st
import pandas as pd

st.title("Bordro Hesaplama")

# Girişler
brüt_ücret = st.number_input("Brüt Ücret (TL)")

bordro = True

hesapla_btn = st.button(" Hesapla")

if hesapla_btn:
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
    damga_vergisi_oranı = brüt_ücret * damga_vergisi
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

        toplam_vergi = kümülatif_vergi
        aylık_net = brüt_ücret - (sgk_işçi + işsizlik_işçi + aylık_gelir_vergisi + damga_vergisi_oranı)
        toplam_net += aylık_net

        sonuclar.append({
            'Ay': ay,
            'Brüt Ücret': brüt_ücret,
            'SGK': sgk_işçi,
            'İşsizlik': işsizlik_işçi,
            'Damga Vergisi': damga_vergisi_oranı,
            'Gelir Vergisi': aylık_gelir_vergisi,
            'Net Ücret': aylık_net
        })

    # Sonuçları göster
    df = pd.DataFrame(sonuclar)

    st.dataframe(
        df.style.format({
            'Brüt Ücret': '{:,.2f} ₺',
            'SGK': '{:,.2f} ₺',
            'İşsizlik': '{:,.2f} ₺',
            'Damga Vergisi': '{:,.2f} ₺',
            'Gelir Vergisi': '{:,.2f} ₺',
            'Net Ücret': '{:,.2f} ₺'
        }),

    )


    st.write(f"**Yıllık Toplam Net Ücret:** {toplam_net:,.2f} ₺")
