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
