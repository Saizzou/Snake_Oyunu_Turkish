import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Kutu(object):
    en = 500
    bolme = 20
    def __init__(self, start, yonx=1, yony=0, color=(255,0,0)):
        self.pos = start
        self.yonx = 1
        self.yony = 0
        self.color = color


    def move(self, yonx, yony):
        self.yonx = yonx
        self.yony = yony
        self.pos = (self.pos[0] + self.yonx, self.pos[1] + self.yony) #hareket tanımı


    def draw(self, surface, gozler=False):
        boy = self.en // self.bolme #boy = en bölü bölme sayısı yani bu projede 25
        i = self.pos[0] #enlem
        j = self.pos[1] #boylam

        pygame.draw.rect(surface,self.color,(i*boy+1,j*boy+1,boy-2,boy-2))

        if gozler:
            orta = boy //2
            cap = 3
            goz1 = (i*boy+orta-cap, j*boy+8)
            goz2 = (i*boy + boy-cap*2, j*boy+8)
            pygame.draw.circle(surface, (255,255,255),goz1,cap)
            pygame.draw.circle(surface, (255,255,255),goz2,cap)


class Yilan(object):
    govde = [] #yem yedikçe büyüyen bir gövde listesi oluşturcaz. Bu liste kutu'lardan oluşacak.
    yon = {} #self.yonx ve self.yony olarak 2 yönü tutan set oluşturcaz
    def __init__(self, color, pos):
        self.color = color
        self.kafa = Kutu(pos) # kafa bizim yön değiştiren kutumuz olacak ve pozisyona göre hareket edecek
        self.govde.append(self.kafa) #Kafa'yı govde listemize ekliyoruz.

        self.yonx = 0
        self.yony = 1


    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            pygame.init()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.yonx = -1
                    self.yony = 0
                    self.yon[self.kafa.pos[:]] = [self.yonx, self.yony] #Yön setini belirledik ve
                    #tüm gövde listesini o yöne çevirdik

                elif keys[pygame.K_DOWN]:
                    self.yony = 1 #Aşağı + pozisyonudur
                    self.yonx = 0
                    self.yon[self.kafa.pos[:]] = [self.yonx, self.yony]

                elif keys[pygame.K_RIGHT]:
                    self.yonx = 1
                    self.yony = 0
                    self.yon[self.kafa.pos[:]] = [self.yonx, self.yony]

                elif keys[pygame.K_UP]:
                    self.yony = -1
                    self.yonx = 0
                    self.yon[self.kafa.pos[:]] = [self.yonx, self.yony]

        for i, c in enumerate(self.govde): #i ve c sabitleri olarak govdedeki her elemanı saydır (bkz:enumerate)
            k = c.pos[:] #liste pozisyonu kaydediyoruz
            if k in self.yon: #eğer kayıt pozisyonu yön noktasındaysa
                don = self.yon[k] #döneceğimiz yon'u aktarıyoruz
                c.move(don[0], don[1]) #donme işlemini sıradaki kübe aktar
                if i == len(self.govde)-1: #son kübe ulaştığımızda
                    self.yon.pop(k) #dönme işlemini durdur (pop: bkz listede çıkarma işlemi)
            else:
                if c.yonx == -1 and c.pos[0] <= 0: c.pos = (c.bolme-1,c.pos[1])
                #x yönünde duvarı geçer (eksi kısmı) ise x'i bölme sayımız(25)-1'e gönder ve y'yi bir önceki kutudan aktar
                elif c.yonx == 1 and c.pos[0] >= c.bolme-1: c.pos = (0,c.pos[1])
                elif c.yony == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.bolme-1)
                elif c.yony == 1 and c.pos[1] >= c.bolme-1: c.pos = (c.pos[0], 0)
                else: c.move(c.yonx, c.yony) # duvara gelmiyor ise yoluna devam et.

    def reset(self, pos):
        self.head = Kutu(pos)
        self.govde = []
        self.govde.append(self.kafa)

        self.yonx = 0
        self.yony = 1

    def draw(self, surface):
        for i, c in enumerate(self.govde):
            if i == 0: #yılan listemizde ilk kutuya göz çizilsin istiyoruz bunun için,
                c.draw(surface, True) #burayı ekledik yani göz oluşsun doğru komutu verdik
            else:
                c.draw(surface) # Döngü False yani gözsüz devam edecektir
    def kutuekle(self):
        kuyruk = self.govde[-1] # Son kutuyu işaret edecek
        kx, ky = kuyruk.yonx, kuyruk.yony

        if kx == 1 and ky == 0: #Yani sol yatayda ise kuyruk
            self.govde.append(Kutu((kuyruk.pos[0]-1,kuyruk.pos[1])))

        elif kx == -1 and ky == 0: #Yani sağ yatayda ise kuyruk
            self.govde.append(Kutu((kuyruk.pos[0]+1,kuyruk.pos[1])))

        elif kx == 0 and ky == 1: #Yani aşağı dikeyde ise ise kuyruk
            self.govde.append(Kutu((kuyruk.pos[0],kuyruk.pos[1]-1)))

        elif kx == 0 and ky == -1: #Yani yukarı dikeyde ise ise kuyruk
            self.govde.append(Kutu((kuyruk.pos[0],kuyruk.pos[1]+1)))

        self.govde[-1].yonx = kx
        self.govde[-1].yony = ky


