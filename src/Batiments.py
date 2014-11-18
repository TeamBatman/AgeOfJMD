#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from PIL import Image, ImageTk
from GraphicsManagement import GraphicsManager


# TODO trouver des valeurs correctes pour le prix en ressources des unités et batiments
# TODO L'hopital ne fait rien avec le healing
# TODO le FOW pour la tour de guet
from Units import Unit
from Units import Noeud
from Commands import Command


class Batiment:
    COUNT = 0  # Un compteur permettant d'avoir un Id unique pour chaque batiment

    BASE = 0
    FERME = 1
    BARAQUE = 2
    HOPITAL = 3
    TOUR_GUET = 4
    LIEU_CULTE = 5
    SCIERIE = 6
    FONDERIE = 7
    GARAGE = 8


    def __init__(self, parent, bid, posX, posY):
        self.posX = posX
        self.posY = posY
        self.id = bid
        self.peutEtreOccupe = False
        self.estOccupe = False
        self.pointsDeVie = 100
        self.estSelectionne = False
        self.tailleX = 128  # Taille en pixels
        self.tailleY = 128  # Taille en pixels
        self.type = ""
        self.image = None
        self.joueur = parent
        self.rechercheCompletee = False
        self.enRecherche = False  # booléen pour empecher de recommencer la fonction de recherche si l'on est déjà en recherche
        self.enCreation = False  # booléen pour empecher de recommencer la fonction de création si l'on est déjà en création
        self.tempsDepartRecherche = 0
        self.tempsDepartCreation = 0
        self.coutRecherche1 = {'bois': 0, 'minerai': 0, 'charbon': 0}
        self.coutRecherche2 = {'bois': 0, 'minerai': 0, 'charbon': 0}
        self.coutCreer1 = {'bois': 0, 'minerai': 0, 'charbon': 0}
        self.coutCreer2 = {'bois': 0, 'minerai': 0, 'charbon': 0}
        self.coutCreer3 = {'bois': 0, 'minerai': 0, 'charbon': 0}

    def getClientId(self):
        """ Returns the Id of the client using the id of the unit
        :return: the id of the clients
        """
        return self.id.split('_')[0]

    def estBatimentDe(self, clientId):
        """ Vérifie si le batiment appartient au client ou non
        :param clientId: le client à tester
        :return: True si elle lui appartient Sinon False
        """
        masterId = int(self.getClientId())
        clientId = int(clientId)
        return masterId == clientId

    @staticmethod
    def generateId(clientId):
        gId = "%s_%s" % (clientId, Batiment.COUNT)
        Batiment.COUNT += 1
        return gId


    def detruire(self):
        self.sortirUnites()
        for batiment in self.joueur.batiments:
            if batiment.posX == self.posX:
                if batiment.posY == self.posY:
                    self.joueur.batiments.remove(batiment)
                    self.retourRessources()
                    return

    def retourRessources(self):
        # A trouver les valeurs à retourner
        if self.type == "Base":
            self.joueur.bois += 100
        elif self.type == "Eglise":
            self.joueur.bois += 50
            self.joueur.minerais += 50
        elif self.type == "Tour de guet":
            self.joueur.bois += 50
            self.joueur.minerais += 50
        elif self.type == "Baraque":
            self.joueur.bois += 50
            self.joueur.minerais += 50
        elif self.type == "Hopital":
            self.joueur.bois += 50
            self.joueur.minerais += 50
            self.joueur.charbon += 50
        elif self.type == "Garage":
            self.joueur.bois += 50
            self.joueur.minerais += 50
            self.joueur.charbon += 50
        elif self.type == "Ferme":
            self.joueur.bois += 50
        elif self.type == "Scierie":
            self.joueur.bois += 50
            self.joueur.minerais += 50
        elif self.type == "Fonderie":
            self.joueur.bois += 50
            self.joueur.minerais += 50
            self.joueur.charbon += 50

    def sortirUnites(self):
        # verifie si le batiment peut etre occupe puis s'il y a des unites dedans et les sort
        if self.peutEtreOccupe == True:
            if self.estOccupe == True:
                for i in range(0, self.joueur.unites):
                    if self.joueur.unites[i].batiment == self:
                        self.joueur.unites[i].batiment == None


