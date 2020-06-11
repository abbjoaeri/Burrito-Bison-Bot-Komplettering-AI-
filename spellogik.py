import numpy as np 
import time

class Spel:

    def __init__(self, bild, kontroll):
        self.bild = bild
        self.kontroll = kontroll
        self.state = 'not started'

    # def kanSeObjekt(self, mall, threshold = 0.9):
    #     matchning = self.vision.hittaMall(mall, threshold = 0.9)
    #     return np.shape(matchning)[1] >= 1
    
    # def klickaObjekt(self, mall, offset = (0,0)):
    #     matchning = self.vision.hittaMall(mall)

    #     x = matchning[1][0] + offset[0]
    #     x = matchning[0][0] + offset[1]
    #     self.kontroll.flyttaMus(x, y)
    #     self.kontroll.vänsterMusKlick()
    #     time.sleep(0.5)
    
    def rundaStartar(self, spelare):
        matchning = self.kanSeObjekt('%s-health-bar' % spelare)
        return np.shape(matchning)[1] >= 1

    def rundaAvslutad(self):
        matchning = self.bild.hittaMall('tap-to-continue')
        return np.shape(matchning)[1] >= 1

    def klickaVidare(self):
        matchning = self.bild.hittaMall('tap-to-continue')
        x = matchning[1][0]
        y = matchning[0][0]
        self.kontroll.flyttaMus(x+50, y+30)
        self.kontroll.vänsterMusKlick()
        time.sleep(0.5)

    def kanStartaRunda(self):
        matchning = self.hittaMall('next-button')
        return np.shape(matchning)[1] >= 1

    def startaRunda(self):
        matchning = self.bild.hittaMall('next-button')
        x = matchning[1][0]
        y = matchning[0][0]
        self.kontroll.flyttaMus(x+100, y+30)
        self.kontroll.vänsterMusKlick()
        time.sleep(0.5)
    
    def användFullRaket(self):
        matchning = self.bild.hittaMall('full-rocket')
        x = matchning[1][0]
        y = matchning[0][0]
        self.kontroll.flyttaMus(x, y)
        self.kontroll.vänsterMusKlick()
        time.sleep(0.5)

    def harFullRaket(self):
        matchning = self.bild.hittaMall('full-rocket', threshold = 0.9)
        return np.shape(matchning)[1] >= 1
    
    # def hittaPinata(self):
    #     matchning = self.bild.hittaMall('filled-with-goodies', threshold = 0.9)
    #     return np.shape(matchning)[1] >= 1
    
    def klickaAvbryt(self):
        matchning = self.bild.hittaMall('cancel-button')
        x = matchning[1][0]
        y = matchning[0][0]
        self.kontroll.flyttaMus(x, y)
        self.kontroll.vänsterMusKlick()
        time.sleep(0.5)

    def lanseraSpelare(self):
        skala = [1.2, 1.1, 1.05, 1.04, 1.03, 1.02, 1.01, 1.0, 0.99, 0.98, 0.97, 0.96, 0.95]
        matchning = self.bild.skaladHittaMallar('left-goalpost', threshold = 0.75, skala = skala)
        x = matchning[1][0]
        y = matchning[0][0]

        self.kontroll.vänsterMusDrag(
            (x, y),
            (x-200, y+10)
        )
        time.sleep(0.5)
    
    def main(self):
        while True:
            self.bild.uppdateraBildruta()
            if self.state == 'inte startad' and self.rundaStartar('bison'):
                self.log('Runda måste startas, laddar bison')
                self.lanseraSpelare()
                self.state = 'startad'

            if self.state == 'inte startad' and self.rundaStartar('pineapple'):
                self.log('Runda måste startas, laddar pineapple')
                try:
                    self.lanseraSpelare()
                    self.state = 'startad'
                except: 
                    self.log('Hittade inte pineapple.')            

            elif self.state == 'startad' and self.hittaPinata():
                self.log('Hittade en pinata, försöker skippa')
                self.klickaAvbryt()

            elif self.state == 'startad' and self.rundaAvslutad():
                self.log('Runda avslutad, klickar för att fortsätta')
                self.klickaVidare()
                self.state = 'uppdrag avslutat'
            
            elif self.state == 'startad' and self.harFullRaket():
                self.log('Runda håller på, har full raket, försöker använda den')
                self.användFullRaket()
            
            elif self.state == 'uppdrag avslutat' and self.kanStartaRunda():
                self.log('Uppdrag avslutat, försöker starta en ny runda')
                self.startaRunda()
                self.state = 'inte startad'

            else:
                self.log('Gör ingenting')
                time.sleep(0.5)
    
    def log(self, text):
        print('[%s] %s' % (time.strftime('%H:%M:%S'), text))