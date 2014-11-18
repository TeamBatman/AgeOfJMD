#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

from datetime import datetime

from Batiments import Batiment
import Batiments
from Commands import Command
from Carte import Carte
from Joueurs import Joueur
from Units import Paysan


class Model:
    def __init__(self, controller):
        self.controller = controller
        self.joueur = None  # Le joueur du client actif
        self.joueurs = {}  # La totalité des joueurs et de leurs unités
        self.grandeurMat = 106
        self.carte = Carte(self.grandeurMat)
        self.enRessource = []  # TODO ?À mettre dans Joueur?

    def update(self):
        """ Permet de lancer les commande updates importantes
        """
        # On UPDATE Chacune des civilisations
        [civ.update() for civ in self.joueurs.values()]

    # ## EXECUTION COMMANDES ###
    def executeCommand(self, command):
        """ Exécute une commande
        :param command: la commande à exécuter [Objet Command]
        """
        commands = {
            Command.CREATE_UNIT: self.executeCreateUnit,
            Command.MOVE_UNIT: self.executeMoveUnit,
            Command.ATTACK_UNIT: self.executeAttackUnit,
            Command.KILL_UNIT: self.executeKillUnit,
            Command.TAKE_RESSOURCES: self.executeTakeRessources,
            
            Command.CREATE_BUILDING: self.executeCreateBuilding,

            Command.CREATE_CIVILISATION: self.executeCreateCivilisation,

            Command.EMPTY: lambda info: None
        }

        try:
            exe = commands[command.data['TYPE']]
            #print("EXECUTE: %s" % datetime.now())      # DEBUG
            exe(command)
        except KeyError:
            raise KeyError("FONCTIONALITÉ NON IMPLÉMENTÉE...")

    def executeCreateUnit(self, command):
        """ Execute la commande crééer unité  selon ses paramètres 
        :param command: la commande à exécuter [Objet Command]
        """

        self.joueurs[command.data['CIV']].createUnit(command.data['ID'], command.data['X'], command.data['Y'],
                                                     command.data['CIV'])

    def executeMoveUnit(self, command):
        """ Execute la commande pour DÉPLACER UNE UNITÉ selon ses paramètres 
        :param command: la commande à exécuter [Objet Commande]
        """
        try:
            unit = self.getUnit(command['ID'])
            unit.changerCible(command.data['X2'], command.data['Y2'], command.data['GROUPE'], command.data['FIN'],
                              command.data['LEADER'], command.data['ENNEMI'])
        except (KeyError, AttributeError):  # On a essayé de déplacer une unité morte
            pass

    def executeAttackUnit(self, command):
        """ Execute la commande ATTAQUER UNE UNITÉ  selon ses paramètres 
        :param command: la commande à exécuter [Objet Commande]
        """
        attacker = self.getUnit(command['SOURCE_ID'])
        target = self.getUnit(command['TARGET_ID'])
        target.recevoirAttaque(self, attacker, command['DMG'])

    def executeKillUnit(self, command):
        """ Execute la commande TUER UNE UNITÉ
          selon ses paramètres 
        :param command: la commande à exécuter [Objet Commande]
        """
        try:
            civId = self.getUnit(command['ID']).getClientId()
            self.joueurs[civId].killUnit(command['ID'])
        except:
            print("Déjà tuée")#Unité déjà morte

    def executeTakeRessources(self, command):
        civId = self.getUnit(command['ID']).getClientId()
        nbRessources = self.carte.matrice[command['X1']][command['Y1']].nbRessources
        
        if nbRessources >= command['NB_RESSOURCES']:
            self.carte.matrice[command['X1']][command['Y1']].nbRessources -= command['NB_RESSOURCES']
            
            if self.joueur.civilisation == civId:
                self.getUnit(command['ID']).nbRessources += command['NB_RESSOURCES']
        else:
            if self.joueur.civilisation == civId:
                self.getUnit(command['ID']).nbRessources += self.carte.matrice[command['X1']][command['Y1']].nbRessources
            self.carte.matrice[command['X1']][command['Y1']].nbRessources = 0
        if self.carte.matrice[command['X1']][command['Y1']].nbRessources <= 0:
            self.carte.matrice[command['X1']][command['Y1']].type = 0 #Gazon -> n'est plus une ressource
            self.carte.matrice[command['X1']][command['Y1']].isWalkable = True
            self.controller.view.update(self.getUnits(), self.getBuildings(),
                                        self.carte.matrice)
        print("reste", self.carte.matrice[command['X1']][command['Y1']].nbRessources, self.getUnit(command['ID']).mode)
            #self.controller.view.frameMinimap.updateMinimap(self.carte.matrice)
            #TODO: Mettre mini map à jour !!!

    def executeCreateBuilding(self, command):
        self.joueurs[command.data['CIV']].createBuilding(command['ID'], command['X'], command['Y'],
                                                         command['BTYPE'])

    def executeCreateCivilisation(self, command):
        self.creerJoueur(command['ID'])
        # TODO CRÉER BASE



    # ## HELPERS ###

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

    def trouverFinMultiSelection(self, cibleX, cibleY, nbUnits, contact):  # cible en x,y
        posFin = []
        liste = [0, -contact, contact]
        #TODO TROUVER PAR CADRAN...
        #TODO TROUVER TOUT LE TEMPS UNE RÉPONSE
        #Marche si pas plus de 9 unités
        for multi in range(1, self.grandeurMat):
            for i in liste:
                for j in liste:
                    if not (i == 0 and j == 0 and multi == 1):
                        #print(multi*i,multi*j)
                        posX = cibleX + multi * i
                        posY = cibleY + multi * j
                        if(posX == cibleX and posY == cibleY):
                            break #Même position que le leader
                        deplacementPossible = True
                        try:
                            casesPossibles = [self.trouverCaseMatrice(posX, posY),
                                              self.trouverCaseMatrice(posX + contact / 2, posY),
                                              self.trouverCaseMatrice(posX, posY + contact / 2),
                                              self.trouverCaseMatrice(posX + contact / 2, posY + contact / 2),
                                              self.trouverCaseMatrice(posX - contact / 2, posY),
                                              self.trouverCaseMatrice(posX, posY - contact / 2),
                                              self.trouverCaseMatrice(posX - contact / 2, posY - contact / 2)]
                            #Gestion des obstacles
                            for case in casesPossibles:
                                if not self.carte.matrice[case[0]][case[1]].isWalkable or case[0] < 0 or case[1] < 0 or \
                                   case[0] > self.grandeurMat or case[1] > self.grandeurMat:
                                    deplacementPossible = False
                                    break

                            if deplacementPossible:
                                posFin.append((posX, posY))
                                if len(posFin) >= nbUnits:
                                    return posFin
                        except:
                            print("hors de la matrice")
                            pass  #Hors de la matrice
        print(len(posFin))
        return -1  #FAIL



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

    # ## JOUEURS ###
    def getUnit(self, uId):
        """ Retourne une unite selon son ID
        :param uId: l'ID de l'unité à trouver
        :returns L'unité si elle est trouvée sinon None
        :rtype : Unit
        """
        try:
            civilisationId = int(uId.split('_')[0])
            return self.joueurs[civilisationId].units[uId]
        except KeyError:
            return None

    def getBuilding(self, bId):
        """ Retourne un bâtiment selon son ID
        :param bId: l'ID du bâtiment à trouver
        """
        try:
            civilisationId = int(bId.split('_')[0])
            return self.joueurs[civilisationId].buildings[bId]
        except KeyError:
            return None

    def creerJoueur(self, clientId):
        """  Permet de crééer un joueur et de l'ajouter à la liste des joueurs
        :param clientId: L'id du client
        """
        self.joueurs[clientId] = Joueur(clientId, self)

    def getUnits(self):
        """ Retoune la totalité des unités de toutes les civilisations
        """
        return {uId: u for civ in self.joueurs.values() for uId, u in civ.units.items()}

    def getBuildings(self):
        """ Retoune la totalité des bâtiments de toutes les civilisations
        """
        return {bId: b for civ in self.joueurs.values() for bId, b in civ.buildings.items()}
