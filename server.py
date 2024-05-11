from socket import *
import os
import base64

# Serverin ip değeri belirtildi.
server_ip = "192.168.1.15"

# hangi port üzerinde çalışılacaği belirtildi.
server_port = 789

# IPv4 ve TCP olduğunu belirttik.
server = socket(AF_INET, SOCK_STREAM)


# binding yaptık yani ip ile portu eşleştirdik.
server.bind((server_ip, server_port))


# server dinlemeye başladı.
server.listen(1)

cSocket, cAdress = server.accept() # TCP özel bir yapıdır.


# Burada mesaj gönderme metotu yazıldı.
def mesajGonder():
    

    while True:

        print(f"{cAdress}'e baglanildi")



        data = cSocket.recv(1024).decode()
        
        if data == "-1":
            break

        else:
            print(f"alinan Mesaj: {data}")


            response = input("Gondermek istediginiz mesajı girin: ")



            cSocket.send(response.encode())
        


# burada resim gönderme metotu yazıldı.
def resimGonder():
    istenenResim = cSocket.recv(1024).decode()
    print(istenenResim)
    if os.path.exists(istenenResim):
        with open(istenenResim, "rb") as file:
            dosya_verisi = file.read()
            sifrelenmis_resim = base64.b64encode(dosya_verisi)
        cSocket.sendall(sifrelenmis_resim)
        print("Dosya okunup gönderildi.")

    else:
        cSocket.send("Error".encode())
        print("Error mesaji client tarafına gonderildi.")



# pdf gönderme metotu yazıldı.
def pdfGonder():
    dosya_adi = cSocket.recv(1024).decode()
    print(f"Istenen dosya {dosya_adi}")
    try:
        with open(dosya_adi, "rb") as dosya:
            dosya_verisi = dosya.read()
            cSocket.sendall(dosya_verisi)
    except:
        cSocket.send("Error".encode())
        print("Error mesajı client tarafında gönderildi.")



# kullanıcının seçimine göre işlem yapılacak
controller = cSocket.recv(1024).decode()
if controller == "1":
    resimGonder()
elif controller == "2":
    mesajGonder()
elif controller == "3":
    pdfGonder()


