#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import time
from Commands import Command
from Carte import Carte
from Joueurs import Joueur

from Units import Paysan


class Model:
    def __init__(self, controller):
        self.controller = controller
        self.joueur = None
        self.units = {}
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
            Et supprime les unités mortes de la liste
        """
        [u.update(self) for u in self.units.values()]
        # On retire les morts
        self.units = {uid: u for uid, u in self.units.items() if u.hp > 0}

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
        return self.units[uId]

    def deleteUnit(self, uId):  # TODO utiliser un tag ou un identifiant à la place des positions x et y (plus rapide)
        """ Supprime une unité à la liste d'unités
        """
        try:
            self.units.pop(uId)
        except Exception:
            pass  # N'existait pas

    def createUnit(self, uid, x, y, civilisation):
        """ Crée et ajoute une nouvelle unité à la liste des unités
        :param x: position x de l'unité
        :param y: position y de l'unité
        """
        # self.units.append(Unit(x, y, self))
        self.units[uid] = Paysan(uid, x, y, self, civilisation)

    def executeCommand(self, command):
        """ Exécute une commande
        :param command: la commande à exécuter
        """
        commands = {
            Command.CREATE_UNIT: self.executeCreateUnit,
            Command.MOVE_UNIT: self.executeMoveUnit,
            Command.ATTACK_UNIT: self.executeAttackUnit,
        }
        exe = commands[command.data['TYPE']]
        exe(command)


    def executeCreateUnit(self, command):
        self.createUnit(command.data['ID'], command.data['X'], command.data['Y'], command.data['CIV'])

    def executeMoveUnit(self, command):
        unit = self.units[command.data['ID']]
        unit.ennemiCible = None
        unit.changerCible(command.data['X2'], command.data['Y2'])

    def executeAttackUnit(self, command):
        try:
            attacker = self.units[command.data['SOURCE_ID']]
            target = self.units[command.data['TARGET_ID']]
            attacker.ennemiCible = target
        except KeyError:
            pass    # L'une des deux unités est mortes alors la commande est inutiles


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