import time
from collections import deque

class app:

	def __init__(self, name):
		self.name = name
		self.value = 0;
		# use a queue to store the time of app is loaded
		self.num_mor_usg = deque();
		self.num_non_usg = deque();
		self.num_ngt_usg = deque();
		

	def get_priority_value(self):
		return self.value

	def set_priority_value(self, val):
		return self.value = val

	def is_opened(self):
		# add time in queue structure
		if (time.strftime('%H') < 12):
			self.num_mor_usg.appendleft(time.time())
		else if (time.strftime('%H') > 19):
			self.num_ngt_usg.appendleft(time.time())
		else:
			self.num_non_usg.appendleft(time.time())

	def get_mor_usg(self):
		while (time.time() - self.num_mor_usg[-1] > 14 * 24 * 3600.0):
			self.num_mor_usg.pop();
		return len(self.num_mor_usg)

	def get_non_usg(self):
		while (time.time() - self.num_non_usg[-1] > 14 * 24 * 3600.0):
			self.num_non_usg.pop();
		return len(self.num_non_usg)

	def get_ngt_usg(self):
		while (time.time() - self.num_ngt_usg[-1] > 14 * 24 * 3600.0):
			self.num_ngt_usg.pop();
		return len(self.num_ngt_usg)