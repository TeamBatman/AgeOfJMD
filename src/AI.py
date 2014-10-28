#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Batiments import *


#TODO mettre les bonnes valeurs pour les couts de construction et de recherche
from Units import *


class AI:
    def __init__(self,parent, civilisation):
        self.civilisation = civilisation
        self.base = Base(self, 10, 10)
        self.parent = parent
        self.manqueRessource = False
        self.ressourceManquante = None
        self.qteRessourceManquante = 0
        self.batiments = []
        self.recherchesCompletes = []
        self.bois = 0
        self.minerais = 0
        self.charbon = 0
        self.nbNourriture = 0
        self.units = []
        parent.createUnit(Unit.generateId(self.civilisation),self.base.posX+1, self.base.posY+1, self.civilisation)
        self.paix = True
        self.paysansOccupes = True
        self.morale = 100
        self.nombreSoldatsAllies = 0
        self.nombreSoldatsEnnemis = 0
        self.hpMoyen = 0
        self.epoque = 0
        #valeurs pour empêcher de rappeler des fonctions trop souvent
        self.derniereFerme = 0
        self.derniereScierie = 0
        self.derniereFonderie = 0
        self.derniereBarraque = 0
        self.derniereEglise = 0
        self.dernierHopital = 0
        self.dernierGarage = 0
        self.derniereFete = 0
        self.lastCheck = time.time()
        self.departEpoque = time.time()
        self.cooldownAutomatisation = 60
        self.cooldownEpoque = 300
        self.cooldownAttaque = 60
        self.derniereAttaque = 0
        self.cooldownRecherche = 120
        self.cooldownRessource = 30
        self.dernierSoldat = 0
        self.dernierPaysan = 0
        self.cooldownUnite = 40
        self.derniereRecherche = 0
        self.derniereRessourceBois = 0
        self.derniereRessourceMinerai = 0
        self.derniereRessourceCharbon = 0
        self.derniereBase = 0
        self.cooldownBatiment = 60

    def penser(self):

        #fais des test requis pour savoir quel mode prendre
        self.blackboard()

        #premier test pour savoir si on est en paix
        if self.paix:

            #si on manque de ressources, aller les miner
            if self.manqueRessource:
                    self.chercherRessource(self.ressourceManquante)
                    if self.ressourceManquante == "bois":
                        if self.qteRessourceManquante <= self.bois:
                            self.manqueRessource = False
                            pass
                    elif self.ressourceManquante == "minerais":
                        if self.qteRessourceManquante <= self.minerais:
                            self.manqueRessource = False
                            pass
                    elif self.ressourceManquante == "nourriture":
                        if self.qteRessourceManquante <= self.nbNourriture:
                            self.manqueRessource = False
                            pass
                    elif self.ressourceManquante == "charbon":
                        if self.qteRessourceManquante <= self.charbon:
                            self.manqueRessource = False
                            pass
                    else:
                        return

            #si l'on peut changer d'époque, le faire
            if time.time() - self.departEpoque >= self.cooldownEpoque and self.epoque > 3:
                self.changerEpoque()
                self.departEpoque = time.time()
                return

            #si tous les paysans sont occupés et que l'on en a moins de 10, créer un nouveau paysan
            if self.paysansOccupes and time.time() - self.dernierPaysan >= self.cooldownUnite:
                self.creerPaysan()
                self.dernierPaysan = time.time()
                return

            #si le moral est trop bas, faire une fête
            if self.morale < 50 and time.time() - self.derniereFete >= self.cooldownRecherche:
                self.augmenterMoral()
                self.derniereFete = time.time()
                return

            #si un ennemi a plus de soldats que nous, creer des soldats
            if self.nombreSoldatsAllies < self.nombreSoldatsEnnemis and time.time() - self.dernierSoldat >= self.cooldownUnite:
                self.creerSoldat()
                self.dernierSoldat = time.time()
                return

            #si un ennemi a moins de soldats que nous, attaquer
            if self.nombreSoldatsAllies > self.nombreSoldatsEnnemis and time.time() - self.derniereAttaque >= self.cooldownAttaque:
                self.attaquer()
                self.derniereAttaque = time.time()
                return

            #si rien d'autre, faire des recgerches
            if time.time() - self.derniereRecherche >= self.cooldownRecherche:
                self.rechercher()
                self.derniereRecherche = time.time()

        #sinon on est en guerre
        else:
            if self.hpMoyen < 50 :
                self.retraite()


    def chercherRessource(self, ressource):
        print(ressource)
        if ressource == "bois":
            self.chercherBois()
        elif ressource == "minerais":
            self.chercherminerais()
        elif ressource == "charbon":
            self.cherchercharbon()
        elif ressource == "nourriture":
            self.chercherNourriture()

    def chercherBois(self):
        for unit in self.units:
            if isinstance(unit, Paysan):
                if unit.typeRessource == 0:
                    if self.epoque >= 2:
                        if time.time() - self.derniereScierie >= self.cooldownAutomatisation:
                            #TODO creer une scierie et y mettre le paysan
                            return

                    if time.time() - self.derniereRessourceBois >= self.cooldownRessource:
                        position = self.trouverRessourcePlusPres(unit, self.parent.parent.carte.FORET)
                        unit.changerCible(position["x"], position["y"])
                        self.derniereRessourceBois = time.time()
                        return

        self.creerPaysan()

    def chercherminerais(self):
        for unit in self.units:
            if isinstance(unit, Paysan):
                if unit.typeRessource == 0:
                    if self.epoque >= 3:
                        if time.time() - self.derniereFonderie >= self.cooldownAutomatisation:
                            #TODO creer une fonderie et y mettre le paysan
                            return
                    if time.time() - self.derniereRessourceMinerai >= self.cooldownRessource:
                        position = self.trouverRessourcePlusPres(unit, self.parent.parent.carte.MINERAI)
                        unit.changerCible(position["x"], position["y"])
                        self.derniereRessourceBois = time.time()
                        return
        self.creerPaysan()

    def cherchercharbon(self):
        for unit in self.units:
            if isinstance(unit, Paysan):
                if unit.typeRessource == 0:
                    if time.time() - self.derniereRessourceCharbon >= self.cooldownRessource:
                        for x in range(unit.x, unit.x+20):
                            for y in range(unit.y, unit.y+20):
                                if time.time() - self.derniereRessourceBois >= self.cooldownRessource:
                                    position = self.trouverRessourcePlusPres(unit, self.parent.parent.carte.CHARBON)
                                    unit.changerCible(position["x"], position["y"])
                                    self.derniereRessourceBois = time.time()
                                    return
        self.creerPaysan()

    def chercherNourriture(self):
        for unit in self.units:
            if isinstance(unit, Paysan):
                if unit.typeRessource == 0:
                        if time.time() - self.derniereFerme >= self.cooldownAutomatisation:
                            #TODO creer une ferme
                            return

        self.creerPaysan()

    def changerEpoque(self):
        print("changer Epoque")
        for batiment in self.batiments:
            if isinstance(batiment, Base):
                if self.epoque == 1:
                    if self.bois >= batiment.coutRecherche2[0]:
                        batiment.changerEpoque()
                    else:
                        self.manqueRessource = True
                        self.qteRessourceManquante = batiment.coutRecherche2[0]
                        self.ressourceManquante = "bois"
                    return

                elif self.epoque == 2:
                    if self.bois >= batiment.coutRecherche2[0]:
                        if self.minerais >= batiment.coutRecherche2[1]:
                            batiment.changerEpoque()
                        else:
                            self.manqueRessource = True
                            self.qteRessourceManquante = batiment.coutRecherche2[1]
                            self.ressourceManquante = "minerais"
                    else:
                        self.manqueRessource = True
                        self.qteRessourceManquante = batiment.coutRecherche2[0]
                        self.ressourceManquante = "bois"
                    return

        #TODO trouver un paysan et le faire créer une nouvelle base

    def creerPaysan(self):
        print("creer Paysan")
        if self.base != None:
                if self.bois >= self.base.coutCreer1[0]:
                    self.base.creer1()
                    return
                else:
                    self.manqueRessource = True
                    self.qteRessourceManquante = self.base.coutCreer1[0]
                    self.ressourceManquante = "bois"
                    return

        #TODO trouver paysan et créer une nouvelle base
        if time.time() - self.derniereBase >= self.cooldownBatiment:
            for unit in self.units:
                if isinstance(unit, Paysan):
                    if unit.typeRessource == 0:
                        position = self.trouverRessourcePlusPres(unit, self.parent.parent.carte.Gazon)
                        self.base = Base(self, position["x"], position["y"])

                        


    def augmenterMoral(self):
        print("augmenter Moral")
        for batiment in self.batiments:
            if isinstance(batiment, Eglise):
                if self.bois >= batiment.coutRecherche1[0]:
                    batiment.recherche1()
                    return
                else:
                    self.manqueRessource = True
                    self.qteRessourceManquante = batiment.coutRecherche1[0]
                    self.ressourceManquante = "bois"
                    return
        #TODO trouver un paysan et creer une nouvelle Église

    def creerSoldat(self):
        print("creer Soldat")
        for batiment in self.batiments:
            if isinstance(batiment, Baraque):
                if not batiment.enCreation:
                    if self.bois >= batiment.coutCreer1[0]:
                        batiment.creer1()
                        return
                    else:
                        self.manqueRessource = True
                        self.qteRessourceManquante = batiment.coutCreer1[0]
                        self.ressourceManquante = "bois"
                        return
        #TODO trouver un paysan et creer une nouvelle baraque

    def attaquer(self):
        print("attaquer")
        for unit in self.units:
            if isinstance(unit, Soldat):
                #TODO faire Attaquer les Soldats
                pass

    def retraite(self):
        print("retraite")
        for unit in self.units:
            if isinstance(unit, Soldat):
                #TODO faire retraiter les Soldats
                pass

    def rechercher(self):
        print("rechercher")
        #TODO figurer comment rechercher
        pass

    def blackboard(self):
        #fais des test 1 fois au 30 sec pour éviter de trop répéter des taches
        if time.time() - self.lastCheck >= 30:
            #vérifie si tous les paysans sont occupés
            for unit in self.units:
                if isinstance(unit, Paysan):
                    if unit.typeRessource == 0:
                        self.paysansOccupes = False

            #compte les soldats à nous et trouve le hp moyen de ces soldats
            self.nombreSoldatsAllies = 0
            hpTotal = 0
            for unit in self.units:
                if isinstance(unit, Soldat):
                    self.nombreSoldatsAllies += 1
                    hpTotal += unit.hp

            self.hpMoyen = hpTotal/self.nombreSoldatsAllies


            #trouve le nombre de soldats de l'ennemi avec le plus de soldats
            ennemis = []
            for unit in self.parent.units:
                if unit.civilisation == "ROUGE":
                    ennemis[0] += 1
                elif unit.civilisation == "BLEU":
                    ennemis[1] += 1
                elif unit.civilisation == "VERT":
                    ennemis[2] += 1
                elif unit.civilisation == "ORANGE":
                    ennemis[3] += 1
                elif unit.civilisation == "MAUVE":
                    ennemis[4] += 1
                elif unit.civilisation == "BLANC":
                    ennemis[5] += 1
                elif unit.civilisation == "NOIR":
                    ennemis[6] += 1
                elif unit.civilisation == "ROSE":
                    ennemis[7] += 1
                elif unit.civilisation == "JAUNE":
                    ennemis[8] += 1

            self.nombreSoldatsEnnemis = 0
            for i in ennemis:
                if self.nombreSoldatsEnnemis < i:
                    self.nombreSoldatsEnnemis = i

    def trouverRessourcePlusPres(self, unit, typeRessource):
        ressource = {"x" : 0 , "y" : 0}

        minX = unit.x - 5
        minY = unit.y - 5
        maxX = unit.x + 5
        maxY = unit.y + 5
        found = False

        while not found:
            if minX < self.parent.parent.carte.size:
                minX = 0

            if minY < self.parent.parent.carte.size:
                minY = 0

            if maxX > self.parent.parent.carte.size:
                minX = self.parent.parent.carte.size

            if maxY > self.parent.parent.carte.size:
                maxY = self.parent.parent.carte.size

            for x in range (minX, maxX):
                for y in range (minY, maxY):
                    if self.parent.parent.carte.matrice[x][y].type == typeRessource:
                        found = True

            minX -= 5
            minY -= 5
            maxX += 5
            maxY += 5

        ressource["x"] = x
        ressource["y"] = y
        print(str(x) + " " + str(y))
        return ressource

