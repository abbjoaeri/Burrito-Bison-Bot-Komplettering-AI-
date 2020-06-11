import cv2 
import numpy as np 

from bild import Bild
from kontroll import Kontroll
from spellogik import Spel

vision = Bild()
controller = Kontroll()

game = Spel(vision, controller)

game.main()