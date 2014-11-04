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

    def updatePaysans(self):
        for paysan in self.enRessource:
            if paysan.mode == 1:
                if not paysan.enDeplacement:
                    paysan.chercherRessources()
            else:
                self.enRessource.remove(paysan)


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
            Command.DESTROY_UNIT: self.executeDestroyUnit
        }
        exe = commands[command.data['TYPE']]
        exe(command)


    def executeCreateUnit(self, command):
        self.createUnit(command.data['ID'], command.data['X'], command.data['Y'], command.data['CIV'])

    def executeMoveUnit(self, command):
        unit = self.units[command.data['ID']]
        unit.changerCible(command.data['X2'], command.data['Y2'], command.data['GROUPE'], command.data['FIN'], command.data['LEADER'])

    def executeAttackUnit(self, command):
        try:
            attacker = self.units[command.data['SOURCE_ID']]
            target = self.units[command.data['TARGET_ID']]
            target.recevoirAttaque(self, attacker, command.data['DMG'])
        except KeyError:    # On a essayer d'attaquer une unité morte
            pass


    def executeDestroyUnit(self, command):
        try:
            uId = command.data['ID']
            self.units.pop(uId)
        except KeyError:    # L'unité n'existe déjà plus
            pass

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

    def trouverFinMultiSelection(self, cibleX, cibleY, nbUnits, contact): #cible en x,y
        posFin = []
        liste = [0,-contact, contact]
        #TODO TROUVER PAR CADRAN...
        #TODO TROUVER TOUT LE TEMPS UNE RÉPONSE
        #Marche si pas plus de 9 unités
        for multi in range(1,self.grandeurMat):
            for i in liste:
                for j in liste:
                    if not (i == 0 and j == 0 and multi == 1):
                        #print(multi*i,multi*j)
                        posX = cibleX + multi*i
                        posY = cibleY + multi*j
                        deplacementPossible =  True
                        try:
                            casesPossibles = [  self.trouverCaseMatrice(posX, posY),
                                            self.trouverCaseMatrice(posX+contact/2, posY),
                                            self.trouverCaseMatrice(posX, posY + contact/2),
                                            self.trouverCaseMatrice(posX+contact/2, posY + contact/2),
                                            self.trouverCaseMatrice(posX-contact/2, posY),
                                            self.trouverCaseMatrice(posX, posY - contact/2),
                                            self.trouverCaseMatrice(posX-contact/2, posY - contact/2)]

                            #Gestion des obstacles
                            for case in casesPossibles:
                                if not self.carte.matrice[case[0]][case[1]].type == 0 or case[0] < 0 or case[1] < 0 or case[0] > self.grandeurMat or case[1] > self.grandeurMat:
                                    deplacementPossible = False
                                    break

                            if deplacementPossible:
                                posFin.append((posX, posY))
                                if len(posFin) >= nbUnits:
                                    return posFin
                        except:
                            print("hors de la matrice")
                            pass #Hors de la matrice
        print(len(posFin))
        return -1#FAIL
            

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
