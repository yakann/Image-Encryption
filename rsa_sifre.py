#!/usr/bin/env python
#-*-coding:utf-8-*-

import random
import time
import pyodbc
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num ** 0.5) + 2, 2):
        if num % n == 0:
            return False
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Sayilar Asal Olmali.')
    elif p == q:
        raise ValueError('p ve q esit olamaz.')
    # n = pq
    n = p * q
    # Phi is the totient of n
    toti = (p - 1) * (q - 1)
    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, toti)
    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, toti)
    while g != 1:
        e = random.randrange(1, toti)
        g = gcd(e, toti)
    d = modinv(e, toti)
    return ((e, n), (d, n))

#ters mod yapariz
# Took from SO
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m


def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher

#def parcala(pk, plaintext):
    #key, n = pk

    #sonuc = ((plaintext ** key) % n)
    #return sonuc

def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)

def mail_gonder(sifreli_mesaj):
    mesaj = MIMEMultipart()
    mesaj["From"] = "baz090909@gmail.com" # Mailin Gonderilecegi Adres
    mesaj["To"] = "mbaykara@firat.edu.tr"  # Mailin Alicisi
    mesaj["Subject"] = "RSA ile sifrelenmis metin."  # Mail Basligi
    yazi = sifreli_mesaj
    # Mesaj
    mesaj_govdesi = MIMEText(yazi, "plain")
    mesaj.attach(mesaj_govdesi)
    try:
        mail = smtplib.SMTP("smtp.gmail.com", 587)  # once bir smtp objesi olusturuyoruz.2.Degisken portumuz.
        mail.ehlo()
        mail.starttls()
        mail.login("baz090909@gmail.com", "Mhmtykn.44")
        mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())
        print("Mail Basariyla Gonderildi...")
        mail.close()
    except:
        sys.stderr.write("Bir Sorun Olustu!")
        sys.stderr.flush()

if __name__ == '__main__':
    #p = int(input("Enter a prime number (17, 19, 23, etc): "))
    #q = int(input("Enter another prime number (Not one you entered above): "))
    print ("""**************************************************************************

            ...RESiM siFRELEME PROGRAMiNA HOsGELDiNiZ.... 
                             
                    +Resim sifrelemek icin (1)' e
                    +Metin sifrelemek icin (2)'ye Basiniz...
                                   
**************************************************************************""")
    time.sleep(2)
    while True:
        asil_secim = input("Sec:")
        if asil_secim != "1" and asil_secim != "2":
            print("Yanlis Giris Yaptiniz")
        else:
            break

    ####Asal sayilari secme islemi.
    while True:
        if asil_secim == "2":
            print("""
                    Asal Sayi Secimi:      a)Max Asal Sayilar(1)
                                           b)Manuel(2) 
__________________________________________________________________________""")
            while True:
                secim = input("Secim:")
                if secim == "2":
                    print("""NOT: Asal sayinin buyuk secilmesi guvenliginiz acisindan
    onem arz etmektedir.
__________________________________________________________________________""")
                    while True:
                        p = int(input("Bir asal sayi giriniz: "))
                        q = int(input("Bir diger asal sayimizi girelim: "))
                        print("__________________________________________________________________________")
                        time.sleep(2)
                        if not (is_prime(p) and is_prime(q)):
                            print("""Sayilar Asal Olmali!!!
                            
        Lutfen Asal Sayilar Giriniz.
__________________________________________________________________________""")
                        elif p == q:
                            print("""p ve q Degerleri Esit Olamaz!!!
__________________________________________________________________________""")
                        else:
                            break
                    break
                elif secim == "1":
                    p = 97#971111
                    q = 103#1000003
                    break
                else:
                    print("""Bir islem Secmediniz Yada Yanlis Deger Girdiniz!
        
        Lutfen Tekrar islem Seciniz.""")
                    print("__________________________________________________________________________")
            break
        elif asil_secim == "1":
            p = 17
            q = 19
            break


    genel, ozel = generate_keypair(p, q)
    print("Genel Anahtarimiz: ", genel, " ve ozel Anahtarimiz: ", ozel)
    print("__________________________________________________________________________")
    time.sleep(1)

    while True:
        if asil_secim == "1":
            print("""
            **Kayitli 2 Adet Resim Bulunmaktadir. Secmek icin 1 yada 2 tusuna Basiniz...  
                """)
            print("__________________________________________________________________________")
            secim2 = input("Secim:")
            baglanti = pyodbc.connect('DRiVER={SQL Server};SERVER=.;DATABASE=hapis;')##VeriTabanimiza Baglaniyoruz.
            cursor = baglanti.cursor()
            cursor.execute("select profil_resmi from ceza_bilgisi")
            rows = cursor.fetchall()
            if secim2 == "1":
                mesaj = rows[0]
                mesaj = str(mesaj)
                print("Secilen Resim -->")
                time.sleep(1)
                break
            elif secim2 == "2":
                mesaj = rows[1]
                mesaj = str(mesaj)
                print("Secilen Resim -->")
                time.sleep(1)
                break
            else:
                print("""Herhangibir islem Secimi Yapmadiniz.
                Lutfen 1 veya 2 numarali tuslara basiniz.
__________________________________________________________________________""")
        elif asil_secim=="2":
            print("""
            Evet simdide sifrelemek istedigimiz Mesaji Girelim. 
            """)
            mesaj = input("-->")
            break
    print("""__________________________________________________________________________
    sifreleme islemi Gerceklestiriliyor... 
    Lutfen Bekleyiniz...
__________________________________________________________________________""")
    time.sleep(1)
    print("a_")
    sifreli_mesaj = encrypt(genel, mesaj)
    print("sifrelenmis Mesajimiz: ")
    print(''.join(map(lambda x: str(x), sifreli_mesaj)))
    print("""__________________________________________________________________________
                sifreyi cozmek icin(decrypt)--> (1)
                sifrelenmis Belgeyi Mail Olarak Almak icin --> (2)
                cikmak icin --> (y)
__________________________________________________________________________""")
    while True:
        secim3 = input("Secim:")
        if secim3 == "1":
            print("__________________________________________________________________________")
            print("""cozulmus Metin:
            
            """)
            time.sleep(1)
            a = decrypt(ozel, sifreli_mesaj)
            print(''.join(map(lambda x: str(x), a)))
        elif secim3 == "2":
            aa = str(sifreli_mesaj)
            mail_gonder(aa)
        elif secim3 == "y":
            print("Programdan cikiliyor.")
            time.sleep(2)
            break
        else:
            print("""Herhangibir islem Secmediniz.
Lutfen Tekrar Deneyiniz!
            """)


