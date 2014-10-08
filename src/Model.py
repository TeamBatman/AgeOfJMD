#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from Commands import Command
from Carte import Carte
from GraphicsManagement import SpriteSheet

import time


class Joueur:
    """docstring for Joueur"""
    # CIVILISATIONS
    NOIR = 0
    BLEU = 1
    VERT = 2

    MAUVE = 3
    ORANGE = 4
    ROSE = 5

    ROUGE = 6
    BLANC = 7
    JAUNE = 8
    NB_CIVLISATION = 9


    def __init__(self, civilisation):
        self.civilisation = civilisation
        self.base = None
        self.ressources = {'bois': 0, 'minerai': 0, 'charbon': 0}
        self.morale = 0
        self.nbNourriture = 0


class Unit():
    COUNT = 0  # Un compteur permettant d'avoir un Id unique pour chaque unité

    def __init__(self, clientId, x, y, parent):
        self.id = Unit._generateId(clientId)
        self.x = x
        self.y = y
        self.parent = parent
        self.vitesse = 5
        self.grandeur = 30
        self.cibleX = x
        self.cibleY = y
        self.cheminTrace = []
        self.cibleXTrace = x
        self.cibleXTrace = y
        self.mode = 0  # 1=ressource

        # ANIMATION
        self.lastAnimtaionTime = time.time()
        self.animationRate = 333  # in millisecond
        self.spriteSheet = SpriteSheet('Units/Age_I/red_caveman_1.png')

        self.animDirection = 'DOWN'
        self.animFrameIndex = 1

        activeFrameKey = '%s_%s' % (self.animDirection, self.animFrameIndex)
        self.activeFrame = self.spriteSheet.frames[activeFrameKey]
        self.activeOutline = self.spriteSheet.framesOutlines[activeFrameKey]


    def getClientId(self):
        """ Returns the Id of the client using the id of the unit
        :return: the id of the clients
        """
        return self.id.split('_')[0]

    def estUniteDe(self, clientId):
        """ Vérifie si l'unité appartient au client ou non
        :param clientId: le client à tester
        :return: True si elle lui appartient Sinon False
        """
        masterId = int(self.getClientId())
        clientId = int(clientId)
        return masterId == clientId





    @staticmethod
    def _generateId(clientId):
        gId = "%s_%s" % (clientId, Unit.COUNT)
        Unit.COUNT += 1
        return gId


    def animer(self):
        """ Lance l'animation de l'unité
        """
        if not time.time() - self.lastAnimtaionTime >= self.animationRate / 1000:
            return

        self.animFrameIndex += 1

        if self.animFrameIndex == self.spriteSheet.NB_FRAME_ROW:
            self.animFrameIndex = 0
        if self.animFrameIndex == 1:  # POSITION NEUTRE ON NE VEUT PAS ÇA
            self.animFrameIndex = 2

        activeFrameKey = '%s_%s' % (self.animDirection, self.animFrameIndex)
        self.activeFrame = self.spriteSheet.frames[activeFrameKey]
        self.activeOutline = self.spriteSheet.framesOutlines[activeFrameKey]
        self.lastAnimtaionTime = time.time()

    def update(self):
        try:
            self.deplacementTrace()
        except:
            print("unit fail")
            self.deplacement()


    def changerCible(self, cibleX, cibleY):
        self.mode = 0
        self.cibleX = cibleX
        self.cibleY = cibleY
        self.choisirTrace()

    def deplacement(self):
        if abs(self.cibleX - self.x) <= self.vitesse:
            self.x = self.cibleX
        if abs(self.cibleY - self.y) <= self.vitesse:
            self.y = self.cibleY

        if self.cibleX > self.x:
            self.x += self.vitesse
            self.animDirection = 'RIGHT'


        elif self.cibleX < self.x:
            self.x -= self.vitesse
            self.animDirection = 'LEFT'

        if self.cibleY > self.y:
            self.y += self.vitesse
            self.animDirection = 'DOWN'

        elif self.cibleY < self.y:
            self.y -= self.vitesse
            self.animDirection = 'UP'

        # Puisqu'il y a eu un déplacement
        self.animer()

    def deplacementTrace(self):
        if len(self.cheminTrace) > 0:
            if self.x == self.cibleX and self.y == self.cibleY:
                del self.cheminTrace[-1]
                if len(self.cheminTrace) <= 0:
                    self.animFrameIndex = 1
                    self.animDirection = 'DOWN'
                    activeFrameKey = 'DOWN_1'
                    self.activeFrame = self.spriteSheet.frames[activeFrameKey]
                    self.activeOutline = self.spriteSheet.framesOutlines[activeFrameKey]
                    return -1
                self.cibleX = self.cheminTrace[-1].x
                self.cibleY = self.cheminTrace[-1].y

            if abs(self.cibleX - self.x) <= self.vitesse:
                self.x = self.cibleX
            if abs(self.cibleY - self.y) <= self.vitesse:
                self.y = self.cibleY

            if self.cibleX > self.x:
                self.x += self.vitesse
                self.animDirection = 'RIGHT'

            elif self.cibleX < self.x:
                self.x -= self.vitesse
                self.animDirection = 'LEFT'

            if self.cibleY > self.y:
                self.y += self.vitesse
                self.animDirection = 'DOWN'

            elif self.cibleY < self.y:
                self.y -= self.vitesse
                self.animDirection = 'UP'

            # Puisqu'il y a eu un déplacement
            self.animer()


    def choisirTrace(self):
        cases = self.parent.trouverCaseMatrice(self.x, self.y)
        caseX = cases[0]
        caseY = cases[1]
        self.mode = 0
        casesCible = self.parent.trouverCaseMatrice(self.cibleX, self.cibleY)
        if not self.parent.carte.matrice[casesCible[0]][casesCible[1]].type == 0:
            if isinstance(self, Paysan):
                print("ressource")
                self.parent.enRessource.append(self)
                self.mode = 1  # ressource
                # TODO Changer le chemin pour aller à côté de la ressource !
            else:
                return -1  # Ne peut pas aller sur un obstacle
        caseCibleX = casesCible[0]
        caseCibleY = casesCible[1]

        noeudInit = Noeud(None, caseX, caseY, caseCibleX, caseCibleY)
        self.open = []
        self.closed = []
        self.open.append(noeudInit)
        time1 = time.time()
        chemin = self.aEtoile()
        print("Temps a*: ", time.time() - time1)
        n = chemin
        if not n == -1:
            self.cheminTrace = []
            while n.parent:
                self.cheminTrace.append(n)
                centreCase = self.parent.trouverCentreCase(n.x, n.y)
                n.x = centreCase[0]
                n.y = centreCase[1]
                n = n.parent
            # print(self.cheminTrace,"len", len(self.cheminTrace))
            if self.cheminTrace:
                # Pour ne pas finir sur le centre de la case (Pour finir sur le x,y du clic)
                if not self.mode == 1:  #pas en mode ressource
                    self.cheminTrace[0] = Noeud(None, self.cibleX, self.cibleY, None, None)
            else:
                if not self.mode == 1:  # pas en mode ressource
                    self.cheminTrace.append(Noeud(None, self.cibleX, self.cibleY, None, None))
                else:
                    self.cheminTrace.append(Noeud(None, self.x, self.y, None, None))

            self.cibleX = self.cheminTrace[-1].x
            self.cibleY = self.cheminTrace[-1].y

    def aEtoile(self):
        nbNoeud = 400
        while self.open:
            n = self.open[0]
            if self.goal(n):
                return n
            self.open.remove(n)
            self.closed.append(n)

            successeurN = self.transition(n)

            for nPrime in successeurN:
                aAjouter = True
                for i in range(len(self.open)):
                    if nPrime.x == self.open[i].x and nPrime.y == self.open[i].y:
                        if nPrime.cout <= self.open[i].cout:
                            del self.open[i]
                        else:
                            aAjouter = False
                        break
                if aAjouter:
                    self.open.append(nPrime)

                    # Mettre dans le if aAjouter ?
                    # time1= time.time()
                self.open.sort(key=lambda x: x.cout)
                # tempsTotal += time.time()-time1
                # print("Temps sort: ", tempsTotal)
                if len(self.open) > nbNoeud:
                    # self.afficherList("open", self.open)
                    #return -1
                    self.open = self.open[:nbNoeud]
                    #print(len(self.open))
                    #self.parent.parent.v.afficherCourantPath(self.open)
        return -1

    def afficherList(self, nom, liste):
        for i in range(0, len(liste)):
            print(i, nom, liste[i].x, liste[i].y, "cout", liste[i].cout)

    def aCoteMur(self, caseX, caseY):  # Pour ne pas aller en diagonale et rentrer dans un mur
        # TODO BUG traverse un mur en diagonale
        if caseY - 1 >= 0:
            if caseX - 1 >= 0 and not self.parent.carte.matrice[caseX - 1][caseY - 1].type == 0:
                return True
            if not self.parent.carte.matrice[caseX][caseY - 1].type == 0:
                return True
            if caseX + 1 < self.parent.grandeurMat and not self.parent.carte.matrice[caseX + 1][caseY - 1].type == 0:
                return True

        if caseX - 1 >= 0 and not self.parent.carte.matrice[caseX - 1][caseY] == 0:
            return False
        if caseX + 1 < self.parent.grandeurMat and not self.parent.carte.matrice[caseX + 1][caseY] == 0:
            return False

        if caseY + 1 < self.parent.grandeurMat:
            if caseX - 1 >= 0 and not self.parent.carte.matrice[caseX - 1][caseY + 1].type == 0:
                return True
            if not self.parent.carte.matrice[caseX][caseY + 1].type == 0:
                return True
            if caseX + 1 < self.parent.grandeurMat and not self.parent.carte.matrice[caseX + 1][caseY + 1].type == 0:
                return True

        return False

    def transition(self, n):
        caseTransition = []

        caseX = n.x
        caseY = n.y
        casesCible = self.parent.trouverCaseMatrice(self.cibleX, self.cibleY)
        caseCibleX = casesCible[0]
        caseCibleY = casesCible[1]

        if caseY - 1 >= 0:
            if caseX - 1 >= 0 and self.parent.carte.matrice[caseX - 1][caseY - 1].type == 0 and not self.aCoteMur(
                            caseX - 1, caseY - 1):
                caseTransition.append(Noeud(n, caseX - 1, caseY - 1, caseCibleX, caseCibleY))
            if self.parent.carte.matrice[caseX][caseY - 1].type == 0:
                caseTransition.append(Noeud(n, caseX, caseY - 1, caseCibleX, caseCibleY))
            if caseX + 1 < self.parent.grandeurMat and self.parent.carte.matrice[caseX + 1][
                        caseY - 1].type == 0 and not self.aCoteMur(caseX + 1, caseY - 1):
                caseTransition.append(Noeud(n, caseX + 1, caseY - 1, caseCibleX, caseCibleY))

        if caseX - 1 >= 0 and self.parent.carte.matrice[caseX - 1][caseY].type == 0:
            caseTransition.append(Noeud(n, caseX - 1, caseY, caseCibleX, caseCibleY))
        if caseX + 1 < self.parent.grandeurMat and self.parent.carte.matrice[caseX + 1][caseY].type == 0:
            caseTransition.append(Noeud(n, caseX + 1, caseY, caseCibleX, caseCibleY))

        if caseY + 1 < self.parent.grandeurMat:
            if caseX - 1 >= 0 and self.parent.carte.matrice[caseX - 1][caseY + 1].type == 0 and not self.aCoteMur(
                            caseX - 1, caseY + 1):
                caseTransition.append(Noeud(n, caseX - 1, caseY + 1, caseCibleX, caseCibleY))
            if self.parent.carte.matrice[caseX][caseY + 1].type == 0:
                caseTransition.append(Noeud(n, caseX, caseY + 1, caseCibleX, caseCibleY))
            if caseX + 1 < self.parent.grandeurMat and self.parent.carte.matrice[caseX + 1][
                        caseY + 1].type == 0 and not self.aCoteMur(caseX + 1, caseY + 1):
                caseTransition.append(Noeud(n, caseX + 1, caseY + 1, caseCibleX, caseCibleY))

        return caseTransition


    def goal(self, noeud):
        casesCible = self.parent.trouverCaseMatrice(self.cibleX, self.cibleY)
        caseCibleX = casesCible[0]
        caseCibleY = casesCible[1]

        if noeud.x == caseCibleX and noeud.y == caseCibleY:
            return True
        elif abs(noeud.x - caseCibleX) <= 1 and abs(
                        noeud.y - caseCibleY) <= 1 and self.mode == 1:  # pour les ressources
            return True
        return False