class Eglise(Batiment):
    def __init__(self, parent, bid, posX, posY):
        super().__init__(parent, bid, posX, posY)
        self.type = Batiment.LIEU_CULTE
        self.tempsDerniereFete = 0
        self.coutRecherche1['bois'] = 50


    def recherche1(self):  # Boost Moral
        if self.joueur.epoque == 2:
            if self.enRecherche == False:
                if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                    if time.time() - self.tempsDerniereFete >= 60:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
            elif time.time() - self.tempsDepartRecherche <= 60:
                self.joueur.moral = 100
                self.enRecherche = False
                self.tempsDerniereFete = time.time()
        else:
            if self.enRecherche == False:
                if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                    self.joueur.moral = 100
                    self.enRecherche = False
                    self.tempsDerniereFete = time.time()

    def miseAJour(self):
        if self.enRecherche:
            self.recherche1()


class TourDeGuet(Batiment):
    def __init__(self, parent, bid, posX, posY):
        super().__init__(parent, bid, posX, posY)
        self.type = Batiment.TOUR_GUET
        self.coutRecherche1['bois'] = 50

    def recherche1(self):  # Meilleure vue du Fog of war
        self.rechercheCompletee = False
        if self.joueur.epoque == 2:
            for recherche in self.joueur.recherche:
                if recherche == "Tour1":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche <= 60:
                    #TODO Decouverir comment le FOW fonctionnera
                    self.enRecherche = False
                    self.joueur.recherche.append("Tour1")

        else:
            for recherche in self.joueur.recherche:
                if recherche == "Tour2":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche <= 60:
                    #TODO Decouverir comment le FOW fonctionnera
                    self.enRecherche = False
                    self.joueur.recherche.append("Tour2")

        self.rechercheCompletee = False

    def miseAJour(self):
        if self.enRecherche:
            self.recherche1()


class Hopital(Batiment):
    def __init__(self, parent, bid, posX, posY):
        super().__init__(parent, bid, posX, posY)
        self.type = Batiment.HOPITAL
        self.peutEtreOccupe = True
        self.vitesseDeCreation = 30
        self.coutRecherche1['bois'] = 50

    def healing(self, unite):
        # TODO decouvrir comment le healing va se faire
        #TODO ajouter le temps de recherche
        pass

    def recherche1(self):  # Amélioration du healing
        self.rechercheCompletee = False
        for recherche in self.joueur.recherche:
            if recherche == "Hopital":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                    self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
            elif time.time() - self.tempsDepartRecherche <= 60:
                self.enRecherche = False
                self.joueur.recherche.append("Hopital")
                #TODO decouvrir comment la regeneration va se faire

    def miseAJour(self):
        if self.enRecherche:
            self.recherche1()


