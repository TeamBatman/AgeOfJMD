#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from PIL import Image, ImageTk
from GraphicsManagement import GraphicsManager
import Model


#TODO trouver des valeurs correctes pour le prix en ressources des unités et batiments
#TODO L'hopital ne fait rien avec le healing
#TODO le FOW pour la tour de guet


class Batiment:
    COUNT = 0  # Un compteur permettant d'avoir un Id unique pour chaque batiment

    def __init__(self, parent, bid, posX, posY):
        self.posX = posX
        self.posY = posY
        self.id = bid
        self.peutEtreOccupe = False
        self.estOccupe = False
        self.pointsDeVie = 100
        self.estSelectionne = False
        self.type = ""
        self.image = None
        self.dejaAfficher = False
        self.parent = parent
        self.rechercheCompletee = False
        self.enRecherche = False  #booléen pour empecher de recommencer la fonction de recherche si l'on est déjà en recherche
        self.enCreation = False  #booléen pour empecher de recommencer la fonction de création si l'on est déjà en création
        self.tempsDepartRecherche = 0
        self.tempsDepartCreation = 0

    def getClientId(self):
        """ Returns the Id of the client using the id of the unit
        :return: the id of the clients
        """
        return self.id.split('_')[0]

    def estUniteDe(self, clientId):
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
        for batiment in self.parent.batiments:
            if batiment.posX == self.posX:
                if batiment.posY == self.posY:
                    self.parent.batiments.remove(batiment)
                    self.retourRessources()
                    return

    def retourRessources(self):
        #A trouver les valeurs à retourner
        if self.type == "Base":
            self.parent.bois += 100
        elif self.type == "Eglise":
            self.parent.bois += 50
            self.parent.metal += 50
        elif self.type == "Tour de guet":
            self.parent.bois += 50
            self.parent.metal += 50
        elif self.type == "Baraque":
            self.parent.bois += 50
            self.parent.metal += 50
        elif self.type == "Hopital":
            self.parent.bois += 50
            self.parent.metal += 50
            self.parent.huile += 50
        elif self.type == "Garage":
            self.parent.bois += 50
            self.parent.metal += 50
            self.parent.huile += 50
        elif self.type == "Ferme":
            self.parent.bois += 50
        elif self.type == "Scierie":
            self.parent.bois += 50
            self.parent.metal += 50
        elif self.type == "Fonderie":
            self.parent.bois += 50
            self.parent.metal += 50
            self.parent.huile += 50

    def sortirUnites(self):
        #verifie si le batiment peut etre occupe puis s'il y a des unites dedans et les sort
        if self.peutEtreOccupe == True:
            if self.estOccupe == True:
                for i in range(0, self.parent.unites):
                    if self.parent.unites[i].batiment == self:
                        self.parent.unites[i].batiment == None