class Noeud:
    def __init__(self, parent, x, y, cibleX, cibleY):
        self.parent = parent
        self.x = x
        self.y = y
        self.cout = 0
        if not (parent == None):
            self.calculerCout(cibleX, cibleY)

    def calculerCout(self, cibleX, cibleY):
        g = self.parent.cout + self.coutTransition(self.parent)
        h = abs(self.x - cibleX) + abs(self.y - cibleY)
        self.cout = g + h

    def coutTransition(self, n2):
        if abs(self.x - n2.x) == 1 and abs(self.y - n2.y) == 1:
            return 14  # Diagonale
        else:
            return 10


class Paysan(Unit):
    def __init__(self, clientId, x, y, parent):
        Unit.__init__(self, clientId, x, y, parent)
        self.vitesseRessource = 0.01  # La vitesse à ramasser des ressources
        self.nbRessourcesMax = 10
        self.nbRessources = 0
        self.typeRessource = 0  # 0 = Rien 1 à 4 = Ressources

    def chercherRessources(self):
        # print(int(self.nbRessources))
        # TODO Regarder le type de la ressource !
        #TODO Enlever nbRessources à la case ressource !
        if self.nbRessources + self.vitesseRessource <= self.nbRessourcesMax:
            self.nbRessources += self.vitesseRessource
        else:
            self.nbRessources = self.nbRessourcesMax
            #print("MAX!", self.nbRessources)
            #TODO Faire retourner à la base !        


