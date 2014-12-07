#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

from Commands import Command
from Carte import Carte
from Joueurs import Joueur
from Units import Paysan
from Units import Noeud
from AI import AI
from Batiments import *

class Model:
    def __init__(self, controller):
        self.controller = controller
        self.joueur = None  # Le joueur du client actif
        self.joueurs = {}  # La totalité des joueurs et de leurs unités
        self.grandeurMat = 106
        self.carte = Carte(self.grandeurMat)
        self.enRessource = []  # TODO ?À mettre dans Joueur?

        self.civNumber = -1  # Numéro de civilisation du joueur représentant le client

    def update(self):
        """ Permet de lancer les commande updates importantes
        """
        # On verifie si la civilisation du client peut évoluer
        if self.joueurs[self.civNumber].canEvolve():
            cmd = Command(cmdType=Command.CIVILISATION_EVOLVE)
            cmd.addData('AGE', self.joueurs[self.civNumber].epoque + 1)
            cmd.addData('CIV', self.civNumber)
            self.controller.sendCommand(cmd)

        # On UPDATE Chacune des civilisations
        [civ.update() for civ in self.joueurs.values()]


    # ## EXECUTION COMMANDES ###
    def executeCommand(self, command):
        """ Exécute une commande
        :param command: la commande à exécuter [Objet Command]
        """
        commands = {

            Command.UNIT_CREATE: self.executeCreateUnit,
            Command.UNIT_MOVE: self.executeMoveUnit,
            Command.UNIT_ATTACK_UNIT: self.executeAttackUnit,
            Command.UNIT_ATTACK_BUILDING: self.executeAttackBuilding,
            Command.UNIT_DIE: self.executeKillUnit,
            Command.UNIT_TAKE_RESSOURCES: self.executeTakeRessources,

            Command.BUILDING_CREATE: self.executeCreateBuilding,
            Command.BUILDING_DESTROY: self.executeDestroyBuilding,

            Command.CIVILISATION_CREATE: self.executeCreateCivilisation,

            Command.CIVILISATION_EVOLVE: self.executeEvolveCivilisation
        }

        try:
            exe = commands[command.data['TYPE']]
        except KeyError:
            raise NotImplementedError("COMMANDE NON IMPLÉMENTÉE...: %s" % command['TYPE'])
        exe(command)

    def executeCreateUnit(self, command):
        """ Execute la commande crééer unité  selon ses paramètres 
        :param command: la commande à exécuter [Objet Command]
        """
        print(self.joueurs)
        if command.data['CLASSE'] == "soldatEpee":
            self.joueurs[command.data['CIV']].createUnitSword(command.data['ID'], command.data['X'], command.data['Y'],
                                                     command.data['CIV'])

        elif command.data['CLASSE'] == "soldatLance":
            self.joueurs[command.data['CIV']].createUnitLance(command.data['ID'], command.data['X'], command.data['Y'],
                                                     command.data['CIV'])

        elif command.data['CLASSE'] == "soldatBouclier":
            self.joueurs[command.data['CIV']].createUnitShield(command.data['ID'], command.data['X'], command.data['Y'],
                                                     command.data['CIV'])

        elif command.data['CLASSE'] == "paysan":
            self.joueurs[command.data['CIV']].createUnit(command.data['ID'], command.data['X'], command.data['Y'],
                                                     command.data['CIV'])

    def executeMoveUnit(self, command):
        """ Execute la commande pour DÉPLACER UNE UNITÉ selon ses paramètres 
        :param command: la commande à exécuter [Objet Commande]
        """
        try:
            unit = self.getUnit(command['ID'])
            unit.changerCible(command.data['X2'], command.data['Y2'], command.data['GROUPE'], command.data['FIN'],
                              command.data['LEADER'], command.data['ENNEMI'], command.data['BTYPE'], command.data['ABID'])
        except (KeyError, AttributeError):  # On a essayé de déplacer une unité morte
            pass

    def executeAttackUnit(self, command):
        """ Execute la commande ATTAQUER UNE UNITÉ  selon ses paramètres 
        :param command: la commande à exécuter [Objet Commande]
        """
        attacker = self.getUnit(command['SOURCE_ID'])
        target = self.getUnit(command['TARGET_ID'])
        target.recevoirAttaque(self, attacker, command['DMG'])

    def executeAttackBuilding(self, command):
        """ Execute la commande ATTAQUER UN BATIMENT  selon ses paramètres
        :param command: la commande à exécuter [Objet Commande]
        """
        attacker = self.getUnit(command['SOURCE_ID'])
        targetBuilding = self.getBuilding(command['TARGET_ID'])
        targetBuilding.recevoirAttaque(self, attacker, command['DMG'])

    def executeKillUnit(self, command):
        """ Execute la commande TUER UNE UNITÉ selon ses paramètres
        :param command: la commande à exécuter [Objet Commande]
        """
        try:
            civId = self.getUnit(command['ID']).getClientId()
            self.joueurs[civId].killUnit(command['ID'])
        except AttributeError:  # On a essayé de tuer Une unité déjà morte
            print("UNIT DÉJÀ MORTE?")  # TODO Comprendre pourquoi

    def executeTakeRessources(self, command):
        civId = self.getUnit(command['ID']).getClientId()
        nbRessources = self.carte.matrice[command['X1']][command['Y1']].nbRessources

        if nbRessources >= command['NB_RESSOURCES']:
            self.carte.matrice[command['X1']][command['Y1']].nbRessources -= command['NB_RESSOURCES']

            if self.joueur.civilisation == civId or isinstance(self.getUnit(command['ID']).joueur, AI):
                self.getUnit(command['ID']).nbRessources += command['NB_RESSOURCES']
        else:
            if self.joueur.civilisation == civId or isinstance(self.getUnit(command['ID']).joueur, AI):
                self.getUnit(command['ID']).nbRessources += self.carte.matrice[command['X1']][
                    command['Y1']].nbRessources
            #self.carte.matrice[command['X1']][command['Y1']].nbRessources = 0
        if self.carte.matrice[command['X1']][command['Y1']].nbRessources <= 0:
            self.carte.matrice[command['X1']][command['Y1']].type = 0  # Gazon -> n'est plus une ressource
            self.carte.matrice[command['X1']][command['Y1']].isWalkable = True
            self.controller.view.update(self.getUnits(), self.getBuildings(),
                                        self.carte.matrice)
        print("reste", self.carte.matrice[command['X1']][command['Y1']].nbRessources, self.getUnit(command['ID']).mode)
        # self.controller.view.frameMinimap.updateMinimap(self.carte.matrice)
        #TODO: Mettre mini map à jour !!!

    def executeCreateBuilding(self, command):
        """ Execute la commande CRÉER UN BÂTIMENT  selon ses paramètres
        :param command: la commande à exécuter [Objet Commande]
        """
        print("batient reseaux...")
        if command['BTYPE'] == 0: #Base TEMPORAIRE !
            self.joueurs[command.data['CIV']].createBuilding(command['ID'], command['X'], command['Y'],
                                                         command['BTYPE'])

    def executeDestroyBuilding(self, command):
        blupid = command.data['ABID']
        print("Le batiment "+blupid+" vient de mourrir!")
        civ = command.data['CIV']
        self.joueurs[civ].destroyBuilding(blupid)
        unitId = command.data['ATTID']
        self.getUnit(unitId).mode = 0

    def executeCreateCivilisation(self, command):
        """ Execute la commande CRÉER UNE CIVILISATION  selon ses paramètres
        :param command: la commande à exécuter [Objet Commande]
        """
        self.creerJoueur(command['ID'])
        # TODO CRÉER BASE



    def executeEvolveCivilisation(self, command):
        """ Execute la commande CHANGER AGE CIVILISATION  selon ses paramètres
        :param command: la commande à exécuter [Objet Commande]
        """
        self.joueurs[command.data['CIV']].changerAge(command['AGE'])













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
        # TODO TROUVER PAR CADRAN...
        #TODO TROUVER TOUT LE TEMPS UNE RÉPONSE
        #Marche si pas plus de 9 unités
        for multi in range(1, self.grandeurMat):
            for i in liste:
                for j in liste:
                    if not (i == 0 and j == 0 and multi == 1):
                        #print(multi*i,multi*j)
                        posX = cibleX + multi * i
                        posY = cibleY + multi * j
                        if (posX == cibleX and posY == cibleY):
                            break  #Même position que le leader
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

    def trouverRessourcePlusPres(self, unit, typeRessource):
        ressource = {"x" : 0 , "y" : 0}

        minX = int(unit.x)
        minY = int(unit.y)
        maxX = int(unit.x)
        maxY = int(unit.y)
        found = False

        while not found:
            print("start check")
            minX = minX - 144
            minY = minY - 144
            maxX += 144
            maxY += 144
            print(minX, minY)
            #si le minimum des X à vérifier est va à moins de 0, mettre à 0
            if minX < 0:
                minX = 0

            #si le minimum des Y à vérifier est va à moins de 0, mettre à 0
            if minY < 0:
                minY = 0

            #si le maximum des X à vérifier est plus grand que la taille de la map, le mettre au max de la map
            #taille de la map * 48 parceque la taille de la map est en tuiles et chaque tuile est de 48 pixels
            if maxX > self.carte.size * 48:
                maxX = self.carte.size * 48

            #si le maximum des Y à vérifier est plus grand que la taille de la map, le mettre au max de la map
            #taille de la map * 48 parceque la taille de la map est en tuiles et chaque tuile est de 48 pixels
            if maxY > self.carte.size * 48:
                maxY = self.carte.size * 48

            print(maxX)
            print(maxY)
            print(minX)
            print(minY)

            for x in range (minX, maxX, 48):
                for y in range (minY, maxY, 48):
                    casesCible = self.trouverCaseMatrice(x, y)
                    caseCibleX = casesCible[0]
                    caseCibleY = casesCible[1]
                    if self.carte.matrice[caseCibleX][caseCibleY].type == typeRessource:
                        ressource["x"] = x
                        ressource["y"] = y
                        print("!", x,y)
                        return ressource

    def validPosBuilding(self, caseX, caseY):
        """Regarde si on peut construire à cette endroit un building
        :param caseX: la case en X du bâtiment
        :param caseY: la case en Y du bâtiment
        """
        if not self.carte.matrice[caseX][caseY].isWalkable:
            print("not walkable")
            return False
        if not self.carte.matrice[caseX + 1][caseY].isWalkable:
            print("not walkable")
            return False
        if not self.carte.matrice[caseX][caseY + 1].isWalkable:
            print("not walkable")
            return False
        if not self.carte.matrice[caseX + 1][caseY + 1].isWalkable:
            print("not walkable")
            return False
        
        return True

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
        self.joueurs[clientId].ressources['bois'] += 100

    def getUnits(self):
        """ Retoune la totalité des unités de toutes les civilisations
        """
        return {uId: u for civ in self.joueurs.values() for uId, u in civ.units.items()}

    def getBuildings(self):
        """ Retoune la totalité des bâtiments de toutes les civilisations
        """
        return {bId: b for civ in self.joueurs.values() for bId, b in civ.buildings.items()}

    def creerAI(self, clientId):
        """  Permet de crééer un joueur et de l'ajouter à la liste des joueurs
        :param clientId: L'id du client
        """
        self.joueurs[clientId] = AI(clientId, self)

    def creerbaseAI(self, clientId):
        idBase = Batiment.generateId(clientId)

        cmd = Command(clientId, Command.BUILDING_CREATE)
        cmd.addData('ID', idBase)
        cmd.addData('X', 400)
        cmd.addData('Y', 600)
        cmd.addData('CIV', clientId)
        cmd.addData('BTYPE', Batiment.BASE)
        self.controller.sendCommand(cmd)

        self.joueurs[clientId].base = self.getBuilding(idBase)















