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
        self.clockwise = True
    def roll(self):
        pixels.fill(led.BLACK)                 # Sets all pixels in array to x color, removes last ball frame
        if self.clockwise:                     # given that ball is moving in clockwise direction
            self.position = self.position - 1  # clockwise is moving backwards through our led array
            print(self.position)
            pixels[self.position] = led.BLUE   # set the led in our array
            pixels.show()                      # this instantiates led to actually light up
            if not self.position:              # given that we have got to the begining of our array
                self.position = led.NUMBEROF   # go back to end of array
        else:                                  # if direction has been set to counter-clockwise 
            self.position = self.position + 1  # set incremental counter-clockwise position
            if self.position == led.NUMBEROF:  # given we exceeded bounds of our array
                self.position = 0
            pixels[self.position] = led.BLUE
            pixels.show()
        self.timer.setTimeout(self.roll, self.startSpeed) # set timeout to progress to next frame
    def deflect(self, vector):
        if vector is self.position:
            self.clockwise = not self.clockwise

pongball = Ball(1)
pongball.roll()
# button b is position 7
# button a is position 2
while True:
    pongball.timer.checkTimeout()