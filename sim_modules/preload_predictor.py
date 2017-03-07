from sim_interface import SimModule
from events import EventType, Event
import device
import datetime
from math import exp


class Preload(SimModule):
    def __init__(self, name, module_type, simulator, module_settings):
        self.name = name
        self.module_type = module_type
        self.simulator = simulator
        self.freq_count_list = []
        # app, timestamp, tuple structure for prediction
        self.prediction = (None, None)
        self.total_predictions = 0
        self.correct = 0

        # new variables, thinking about making it similar to freq_count
        # list of dictionaries [{morn_freq}, {aftn_freq}, {ngt_freq}]
        # freq_dict_index(time) -> the interval index
        self.interval_time = int(module_settings["interval_time"])
        self.intervals = 24 // self.interval_time
        self.time_expon = 1
        self.index = 0

    def build(self):
        self.simulator.subscribe(EventType.SCREEN, self.preload, lambda event: return event.state == ScreenState.USER_PRESENT)
        self.simulator.subscribe(EventType.APP_ACTIVITY_USAGE, self.verify)
        for x in range(self.intervals):
            self.freq_count_list.append({})

    def finish(self):
        print("accuracy: " + str(self.correct / self.total_predictions))

    # method to handle the event type being called
    def preload(self, event):
        # gets the current time and converts that into an index
        current_hour = event.timestamp.hour
        self.index = current_hour // self.interval_time

        # appends the corresponding number of index to the freq_count_list
        for app in self.freq_count_list[self.index]:
            self.freq_count_list[self.index].update({app: self.freq_count_list[self.index][app] * 0.5})

        # check Screen On event and preloads the app that has the highest frequency of usage
        # before preloading the app check to see if it is morning, afternoon or night and then preload the
        # corresponding application for current time : simulator.get_current_time`
        # morn[freq, accessed_in_interval]
        # get hour of the time out of this current_time
        if len(self.freq_count_list[self.index]) > 0:
            highest_app = max(self.freq_count_list[self.index], key=self.freq_count_list[self.index].get)
            self.total_predictions += 1
            self.prediction = (highest_app, event.timestamp)
            self.simulator.broadcast(Event(event.timestamp, EventType.PRELOAD_APP))

    # method to verify the preload result
    def verify(self, event):
        # set time margin
        margin = datetime.timedelta(seconds=5 * 60)
        app_id, timestamp = self.prediction
        if timestamp is not None and event.timestamp - timestamp < margin and event.app_id == app_id:
            self.correct += 1
            self.prediction = (None, None)

        # update freq count dictionary
        if event.app_id in self.freq_count_list[self.index] and timestamp is not None:
            self.freq_count_list[self.index].update({event.app_id: self.freq_count_list[self.index][event.app_id] + 1})

        else:
            self.freq_count_list[self.index].update({event.app_id: 1})

        # for each app event in the frequency table, need to add a time_expon factor where it is decremented
        # at an logorithmic rate when verify is called every app in the corresponding freq_count table will
        # be logged except for the app that is called
