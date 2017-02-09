from app import app
from math import exp
import heapq
import time
import csv

# list class store all apps and their priority value.
class applist:
    def __init__(self):
        # dict contains all apps
        self.list = {}
        # use three priority queues to put app with priority value
        self.pq = []

    # writes result to csv file
    def get_result(self, path, num):
        f = open(path, 'wt')
        try:
            writer = csv.writer(f)
            writer.writerow(('app', 'overall', 'mor', 'non', 'ngt'));
            list = self.get_app(num)
            for app in self.list:
                writer.writerow((app, self.list[app].mor_val + self.list[app].non_val +
                    self.list[app].ngt_val, self.list[app].mor_val, self.list[app].non_val,
                    self.list[app].ngt_val))
        finally:
            f.close()

    def load_app(self, name):
        # create app if it doesn't exist
        if name not in self.list:
            self.list[name] = app(name)
        # call is_open method push time point
        self.list[name].is_opened()

    def get_app(self, num):
        self.cal_val()
        return heapq.nlargest(num, self.pq)

    # calculate priority value
    def cal_val(self):
        self.pq = []
        for app in self.list:
            self.list[app].mor_val = self.cal_exp(self.list[app].num_mor_usg)
            self.list[app].non_val = self.cal_exp(self.list[app].num_non_usg)
            self.list[app].ngt_val = self.cal_exp(self.list[app].num_ngt_usg)
            # push each app into heap according to value
            heapq.heappush(self.pq, (self.list[app].mor_val + self.list[app].non_val + self.list[app].ngt_val, app))

    # exponentially decrease the priority value
    def cal_exp(self, dq):
        val = 0;
        for tp in dq:
            val += exp((tp - time.time()) / (14 * 24 * 2400))
        # increase all value by multiply 10
        val *= 10
        return val
