# PONG example Copyright 2017 ~ Paul Beaudet ~ License MIT
from digitalio import DigitalInOut, Direction, Pull # Methods in digitalio library that we would like (for buttons)
import board
import neopixel                                     # Library for multi colored leds
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

class PixelControl:
    def __init__(self):
        # self.RED    = (0x10, 0, 0)
        # self.YELLOW = (0x10, 0x10, 0)
        self.GREEN  = (0, 0x10, 0)
        # self.AQUA   = (0, 0x10, 0x10)
        self.BLUE   = (0, 0, 0x10)
        self.PURPLE = (0x10, 0, 0x10)
        self.BLACK  = (0, 0, 0)
        self.NUMBEROF = 10
        self.pixels = neopixel.NeoPixel(board.NEOPIXEL, self.NUMBEROF, brightness=1) # setup and array of neopixels
        # self.pixels = [self.GREEN for i in range(0, self.NUMBEROF)]
        self.pixels.fill(self.GREEN)
        self.pixels[2] = self.PURPLE
        self.pixels[7] = self.PURPLE
        self.pixels.show()                                # instantiate recorded changes

class Button():                                           # multiple unique button objects can be created with this one class
    def __init__(self, pin, bounceTime=0.01):             # __init__ Constructors are called when an instance of an object is created
        self.button = DigitalInOut(pin)                   # set pin of this unique button to the pin that is given on construction
        self.button.direction = Direction.INPUT           # direction of a button is always set to INPUT
        self.button.pull = Pull.DOWN                      # Use internal pull down resistor, opposed to using an external resistor
        self.changeStart = time.monotonic()               # give a time to start from to keep track of passing time
        self.bouncePeriod = False                         # bounces happen in a window of milliseconds when metal surfaces connect
        self.held = False                                 # remember if this button is being held or not
        self.lastGoodState = self.button.value            # remember first resting state
        self.bounceTime = bounceTime                      # 10 to 20 milliseconds is a good waiting range to ignore contact bounce
    def detect(self, onClick, onRelease=False, onHold=False): # poll this method to detect button changes without detecting bounce
        stateDurration = time.monotonic() - self.changeStart  # durration since last state change
        if self.bouncePeriod:                             # durring bounce period ( after a detected change )
            if stateDurration > self.bounceTime:          # ignoring bounces from being detected
                self.bouncePeriod = False                 # conclude bounce period
        else:                                             # where there is no concern of bounce
            currentState = self.button.value              # placehold current button state, may change if parsed multiple times
            if self.lastGoodState == currentState:        # given state persist / remains same as last good state
                if currentState and stateDurration > 0.4 and not self.held: # given button is being held DOWN
                    self.held = True                      # Remember this button is being held
                    if onHold:                            # if a hold callback was passed
                        onHold(0.1)                       # execute that callback {blink} with a 100 millisecond durration
            else:                                         # given state changed, button pressed or released
                self.changeStart = time.monotonic()       # note timestamp of change to measure how long to ignore potential bounce and detect hold
                self.bouncePeriod = True                  # this button is now in a period of detecting a bounce
                self.held = False                         # note that this button is no longer being held in its state, redundant for release
                self.lastGoodState = currentState         # remember last good state to compare in future
                if currentState:                          # shorthand for if pressed. pressed == True
                    onClick()                             # execute callback to call on a click event
                elif onRelease:                           # opposite of being pressed is being released
                    onRelease()                           # execute release callback

