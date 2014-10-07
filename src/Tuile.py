class Tuile(object):
	"""Representation d'une tuile (ou case) dans la matrice de la carte
	La tuile peut etre de type sol (0) ou ressource (tous les autres int)
	le parametre units est utilise par les ressources jusqu'a ce qu'elle s'epuise
	et devienne du sol standard"""

	def __init__(self):
		#Type de la ressource sur la case
		self.type = 0
		self.ressourceUnits = 0


	def walkable(self):
		#Retource True si on peut marcher sur la tuile
		return self.type == 0