class Base(Batiment):
    def __init__(self, parent, bid, posX, posY):
        super().__init__(parent, bid, posX, posY)
        self.type = Batiment.BASE
        self.rawImage = GraphicsManager.getImage('Graphics/Buildings/Age_I/Base.png')
        self.resized = self.rawImage.resize((96, 96), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.resized)
        self.vitesseDeCreation = 10
        self.coutRecherche1['bois'] = 50
        self.coutRecherche2['bois'] = 50
        self.coutRecherche2['minerai'] = 50
        self.coutCreer1['bois'] = 50
        print(posX, posY)
        cases = self.joueur.model.trouverCentreCase(posX, posY)
        self.joueur.base = Noeud(None, cases[0], cases[1], None, None)
        self.typeRecherche = None


    def creer1(self):  # création des paysans
        #print("creaa", self.posX,self.posY,self.enCreation, time.time() - self.tempsDepartCreation , self.vitesseDeCreation)
        if not self.enCreation:
            if self.joueur.ressources['bois'] >= self.coutCreer1['bois']:
                self.joueur.ressources['bois'] -= self.coutCreer1['bois']
                self.enCreation = True
                self.tempsDepartCreation = time.time()
                print("creation",self.enCreation)

        elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
            posXUnit, posYUnit = self.joueur.model.trouverCentreCase(self.posX-1, self.posY-1)
            print("UNIT",posXUnit,posYUnit )
            cmd = Command(self.joueur.civilisation, Command.CREATE_UNIT)
            cmd.addData('ID', Unit.generateId(self.joueur.civilisation))
            cmd.addData('X', posXUnit)
            cmd.addData('Y', posYUnit)
            cmd.addData('CIV', self.joueur.civilisation)
            self.joueur.model.controller.network.client.sendCommand(cmd)
            print("Paysan créé?")
            self.enCreation = False


    def recherche1(self):  # meilleure vitesse de création de paysans
        self.rechercheCompletee = False
        if self.joueur.epoque == 1:
            for recherche in self.joueur.recherche:
                if recherche == "Paysan Vitesse 1":
                    self.rechercheCompletee = True
            if not self.rechercheCompletee:
                if not self.enRecherche:
                    if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.typeRecherche = 1
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche <= 60:
                    self.enRecherche = False
                    self.vitesseDeCreation *= 0.9
                    self.rechercheCompletee = False
                    self.typeRecherche = None
                    self.joueur.recherche.append("Paysan Vitesse 1")

        elif self.joueur.epoque == 2:
            for recherche in self.joueur.recherche:
                if recherche == "Paysan Vitesse 2":
                    self.rechercheCompletee = True
            if not self.rechercheCompletee:
                if not self.enRecherche:
                    if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.typeRecherche = 1
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.enRecherche = False
                    self.typeRecherche = None
                    self.vitesseDeCreation *= 0.9
                    self.rechercheCompletee = False
                    self.joueur.recherche.append("Paysan Vitesse 2")

        else:
            for recherche in self.joueur.recherche:
                if recherche == "Paysan Vitesse 3":
                    self.rechercheCompletee = True
            if not self.rechercheCompletee:
                if not self.enRecherche:
                    if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.typeRecherche = 1
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.rechercheCompletee = False
                    self.enRecherche = False
                    self.typeRecherche = None
                    self.vitesseDeCreation = self.vitesseDeCreation * 0.9
                    self.joueur.recherche.append("Paysan Vitesse 3")

    def recherche2(self):  # changer d'époque
        self.rechercheCompletee = False
        if self.joueur.epoque == 1:
            for recherche in self.joueur.recherche:
                if recherche == "Époque 2":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources['bois'] >= self.coutRecherche2['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche2['bois']
                        self.enRecherche = True
                        self.typeRecherche = 2
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.enRecherche = False
                    self.joueur.epoque = 2
                    self.typeRecherche = None
                    self.joueur.recherche.append("Époque 2")
                    print("époque changée")
        elif self.joueur.epoque == 2:
            for recherche in self.joueur.recherche:
                if recherche == "Époque 3":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources['bois'] >= self.coutRecherche2['bois'] and self.joueur.ressources['minerai'] >= self.coutRecherche2['minerai']:
                        self.joueur.ressources['bois'] -= self.coutRecherche2['bois']
                        self.joueur.ressources['minerai'] -= self.coutRecherche2['minerai']
                        self.enRecherche = True
                        self.typeRecherche = 2
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.enRecherche = False
                    self.joueur.epoque = 2
                    self.joueur.recherche.append("Époque 3")
                    self.typeRecherche = None
                    print("époque changée")

    def miseAJour(self):
        if self.enCreation:
            self.creer1()
        if self.enRecherche:
            if self.typeRecherche == 1:
                self.recherche1()
            else:
                self.recherche2()


class Baraque(Batiment):
    def __init__(self, parent, bid, posX, posY):
        super().__init__(parent, bid, posX, posY)
        self.type = Batiment.BARAQUE
        self.vitesseDeCreation = 40
        self.typeCreation = ""
        self.typeRecherche = ""
        self.coutRecherche1['bois'] = 50
        self.coutRecherche2['bois'] = 50
        self.coutCreer1['bois'] = 50
        self.coutCreer2['bois'] = 50
        self.coutCreer3['bois'] = 50



    def creer1(self):  # création de soldats avec épée
        if self.enCreation == False:
            if self.joueur.ressources['bois'] >= self.coutCreer1['bois']:
                self.joueur.ressources['bois'] -= self.coutCreer1['bois']
                self.enCreation = True
                self.typeCreation = "Epee"
                self.tempsDepartCreation = time.time()
        elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
            cmd = Command(self.joueur.civilisation, Command.CREATE_UNIT)
            cmd.addData('ID', Unit.generateId(self.joueur.civilisation))
            cmd.addData('X', self.posX + 10)
            cmd.addData('Y', self.posY + 10)
            cmd.addData('CIV', self.joueur.civilisation)
            self.joueur.parent.controller.network.client.sendCommand(cmd)
            self.enCreation = False


    def creer2(self):  # création de soldats avec lances
        if self.enCreation == False:
            if self.joueur.ressources['bois'] >= self.coutCreer2['bois']:
                self.joueur.ressources['bois'] -= self.coutCreer2['bois']
                self.enCreation = True
                self.typeCreation = "Lance"
                self.tempsDepartCreation = time.time()
        elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
            cmd = Command(self.joueur.civilisation, Command.CREATE_UNIT)
            cmd.addData('ID', Unit.generateId(self.joueur.civilisation))
            cmd.addData('X', self.posX + 10)
            cmd.addData('Y', self.posY + 10)
            cmd.addData('CIV', self.joueur.civilisation)
            self.joueur.parent.controller.network.client.sendCommand(cmd)
            self.enCreation = False


    def creer3(self):  # création de soldats avec boucliers
        if self.enCreation == False:
            if self.joueur.ressources['bois'] >= self.coutCreer3['bois']:
                self.joueur.ressources['bois'] -= self.coutCreer3['bois']
                self.enCreation = True
                self.typeCreation = "Bouclier"
                self.tempsDepartCreation = time.time()
        elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
            cmd = Command(self.joueur.civilisation, Command.CREATE_UNIT)
            cmd.addData('ID', Unit.generateId(self.joueur.civilisation))
            cmd.addData('X', self.posX + 10)
            cmd.addData('Y', self.posY + 10)
            cmd.addData('CIV', self.joueur.civilisation)
            self.joueur.parent.controller.network.client.sendCommand(cmd)
            self.enCreation = False


    def recherche1(self):  # meilleure attaque
        self.rechercheCompletee = False
        if self.joueur.epoque == 2:
            for recherche in self.joueur.recherche:
                if recherche == "Soldat Attaque 1":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                        self.typeRecherche = "Attaque"

                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.enRecherche = False
                    for unite in self.joueur.units:
                        if isinstance(unite, Soldat):
                            unite.attaque = unite.attaque * 1.1
                    self.rechercheCompletee = False
                    self.joueur.recherche.append("Soldat Attaque 1")

        else:
            for recherche in self.joueur.recherche:
                if recherche == "Soldat Attaque 2":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                        self.typeRecherche = "Attaque"

            elif time.time() - self.tempsDepartRecherche >= 60:
                self.enRecherche = False
                for unite in self.joueur.units:
                    if isinstance(unite, Soldat):
                        unite.attaque = unite.attaque * 1.1
                self.rechercheCompletee = False
                self.joueur.recherche.append("Soldat Attaque 2")


    def recherche2(self):  # meilleure vitesse de création
        self.rechercheCompletee = False
        if self.joueur.epoque == 2:
            for recherche in self.joueur.recherche:
                if recherche == "Soldat Vitesse 1":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources['bois'] >= self.coutRecherche2['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche2['bois']
                        self.enRecherche = True
                        self.typeRecherche = "Vitesse"
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.vitesseDeCreation = self.vitesseDeCreation * 0.9
                    self.rechercheCompletee = False
                    self.joueur.recherche.append("Soldat Vitesse 1")
                    self.enRecherche = False

        else:
            for recherche in self.joueur.recherche:
                if recherche == "Soldat Vitesse 2":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources['bois'] >= self.coutRecherche2['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche2['bois']
                        self.enRecherche = True
                        self.typeRecherche = "Vitesse"
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.vitesseDeCreation = self.vitesseDeCreation * 0.9
                    self.rechercheCompletee = False
                    self.enRecherche = False
                    self.joueur.recherche.append("Soldat Vitesse 2")


    def miseAJour(self):
        if self.enCreation:
            if self.typeCreation == "Epee":
                self.creer1()
            elif self.typeCreation == "Lance":
                self.creer2()
            else:
                self.creer3()
        if self.enRecherche:
            if self.typeRecherche == "Attaque":
                self.recherche1()
            else:
                self.recherche2()


class Ferme(Batiment):
    def __init__(self, parent, bid, posX, posY):
        super().__init__(parent, bid, posX, posY)
        self.tailleX = 128
        self.tailleY = 128
        self.peutEtreOccupe = True
        self.production = 10
        self.tempsProduction = 10
        self.type = Batiment.FERME
        self.rawImage = GraphicsManager.getImage('Graphics/Buildings/Age_I/Farm.png')
        self.resized = self.rawImage.resize((96, 96), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.resized)
        self.coutRecherche1['bois'] = 50

    def produire(self):
        # TODO a se renseigner sur les valeurs pour la production
        if self.estOccupe:
            if time.time() - self.tempsProduction >= 10:
                self.joueur.nourriture += self.production
                self.tempsProduction = time.time()


    def recherche1(self):  # meilleure vitesse de production
        self.rechercheCompletee = False
        if self.joueur.epoque == 1:
            for recherche in self.joueur.recherche:
                if recherche == "Ferme 1":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.rechercheCompletee = False
                    self.enRecherche = False
                    self.joueur.recherche.append("Ferme 1")

        elif self.joueur.epoque == 2:
            for recherche in self.joueur.recherche:
                if recherche == "Ferme 2":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.rechercheComplete = False
                    self.enRecherche = False
                    self.joueur.recherche.append("Ferme 2")

        else:
            for recherche in self.joueur.recherche:
                if recherche == "Ferme 3":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.rechercheCompletee = False
                    self.enRecherche = False
                    self.joueur.recherche.append("Ferme 3")

    def miseAJour(self):
        if self.enRecherche:
            self.recherche1()

        self.produire()


class Scierie(Batiment):
    def __init__(self, parent, bid, posX, posY):
        super().__init__(parent, bid, posX, posY)
        self.peutEtreOccupe = True
        self.production = 10
        self.tempsProduction = 10
        self.coutRecherche1['bois'] = 50
        self.type = Batiment.SCIERIE

    def produire(self):
        # TODO a se renseigner sur les valeurs pour la production
        if self.estOccupe:
            if time.time() - self.tempsProduction >= 10:
                self.joueur.bois += self.production
                self.tempsProduction = time.time()

    def recherche1(self):  # meilleure vitesse de production
        self.rechercheCompletee = False
        if self.joueur.epoque == 2:
            for recherche in self.joueur.recherche:
                if recherche == "Scierie 1":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.rechercheCompletee = False
                    self.enRecherche = False
                    self.joueur.recherche.append("Scierie 1")

        else:
            for recherche in self.joueur.recherche:
                if recherche == "Scierie 2":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.rechercheCompletee = False
                    self.enRecherche = False
                    self.joueur.recherche.append("Scierie 2")

    def miseAJour(self):
        if self.enRecherche:
            self.recherche1()

        self.produire()


class Fonderie(Batiment):
    def __init__(self, parent, bid, posX, posY):
        super().__init__(parent, bid, posX, posY)
        self.peutEtreOccupe = True
        self.production = 10
        self.tempsProduction = 10
        self.coutRecherche1['bois'] = 50
        self.type = Batiment.FONDERIE

    def produire(self):
        # TODO a se renseigner sur les valeurs pour la production
        if self.estOccupe:
            if time.time() - self.tempsProduction >= 10:
                self.joueur.minerais += self.production
                self.tempsProduction = time.time()

    def recherche1(self):  # meilleure vitesse de production
        self.rechercheCompletee = False
        for recherche in self.joueur.recherche:
            if recherche == "Fonderie 1":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                    self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
        elif time.time() - self.tempsDepartRecherche >= 60:
            self.production = self.production * 1.1
            self.rechercheCompletee = False
            self.enRecherche = False
            self.joueur.recherche.append("Fonderie 1")

    def miseAJour(self):
        if self.enRecherche:
            self.recherche1()

        self.produire()


class Garage(Batiment):
    def __init__(self, parent, bid, posX, posY):
        super().__init__(parent, bid, posX, posY)
        self.vitesseDeCreation = 60
        self.typeRecherche = ""
        self.coutRecherche1['bois'] = 50
        self.coutRecherche2['bois'] = 50
        self.coutCreer1['bois'] = 50
        self.type = Batiment.GARAGE

    def creer1(self):  # créer des tanks
        if self.enCreation == False:
            if self.joueur.ressources['bois'] >= self.coutCreer1['bois']:
                self.joueur.ressources['bois'] -= self.coutCreer1['bois']
                self.enCreation = True
                self.tempsDepartCreation = time.time()
        elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
            self.enCreation = False
            cmd = Command(self.joueur.civilisation, Command.CREATE_UNIT)
            cmd.addData('ID', Unit.generateId(self.joueur.civilisation))
            cmd.addData('X', self.posX + 10)
            cmd.addData('Y', self.posY + 10)
            cmd.addData('CIV', self.joueur.civilisation)
            self.joueur.parent.controller.network.client.sendCommand(cmd)

    def recherche1(self):  # meilleure vitesse de création de tanks
        self.rechercheCompletee = False
        for recherche in self.joueur.recherche:
            if recherche == "Tank Vitesse":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.joueur.ressources['bois'] >= self.coutRecherche1['bois']:
                    self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
                    self.typeRecherche = "Vitesse"
            elif time.time() - self.tempsDepartRecherche >= 60:
                self.rechercheCompletee = False
                self.enRecherche = False
                self.vitesseDeCreation = self.vitesseDeCreation * 0.8
                self.joueur.recherche.append("Tank Vitesse")

    def recherche2(self):  # amélioration du HP des tanks
        self.rechercheCompletee = False
        for recherche in self.joueur.recherche:
            if recherche == "Tank HP":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.joueur.ressources['bois'] >= self.coutRecherche2['bois']:
                    self.joueur.ressources['bois'] -= self.coutRecherche2['bois']
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
                    self.typeRecherche = "HP"
            elif time.time() - self.tempsDepartRecherche >= 60:
                self.rechercheCompletee = False
                self.enRecherche = False
                self.joueur.recherche.append("Tank HP")
                for tank in self.joueur.units:
                    if isinstance(tank, Tank):
                        tank.hpMax = 120

    def miseSJour(self):
        if self.enCreation:
            self.creer1()
        if self.enRecherche:
            if self.typeRecherche == "Vitesse":
                self.recherche1()
            else:
                self.recherche2()
