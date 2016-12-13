from ev3dev.ev3 import GyroSensor
from sensor_watcher import SensorWatcher

class CalibrationError(Exception):
    def __init__(self, msg, value = None):
        self.msg   = msg
        self.value = value

class GyroWatcher(SensorWatcher):
    def __init__(self, event_receiver, watch_frequency = 0.2):
        self.gs         = GyroSensor()
        self.last_angle = 0
        self.fix_drift()
        SensorWatcher.__init__(self, event_receiver, GyroWatcher.watcher_fun, watch_frequency)
    
    def fix_drift(self):
        self.gs.mode = 'GYRO-CAL'
        sleep(1)
        self.gs.mode = 'GYRO-ANG'
        self.measures = 4
        for i in range(self.measures):
            sleep(0.5)
            if self.gs.value() != 0:
                raise CalibrationError("Angle is drifting ", self.gs.value())

    def watcher_fun(self):
        self.current_angle = self.gs.value()
        if self.current_angle != self.last_angle:
            self.event_receiver.angle_changed(self.current_angle)
            self.last_angle = self.current_angle
