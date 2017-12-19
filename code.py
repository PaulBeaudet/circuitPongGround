# PONG example Copyright 2017 ~ Paul Beaudet ~ License MIT
import board
import neopixel
import time

class Colors:
    def __init__(self):
        self.RED    = (0x10, 0, 0)
        self.YELLOW = (0x10, 0x10, 0)
        self.GREEN  = (0, 0x10, 0)
        self.AQUA   = (0, 0x10, 0x10)
        self.BLUE   = (0, 0, 0x10)
        self.PURPLE = (0x10, 0, 0x10)
        self.BLACK  = (0, 0, 0)

color = Colors();                                             # instantiate our color constants
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2) # setup and array of neopixels
pixels.fill(color.BLUE)                                       # Sets all pixels in array to x color
pixels.show()                                                 # instantiate recorded changes
time.sleep(9)
pixels.fill(color.AQUA)
pixels.show()
 