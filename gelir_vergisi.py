import streamlit as st
import pandas as pd

#Başlık ekliyoruz. Stream importu için st.(title)
st.title(" Gelir Vergisi Hesaplama ")

#st.selectbox olarak iniglizce olarakda anlayabiliriz select seçmek box kutu demek.Kutu secmek
#Misal "Gelir Unsuru Secin" string,[ücretli,Ücret dışı] ise list metodur ancak type ile bakarsanız tupple olacaktır.
#matrah_aylik olarak variable olusturduk ve buna numeric girebilmek için ise number metodunu sectık

gelir_unsuru = st.selectbox("Gelir Unsuru Seçin:", ["Ücretli", "Ücret Dışı"])
matrah_aylik = st.number_input(
    "Aylık Brüt Gelir (TL)",
    min_value=0.0, #Minimum Girilecek Değer
    value=20000.0,#Box daki değer
    step=500.0 # Sayı arttırmak için kullanılacak değerdir.


)


# def metoduyla oluşturduk, matrah_aylik, gelir_unsuru fonksiyonlarını çağırdık
def hesapla_vergi_ve_net(matrah_aylik, gelir_unsuru):
    if gelir_unsuru == "Ücretli":
        yillik_matrah = matrah_aylik * 12 # Burada yıllık matrahı buluyoruz
        if yillik_matrah <= 158_000: # Eğer yıllık matrah 158 ve 158 000 altındaysa örnek :  (12_000 x12_000=144_000) yıllık matrah= 144_000*0.15=21_600 yıllık vergi
            vergi = yillik_matrah * 0.15
        elif yillik_matrah <= 330_000:# Eğer yıllık matrah 158.000<yıllık_matrah<=330_000 ise demektir bu kosul . misal (15_000*12)=180_000(180_000-158_00)*0.20 +23_700
            vergi = 23_700 + 0.20 * (yillik_matrah - 158_000) 
            vergi+=2400
        elif yillik_matrah <= 1_200_000:
            vergi = 58_100 + 0.27 * (yillik_matrah - 330_000)  
        elif yillik_matrah <= 4_300_000:
            vergi = 293_000 + 0.35 * (yillik_matrah - 1_200_000)
        else:
            vergi = 1_378_000 + 0.40 * (yillik_matrah - 4_300_000)

    net_yillik = yillik_matrah - vergi  #net yıllık gelir için örnek(33_000 X 12)=396_000=320_080
    net_aylik = (net_yillik / 12) if gelir_unsuru == "Ücretli" else None
    #ücretli için net ayliği bulmak (net yıllık/12) 320_080/12= 26_673 net_aylik
    tahakkuk_vergi=(matrah_aylik-net_aylik)if net_aylik is not None else None   # 33.000 - 26.673= 6.326
    # def ile oluşturduğum variable yani fonksiyonları return ile geri çağırıyorum
    return (float(f"{yillik_matrah:.2f}"),
            float(f"{vergi:.2f}"),
            float(f"{net_yillik:.2f}"),
            float(f"{net_aylik:.2f}"),
            float(f"{tahakkuk_vergi:.2f}")
           )

if st.button("Vergiyi Hesapla"):
    yillik_matrah, vergi, net_yillik, net_aylik,tahakkuk_vergi = hesapla_vergi_ve_net(matrah_aylik, gelir_unsuru)
    #st button iste bu işlemi gerçekleştirmek için oluşturulan kutucuk metodudur.
    # Gördüğünüz gibi yukarıdaki return ile çağırdım fonkz"iyonları bu butonun içine atıyorum.



  #Data_Frame denilen olay veriyi tablo haline çevirmedir.
    #import pandas as pd ile çekeriz
    # Misal Sütunlar(columns)
    #satırlar (rows) diye adlandırılır.
    # Aşağıdaki mantıkla sütunları doldururz
    df = pd.DataFrame({
        "Gelir Unsuru": [gelir_unsuru],  # Bu genellikle string, float yapmaya gerek yok
    "Aylık Brüt Gelir (₺)": [(matrah_aylik)],
    "Yıllık Matrah (₺)": [(yillik_matrah)],
    "Yıllık Vergi (₺)": [(vergi)],
    "Tahakkuk Eden Vergi (₺)": [(tahakkuk_vergi)],
    "Net Yıllık Gelir (₺)": [(net_yillik)],
    "Net Aylık Gelir (₺)": [(net_aylik)]
})



    st.subheader("Sonuc:")#altbaslık metodu ıcın st.subheader
    st.table(df)    # Streamda tablo ile göstermek içindir









































