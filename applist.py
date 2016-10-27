import heapq
import time
import csv

# applist class store all apps and their priority value.
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
            applist = get_app(num)
            for app in applist:
                writer.writerow((app, app.mor_val + app.non_val + app.ngt_val, app.mor_val, app.non_val, app.ngt_val))
        finally:
            f.close()

    def get_result(self, num):
        get_result(self, 'default.csv', num)

    def load_app(self, name):
        # create app if it doesn't exist
        if (name not in self.list):
            self.list[name] = app(name)
        # call is_open method push time point
        self.list[name].is_opened()

    def get_app(self, num):
        cal_val()
    	return heapq.nlargest(num, self.pq)

    # calculate priority value
    def cal_val(self):
    	for app in self.list:
            app.mor_val = cal_exp(num_mor_usg)
            app.non_val = cal_exp(num_non_usg)
            app.ngt_val = cal_exp(num_ngt_usg)
            # push each app into heap according to value
    		heapq.heappush(self.pq, (app.mor_val + app.non_val + app.ngt_val, app))

    # exponentially decrease the priority value
    def cal_exp(self, dq):
    	val = 0;
    	for tp in dp:
    		val += math.exp((tp - time.time()) / (14 * 24 * 2400))
    	# increase all value by multiply 10
    	val *= 10
    	return val
