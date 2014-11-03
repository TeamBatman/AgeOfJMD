from Tuile import Tuile
import random

class Carte(object):

    """VARIABLE GLOBALE"""

    GAZON    = 0
    FORET    = 1
    MINERAI  = 2
    CHARBON  = 3
    EAU      = 4


    """Modelisation de la carte de jeu"""

    def __init__(self, size):

        self.size = size
        #Initialisation de la matrice de tuile
        self.matrice = [[Tuile() for x in range(0,self.size)] for x in range(0, self.size)]
        #Passer le seed pour avoir la meme map random
        #TODO Aller chercher le seed commun
        random.seed(2)
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
                if self.matrice[x][y].type < 62:
                    self.matrice[x][y].type = Carte.GAZON

                elif self.matrice[x][y].type < 67:
                    self.matrice[x][y].type = Carte.FORET
                    self.matrice[x][y].isWalkable = False

                elif self.matrice[x][y].type < 72:
                    self.matrice[x][y].type = Carte.MINERAI
                    self.matrice[x][y].isWalkable = False

                elif self.matrice[x][y].type < 100:
                    self.matrice[x][y].type = Carte.CHARBON
                    self.matrice[x][y].isWalkable = False

                else:
                    self.matrice[x][y].type = Carte.EAU
                    self.matrice[x][y].isWalkable = False


def test():
    carte = Carte(100)

if __name__ == '__main__':
    test()