def drawGrid(surface):
    en = 500
    yukseklik = 500
    bolme = 20
    mesafe = 25 # // burda sonucu tuple değil integer olmasını sağlar.

    x = 0 # Başlangıç noktamızı belirliyor
    y = 0
    for l in range(20): # bölme sayımız kadar loop oluşturup ekranı böleceğiz.
        x = x + mesafe
        y = y + mesafe

        pygame.draw.line(surface, (255,255,255), (x,0), (x,en))
        pygame.draw.line(surface, (255,255,255), (0,y), (yukseklik,y))

def redrawWindow(surface):
    global bolme, en, y, yem
    surface.fill((0,0,0)) #Arkaplanı siyah yaptık.
    y.draw(surface) #Yılanı çiz fonksiyonu
    yem.draw(surface) #Yem'i çiz fonksiyonu
    drawGrid(surface) #Ustten bilgi alıp çizgilerimizi çekecektir.
    pygame.display.update() #Yenilenmeyi sağlayan pygame fonksiyonu

def randomYem(bolme, item):
    yer = item.govde # Yılanın yerini bulduracak

    while True: #Doğru yanlış döngüsü ile yılanın bulunduğu yerde değilse diyeceğiz
        x = random.randrange(bolme)
        y = random.randrange(bolme)
        if len(list(filter(lambda z:z.pos == (x,y), yer))) > 0:
            continue
        else:
            break

    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost",True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    #Pencere özelliklerini belirtiyoruz.
    global en, bolme, y, yukseklik, yem #global bu fonksiyon içindeki sabitleri fonksiyon dışındada kullandırır.
    yukseklik = 500
    en = 500
    bolme = 20
    pygame.init()

    win = pygame.display.set_mode((en, yukseklik)) #Pencere oluşturuyoruz.

    y = Yilan((0, 255, 0),(10, 10)) #Yılanı oluşturduk (renk,boyut) olarak.

    saat = pygame.time.Clock()

    flag = True
    # Penceremizi durmadan calışması için döndürüyoruz.
    yem = Kutu(randomYem(bolme, y), color=(255,255,0))

    while flag:
        if y.govde[0].pos == yem.pos: # Kafa ile yem çarpışır ise:
            y.kutuekle() #Yılan boyunu uzatacak
            yem = Kutu(randomYem(bolme, y), color=(255,255,0)) #Yeni yem oluşturacak

        pygame.time.delay(50) #Oyun başlamadan biraz bekletir.
        saat.tick(5) #Bu bizim FPS ayarımız.
        y.move()

        for x in range(len(y.govde)):
            if y.govde[x].pos in list(map(lambda z:z.pos,y.govde[x+1:])): #Bu yılan kendi içinde kesişti mi diye kontrol edecektir
                print('Score:', len(y.govde))
                message_box('Kaybettiniz!','Bir daha oyna..')
                y.reset((10,10))
                break

        redrawWindow(win) #oluşturduğumuz pencereyi redraw fonksiyonu ile oluşturuyoruz.
main()