from output.motor_control import MotorControl

import threading            

class SensorEventHandler(threading.Thread):
    """ Simple FIFO Event Processor """
    def __init__(self, motor_thread):
        self.e        = threading.Event()
        self.active_q = 0
        self.event_q  = ([], [])
        self.motor_thread  = motor_thread
        self.is_running    = False
        threading.Thread.__init__(self)

    def angle_changed(self, new_angle):
        self.event_q[self.active_q].append(("angle_changed", new_angle))        
        self.e.set()

    def button_pressed(self):
        self.event_q[self.active_q].append(("button_pressed", ))
        self.e.set()        

    def button_released(self):
        self.event_q[self.active_q].append(("button_released", ))
        self.e.set()

    def handle_button_release(self):
        if self.is_running:
            motor_thread.set_speed(0, 0)
            self.is_running = False
        else:
            motor_thread.set_speed(-50, -50)
            self.is_running = True

    def handle_angle_change(angle):
        if self.is_running:
            if self.
            
    def run(self):
        while True:
            self.e.wait()
            self.passive_q = self.active_q
            self.active_q  = (self.active_q + 1) % 2
            for event in self.event_q[self.passive_q]:
                print ("Processing", event)
                if event[0] == "button_released":
                    handle_button_release(self)
                elif event[0] == "angle_changed":
                    handle_angle_change(event[1])
            list.clear(self.event_q[self.passive_q])
                

def main():
    motor_control = MotorControl('outB', 'outC')
    motor_control.start()
    sensor_event_handler = SensorEventHandler(motor_thread)
    sensor_event_handler.start()
    gyro_watcher = GyroWatcher(sensor_event_handler)
    gyro_watcher.start()
    touch_watcher = TouchWatcher(sensor_event_handler)
    touch_watcher.start()
    print ("Started.")

if __name__ == "__main__":
    main()
