import cv2
from mss import mss
from PIL import Image
import numpy as np
import time

class Bild:
    def __init__(self):
        self.statiskaBilder = {
            'left-goalpost': 'assets/left-goalpost.png',
            'bison-head': 'assets/bison-head.png',
            'pineapple-head': 'assets/pineapple-head.png',
            'bison-health-bar': 'assets/bison-health-bar.png',
            'pineapple-health-bar': 'assets/pineapple-health-bar.png',
            'cancel-button': 'assets/cancel-button.png',
            'filled-with-goodies': 'assets/filled-with-goodies.png',
            'next-button': 'assets/next-button.png',
            'tap-to-continue': 'assets/tap-to-continue.png',
            'unlocked': 'assets/unlocked.png',
            'full-rocket': 'assets/full-rocket.png'
        }

        self.mallar = { k: cv2.imread(v, 0) for (k, v) in self.statiskaBilder.items() }
        self.monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        self.skärm = mss()
        self.bildruta = None

    def konverteraRgbTillBgr(self, img):
        return img[:, :, ::-1]

    def taSkärmdump(self):
        sct_img = self.skärm.grab(self.monitor)
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        img = np.array(img)
        img = self.konverteraRgbTillBgr(img)
        imgGråskalad = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return imgGråskalad

    def uppdateraBildruta(self):
        self.frame = self.taSkärmdump()
    
    def matchaMall(self, imgGråskalad, template, threshold = 0.9):
        res = cv2.matchTemplate(imgGråskalad, template, cv2.TM_CCOEFF_NORMED)
        matchning = np.where(res >= threshold)
        return matchning

    def hittaMall(self, namn, bild = None, threshold = 0.9):
        if bild is None:
            if self.bildruta is None:
                self.uppdateraBildruta()
            bild = self.bildruta
        return self.matchaMall(
            bild,
            self.mallar[namn],
            threshold
        )
    
    def skaladHittaMallar(self, namn, bild = None, threshold = 0.9, scales =[1.0, 0.9, 1.1]):
        if bild is None:
            if self.bildruta is None:
                self.uppdateraBildruta()
            bild = self.bildruta
        
        initialMall = self.mallar[namn]
        for skala in skalor:
            skaladMall = cv2.resize(initialMall, (0,0), fX = skala, fY = skala)
            matchning = self.matchaMall(
                bild,
                skaladMall, 
                threshold
            )
            if np.shape(matchning)[1] >= 1:
                return matchning
        return matchning