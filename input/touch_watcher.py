from ev3dev.ev3 import TouchSensor
from sensor_watcher import SensorWatcher

class TouchWatcher(SensorWatcher):
    def __init__(self, event_receiver, watch_frequency = 0.1):
        self.ts         = TouchSensor()
        self.last_value = 0
        SensorWatcher.__init__(self, event_receiver, TouchWatcher.watcher_fun, watch_frequency)

    def watcher_fun(self):
        self.current_value = self.ts.value()
        if self.last_value != self.current_value:
            if self.last_value == 0:
                self.event_receiver.button_pressed()
            else:
                self.event_receiver.button_released()
            self.last_value = self.current_value
