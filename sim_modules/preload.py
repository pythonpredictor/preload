from sim_interface import SimModule
from events import EventType

class Preload(SimModule):
    def __init__(self, name, module_type, simulator):
        self.name = name
        self.module_type = module_type
        self.simulator = simulator

    def build(self):
        self.simulator.subscribe(EventType.PRELOAD_APP, self.callback)

    def finish(self):
        pass

    def callback(self, event):
        print('This is a test for preload predictor')