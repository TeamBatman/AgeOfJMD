#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from PIL import Image, ImageTk
from Commands import Command
from GraphicsManagement import GraphicsManager, OneTimeAnimation


# TODO trouver des valeurs correctes pour le prix en ressources des unités et batiments
# TODO L'hopital ne fait rien avec le healing
# TODO le FOW pour la tour de guet
from Units import Unit
from Units import Noeud
from Civilisations import Civilisation


class Batiment:
    COUNT = 0  # Un compteur permettant d'avoir un Id unique pour chaque batiment

    BASE = 0
    FERME = 1
    BARAQUE = 2
    HOPITAL = 3
    TOUR_GUET = 4
    LIEU_CULTE = 5


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
        self.determineImage()

        self.oneTimeAnimations = []

    def getClientId(self):
        """ Returns the Id of the client using the id of the building
        :return: the id of the clients
        """
        return int(self.id.split('_')[0])

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

    def determineImage(self):
        raise Exception("La méthode determineImage doit être surchargée par tous les sous-classes de Unit et doit ")

    def recevoirAttaque(self, model, attacker, dommage):
        """ Recois les dommages d'une commande d'attaque
        :param attacker: unité qui la attaquer
        :param dommage:  dommage causé par l'attaquant
        """
        print(self.pointsDeVie)

        self.pointsDeVie -= dommage

        anim = OneTimeAnimation(GraphicsManager.getAnimationSheet('Animations/mayoche.png', 1, 3), 50)
        self.oneTimeAnimations.append(anim)


        if self.pointsDeVie <= 0:
            self.pointsDeVie = 0  # building mort
            cmd = Command(self.getClientId(), Command.BUILDING_DESTROY)

            cmd.addData('ID', self.id)
            cmd.addData('ABID', self.id)
            cmd.addData('ATTID', attacker.id)
            cmd.addData('CIV', self.getClientId())
            model.controller.sendCommand(cmd)


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
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "eglise"
        self.tempsDerniereFete = 0
        self.coutRecherche1['bois'] = 50


    def recherche1(self):  # Boost Moral
        if self.joueur.epoque == 2:
            if self.enRecherche == False:
                if self.joueur.ressources >= self.coutRecherche1:
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
                if self.joueur.ressources >= self.coutRecherche1:
                    if time.time() - self.tempsDerniereFete >= 60:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
            elif time.time() - self.tempsDepartRecherche <= 120:
                self.joueur.moral = 100
                self.enRecherche = False
                self.tempsDerniereFete = time.time()

    def miseAJour(self):
        if self.enRecherche:
            self.recherche1()


