import Batiments
from Commands import Command
from Units import *


class Ressources:   # TODO appliquer à toutes les références de ressources
    BOIS = 'bois'
    MINERAI = 'minerai'
    CHARBON = 'charbon'
    NOURRITURE = 'nourriture'


class Joueur:
    """docstring for Joueur"""

    def __init__(self, civilisation, model):
        self.model = model
        self.civilisation = civilisation  # Couleur de la civilisation
        self.base = None  # TODO Base Vivante ne pourrait pas juste être remplacer par un if self.base: ?
        self.baseVivante = False  # À modifier, doit être true quand on commence une vraie partie
        #self.ressources = {Ressources.BOIS: 0, Ressources.MINERAI: 0, Ressources.CHARBON: 0}
        self.ressources = {'bois': 0, 'minerai': 0, 'charbon': 0, 'nourriture': 0}
        self.morale = 0
        self.nbNourriture = 0
        self.epoque = 1
        self.recherche = []  # Liste des recherches effectuées
        self.units = {}
        self.enRessource = []
        self.buildings = {}


    def ajouterRessource(self, typeRessource, nbRessources):
        print("type", typeRessource, self.civilisation)
        if typeRessource == 1 or typeRessource == Ressources.BOIS:
            self.ressources['bois'] += nbRessources
        elif typeRessource == 2 or typeRessource == Ressources.MINERAI:
            self.ressources['minerai'] += nbRessources
        elif typeRessource == 3 or typeRessource == Ressources.CHARBON:
            self.ressources['charbon'] += nbRessources
        elif typeRessource == Ressources.NOURRITURE:
            self.ressources['nourriture'] += nbRessources
        civ = self.civilisation
        if civ == self.model.joueur.civilisation:
            self.model.joueurs[civ].model.controller.view.frameBottom.updateResources(self.model.joueurs[civ])

    def update(self):
        """ Permet de lancer les commande updates importantes
        """

        self.updateUnits()
        self.updatePaysans()
        self.updateBuildings()


    def canEvolve(self):
        """ Vérifie si la civilisation à les prérequis pour changer d'age
        :return:
        """

        # ÉVOLUTION VERS AGE 2
        if self.epoque == 1:
            nbFermes = len([f for f in self.buildings.values() if isinstance(f, Batiments.Ferme)])
            nbUnites = len(self.units)
            #return self.base and nbUnites >= 30 and nbFermes >= 1 and self.ressources[Ressources.BOIS] >= 500
            return self.base and nbUnites >= 2
        # ÉVOLUTION VERS AGE 3
        if self.epoque == 2:
            return False    # TODO Déterminer

        return False

    def changerAge(self, nouvelAge):
        self.epoque = nouvelAge
        # TODO Changer les images pour les buildings
        #[b.determineImage() for b in self.buildings.values()]
        # TODO Changer les images pour les unités
        [u.determineSpritesheet() for u in self.units.values()]





    def annihilate(self):
        """ Annihilation de la civilisation 
            Donc suppression:
                des buildings
                des unités
        """
        self.units = {}
        self.buildings = {}


    # ## UNITS ###
    def createUnit(self, uId, x, y, civilisation):
        """ Crée et ajoute une nouvelle unité à la liste des unités
        :param uId: ID que l'on souhaite attribuer à l'unité
        :param x: position x de l'unité
        :param y: position y de l'unité
        """
        self.units[uId] = Paysan(uId, x, y, self, civilisation)

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
        # print(self.enRessource)
        for paysan in self.enRessource:
            #print(paysan.id, paysan.mode)
            if paysan.mode == 1:
                #print(paysan.id)
                if not paysan.enDeplacement and paysan.ressource:
                    paysan.chercherRessources()
                elif not paysan.cheminTrace and not paysan.ressourceEnvoye:
                    self.ajouterRessource(paysan.typeRessource, paysan.nbRessources)
                    paysan.nbRessources = 0
                    cases = self.model.trouverCaseMatrice(paysan.posRessource.x, paysan.posRessource.y)
                    if self.model.carte.matrice[cases[0]][cases[1]].type == 0:
                        paysan.mode = 0
                        print("Paysan mode", paysan.mode)
                    print(paysan.id, self.ressources)
                    groupe = []
                    groupe.append(paysan)
                    self.model.controller.eventListener.onMapRClick(paysan.posRessource, groupe)
                    paysan.ressourceEnvoye = True
            else:
                print("remove", paysan.id)
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
        if btype == Batiments.Batiment.FERME:
            newID = Batiments.Batiment.generateId(self.civilisation)
            createdBuild = Batiments.Ferme(self, newID, posX, posY)
        elif btype == Batiments.Batiment.BARAQUE:
            newID = Batiments.Batiment.generateId(self.civilisation)
            createdBuild = Batiments.Baraque(self, newID, posX, posY)
        elif btype == Batiments.Batiment.HOPITAL:
            newID = Batiments.Batiment.generateId(self.civilisation)
            createdBuild = Batiments.Hopital(self, newID, posX, posY)
        elif btype == Batiments.Scierie:
            newID = Batiments.Batiment.generateId(self.civilisation)
            createdBuild = Batiments.Scierie(self, newID, posX, posY)
        elif btype == Batiments.Fonderie:
            newID = Batiments.Batiment.generateId(self.civilisation)
            createdBuild = Batiments.Fonderie(self, newID, posX, posY)
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
        self.model.controller.view.carte.drawSpecificBuilding(createdBuild)
        self.model.carte.matrice[posX][posY].isWalkable = False
        self.model.carte.matrice[posX + 1][posY].isWalkable = False
        self.model.carte.matrice[posX][posY + 1].isWalkable = False
        self.model.carte.matrice[posX + 1][posY + 1].isWalkable = False
        self.model.carte.matrice[posX][posY].type = 5  # batiments
        self.model.carte.matrice[posX + 1][posY].type = 5  # batiments
        self.model.carte.matrice[posX][posY + 1].type = 5  # batiments
        self.model.carte.matrice[posX + 1][posY + 1].type = 5  # batiments

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
<<<<<<< HEAD
        [b.miseAJour() for b in self.buildings.values()]

    def cheat(self):
        posUnitX,posUnitY = self.model.trouverCentreCase(5,5)
        cmd = Command(self.civilisation, Command.UNIT_CREATE)
        cmd.addData('ID', Unit.generateId(self.civilisation))
        cmd.addData('X', posUnitX)
        cmd.addData('Y', posUnitY)
        cmd.addData('CIV', self.civilisation)
        cmd.addData('CLASSE', "soldatEpee")
        self.model.controller.sendCommand(cmd)
=======
        [b.miseAJour() for b in self.buildings.values() if b.joueur == self]
>>>>>>> origin/dev
