# PONG example Copyright 2017 ~ Paul Beaudet ~ License MIT
import board
import neopixel
import time

class LED:
    def __init__(self):
        self.RED    = (0x10, 0, 0)
        self.YELLOW = (0x10, 0x10, 0)
        self.GREEN  = (0, 0x10, 0)
        self.AQUA   = (0, 0x10, 0x10)
        self.BLUE   = (0, 0, 0x10)
        self.PURPLE = (0x10, 0, 0x10)
        self.BLACK  = (0, 0, 0)
        self.NUMBEROF = 10

led = LED();                                                            # instantiate our color constants
pixels = neopixel.NeoPixel(board.NEOPIXEL, led.NUMBEROF, brightness=.2) # setup and array of neopixels
pixels.fill(led.BLACK)                                                  # Sets all pixels in array to x color
pixels.show()                                                           # instantiate recorded changes

class Ball:
    def __init__(self):
        self.position = led.NUMBEROF
    def roll(self, delay):
        self.position = self.position - 1
        pixels.fill(led.BLACK)                                         # Sets all pixels in array to x color
        pixels[self.position] = led.BLUE
        pixels.show()
        time.sleep(delay)
        if not self.position:
           self.position = led.NUMBEROF

pongball = Ball()
while True:
    pongball.roll(.001)