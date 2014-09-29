from Tuile import Tuile

class Carte(object):
	"""docstring for Carte"""
	def __init__(self, size):
		self.matrice = [[Tuile() for x in range(0,size)] for x in range(0,size)]

	def createRessources(self):
		for x in range(0,self.size):
			for y in range(0,self.size):
				self.matrice[x][y].type = random.randint(0,100)
				if x > 0 and y > 0 and self.matrice[x][y].type < 100:
					moyenne = (self.matrice[x][y].type + self.matrice[x-1][y] + self.matrice[x][y-1]) / 3
					self.matrice[x][y].type = moyenne


		for x in range(0,self.size):
			for y in range(0,self.size):
				if self.matrice[x][y].type < 55:
					self.matrice[x][y].type = 0

				elif self.matrice[x][y].type < 60:
					self.matrice[x][y].type = 1

				elif self.matrice[x][y].type < 72:
					self.matrice[x][y].type = 2

				elif self.matrice[x][y].type < 100:
					self.matrice[x][y].type = 3

				else:
					self.matrice[x][y].type = 4