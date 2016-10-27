import heapq
import time

# applist class store all apps and their priority value.
class applist:
    def __init__(self):
        # dict contains all apps
        self.list = {}
        # use three priority queues to put app with priority value
        self.pq = []
        self.mor_pq = []
        self.non_pq = []
        self.ngt_pq = []

    def load_app(self, name):
        # create app if it doesn't exist
        if (name not in self.list):
            self.list[name] = app(name)
        # call is_open method push time point
        self.list[name].is_opened()

    def get_app(self, num):
    	return heapq.nlargest(num, self.pq)

    # get first n of apps in list
    def get_mor_app(self, num):
        return heapq.nlargest(num, self.mor_pq)

    # get first n of apps in list
    def get_non_app(self, num):
        return heapq.nlargest(num, self.non_pq)

    # get first n of apps in list
    def get_ngt_app(self, num):
        return heapq.nlargest(num, self.ngt_pq)

    def cal_val(self):
    	for app in self.list:
    		heapq.heappush(self.pq, (app.mor_val + app.non_val + app.ngt_val, app))

    def cal_mor_val(self):
        # initialize list to empty each time
        self.mor_pq = []
        for app in self.list:
            # flip value for min heap, keep app most frequent used
            # at root
            app.mor_val = cal_exp(app.get_mor_usg)
            heapq.heappush(self.mor_pq, (app.mor_val, app))

    def cal_non_val(self):
        # initialize list to empty each time
        self.non_pq = []
        for app in self.list:
            # flip value for min heap, keep app most frequent used
            # at root
            app.non_val = cal_exp(app.get_non_usg)
            heapq.heappush(self.non_pq, (app.non_val, app))

    def cal_ngt_val(self):
        # initialize list to empty each time
        self.ngt_pq = []
        for app in self.list:
            # flip value for min heap, keep app most frequent used
            # at root
            app.ngt_val = cal_exp(app.get_ngt_usg)
            heapq.heappush(self.ngt_pq, (app.ngt_val, app))

    # exponentially decrease the priority value
    def cal_exp(self, dq):
    	val = 0;
    	for tp in dp:
    		val += math.exp((tp - time.time()) / (14 * 24 * 2400))
    	# increase all value by multiply 10
    	val *= 10
    	return val
