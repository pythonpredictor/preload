from sim_interface import SimModule
from events import EventType, AppLaunchEvent
import datetime


class Preload(SimModule):
    def __init__(self, name, module_type, simulator):
        self.name = name
        self.module_type = module_type
        self.simulator = simulator
        self.freq_count = {}
        # app, timestamp, tuple structure for prediction
        self.prediction = (None, None)
        self.total_time = 0
        self.correct = 0

    def build(self):
        self.simulator.subscribe(EventType.SCREEN, self.preload)
        self.simulator.subscribe(EventType.NOTIFICATION, self.verify)

    def finish(self):
        pass

    # method to handle the event type being called
    def preload(self, event):
        # check Screen On event
        if event.state.name == "ON" and len(self.freq_count) > 0:
            highest_app = max(self.freq_count, key=self.freq_count.get)
            self.prediction = (highest_app, event.timestamp)
            self.simulator.broadcast(AppLaunchEvent(event.timestamp, highest_app))

    # method to verify the preload result
    def verify(self, event):
        # update freq count dictionary
        if event.app_id in self.freq_count:
            self.freq_count.update({event.app_id: self.freq_count[event.app_id] + 1})
        else:
            self.freq_count.update({event.app_id: 1})
        # set time margin
        margin = datetime.timedelta(seconds=5 * 3600)
        app_id, timestamp = self.prediction
        if timestamp is not None and event.timestamp - timestamp < margin and event.app_id == app_id:
            self.correct += 1
        self.total_time += 1
        print("accuracy: " + str(float(self.correct) / self.total_time))
