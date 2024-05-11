from socket import *
import numpy as np
import base64
import cv2

# istek atılacak sunucu yazıldı.
server_ip = "192.168.1.15"


# istek atılacak sunucu port değeri yazıldı.
server_port = 789

# IPv4 ve TCP olduğu belirtildi.
client = socket(AF_INET, SOCK_STREAM)


client.connect((server_ip, server_port))


# mesaj gönderme metotu yazıldı.
def mesajGonder():
    client.send("2".encode())

    while True:
        message = input("Bir mesaj gönder: ")
        if message == "-1":
            client.send("-1".encode())
            break
        else:
            client.send(message.encode())


            response = client.recv(1024).decode()


            print(f"Server: {response}")


    

# resim isteginde bulunma metotu
def resimIstegindeBulun():
    client.send("1".encode())
    dosya_yolu = input("Istenen resim ismini girin: ")
    client.send(dosya_yolu.encode())
    ilk_mesaj = client.recv(1024).decode()
    
    if ilk_mesaj == "Error":
        print("Istediginiz dosya sistemde bulunamadi.")
    else:
        veri = b"" + ilk_mesaj.encode()
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            veri = veri + chunk

        if veri:
            sifresi_cozulmus_resim = base64.b64decode(veri)
            resim_np_array = np.frombuffer(sifresi_cozulmus_resim, dtype=np.uint8)

            numpy_arrayden_resime = cv2.imdecode(resim_np_array, cv2.IMREAD_COLOR)
            
            dosyaIsmi = input("Resmi hangi isimle kaydetmek istiyorsunuz?\n")

            cv2.imwrite(dosyaIsmi, numpy_arrayden_resime)
        
        


# pdf isteginde bulunma metotu yazıldı.
def pdfIstegindeBulun():
    client.send("3".encode())
    dosya_yolu = input("Istenen PDF'yi girin: ")
    client.send(dosya_yolu.encode())
    ilk_mesaj = client.recv(6).decode()
    if ilk_mesaj == "Error":
        print("Istediginiz dosya sistemde bulunamadi.")
    else:
        veri = b"" + ilk_mesaj.encode()
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            veri = veri + chunk

        if veri:
            dosyaAdi = input("PDF'yi hangi isimle kaydetmek istersiniz?\n")
            with open(dosyaAdi,"wb") as dosya:
                dosya.write(veri)
            




# kullanıcının seçimine göre işlem yapıldı.
controller = input("resim icin 1, mesaj icin 2, pdf icin 3 tiklayiniz\n")
if controller == "1":
    resimIstegindeBulun()
elif controller == "2":
    mesajGonder()
elif controller == "3":
    pdfIstegindeBulun()




