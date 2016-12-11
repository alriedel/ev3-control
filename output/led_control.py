from ev3dev.ev3 import Leds
import threading
from time import sleep

_MIN_BLINK_PERIOD_ = 0.7

class LedControl(threading.Thread):
    
    def __init__(self, init_left_color = Leds.GREEN, init_right_color = Leds.GREEN):
        self.init_left_color = init_left_color
        self.init_right_color = init_right_color
        self.last_left_color  = None
        self.last_right_color = None
        self.should_blink = False
        self.running      = True
        self.blink_period = _MIN_BLINK_PERIOD_
        self.set_colors(init_left_color, init_right_color)
        threading.Thread.__init__(self)

    def stop(self):
        self.running = False
        
    def blink(self, color, period_s = 0.7):
        self.set_color(color)
        self.blink_period = max(period_s, _MIN_BLINK_PERIOD_) 
        self.should_blink = True

    def stop_blinking(self):
        self.should_blink = False
        self.refresh_colors()

    def set_color(self, color):
        self.set_colors(color, color)

    def refresh_colors(self):
        self.set_colors(self.left_color, self.right_color)
        
    def set_colors(self, left_color, right_color):
        self.left_color = left_color
        self.right_color = right_color
        self.last_left_color = None
        self.last_right_color = None

    def run(self):
        while self.running:
            if (self.last_left_color != self.left_color or
                self.last_right_color != self.right_color):
                Leds.set_color(Leds.LEFT, self.left_color)
                Leds.set_color(Leds.RIGHT, self.right_color)
                self.last_left_color = self.left_color
                self.last_right_color = self.right_color
            if self.should_blink:
                Leds.set(Leds.LEFT, brightness=0)
                Leds.set(Leds.RIGHT, brightness=0)
                # it does not work to set brightness to 1, so workaround
                # is to set the color instead
                self.refresh_colors()
            sleep(self.blink_period)
        # keep the initial colors before existing
        Leds.set_color(Leds.LEFT, self.init_left_color)
        Leds.set_color(Leds.RIGHT, self.init_right_color)

