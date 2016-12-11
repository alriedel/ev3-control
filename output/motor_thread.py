import ev3dev.ev3 as ev3
import threading

class MotorThread(threading.Thread):
    """ Simple thread dealing with driving motors """
    def __init__(self, left_motor_out, right_motor_out):
        self.left_motor  = ev3.LargeMotor(left_motor_out)
        self.right_motor = ev3.LargeMotor(right_motor_out)
        self.running     = True
        self.speed_left  = 0
        self.speed_right = 0
        self.e           = threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        while self.running:
            self.e.wait()
            self.left_motor.run_direct(duty_cycle_sp=self.speed_left)
            self.right_motor.run_direct(duty_cycle_sp=self.speed_right)
            self.e.clear()

    def stop(self):
        print ("Motor thread stopping!")
        self.running = False
        self.left_motor.stop()
        self.right_motor.stop()
        self.e.set()

    def set_speed(self, speed):
        self.speed_left  = speed[0]
        self.speed_right = speed[1]
        self.e.set()
