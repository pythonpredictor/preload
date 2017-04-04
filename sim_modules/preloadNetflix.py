from sim_interface import SimModule
from events import EventType

class PreloadNetflix(SimModule):
    def __init__(self, name, module_type, simulator):
        self.name = name
        self.module_type = module_type
        self.simulator = simulator
        success_preloads = 0
        total_preloads = 0

    # @preloadNetflix: the callback function, 
    # preloads Netflix after observing a screenOn event
    def build(self):
        self.simulator.subscribe(EventType.SCREEN, self.callback)
    
        # Use alarm to set 5min delay check
        # alarm = None;

    # TO-DO
    def finish(self):
        pass

    # probably should be named differently for each SimModule
    def callback(self, event):
        # This if statement should be modified
        # so that it checks if the preload is successful
        if event.event_type == EventType.SCREEN:
            # screen is turned on
            # total_preloads += 1
            if (event.SCREEN.state != 'on'):
                # success_preloads += 1
                print("Proloading Netflix")
            else: 
                print("Screen not on")
        