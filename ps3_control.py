#!/usr/bin/env python3
import evdev
import ev3dev.ev3 as ev3
from ev3dev.ev3 import Leds
import threading
from time import sleep

Leds.set_color(Leds.LEFT, Leds.RED)
Leds.set_color(Leds.RIGHT, Leds.RED)

SPEED_MAX = 100
STICK_MAX = 255
STICK_MIN = 0
POLARIZATION = -1

FOR_BACK_INT = 40
FOR_BACK_MIN = round(STICK_MAX / 2) - FOR_BACK_INT / 2
FOR_BACK_MAX = round(STICK_MAX / 2) + FOR_BACK_INT / 2

NON_STRAIGHT_INT = round(STICK_MAX / 4)
LEFT_ROT_MIN = STICK_MIN
LEFT_ROT_MAX = round(STICK_MAX / 4)
RIGHT_ROT_MIN = round(STICK_MAX / 4) * 3
RIGHT_ROT_MAX = STICK_MAX
LEFT_TURN_MIN = LEFT_ROT_MAX
LEFT_TURN_MAX = round(STICK_MAX / 2)
RIGHT_TURN_MIN = round(STICK_MAX / 2)
RIGHT_TURN_MAX = RIGHT_ROT_MIN

class MotorThread(threading.Thread):
    def __init__(self):
        self.left_motor  = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.running     = True
        self.speed_left  = 0
        self.speed_right = 0
        threading.Thread.__init__(self)

    def run(self):
        print ("Motor thread running!")
        while self.running:
            self.left_motor.run_direct(duty_cycle_sp=self.speed_left)
            self.right_motor.run_direct(duty_cycle_sp=self.speed_right)

    def stop(self):
        print ("Motor thread stopping!")
        self.running = False
        self.left_motor.stop()
        self.right_motor.stop()

    def set_speed(self, speed):
        self.speed_left  = speed[0]
        self.speed_right = speed[1]

def choose_move_action(x):
    if x > FOR_BACK_MIN and x < FOR_BACK_MAX:
        return "FOR_BACK"
    elif x > LEFT_ROT_MIN and x < LEFT_ROT_MAX:
        return "LEFT_ROTATE"
    elif x > RIGHT_ROT_MIN and x < RIGHT_ROT_MAX:
        return "RIGHT_ROTATE"
    elif x < (STICK_MAX / 2):
        return "LEFT_TURN"
    else:
        return "RIGHT_TURN"

def scale_to_engine_speed(move_action, x, y):
    if move_action == "FOR_BACK":
        return for_back_scaling(y)
    elif move_action == "LEFT_TURN":
        return left_turn_scaling(x)
    elif move_action == "RIGHT_TURN":
        return right_turn_scaling(x)
    elif move_action == "LEFT_ROTATE":
        return left_rotation_scaling(x)
    else:
        return right_rotation_scaling(x)

def for_back_scaling(y):
    sp = float(y) / STICK_MAX * 2 * SPEED_MAX - SPEED_MAX
    return (sp, sp)

def left_turn_scaling(x):
    return (scale_inc_x_inc_speed(x) * POLARIZATION, SPEED_MAX * POLARIZATION)

def right_turn_scaling(x):
    return (SPEED_MAX * POLARIZATION, scale_inc_x_dec_speed(x) * POLARIZATION)

def left_rotation_scaling(x):
    return (scale_inc_x_dec_speed(x), SPEED_MAX * POLARIZATION)

def right_rotation_scaling(x):
    return (SPEED_MAX * POLARIZATION, scale_inc_x_inc_speed(x))

def scale_inc_x_inc_speed(x):
    return (x % NON_STRAIGHT_INT)/NON_STRAIGHT_INT * SPEED_MAX

def scale_inc_x_dec_speed(x):
    return (NON_STRAIGHT_INT - (x % NON_STRAIGHT_INT))/NON_STRAIGHT_INT * SPEED_MAX

class StickEventHandler(threading.Thread):
    def __init__(self):
        self.running = True
        self.last_x  = 0
        self.last_y  = 0
        self.e       = threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        print ("StickEventHandler running!")
        while self.running:
            self.e.wait()
            speed = scale_to_engine_speed(choose_move_action(self.last_x),
                                          self.last_x,
                                          self.last_y)
            motor_thread.set_speed(speed)
            self.e.clear()

    def stop(self):
        print ("StickEventHandler thread stopping!")
        self.running = False
        self.e.set()

    def set_x(self, x):
        self.last_x = x
        self.e.set()

    def set_y(self, y):
        self.last_y = y
        self.e.set()

## =============== MAIN ================ ##
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    if device.name == 'PLAYSTATION(R)3 Controller':
        ps3dev = device.fn

gamepad = evdev.InputDevice(ps3dev)

motor_thread = MotorThread()
motor_thread.setDaemon(True)
motor_thread.start()

stick_event_handler = StickEventHandler()
stick_event_handler.start()

print ("And here we go... (start moving the right stick on the controller!).")
Leds.set_color(Leds.LEFT, Leds.ORANGE)
Leds.set_color(Leds.RIGHT, Leds.ORANGE)
for event in gamepad.read_loop():
    if event.type == 3:             #A stick is moved
        if event.code == 2:   #X axis on right stick
            stick_event_handler.set_x(event.value)
        elif event.code == 5: #Y axis on right stick
            stick_event_handler.set_y(event.value)
    elif event.type == 1 and event.code == 302 and event.value == 1:
        print ("X button is pressed. Stopping.")
        break

motor_thread.stop()
stick_event_handler.stop()
Leds.set_color(Leds.LEFT, Leds.GREEN)
Leds.set_color(Leds.RIGHT, Leds.GREEN)