class Model:
    def __init__(self, controller):
        self.controller = controller
        self.joueur = None
        self.units = []
        self.grandeurMat = 106
        self.carte = Carte(self.grandeurMat)
        self.enRessource = []  # TODO ?À mettre dans Joueur?

    def update(self):
        self.updateUnits()

    def updateUnits(self):
        for unit in self.units:
            unit.update()


    def deleteUnit(self, x, y):  # TODO utiliser un tag ou un identifiant à la place des positions x et y (plus rapide)
        """ Supprime une unité à la liste d'unités
        :param x: position x de l'unité
        :param y: position y de l'unité
        """
        for unit in self.units:
            if unit.x == x and unit.y == y:
                self.units.remove(unit)

    def createUnit(self, clientId, x, y):
        """ Crée et ajoute une nouvelle unité à la liste des unités
        :param x: position x de l'unité
        :param y: position y de l'unité
        """
        # self.units.append(Unit(x, y, self))
        self.units.append(Paysan(clientId, x, y, self))

    def executeCommand(self, command):
        """ Exécute une commande
        :param command: la commande à exécuter
        """
        if command.data['TYPE'] == Command.CREATE_UNIT:
            self.createUnit(command.clientId, command.data['X'], command.data['Y'])

        elif command.data['TYPE'] == Command.DELETE_UNIT:
            self.deleteUnit(command.data['X'], command.data['Y'])
        elif command.data['TYPE'] == Command.MOVE_UNIT:
            for unit in self.units:
                if unit.x == command.data['X1'] and unit.y == command.data['Y1']:
                    unit.changerCible(command.data['X2'], command.data['Y2'])

    def trouverCaseMatrice(self, x, y):
        # TODO ? Mettre dans la vue ?

        grandeurCanevasRelle = self.grandeurMat * self.controller.view.item
        grandeurCase = grandeurCanevasRelle / self.grandeurMat
        caseX = int(x / grandeurCase)
        caseY = int(y / grandeurCase)

        return caseX, caseY

    def trouverCentreCase(self, caseX, caseY):
        # TODO ? Mettre dans la vue ?

        grandeurCanevasRelle = self.grandeurMat * self.controller.view.item
        grandeurCase = grandeurCanevasRelle / self.grandeurMat
        centreX = (grandeurCase * caseX) + grandeurCase / 2
        centreY = (grandeurCase * caseY) + grandeurCase / 2

        return centreX, centreY

    def creerJoueur(self, clientId):
        """  Permet de crééer l'entité joueur
        :param clientId: L'id du client
        """
        self.joueur = Joueur(clientId)
