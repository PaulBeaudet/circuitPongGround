# PONG example Copyright 2017 ~ Paul Beaudet ~ License MIT
import board
import neopixel
import time

class JSTimer: # TODO modify in such a way that only one check is needed for multiple timeouts
    def __init__(self):
        self.pending = False
    def setTimeout(self, callback, lapse): # pass function without() and lapse in seconds
        self.timeoutFunc = callback        # Set a new callback
        self.wait = lapse                  # set a new time to wait for
        self.pending = True
        self.startTime = time.monotonic()  # Get start with a base time for hello
    def checkTimeout(self):
        if self.pending:
            current = time.monotonic()
            elapsed = current - self.startTime
            if elapsed > self.wait:
                self.pending = False
                self.timeoutFunc()

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
    def __init__(self, startSpeed):
        self.position = led.NUMBEROF
        self.timer = JSTimer()
        self.startSpeed = startSpeed
    def roll(self):
        self.position = self.position - 1
        pixels.fill(led.BLACK)                                         # Sets all pixels in array to x color
        pixels[self.position] = led.BLUE
        pixels.show()
        if not self.position:
           self.position = led.NUMBEROF
        self.timer.setTimeout(self.roll, self.startSpeed)

pongball = Ball(.01)
pongball.roll()
while True:
    pongball.timer.checkTimeout()