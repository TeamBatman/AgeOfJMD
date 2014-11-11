import Batiments
from Units import Paysan


class Joueur:
    """docstring for Joueur"""
    def __init__(self, civilisation, model):
        self.model = model
        self.civilisation = civilisation    # Couleur de la civilisation
        self.base = None            # TODO Base Vivante ne pourrait pas juste être remplacer par un if self.base: ?
        self.baseVivante = False # À modifier, doit être true quand on commence une vraie partie
        self.ressources = {'bois': 0, 'minerai': 0, 'charbon': 0}
        self.morale = 0
        self.nbNourriture = 0

        self.units = {}
        self.enRessource = []
        self.buildings = {}


    def update(self):
        """ Permet de lancer les commande updates importantes
        """
        self.updateUnits()
        self.updatePaysans()
        self.updateBuildings()

    def annihilate(self):
        """ Annihilation de la civilisation 
            Donc suppression:
                des buildings
                des unités
        """
        self.units = {}
        self.buildings = {}




    ### UNITS ###
    def createUnit(self, uId, x, y, civilisation):
        """ Crée et ajoute une nouvelle unité à la liste des unités
        :param uId: ID que l'on souhaite attribuer à l'unité
        :param x: position x de l'unité
        :param y: position y de l'unité
        """
        self.units[uId] = Paysan(uId, x, y, self.model, civilisation)

    def killUnit(self, uId):
        """ Permet de tuer une unité selon son Id 
        (donc retirer de la liste des unités)
        """
        try:
            self.units.pop(uId)
        except KeyError:  # L'unité n'existe déjà plus
            pass

    def updateUnits(self):
        """ Met à jour chacune des unités
            Et supprime les unités mortes de la liste
        """
        [u.update(self.model) for u in self.units.values()]

    def updatePaysans(self):
        """ Met à jours les unités de types paysan 
        """  # TODO mettre dans update des paysans
        for paysan in self.enRessource:
            if paysan.mode == 1:
                if not paysan.enDeplacement:
                    paysan.chercherRessources()
            else:
                self.enRessource.remove(paysan)

    ### BUILDINGS ###
    def createBuilding(self, bId, posX, posY, btype):  # TODO CLEAN UP
        """ Crée et ajoute un nouveaue bâtiment à la liste des bâtiments
        :param bId: ID que l'on souhaite attribuer au bâtiment
        :param posX: position X du bâtiment
        :param posY: position Y du bâtiment
        :param btype: Type de bâtiment à construire
        """
        posX, posY = self.model.trouverCaseMatrice(posX, posY)
        if not self.model.carte.matrice[posX][posY].isWalkable:
            print("not walkable")
        else:
            if not self.model.carte.matrice[posX + 1][posY].isWalkable:
                print("not walkable")
            else:
                if not self.model.carte.matrice[posX][posY + 1].isWalkable:
                    print("not walkable")
                else:
                    if not self.model.carte.matrice[posX + 1][posY + 1].isWalkable:
                        print("not walkable")
                    else:
                        print(posX, posY)
                        print(posX, posY)
                        if btype == Batiments.Batiment.FERME:
                            newID = Batiments.Batiment.generateId(self.civilisation)
                            createdBuild = Batiments.Ferme(self, newID, posX, posY)
                        elif btype == Batiments.Batiment.BARAQUE:
                            pass
                        elif btype == Batiments.Batiment.HOPITAL:
                            pass
                        elif btype == Batiments.Batiment.BASE:
                            if not self.baseVivante:
                                newID = Batiments.Batiment.generateId(self.civilisation)
                                createdBuild = Batiments.Base(self, newID, posX, posY)
                                self.baseVivante = True
                            else:
                                print("base already exist")
                                return
                        self.buildings[newID] = createdBuild
                        print(newID)
                        #self.controller.view.carte.drawSpecificBuilding(createdBuild)
                        self.model.carte.matrice[posX][posY].isWalkable = False
                        self.model.carte.matrice[+1][posY].isWalkable = False
                        self.model.carte.matrice[posX][posY + 1].isWalkable = False
                        self.model.carte.matrice[posX + 1][posY + 1].isWalkable = False

    def destroyBuilding(self, bId):
        """ Détruit un bâtiment 
        """
        try:
            self.buildings.pop(bId)
        except KeyError:  # Le bâtiment n'existe déjà plus
            pass

    def updateBuildings(self):
        """ Met à jour les bâtiments 
        """
        # TODO Ajouter Méthode Update dans les bâtiments
        #[b.update(self.model) for b in self.buildings.values()]
        pass








