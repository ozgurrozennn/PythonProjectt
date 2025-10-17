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
if 0<matrah_aylik <=1000:#misal burda 1000 ve aşağısını 1000 sabitledik misal 90 da yazsa 1000den hesaplamasını istedik.
    matrah_aylik = 1000# = atama operatoruyle 1000 sabitledik

# def metoduyla oluşturduk, matrah_aylik, gelir_unsuru fonksiyonlarını çağırdık
def hesapla_vergi_ve_net(matrah_aylik, gelir_unsuru):
    if gelir_unsuru == "Ücretli":   # Burda gelir unsuru ücretli seçildiğinde
        yillik_matrah = matrah_aylik * 12   # yıllık matrahı oluşturduk (33.000X12=396.000)
    else:
        yillik_matrah = matrah_aylik    # ücret dışı secmişs se çarpma işlemi yapılmaz Ücret dışını yıllık al direk 396.000


        if yillik_matrah <= 158_000:
            vergi = yillik_matrah * 0.15
        elif yillik_matrah <= 330_000:
            vergi = 158_000 * 0.15 + yillik_matrah-158.000*0.20
        elif yillik_matrah <= 1_200_000:
            vergi = 158_000 * 0.15 + 172_000 * 0.20 + yillik_matrah - 330_000 * 0.27
        elif yillik_matrah <= 4_300_000:
            vergi = 158_000 * 0.15 + 172_000 * 0.20 + 870_000 * 0.27 + yillik_matrah - 1_200_000 * 0.35
        else:
            vergi = 158_000 * 0.15 + 172_000 * 0.20 + 870_000 * 0.27 + 3_100_000 * 0.35 + yillik_matrah - 4_300_000 * 0.40

    net_yillik = yillik_matrah - vergi  #net yıllık gelir için örnek(33_000 X 12)=396_000=320_080
    net_aylik = (net_yillik / 12) if gelir_unsuru == "Ücretli" else None
    #ücretli için net ayliği bulmak (net yıllık/12) 320_080/12= 26_673 net_aylik
    tahakkuk_vergi=(matrah_aylik-net_aylik)if net_aylik is not None else None   # 33.000 - 26.673= 6.326
    return yillik_matrah, vergi, net_yillik, net_aylik,tahakkuk_vergi
    # def ile oluşturduğum variable yani fonksiyonları return ile geri çağırıyorum

def format_sayi(sayi):# Misal burda da sayı atadık ki ondalık hatasını engelledik
        if sayi is None:# Eğer sayı none değeri verirse
            return "-"
        elif sayi.is_integer():# sayının yanı float degerindeki sayınının tam sayı olup olmadığını kontrol eder
            return f"{int(sayi):,}".replace(",", ".")
            # 360.00 floattır ama bu metota göre tam sayıdır ancak 360.05 float sayısıdır.
            # virgül koyulursa nokta olarak işleme almak için replace metodu kullanılmıştır.
        else:
            return f"{sayi:,.2f}".replace(",", ".")  # misal ondalıklı sayı cıkarsa son iki rakamını al ve virgül ise noktaya çevir




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
        "Gelir Unsuru": [gelir_unsuru],
        "Aylık Brüt Gelir (₺)": [format_sayi(matrah_aylik)],# burada format eklemeyı unutmuyoruz yoksa liste de ondalıklı verir.
        "Yıllık Matrah (₺)": [format_sayi(yillik_matrah)],## burada format eklemeyı unutmuyoruz yoksa liste de ondalıklı verir.
        "Yıllık Vergi (₺)": [format_sayi(vergi)],## burada format eklemeyı unutmuyoruz yoksa liste de ondalıklı verir.
        "Tahakkuk Eden Vergi":[format_sayi(tahakkuk_vergi)],## burada format eklemeyı unutmuyoruz yoksa liste de ondalıklı verir.
    "Net Yıllık Gelir (₺)": [format_sayi(net_yillik)],## burada format eklemeyı unutmuyoruz yoksa liste de ondalıklı verir.
        "Net Aylık Gelir (₺)": [format_sayi(net_aylik)]## burada format eklemeyı unutmuyoruz yoksa liste de ondalıklı verir.
        

    })

    st.subheader("Sonuc:")#altbaslık metodu ıcın st.subheader
    st.table(df)    # Streamda tablo ile göstermek içindir