class Eglise(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "Eglise"
        self.tempsDerniereFete = 0


    def recherche1(self):  #Boost Moral
        if self.parent.epoque == 2:
            if self.enRecherche == False:
                if self.parent.bois >= 50:
                    if time.time() - self.tempsDerniereFete >= 60:
                        self.parent.bois -= 50
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
            elif time.time() - self.tempsDepartRecherche <= 60:
                self.parent.moral = 100
                self.enRecherche = False
                self.tempsDerniereFete = time.time()
        else:
            if self.enRecherche == False:
                if self.parent.bois >= 50:
                    if time.time() - self.tempsDerniereFete >= 60:
                        self.parent.bois -= 50
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
            elif time.time() - self.tempsDepartRecherche <= 120:
                self.parent.moral = 100
                self.enRecherche = False
                self.tempsDerniereFete = time.time()

    def miseAJour(self):
        if self.enRecherche:
            self.recherche1()


class TourDeGuet(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "Tour de guet"

    def recherche1(self):  #Meilleure vue du Fog of war
        if self.parent.epoque == 2:
            for recherche in self.parent.recherche:
                if recherche == "Tour1":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.parent.bois >= 50:
                        self.parent.bois -= 50
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche <= 60:
                    #TODO Decouverir comment le FOW fonctionnera
                    self.enRecherche = False
                    self.parent.recherche.append("Tour1")

        else:
            for recherche in self.parent.recherche:
                if recherche == "Tour2":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.parent.bois >= 50:
                        self.parent.bois -= 50
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche <= 60:
                    #TODO Decouverir comment le FOW fonctionnera
                    self.enRecherche = False
                    self.parent.recherche.append("Tour2")

        self.rechercheCompletee = False

    def miseAJour(self):
        if self.enRecherche:
            self.recherche1()


class Hopital(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "Hopital"
        self.peutEtreOccupe = True
        self.vitesseDeCreation = 30

    def healing(self, unite):
        #TODO decouvrir comment le healing va se faire
        #TODO ajouter le temps de recherche
        pass

    def recherche1(self):  #Amélioration du healing
        for recherche in self.parent.recherche:
            if recherche == "Hopital":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.parent.bois >= 50:
                    self.parent.bois -= 50
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
            elif time.time() - self.tempsDepartRecherche <= 60:
                self.enRecherche = False
                self.parent.recherche.append("Hopital")
                #TODO decouvrir comment la regeneration va se faire

    def miseAJour(self):
        if self.enRecherche:
            self.recherche1()


class Base(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "Base"
        self.vitesseDeCreation = 40


    def creer1(self):  #création des paysans
        if self.enCreation == False:
            if self.parent.bois >= 50:
                self.parent.bois -= 50
                self.enCreation = True
                self.tempsDepartCreation = time.time()

        elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
            self.parent.units.append(Paysan(self.posX + 4, self.posY + 4, self.parent))
            self.enCreation = False


    def recherche1(self):  #meilleure vitesse de création de paysans
        if self.parent.epoque == 1:
            for recherche in self.parent.recherche:
                if recherche == "Paysan Vitesse 1":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.parent.bois >= 50:
                        self.parent.bois -= 50
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche <= 60:
                    self.enRecherche = False
                    self.vitesseDeCreation = self.vitesseDeCreation * 0.9
                    self.rechercheCompletee = False
                    self.parent.recherche.append("Paysan Vitesse 1")

        elif self.parent.epoque == 2:
            for recherche in self.parent.recherche:
                if recherche == "Paysan Vitesse 2":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.parent.bois >= 50:
                        self.parent.bois -= 50
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.enRecherche = False
                    self.vitesseDeCreation = self.vitesseDeCreation * 0.9
                    self.rechercheCompletee = False
                    self.parent.recherche.append("Paysan Vitesse 2")

        else:
            for recherche in self.parent.recherche:
                if recherche == "Paysan Vitesse 3":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.parent.bois >= 50:
                        self.parent.bois -= 50
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.rechercheCompletee = False
                    self.enRecherche = False
                    self.vitesseDeCreation = self.vitesseDeCreation * 0.9
                    self.parent.recherche.append("Paysan Vitesse 3")

    def miseAJour(self):
        if self.enCreation:
            self.creer1()
        if self.enRecherche:
            self.recherche1()


class Baraque(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "Baraque"
        self.vitesseDeCreation = 40
        self.typeCreation = ""
        self.typeRecherche = ""


0


def creer1(self):  #création de soldats avec épée
    if self.enCreation == False:
        if self.parent.bois >= 50:
            self.parent.bois -= 50
            self.enCreation = True
            self.typeCreation = "Epee"
            self.tempsDepartCreation = time.time()
    elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
        self.parent.unites.add(SoldatEpee(self.posX + 4, self.posY + 4, self.parent))
        self.enCreation = False


def creer2(self):  #création de soldats avec lances
    if self.enCreation == False:
        if self.parent.bois >= 50:
            self.parent.bois -= 50
            self.enCreation = True
            self.typeCreation = "Lance"
            self.tempsDepartCreation = time.time()
    elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
        self.parent.unites.add(SoldatLance(self.posX + 4, self.posY + 4, self.parent))
        self.enCreation = False


def creer3(self):  #création de soldats avec boucliers
    if self.enCreation == False:
        if self.parent.bois >= 50:
            self.parent.bois -= 50
            self.enCreation = True
            self.typeCreation = "Bouclier"
            self.tempsDepartCreation = time.time()
    elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
        self.parent.unites.add(SoldatBouclier(self.posX + 4, self.posY + 4, self.parent))
        self.enCreation = False


def recherche1(self):  #meilleure attaque
    if self.parent.epoque == 2:
        for recherche in self.parent.recherche:
            if recherche == "Soldat Attaque 1":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.parent.bois >= 50:
                    self.parent.bois -= 50
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
                if self.parent.bois >= 50:
                    self.parent.bois -= 50
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


def recherche2(self):  #meilleure vitesse de création
    if self.parent.epoque == 2:
        for recherche in self.parent.recherche:
            if recherche == "Soldat Vitesse 1":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.parent.bois >= 50:
                    self.parent.bois -= 50
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
                if self.parent.bois >= 50:
                    self.parent.bois -= 50
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
        self.peutEtreOccupe = True
        self.production = 10
        self.tempsProduction = 10
        self.type = "Ferme"
        self.rawImage = GraphicsManager.get('Graphics/Buildings/Age_I/Farm.png')
        self.resized = self.rawImage.resize((96,96),Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.resized)
        print("bob")

    def produire(self):
        #TODO a se renseigner sur les valeurs pour la production
        if self.estOccupe:
            if time.time() - self.tempsProduction >= 10:
                self.parent.nourriture += self.production
                self.tempsProduction = time.time()


    def recherche1(self):  #meilleure vitesse de production
        if self.parent.epoque == 1:
            for recherche in self.parent.recherche:
                if recherche == "Ferme 1":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.parent.bois >= 50:
                        self.parent.bois -= 50
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.rechercheCompletee = False
                    self.enRecherche = False
                    self.parent.recherche.append("Ferme 1")

        elif self.parent.epoque == 2:
            for recherche in self.parent.recherche:
                if recherche == "Ferme 2":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.parent.bois >= 50:
                        self.parent.bois -= 50
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.rechercheComplete = False
                    self.enRecherche = False
                    self.parent.recherche.append("Ferme 2")

        else:
            for recherche in self.parent.recherche:
                if recherche == "Ferme 3":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.parent.bois >= 50:
                        self.parent.bois -= 50
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.rechercheCompletee = False
                    self.enRecherche = False
                    self.parent.recherche.append("Ferme 3")

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

    def produire(self):
        #TODO a se renseigner sur les valeurs pour la production
        if self.estOccupe:
            if time.time() - self.tempsProduction >= 10:
                self.parent.bois += self.production
                self.tempsProduction = time.time()

    def recherche1(self):  #meilleure vitesse de production
        if self.parent.epoque == 2:
            for recherche in self.parent.recherche:
                if recherche == "Scierie 1":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.parent.bois >= 50:
                        self.parent.bois -= 50
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.rechercheCompletee = False
                    self.enRecherche = False
                    self.parent.recherche.append("Scierie 1")

        else:
            for recherche in self.parent.recherche:
                if recherche == "Scierie 2":
                    self.rechercheCompletee = True
            if self.rechercheCompletee == False:
                if self.enRecherche == False:
                    if self.parent.bois >= 50:
                        self.parent.bois -= 50
                        self.enRecherche = True
                        self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.rechercheCompletee = False
                    self.enRecherche = False
                    self.parent.recherche.append("Scierie 2")

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

    def produire(self):
        #TODO a se renseigner sur les valeurs pour la production
        if self.estOccupe:
            if time.time() - self.tempsProduction >= 10:
                self.parent.metal += self.production
                self.tempsProduction = time.time()

    def recherche1(self):  #meilleure vitesse de production
        for recherche in self.parent.recherche:
            if recherche == "Fonderie 1":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.parent.bois >= 50:
                    self.parent.bois -= 50
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
        elif time.time() - self.tempsDepartRecherche >= 60:
            self.production = self.production * 1.1
            self.rechercheCompletee = False
            self.enRecherche = False
            self.parent.recherche.append("Fonderie 1")

    def miseAJour(self):
        if self.enRecherche:
            self.recherche1()

        self.produire()


class Garage(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.vitesseDeCreation = 60
        self.typeRecherche = ""

    def creer1(self):  #créer des tanks
        if self.enCreation == False:
            if self.parent.bois >= 50:
                self.parent.bois -= 50
                self.enCreation = True
                self.tempsDepartCreation = time.time()
        elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
            self.enCreation = False
            self.parent.units.append(Tank(self.posX + 4, self.posY + 4, self.parent))

    def recherche1(self):  #meilleure vitesse de création de tanks
        for recherche in self.parent.recherche:
            if recherche == "Tank Vitesse":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.parent.bois >= 50:
                    self.parent.bois -= 50
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
                    self.typeRecherche = "Vitesse"
            elif time.time() - self.tempsDepartRecherche >= 60:
                self.rechercheCompletee = False
                self.enRecherche = False
                self.vitesseDeCreation = self.vitesseDeCreation * 0.8
                self.parent.recherche.append("Tank Vitesse")

    def recherche2(self):  #amélioration du HP des tanks
        for recherche in self.parent.recherche:
            if recherche == "Tank HP":
                self.rechercheCompletee = True
        if self.rechercheCompletee == False:
            if self.enRecherche == False:
                if self.parent.bois >= 50:
                    self.parent.bois -= 50
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
                    self.typeRecherche = "HP"
            elif time.time() - self.tempsDepartRecherche >= 60:
                self.rechercheCompletee = False
                self.enRecherche = False
                self.parent.recherche.append("Tank HP")
                for tank in self.parent.units:
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