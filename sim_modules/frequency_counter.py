from sim_interface import SimModule
from events import EventType, Event, ScreenEvent


class FrequencyCounter(SimModule):
    def __init__(self, name, module_type, simulator, module_settings):
        super(FrequencyCounter, self).__init__(name, module_type, simulator)
        self.name = name
        self.module_type = module_type
        self.simulator = simulator
        self.event_counter = {}

    def build(self):
        for i, event_type in enumerate(EventType):
            self.simulator.subscribe(event_type, self.freq_count)

    def finish(self):
        for key, val in self.event_counter.items():
            print(str(key) + ": " + str(val))

    # method to handle the event type being called
    def freq_count(self, event):
        if event in self.event_counter:
            self.event_counter.update({event: self.event_counter[event] + 1})
        else:
            self.event_counter.update({event: 1})

    # method to verify the preload result
    def verify(self, event):
        pass

    def print_stats(self, output):
        pass
