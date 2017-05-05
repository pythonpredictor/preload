from sim_interface import SimModule
from events import EventType, Event, SimAlarm
import datetime
from device import ScreenState


class Preload(SimModule):
    def __init__(self, name, module_type, simulator, module_settings):
        super(Preload, self).__init__(name, module_type, simulator)
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
        self.interval_time = int(module_settings['interval_time'])
        self.depreciation = float(module_settings['depreciation'])
        self.intervals = 24 // self.interval_time
        self.time_expon = 1
        self.index = 0

        # new variables to keep track of app launched
        self.num_launched = 0
        self.prev_app_launched = None

        # new variables to record timeliness stats
        self.timeliness_min = 0
        self.timeliness_max = 0
        self.timeliness_sum = 0
        self.timeliness_count = 0

        # add an alarm
        self.alarm = None

    def build(self):
        self.simulator.subscribe(EventType.SCREEN, self.preload, lambda event: event.state == ScreenState.USER_PRESENT)
        self.simulator.subscribe(EventType.APP_ACTIVITY_USAGE, self.verify)
        for x in range(self.intervals):
            self.freq_count_list.append({})
        self.alarm = SimAlarm(self.simulator.get_current_time(), self.decrement,
                              datetime.timedelta(hours=self.interval_time))
        self.simulator.register_alarm(self.alarm)

    def finish(self):
        pass

    def decrement(self):
        for app in self.freq_count_list[self.index]:
            self.freq_count_list[self.index][app] *= self.depreciation

    # method to handle the event type being called
    def preload(self, event):
        # subscribe to an alarm at first preload
        # if self.alarm is None:
        #     self.alarm = SimAlarm(self.simulator.get_current_time(), self.decrement,
        #                           datetime.timedelta(hours=self.interval_time))
        #     self.simulator.register_alarm(self.alarm)

        # gets the current time and converts that into an index
        self.index = event.timestamp.hour // self.interval_time

        # check Screen On event and preloads the app that has the highest frequency of usage
        # before preloading the app check to see if it is morning, afternoon or night and then preload the
        # corresponding application for current time : simulator.get_current_time`
        # morn[freq, accessed_in_interval]
        # get hour of the time out of this current_time
        if len(self.freq_count_list[self.index]) > 0:
            highest_app = max(self.freq_count_list[self.index], key=self.freq_count_list[self.index].get)
            if self.freq_count_list[self.index][highest_app] > 20:
                self.total_predictions += 1
                self.prediction = (highest_app, event.timestamp)
                self.simulator.broadcast(Event(event.timestamp, EventType.PRELOAD_APP))

    # method to verify the preload result
    def verify(self, event):
        # if self.alarm is not None:
        #     self.alarm.cancel()

        # set time margin
        if self.prev_app_launched != event:
            self.num_launched += 1
        self.prev_app_launched = event
        margin = datetime.timedelta(seconds=5 * 60)
        app_id, timestamp = self.prediction
        if timestamp is not None and event.timestamp - timestamp < margin and event.app_id == app_id:
            self.correct += 1
            self.prediction = (None, None)
            time_diff = (event.timestamp - timestamp).total_seconds()
            if time_diff > self.timeliness_max:
                self.timeliness_max = time_diff
            elif time_diff < self.timeliness_min:
                self.timeliness_min = time_diff
            self.timeliness_sum += time_diff
            self.timeliness_count += 1

        # update current index to correct interval
        self.index = event.timestamp.hour // self.interval_time

        # update freq count dictionary
        if event.app_id in self.freq_count_list[self.index]:
            self.freq_count_list[self.index][event.app_id] += 1
        else:
            self.freq_count_list[self.index].update({event.app_id: 1})

    def print_stats(self, output):
        output.write("num correct: %s\n" % self.correct)

        output.write("total prediction: %s\n" % self.total_predictions)
        output.write("accuracy: %s\n" % (self.correct / self.total_predictions))
        output.write("converge: %s\n" % (self.correct / self.num_launched))
        output.write("timeliness: min -  %s\n" % self.timeliness_min)
        output.write("timeliness: max - %s\n" % self.timeliness_max)
        output.write("timeliness: average - %s\n" % (self.timeliness_sum * 1.0 / self.timeliness_count))
