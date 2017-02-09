import time
from collections import deque

# app class represents an App in mobile. it includes three deques to store
# time of app is loaded.

class app:
	def __init__(self, name):
		self.name = name
		# record value for each state
		self.mor_val = 0;
		self.non_val = 0;
		self.ngt_val = 0;
		# use a queue to store the time of app is loaded
		self.num_mor_usg = deque()
		self.num_non_usg = deque()
		self.num_ngt_usg = deque()

	def is_opened(self):
		# add time in queue structure
		if (time.strftime('%H') < 12):
			self.num_mor_usg.appendleft(time.time())
		elif (time.strftime('%H') > 19):
			self.num_ngt_usg.appendleft(time.time())
		else:
			self.num_non_usg.appendleft(time.time())

	def get_mor_usg(self):
        # pop out time point passes 2 weeks interval
		while (time.time() - self.num_mor_usg[-1] > 14 * 24 * 3600.0):
			self.num_mor_usg.pop()
		return self.num_mor_usg

	def get_non_usg(self):
        # pop out time point passes 2 weeks interval
		while (time.time() - self.num_non_usg[-1] > 14 * 24 * 3600.0):
			self.num_non_usg.pop()
		return self.num_non_usg

	def get_ngt_usg(self):
        # pop out time point passes 2 weeks interval
		while (time.time() - self.num_ngt_usg[-1] > 14 * 24 * 3600.0):
			self.num_ngt_usg.pop();
		return self.num_ngt_usg