class Ball:
    def __init__(self, startSpeed):
        self.position = neo.NUMBEROF
        self.lastPos = 0
        self.offsetColor = neo.pixels[0]
        self.timer = JSTimer()
        self.frameDelay = startSpeed           # time to delay between frames, less is faster more is slow
        self.clockwise = True
        self.vollyWait = False                 # flag that prevents speed from being incremented and decremented at same time
    def roll(self):
        neo.pixels[self.lastPos] = self.offsetColor# turn off last led that was lit
        if self.clockwise:                     # given that ball is moving in clockwise direction
            self.position = self.position - 1  # clockwise is moving backwards through our led array
            self.offsetColor = neo.pixels[self.position]
            neo.pixels[self.position] = neo.BLUE   # set the led in our array
            neo.pixels.show()                      # this instantiates led to actually light up
            self.lastPos = self.position       # remember last led lit
            if not self.position:              # given that we have got to the begining of our array
                self.position = neo.NUMBEROF   # go back to end of array
        else:                                  # if direction has been set to counter-clockwise 
            self.position = self.position + 1  # set incremental counter-clockwise position
            if self.position == neo.NUMBEROF:  # given we exceeded bounds of our array
                self.position = 0
            self.offsetColor = neo.pixels[self.position]
            neo.pixels[self.position] = neo.BLUE
            neo.pixels.show()
            self.lastPos = self.position
        self.volly()                           # Check for volocity changes
        player1.defence(self.position)         # Check for misses
        # player2.defence(self.position)
        self.timer.setTimeout(self.roll, self.frameDelay) # set timeout to progress to next frame
    def deflect(self, vector):
        if vector is self.position:
            self.clockwise = not self.clockwise
            self.volly(True)
            return True
        return False
    def volly(self, volly=False):
        volocity = .298
        if self.frameDelay <= .05:
            volocity = .002
        elif self.frameDelay > .05 and self.frameDelay <= .15:
            volocity = .005
        elif self.frameDelay > .15 and self.frameDelay <= .7:
            volocity = .072
        if self.position is 7 or self.position is 2:
            if volly:                      # given this is a trigger for a volly
                self.frameDelay = self.frameDelay - volocity
                self.vollyWait = False     # disarm decrement of frame rate
            else:                          # in case there is no volly
                self.vollyWait = True      # wait flag gives opportunity for volly to happen before adding time
            return                         # it will trigger itself in final condition other wise
        if not volly and self.vollyWait:   # given wait flag was never disarmed by a volly
            if self.frameDelay > 1:
                volocity = 0
            self.frameDelay = self.frameDelay + volocity # slow down ball given a miss
            self.vollyWait = False         # only do this once it gets polled on every frame


class Player:      # tracks individual player state
    def __init__(self, ledNumber):
        self.score = 0
        self.relayAward = 1
        self.vollies = 0
        self.ledNumber = ledNumber
        self.waitingForVolly = False
    def penalty(self, penalty=0):
        self.vollies = 0
        if penalty:
            self.score = self.score - penalty
        self.relayAward = 1
    def printScore(self):
        print("player " + str(self.ledNumber) + " score:" + str(self.score))
    def offence(self, vollied):
        if not self.score:           # start a new game
            self.score = 10          # reset with full health
            self.relayMultiplier = 1 # and normal modifier
        if vollied:
            self.waitingForVolly = False
            self.vollies = self.vollies + 1
            if self.vollies is 2:
                self.relayAward = 2
            self.score = self.score + self.relayAward
        else:
            self.penalty(self.relayAward)
        self.printScore()
    def defence(self, ballPos):
        if ballPos is self.ledNumber:
            self.waitingForVolly = True      # wait to see if player deflects ball
        else:                                # important: only after our led
            if self.waitingForVolly:         # A volly will set this to false
                self.waitingForVolly = False # Lets only take a penalty once
                self.penalty(2)              # penalty for missing
                # self.printScore()

# High level business end of code starts here!
# instantiate hardware that is going to be used
player1 = Player(2)
# player2 = Player(7)
neo = PixelControl()             # instantiate added controls and constants for neopixels
buttonA = Button(board.BUTTON_A) # Creates a unique instance of Button class with pin of button A
buttonB = Button(board.BUTTON_B) # ButtonB is a unique object from buttonA
pongball = Ball(1)               # Create a pongball with x speed
pongball.roll()                  # get dat ball rolling!

def deflectA():
    player1.offence(pongball.deflect(2)) # Button A is near LED position 2

def deflectB():
    pongball.deflect(7) # Button B is near LED position 7

while True:
    buttonA.detect(deflectA) # Detect when button is pressed, pass "pointers" to methods to use AKA callbacks
    # methods/functions without parentheses reffer/point at the act. Using parentheses executes the action
    buttonB.detect(deflectB) # Also ignores button contact bounces that would produce false signals
    pongball.timer.checkTimeout()