class Tuile(object):
	"""docstring for Tuile"""
	def __init__(self):
		self.type = 0

	def walkable(self):
		return self.type == 0