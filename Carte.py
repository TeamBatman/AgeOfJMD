from Tuile import Tuile
import random

class Carte(object):
	"""Modelisation de la carte de jeu"""
	def __init__(self, size):

		#Initialisation de la matrice de tuile
		self.size = size
		self.matrice = [[Tuile() for x in range(0,self.size)] for x in range(0,self.size)]
		self.createRessources()

	#Creation des differentes ressources selon des parametres au hasard
	def createRessources(self):

		#Creation de la ressource en grappe
		for x in range(0,self.size):
			for y in range(0,self.size):
				self.matrice[x][y].type = random.randint(0,100)
				if x > 0 and y > 0 and self.matrice[x][y].type < 100:
					moyenne = (self.matrice[x][y].type + self.matrice[x-1][y].type + self.matrice[x][y-1].type) / 3
					self.matrice[x][y].type = moyenne

		#Distribution de la ressource selon le pourcentage
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

def test():
	carte = Carte(100)

if __name__ == '__main__':
	test()