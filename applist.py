import heapq

# applist class store all apps and their priority value.
class applist:
    def __init__(self):
        # dict contains all apps
        self.list = {}
        # use three priority queues to put app with priority value
        self.mor_pq = []
        self.non_pq = []
        self.ngt_pq = []

	def load_app(self, name):
        # create app if it doesn't exist
        if (name not in self.list):
            self.list[name] = app(name)
        # call is_open method push time point
        self.list[name].is_opened()

    # get first n of apps in list
    def get_mor_app(self, num):
        return heapq.nsmallest(num, self.mor_pq)

    # get first n of apps in list
    def get_non_app(self, num):
        return heapq.nsmallest(num, self.non_pq)

    # get first n of apps in list
    def get_ngt_app(self, num):
        return heapq.nsmallest(num, self.ngt_pq)

    def cal_mor_val(self):
        # initialize list to empty each time
        self.mor_pq = []
        for app in self.list:
            # flip value for min heap, keep app most frequent used
            # at root
            heapq.heappush(self.mor_pq, (-len(app.num_mor_usg), app))

    def cal_non_val(self):
        # initialize list to empty each time
        self.non_pq = []
        for app in self.list:
            # flip value for min heap, keep app most frequent used
            # at root
            heapq.heappush(self.non_pq, (-len(app.num_non_usg), app))

    def cal_ngt_val(self):
        # initialize list to empty each time
        self.ngt_pq = []
        for app in self.list:
            # flip value for min heap, keep app most frequent used
            # at root
            heapq.heappush(self.ngt_pq, (-len(app.num_ngt_usg), app))