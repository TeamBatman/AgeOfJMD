class Tuile(object):
	"""docstring for Tuile"""
	def __init__(self):

		#Type de la ressource sur la case
		self.type = 0

	def walkable(self):
		#Retource True si on peut marcher sur la tuile
		return self.type == 0