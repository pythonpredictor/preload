class applist:

	def __init__(self):
		self.list = {}

	def load_app(self, name):
		if (name not in self.list):
			self.list[name] = app(name)	
		self.list[name].is_opened()

	def get_priority_value(self, name):
		return self.list[name].get_priority_value()

	def set_priority_value(self, name, val):
		return self.list[name].set_priority_value(val)
