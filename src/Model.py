#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from Commands import Command
from Carte import Carte
from Joueurs import Joueur
from Units import Paysan

class Model:
    def __init__(self, controller):
        self.controller = controller
        self.joueur = None
        self.units = []
        self.grandeurMat = 106
        self.carte = Carte(self.grandeurMat)
        self.enRessource = []  # TODO ?À mettre dans Joueur?

    def update(self):
        """ Permet de lancer les commande updates importantes
        """
        self.updateUnits()
        self.updatePaysans()


    def updateUnits(self):
        """ Met à jour chacune des unités
        """
        [u.update() for u in self.units]


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
        return next((u for u in self.units if u.id == uId), None)

    def deleteUnit(self, uId):  # TODO utiliser un tag ou un identifiant à la place des positions x et y (plus rapide)
        """ Supprime une unité à la liste d'unités
        """
        try:
            self.units.remove(self.getUnit(uId))
        except Exception:
            pass   # N'existait pas

    def createUnit(self, uid, x, y, civilisation):
        """ Crée et ajoute une nouvelle unité à la liste des unités
        :param x: position x de l'unité
        :param y: position y de l'unité
        """
        # self.units.append(Unit(x, y, self))
        self.units.append(Paysan(uid, x, y, self, civilisation))

    def executeCommand(self, command):
        """ Exécute une commande
        :param command: la commande à exécuter
        """
        if command.data['TYPE'] == Command.CREATE_UNIT:
            self.createUnit(command.data['ID'], command.data['X'], command.data['Y'], command.data['CIV'])

        elif command.data['TYPE'] == Command.DELETE_UNIT:
            self.deleteUnit(command.data['X'], command.data['Y'])

        elif command.data['TYPE'] == Command.MOVE_UNIT:
            self.getUnit(command.data['ID']).changerCible(command.data['X2'], command.data['Y2'], command.data['LEADER'])

    def trouverPlusProche(self, listeElements, coordBut):
        """On reçoit des x,y et non des cases ! """
        if listeElements:
            elementResultat = listeElements[0]
            diff = abs(listeElements[0].x - coordBut[0]) + abs(listeElements[0].y - coordBut[1])

            for element in listeElements:
                diffCase = abs(element.x - coordBut[0]) + abs(element.y - coordBut[1])
                if diff > diffCase:
                    elementResultat = element
            return elementResultat

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
