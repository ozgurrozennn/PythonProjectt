"""
GRUP CHAT SUNUCU
Birden fazla kişi bağlanabilir, herkes herkese mesaj atabilir
"""

import socket
import threading
import time
import streamlite
class GrupChatSunucu:
    def __init__(self):
        self.istemciler = []  # Bağlı kullanıcılar
        self.isimler = {}  # Kullanıcı isimleri
        self.sunucu = None

    def sunucu_baslat(self):
        print("=" * 70)
        print("👥 GRUP CHAT SUNUCU BAŞLADI")
        print("=" * 70)
        print("📡 Port: 5555")
        print("🌐 Birden fazla kişi bağlanabilir!")
        print("⏳ Bağlantılar bekleniyor...")
        print()

        self.sunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sunucu.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sunucu.bind(('0.0.0.0', 5555))
        self.sunucu.listen(10)  # 10 kişiye kadar

        while True:
            try:
                baglanti, adres = self.sunucu.accept()

                # Kullanıcı adı al
                baglanti.send("ISIM_SOR".encode('utf-8'))
                isim = baglanti.recv(1024).decode('utf-8')

                # Listeye ekle
                self.istemciler.append(baglanti)
                self.isimler[baglanti] = isim

                print(f"✅ YENİ BAĞLANTI: {isim} ({adres})")
                print(f"👥 Toplam kullanıcı: {len(self.istemciler)}")
                print("-" * 70)

                # Herkese bildir
                self.herkese_gonder(f"📢 {isim} sohbete katıldı!", baglanti)

                # Bu kullanıcı için thread başlat
                thread = threading.Thread(
                    target=self.istemci_dinle,
                    args=(baglanti, isim)
                )
                thread.start()

            except Exception as e:
                print(f"❌ Hata: {e}")
                break

    def istemci_dinle(self, baglanti, isim):
        """Her kullanıcının mesajlarını dinle"""
        while True:
            try:
                mesaj = baglanti.recv(1024).decode('utf-8')

                if mesaj:
                    # Mesajı herkese gönder
                    tam_mesaj = f"{isim}: {mesaj}"
                    print(f"\n💬 {tam_mesaj}")
                    self.herkese_gonder(tam_mesaj, baglanti)
                else:
                    break

            except:
                break

        # Bağlantı kesildi
        self.istemciler.remove(baglanti)
        del self.isimler[baglanti]
        baglanti.close()

        print(f"\n🔴 {isim} ayrıldı")
        print(f"👥 Kalan kullanıcı: {len(self.istemciler)}")
        print("-" * 70)

        self.herkese_gonder(f"📢 {isim} sohbetten ayrıldı")

    def herkese_gonder(self, mesaj, gonderen=None):
        """Mesajı tüm kullanıcılara gönder (kendisi hariç)"""
        for istemci in self.istemciler:
            if istemci != gonderen:
                try:
                    istemci.send(mesaj.encode('utf-8'))
                except:
                    pass

if __name__ == "__main__":
    try:
        sunucu = GrupChatSunucu()
        sunucu.sunucu_baslat()
    except KeyboardInterrupt:
        print("\n\n🛑 Sunucu kapatıldı")
    except Exception as e:
        print(f"\n❌ HATA: {e}")

