from sim_interface import SimModule
from events import EventType
import csv


class ChromePreloader(SimModule):
    def __init__(self, name, module_type, simulator):
        self.name = name
        self.module_type = module_type
        self.simulator = simulator

    def build(self):
        self.simulator.subscribe(EventType.SCREEN, self.preloadNetflix)

    def finish(self):
        pass

    #method to handle the event type being called
    def preloadNetflix(self, event):
    	# This if statement should be modified
    	# so that it checks if the preload is successful
        self.simulator.broadcast("org.chromium.chrome.browser.document.ChromeLauncherActivity")

        # make an alarm that
        register_alarm(300000, verify())


        #
    	# if event.event_type == EventType.PSEUDO:
    	# 	print("Preload Successful")
    	# print('This is a test for preload predictor')
    def verify(self):
