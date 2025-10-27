#p2p mesajlasma kodu
#import hashlib
#sifre="1453"
#x=hashlib.sha256(sifre.encode()).hexdigest()
#x=hashlib.md5(sifre.encode()).hexdigest()
#print(x)
#kriptoloji
#erlang
#webrtc
#ismd5=st.checkbox("Md5 Formatında Görmek İstermisin")
#import streamlit as st
#import hashlib
#sifre=st.text_area("Sifre Giriniz:")
#col1,col2,col3=st.columns(3)
#with col1:
    #ismd5=st.checkbox("MD5")
#with col2:
        issha256=st.checkbox("SHA256")
#with col3:
    #btn=st.button("Getir")
#if btn:
    #if ismd5:
        #md5=hashlib.md5(sifre.encode()).hexdigest()
        #st.subheader("MD5")
        #st.code(md5)
    #if issha256:
        #sha256=hashlib.sha256(sifre.encode()).hexdigest()
        #st.subheader("Sha256")
        #st.code(sha256)



#if ismd5:
    #md5=hashlib.md5(sifre.encode()).hexdigest()
    #st.write("Md5 Formatı")
    #st.code(md5)
#ismd5=st.checkbox("Md5 Formatında Görmek İstermisin")
#btn=st.button("Getir")
#if btn:
    #st.code(sifre)
#if ismd5:
    #md5=hashlib.md5(sifre.encode()).hexdigest()
    #st.write("Md5 Formatı")
    #st.code(md5)



import random
import string
import streamlite as st


adet = st.number_input

kh = string.ascii_lowercase
bh = string.ascii_uppercase
dg = string.digits
sy = string.punctuation

secim = []

iskh = True
isbh = True
isdg = True
issy = False

if kh:
    secim.append(kh)
if isbh:
    secim.append(bh)
if isdg:
    secim.append(isdg)
if issy:
    secim.append(sy)

per = adet // len(secim)
kalan = adet % len(secim)

sifre = []
for i in secim:
    sifre.extend(random.choices(i, k=per))

sifre.extend(random.choices(secim[0], k=kalan))

random.shuffle(sifre)

sifre = "".join(sifre)

print(sifre)