class TourDeGuet(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "tour"
        self.coutRecherche1['bois'] = 50

    def recherche1(self):  # Meilleure vue du Fog of war
        self.rechercheCompletee = False
        if self.joueur.epoque == 2:
            for recherche in self.joueur.recherche:
                if recherche == "Tour1":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources >= self.coutRecherche1:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche <= 60:
                    # TODO Decouverir comment le FOW fonctionnera
                    self.enRecherche = False
                    self.joueur.recherche.append("Tour1")

        else:
            for recherche in self.joueur.recherche:
                if recherche == "Tour2":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources >= self.coutRecherche1:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche <= 60:
                    # TODO Decouverir comment le FOW fonctionnera
                    self.enRecherche = False
                    self.joueur.recherche.append("Tour2")

        self.rechercheCompletee = False

    def miseAJour(self):
        if self.enRecherche:
            self.recherche1()


class Hopital(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "hopital"
        self.peutEtreOccupe = True
        self.vitesseDeCreation = 30
        self.coutRecherche1['bois'] = 50

    def healing(self, unite):
        # TODO decouvrir comment le healing va se faire
        # TODO ajouter le temps de recherche
        pass

    def recherche1(self):  # Amélioration du healing
        self.rechercheCompletee = False
        for recherche in self.joueur.recherche:
            if recherche == "Hopital":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.joueur.ressources >= self.coutRecherche1:
                    self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
            elif time.time() - self.tempsDepartRecherche <= 60:
                self.enRecherche = False
                self.joueur.recherche.append("Hopital")
                # TODO decouvrir comment la regeneration va se faire

    def miseAJour(self):
        if self.enRecherche:
            self.recherche1()


class Base(Batiment):
    def __init__(self, parent, bid, posX, posY):
        super().__init__(parent, bid, posX, posY)
        self.type = "base"
        self.determineImage()
        self.vitesseDeCreation = 3
        self.coutRecherche1['bois'] = 50
        self.coutRecherche2['bois'] = 50
        self.coutRecherche2['minerai'] = 50
        self.coutCreer1['bois'] = 5
        self.paysanAFaire = 0 #Le nombre de paysan à faire (Queue)
        print(posX, posY)
        cases = self.joueur.model.trouverCentreCase(posX, posY)
        self.joueur.base = Noeud(None, cases[0], cases[1], None, None)


    def determineImage(self):
        #self.image = GraphicsManager.getPhotoImage('Graphics/Buildings/Age_I/Base.png')
        """self.rawImage = GraphicsManager.getImage('Graphics/Buildings/Age_I/Base.png')
        self.resized = self.rawImage.resize((96, 96), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.resized)"""
        ageString = {1: 'Age_I', 2: 'Age_II', 3: 'Age_III'}
        age = ageString[self.joueur.epoque]

        baseImages = {
            Civilisation.BLANC: 'Buildings/%s/Base/base_blanche.png' % age,
            Civilisation.BLEU: 'Buildings/%s/Base/base_bleue.png' % age,
            Civilisation.JAUNE: 'Buildings/%s/Base/base_jaune.png' % age,

            Civilisation.MAUVE: 'Buildings/%s/Base/base_mauve.png' % age,
            Civilisation.NOIR: 'Buildings/%s/Base/base_noire.png' % age,
            Civilisation.ORANGE: 'Buildings/%s/Base/base_orange.png' % age,

            Civilisation.ROUGE: 'Buildings/%s/Base/base_rouge.png' % age,
            Civilisation.VERT: 'Buildings/%s/Base/base_verte.png' % age,
            Civilisation.ROSE: 'Buildings/%s/Base/base_rose.png' % age
        }
        img = GraphicsManager.getImage(baseImages[self.joueur.civilisation])
        resized = img.resize((96, 96), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)






    def creer1(self):  # création des paysans
        if self.joueur.ressources['bois'] >= self.coutCreer1['bois']:
            print("in creation 1", self.paysanAFaire)
            self.joueur.ajouterRessource('bois', -self.coutCreer1['bois'])
            #self.joueur.ressources['bois'] -= self.coutCreer1['bois']
            self.paysanAFaire += 1
            civ = self.getClientId()
            if self.joueur.civilisation == civ:
                self.joueur.model.controller.view.frameBottom.updateResources(self.joueur)
            if not self.enCreation:
                self.tempsDepartCreation = time.time()
                self.enCreation = True

    def updateCreer1(self):
        if self.enCreation and time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
            print("creating lalala", self.paysanAFaire)
            posUnitX,posUnitY = self.joueur.model.trouverCentreCase(self.posX-1,self.posY-1)
            cmd = Command(self.joueur.civilisation, Command.UNIT_CREATE)
            cmd.addData('ID', Unit.generateId(self.joueur.civilisation))
            cmd.addData('X', posUnitX)
            cmd.addData('Y', posUnitY)
            cmd.addData('CIV', self.joueur.civilisation)
            self.joueur.model.controller.sendCommand(cmd)
            self.paysanAFaire -= 1
            if self.paysanAFaire > 0:
                self.tempsDepartCreation = time.time()
            else:
                self.enCreation = False

    def recherche1(self):  # meilleure vitesse de création de paysans
        self.rechercheCompletee = False
        if self.joueur.epoque == 1:
            for recherche in self.joueur.recherche:
                if recherche == "Paysan Vitesse 1":
                    self.rechercheCompletee = True
            if not self.rechercheCompletee:
                if not self.enRecherche:
                    if self.joueur.ressources >= self.coutRecherche1:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche <= 60:
                    self.enRecherche = False
                    self.vitesseDeCreation *= 0.9
                    self.rechercheCompletee = False
                    self.joueur.recherche.append("Paysan Vitesse 1")

        elif self.joueur.epoque == 2:
            for recherche in self.joueur.recherche:
                if recherche == "Paysan Vitesse 2":
                    self.rechercheCompletee = True
            if not self.rechercheCompletee:
                if not self.enRecherche:
                    if self.joueur.ressources >= self.coutRecherche1:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.enRecherche = False
                    self.vitesseDeCreation *= 0.9
                    self.rechercheCompletee = False
                    self.joueur.recherche.append("Paysan Vitesse 2")

        else:
            for recherche in self.joueur.recherche:
                if recherche == "Paysan Vitesse 3":
                    self.rechercheCompletee = True
            if not self.rechercheCompletee:
                if not self.enRecherche:
                    if self.joueur.ressources >= self.coutRecherche1:
                        self.joueur.ressources['bois'] -= self.coutRecherche1['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.rechercheCompletee = False
                    self.enRecherche = False
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
                    if self.joueur.ressources >= self.coutRecherche2:
                        self.joueur.ressources['bois'] -= self.coutRecherche2['bois']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.enRecherche = False
                    self.joueur.epoque = 2
                    self.joueur.recherche.append("Époque 2")
        elif self.joueur.epoque == 2:
            for recherche in self.joueur.recherche:
                if recherche == "Époque 3":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources >= self.coutRecherche2:
                        self.joueur.ressources['bois'] -= self.coutRecherche2['bois']
                        self.joueur.ressources['minerai'] -= self.coutRecherche2['minerai']
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.enRecherche = False
                    self.joueur.epoque = 2
                    self.joueur.recherche.append("Époque 3")

    def miseAJour(self):
        if self.enCreation:
            self.updateCreer1()
        if self.enRecherche:
            self.recherche1()


class Baraque(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "baraque"
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
        if self.parent.ressources >= self.coutCreer1:
            self.parent.ressources['bois'] -= self.coutCreer1['bois']
            self.enCreation = True
            self.typeCreation = "Epee"
            self.tempsDepartCreation = time.time()
    elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
        self.parent.unites.add(SoldatEpee(self.posX + 4, self.posY + 4, self.parent))
        self.enCreation = False


def creer2(self):  # création de soldats avec lances
    if self.enCreation == False:
        if self.parent.ressources >= self.coutCreer2:
            self.parent.ressources['bois'] -= self.coutCreer2['bois']
            self.enCreation = True
            self.typeCreation = "Lance"
            self.tempsDepartCreation = time.time()
    elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
        self.parent.unites.add(SoldatLance(self.posX + 4, self.posY + 4, self.parent))
        self.enCreation = False


def creer3(self):  # création de soldats avec boucliers
    if self.enCreation == False:
        if self.parent.ressources >= self.coutCreer3:
            self.parent.ressources['bois'] -= self.coutCreer3['bois']
            self.enCreation = True
            self.typeCreation = "Bouclier"
            self.tempsDepartCreation = time.time()
    elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
        self.parent.unites.add(SoldatBouclier(self.posX + 4, self.posY + 4, self.parent))
        self.enCreation = False


def recherche1(self):  # meilleure attaque
    self.rechercheCompletee = False
    if self.parent.epoque == 2:
        for recherche in self.parent.recherche:
            if recherche == "Soldat Attaque 1":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.parent.ressources >= self.coutRecherche1:
                    self.parent.ressources['bois'] -= self.coutRecherche1['bois']
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
                    self.typeRecherche = "Attaque"

            elif time.time() - self.tempsDepartRecherche >= 60:
                self.enRecherche = False
                for unite in self.parent.units:
                    if isinstance(unite, Soldat):
                        unite.attaque = unite.attaque * 1.1
                self.rechercheCompletee = False
                self.parent.recherche.append("Soldat Attaque 1")

    else:
        for recherche in self.parent.recherche:
            if recherche == "Soldat Attaque 2":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.parent.ressources >= self.coutRecherche1:
                    self.parent.ressources['bois'] -= self.coutRecherche1['bois']
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
                    self.typeRecherche = "Attaque"

        elif time.time() - self.tempsDepartRecherche >= 60:
            self.enRecherche = False
            for unite in self.parent.units:
                if isinstance(unite, Soldat):
                    unite.attaque = unite.attaque * 1.1
            self.rechercheCompletee = False
            self.parent.recherche.append("Soldat Attaque 2")


def recherche2(self):  # meilleure vitesse de création
    self.rechercheCompletee = False
    if self.parent.epoque == 2:
        for recherche in self.parent.recherche:
            if recherche == "Soldat Vitesse 1":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.parent.ressources >= self.coutRecherche2:
                    self.parent.ressources['bois'] -= self.coutRecherche2['bois']
                    self.enRecherche = True
                    self.typeRecherche = "Vitesse"
                    self.tempsDepartRecherche = time.time()
            elif time.time() - self.tempsDepartRecherche >= 60:
                self.vitesseDeCreation = self.vitesseDeCreation * 0.9
                self.rechercheCompletee = False
                self.parent.recherche.append("Soldat Vitesse 1")
                self.enRecherche = False

    else:
        for recherche in self.parent.recherche:
            if recherche == "Soldat Vitesse 2":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.parent.ressources >= self.coutRecherche2:
                    self.parent.ressources['bois'] -= self.coutRecherche2['bois']
                    self.enRecherche = True
                    self.typeRecherche = "Vitesse"
                    self.tempsDepartRecherche = time.time()
            elif time.time() - self.tempsDepartRecherche >= 60:
                self.vitesseDeCreation = self.vitesseDeCreation * 0.9
                self.rechercheCompletee = False
                self.enRecherche = False
                self.parent.recherche.append("Soldat Vitesse 2")


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
            recherche2()


class Ferme(Batiment):
    def __init__(self, parent, bid, posX, posY):
        super().__init__(parent, bid, posX, posY)
        self.tailleX = 96
        self.tailleY = 96
        self.peutEtreOccupe = True
        self.unitInBuilding = [] # Les unités dans la ferme
        self.production = 5
        self.tempsProduction = 10
        self.type = "ferme"
        #self.rawImage = GraphicsManager.getImage('Graphics/Buildings/Age_I/Farm.png')
        #self.resized = self.rawImage.resize((self.tailleX, self.tailleY), Image.ANTIALIAS)
        #self.image = ImageTk.PhotoImage(self.resized)
        self.coutRecherche1['bois'] = 50
        self.determineImage()

    def determineImage(self):
        """ Permet de déterminer l'image du bâtiment
        """
        ageString = {1: 'Age_I', 2: 'Age_II', 3: 'Age_III'}
        age = ageString[self.joueur.epoque]

        fermesImages = {
            Civilisation.BLANC: 'Buildings/%s/Ferme/ferme_blanche.png' % age,
            Civilisation.BLEU: 'Buildings/%s/Ferme/ferme_bleue.png' % age,
            Civilisation.JAUNE: 'Buildings/%s/Ferme/ferme_jaune.png' % age,

            Civilisation.MAUVE: 'Buildings/%s/Ferme/ferme_mauve.png' % age,
            Civilisation.NOIR: 'Buildings/%s/Ferme/ferme_noire.png' % age,
            Civilisation.ORANGE: 'Buildings/%s/Ferme/ferme_orange.png' % age,

            Civilisation.ROUGE: 'Buildings/%s/Ferme/ferme_rouge.png' % age,
            Civilisation.VERT: 'Buildings/%s/Ferme/ferme_verte.png' % age,
            Civilisation.ROSE: 'Buildings/%s/Ferme/ferme_rose.png' % age
        }
        img = GraphicsManager.getImage(fermesImages[self.joueur.civilisation])
        resized = img.resize((96, 96), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)

    def produire(self):
        # TODO a se renseigner sur les valeurs pour la production
        if self.unitInBuilding:
            if time.time() - self.tempsProduction >= 10:
                self.joueur.ajouterRessource('nourriture',self.production * len(self.unitInBuilding) )
                #self.joueur.ressources['nourriture'] += self.production * len(self.unitInBuilding)
                civ = self.getClientId()
                self.joueur.model.joueurs[civ].model.controller.view.frameBottom.updateResources(self.joueur.model.joueurs[civ])
                self.tempsProduction = time.time()

    def sortir(self):
        for unit in self.unitInBuilding:
            unit.inBuilding = False
        unitExit = self.unitInBuilding
        self.unitInBuilding = []

        #trouve une case pour mettre les units
        if unitExit:
            cases = self.joueur.model.trouverCentreCase(self.posX, self.posY)
            posFin = self.joueur.model.trouverFinMultiSelection(cases[0],cases[1],1, unitExit[0].grandeur)[0]
            print("fin exit", posFin)
            self.joueur.model.controller.eventListener.onMapRClick(Noeud(None, posFin[0], posFin[1], None, None), unitExit)
            
        #for i in listeI:
        #    for j in listeJ:
                
        

    def recherche1(self):  # meilleure vitesse de production
        self.rechercheCompletee = False
        if self.joueur.epoque == 1:
            for recherche in self.joueur.recherche:
                if recherche == "Ferme 1":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.joueur.ressources >= self.coutRecherche1:
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
                    if self.joueur.ressources >= self.coutRecherche1:
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
                    if self.joueur.ressources >= self.coutRecherche1:
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
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.peutEtreOccupe = True
        self.production = 10
        self.tempsProduction = 10
        self.coutRecherche1['bois'] = 50

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
                    if self.joueur.ressources >= self.coutRecherche1:
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
                    if self.joueur.ressources >= self.coutRecherche1:
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
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.peutEtreOccupe = True
        self.production = 10
        self.tempsProduction = 10
        self.coutRecherche1['bois'] = 50

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
                if self.joueur.ressources >= self.coutRecherche1:
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
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.vitesseDeCreation = 60
        self.typeRecherche = ""
        self.coutRecherche1['bois'] = 50
        self.coutRecherche2['bois'] = 50
        self.coutCreer1['bois'] = 50

    def creer1(self):  # créer des tanks
        if self.enCreation == False:
            if self.joueur.ressources >= self.coutCreer1:
                self.joueur.ressources['bois'] -= self.coutCreer1['bois']
                self.enCreation = True
                self.tempsDepartCreation = time.time()
        elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
            self.enCreation = False
            self.joueur.units.append(Tank(self.posX + 4, self.posY + 4, self.joueur))

    def recherche1(self):  # meilleure vitesse de création de tanks
        self.rechercheCompletee = False
        for recherche in self.joueur.recherche:
            if recherche == "Tank Vitesse":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.joueur.ressources >= self.coutRecherche1:
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
                if self.joueur.ressources >= self.coutRecherche2:
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
