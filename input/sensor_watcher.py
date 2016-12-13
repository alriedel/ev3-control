import threading
from time import sleep

class SensorWatcher(threading.Thread):
    def __init__(self, event_receiver, watcher_fun, watch_frequency = 0.2):
        self.event_receiver  = event_receiver
        self.watch_frequency = watch_frequency
        self.running         = True
        self.watcher_fun     = watcher_fun
        threading.Thread.__init__(self)

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            sleep(self.watch_frequency)
            self.watcher_fun(self)
