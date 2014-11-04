#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import Batiments
from Commands import Command
from Carte import Carte
from Joueurs import Joueur
from Units import Paysan
from AI import *


class Model:
    def __init__(self, controller):
        self.controller = controller
        self.joueur = None
        self.units = {}
        self.buildings = {}
        self.grandeurMat = 106
        self.carte = Carte(self.grandeurMat)
        self.enRessource = []  # TODO ?À mettre dans Joueur?
        self.ai = None


    def update(self):
        self.updateUnits()
        self.updateBuildings()
        self.updatePaysans()
        self.ai.delaiPenser()


    def updateBuildings(self):
        [build.miseAJour() for build in self.buildings.values()]

    def updateUnits(self):
        [u.update() for u in self.units.values()]


    def updatePaysans(self):
        for paysan in self.enRessource:
            if paysan.mode == 1:
                paysan.chercherRessources()
            else:
                del paysan


    def getUnit(self, uId):
        """ Returns a unit according to its ID
        :param uId: the id of the unit to find
        """

        return next((u for u in self.units.values() if u.id == uId), None)

    def deleteUnit(self, uId):  # TODO utiliser un tag ou un identifiant à la place des positions x et y (plus rapide)
        """ Supprime une unité à la liste d'unités
        """
        try:
            self.units.remove(self.units[uId])
        except Exception:
            pass   # N'existait pas

    def createUnit(self, uid, x, y, civilisation):
        """ Crée et ajoute une nouvelle unité à la liste des unités
        :param x: position x de l'unité
        :param y: position y de l'unité
        """
        # self.units.append(Unit(x, y, self))
        self.units[uid] = Paysan(uid, x, y, self, civilisation)

    def createBuilding(self, userId, type, posX, posY):
        x,y = self.trouverCaseMatrice(posX,posY)
        if not self.carte.matrice[x][y].isWalkable:
            print("not walkable")
        else:
            if not self.carte.matrice[x+1][y].isWalkable:
                print("not walkable")
            else:
                if not self.carte.matrice[x][y+1].isWalkable:
                    print("not walkable")
                else:
                    if not self.carte.matrice[x+1][y+1].isWalkable:
                        print("not walkable")
                    else:
                        print(posX,posY)
                        print(x,y)
                        if type == self.controller.view.FERME:
                            newID = Batiments.Batiment.generateId(userId)
                            createdBuild = Batiments.Ferme(self, newID, x, y)
                        elif type == self.controller.view.BARAQUE:
                            pass
                        elif type == self.controller.view.HOPITAL:
                            pass
                        elif type == self.controller.view.BASE:
                            if self.joueur.baseVivante == False:
                                newID = Batiments.Batiment.generateId(userId)
                                createdBuild = Batiments.Base(self,newID,x,y)
                                self.joueur.baseVivante = True
                            else:
                                print("base already exist")
                                return
                        self.buildings[newID] = createdBuild
                        print(newID)
                        self.controller.view.carte.drawSpecificBuilding(createdBuild)
                        self.carte.matrice[x][y].isWalkable = False
                        self.carte.matrice[+1][y].isWalkable = False
                        self.carte.matrice[x][y+1].isWalkable = False
                        self.carte.matrice[x+1][y+1].isWalkable = False
                        return newID


    def executeCommand(self, command):
        """ Exécute une commande
        :param command: la commande à exécuter
        """
        if command.data['TYPE'] == Command.CREATE_UNIT:
            self.createUnit(command.data['ID'], command.data['X'], command.data['Y'], command.data['CIV'])

        elif command.data['TYPE'] == Command.DELETE_UNIT:
            self.deleteUnit(command.data['X'], command.data['Y'])

        elif command.data['TYPE'] == Command.MOVE_UNIT:
            self.units[command.data['ID']].changerCible(command.data['X2'], command.data['Y2'])




    def trouverCaseMatrice(self, x, y):
        # TODO ? Mettre dans la vue ?

        grandeurCanevasRelle = self.grandeurMat * self.controller.view.carte.item
        grandeurCase = grandeurCanevasRelle / self.grandeurMat
        caseX = int(x / grandeurCase)
        caseY = int(y / grandeurCase)

        return caseX, caseY

    def trouverCentreCase(self, caseX, caseY):
        # TODO ? Mettre dans la vue ?

        grandeurCanevasRelle = self.grandeurMat * self.controller.view.carte.item
        grandeurCase = grandeurCanevasRelle / self.grandeurMat
        centreX = (grandeurCase * caseX) + grandeurCase / 2
        centreY = (grandeurCase * caseY) + grandeurCase / 2

        return centreX, centreY

    def creerJoueur(self, clientId):
        """  Permet de crééer l'entité joueur
        :param clientId: L'id du client
        """
        self.joueur = Joueur(clientId)
        self.ai = AI(6, self)
        self.ai.base = self.buildings[self.createBuilding(6, self.controller.view.BASE, 80, 80)]