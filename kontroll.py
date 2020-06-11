import time
from pynput.mouse import Button, Controller as MouseController

class Kontroll:
    def __init__(self):
        self.mouse = MouseController()

    def flyttaMus(self, x, y):
        def bestämMusPosition(x, y):
            self.mouse.position = (int(x), int(y))
        def mjukMusFörflyttning(frånX, frånY, tillX, tillY, hastighet = 0.2):
            steg = 40 # testa justera
            vila = hastighet // steg
            deltaX = (tillX - frånX) / steg
            deltaY = (tillY - frånY) / steg
            for varjeSteg in range(steg):
                nyttX = deltaX * (steg + 1) + frånX
                nyttY = deltaY * (steg + 1) + frånY
                nyMusPosition(nyttX, nyttY)
                time.sleep(vila)
        return mjukMusFörflyttning(
            self.mouse.position[0],
            self.mouse.position[1],
            x,
            y
        )

        def vänsterMusKlick(self):
            self.mouse.click(Button.left)

        def vänsterMusDrag(self, start, end):
            self.flyttaMus(*start)
            time.sleep(0.2)
            self.mouse.press(Button.left)
            time.sleep(0.2)
            self.flyttaMus(*end)
            time.sleep(0.2)
            self.mouse.release(Button.left)
            time.sleep(0.2)



