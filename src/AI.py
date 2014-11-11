#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Batiments import *

#TODO mode rechercher
#TODO mettre les bonnes valeurs pour les couts de construction et de recherche
from Joueurs import Joueur
from Units import Paysan
from Batiments import *


class AI(Joueur):
    def __init__(self, civilisation, parent):
        super().__init__(civilisation)
        self.civilisation = civilisation
        self.parent = parent
        self.base = None
        self.manqueRessource = False
        self.ressourceManquante = None
        self.qteRessourceManquante = 0
        self.batiments = {}
        self.recherchesCompletes = []
        self.ressources = {"bois" : 50, "minerai" : 0, "charbon" : 0}
        self.nbNourriture = 0
        self.units = []
        self.paix = True
        self.paysansOccupes = True
        self.moral = 100
        self.nombreSoldatsAllies = 0
        self.nombreSoldatsEnnemis = 0
        self.hpMoyen = 0
        self.epoque = 1
        #valeurs pour empêcher de rappeler des fonctions trop souvent
        self.derniereFerme = 0
        self.derniereScierie = 0
        self.derniereFonderie = 0
        self.derniereBarraque = 0
        self.derniereEglise = 0
        self.dernierHopital = 0
        self.dernierGarage = 0
        self.derniereFete = 0
        self.lastCheck = 0
        self.departEpoque = time.time()
        self.cooldownAutomatisation = 60
        self.cooldownEpoque = 60
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
        self.derniereAction = 0
        self.nombrePaysans = 0

    def penser(self):
        #fais des test requis pour savoir quel mode prendre
        self.blackboard()
        #premier test pour savoir si on est en paix
        if self.paix:
            #print("paix")
            #si on manque de ressources, aller les miner
            if self.manqueRessource:
                print("manque ressource")
                self.chercherRessource(self.ressourceManquante)
                if self.ressourceManquante == "bois":
                    if self.qteRessourceManquante >= self.ressources["bois"]:
                        self.manqueRessource = False
                    else:
                        self.chercherRessource("bois")
                        return
                elif self.ressourceManquante == "minerais":
                    if self.qteRessourceManquante >= self.ressources["minerai"]:
                        self.manqueRessource = False
                    else:
                        self.chercherRessource("minerais")
                        return
                elif self.ressourceManquante == "nourriture":
                    if self.qteRessourceManquante >= self.nbNourriture:
                        self.manqueRessource = False
                    else:
                        self.chercherRessource("nourriture")
                        return
                elif self.ressourceManquante == "charbon":
                    if self.qteRessourceManquante >= self.ressources["charbon"]:
                        self.manqueRessource = False
                    else:
                        self.chercherRessource("charbon")
                        return


            #si l'on peut changer d'époque, le faire
            if time.time() - self.departEpoque >= self.cooldownEpoque and self.epoque < 3:
                print("peux changer époque")
                self.changerEpoque()
                self.departEpoque = time.time()
                return
            #print("peux pas changer d'époque")
            #si tous les paysans sont occupés et que l'on en a moins de 10, créer un nouveau paysan
            if (self.paysansOccupes and time.time() - self.dernierPaysan >= self.cooldownUnite) or self.nombrePaysans < 10:
                print("besoin Paysan")
                self.creerPaysan()
                self.dernierPaysan = time.time()
                return
            #print("paysans libres")
            #si le moral est trop bas, faire une fête
            if self.moral < 50 and time.time() - self.derniereFete >= self.cooldownRecherche:
                print("moral bas")
                self.augmenterMoral()
                self.derniereFete = time.time()
                return
            #print("moral assez haut")
            #si un ennemi a plus de soldats que nous, creer des soldats
            if self.nombreSoldatsAllies < self.nombreSoldatsEnnemis and time.time() - self.dernierSoldat >= self.cooldownUnite:
                print("besoin soldats")
                self.creerSoldat()
                self.dernierSoldat = time.time()
                return
            #print("soldats suffisants")
            #si un ennemi a moins de soldats que nous, attaquer
            if self.nombreSoldatsAllies > self.nombreSoldatsEnnemis and time.time() - self.derniereAttaque >= self.cooldownAttaque:
                print("a l'attaque")
                self.attaquer()
                self.derniereAttaque = time.time()
                return
            #print("peux pas attaquer")
            #si rien d'autre, faire des recgerches
            if time.time() - self.derniereRecherche >= self.cooldownRecherche:
                print("démarrer recherche")
                self.rechercher()
                return
            #print("cooldown recherche")
        #sinon on est en guerre
        else:
            if self.hpMoyen < 50 :
                print("retreat")
                self.retraite()
            #print("pas besoin retraite")


    def chercherRessource(self, ressource):
        print(ressource)
        if ressource == "bois":
            print("chercherBois")
            self.chercherBois()
        elif ressource == "minerai":
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
                            position = self.trouverRessourcePlusPres(unit, self.parent.carte.GAZON)
                            self.parent.createBuilding(self.civilisation, self.parent.controller.view.SCIERIE, position["x"], position["y"])
                            print("scierie créée?")
                            return
                    if time.time() - self.derniereRessourceBois >= self.cooldownRessource:
                        print("not cd")
                        position = self.trouverRessourcePlusPres(unit, self.parent.carte.FORET)
                        unit.changerCible(position["x"], position["y"])
                        self.derniereRessourceBois = time.time()
                        return
                    else:
                        print("en cooldown bois")
                        return
                else:
                    print("WTF")
                    return
        self.creerPaysan()

    def chercherminerais(self):
        for unit in self.units:
            if isinstance(unit, Paysan):
                if unit.typeRessource == 0:
                    if self.epoque >= 3:
                        if time.time() - self.derniereFonderie >= self.cooldownAutomatisation:
                            position = self.trouverRessourcePlusPres(unit, self.parent.carte.GAZON)
                            self.parent.createBuilding(self.civilisation, self.parent.controller.view.FONDERIE, position["x"], position["y"])
                            print("fonderie créée?")
                            return
                    if time.time() - self.derniereRessourceMinerai >= self.cooldownRessource:
                        position = self.trouverRessourcePlusPres(unit, self.parent.carte.MINERAI)
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
                                    position = self.trouverRessourcePlusPres(unit, self.parent.carte.CHARBON)
                                    unit.changerCible(position["x"], position["y"])
                                    self.derniereRessourceBois = time.time()
                                    return
        self.creerPaysan()

    def chercherNourriture(self):
        for unit in self.units:
            if isinstance(unit, Paysan):
                if unit.typeRessource == 0:
                        if time.time() - self.derniereFerme >= self.cooldownAutomatisation:
                            position = self.trouverRessourcePlusPres(unit, self.parent.carte.GAZON)
                            self.parent.createBuilding(self.civilisation, self.parent.controller.view.FERME, position["x"], position["y"])
                            print("ferme créée?")
                            return

        self.creerPaysan()

    def changerEpoque(self):
        if self.base != None:
            if self.epoque == 1:
                if self.ressources["bois"] >= self.base.coutRecherche2["bois"]:
                    self.base.recherche2()
                else:
                    self.manqueRessource = True
                    self.qteRessourceManquante = self.base.coutRecherche2["bois"]
                    self.ressourceManquante = "bois"
                return

            elif self.epoque == 2:
                if self.ressources["bois"] >= self.base.coutRecherche2["bois"]:
                    if self.ressources["minerai"] >= self.base.coutRecherche2["minerai"]:
                        self.base.recherche2()
                    else:
                        self.manqueRessource = True
                        self.qteRessourceManquante = self.base.coutRecherche2["minerai"]
                        self.ressourceManquante = "minerai"
                else:
                    self.manqueRessource = True
                    self.qteRessourceManquante = self.base.coutRecherche2["bois"]
                    self.ressourceManquante = "bois"
                return
            return

        print("pas de base")
        if time.time() - self.derniereBase >= self.cooldownBatiment:
            for unit in self.units:
                if isinstance(unit, Paysan):
                    if unit.typeRessource == 0:
                        position = self.trouverRessourcePlusPres(unit, self.parent.carte.GAZON)
                        self.parent.createBuilding(self.civilisation, self.parent.controller.view.BASE, position["x"], position["y"])
                        for building in self.parent.buildings.values():
                            if building.type == "base":
                                print("bob")
                                if building.parent.ai.civilisation == self.civilisation:
                                    self.base = building
                                    print("ok")
                        print("base créée poel")

    def creerPaysan(self):
        print("creer Paysan")
        if self.base != None:
            if self.ressources["bois"] >= self.base.coutCreer1["bois"]:
                self.base.creer1()
                print("départ création")
                return
            else:
                self.manqueRessource = True
                self.qteRessourceManquante = self.base.coutCreer1["bois"]
                self.ressourceManquante = "bois"
                print("il manque" + " " + str(self.qteRessourceManquante) + ":" + str(self.ressourceManquante))
                return

        print("pas de base")
        if time.time() - self.derniereBase >= self.cooldownBatiment:
            for unit in self.units:
                if isinstance(unit, Paysan):
                    if unit.typeRessource == 0:
                        position = self.trouverRessourcePlusPres(unit, self.parent.carte.GAZON)
                        self.parent.createBuilding(self.civilisation, self.parent.controller.view.BASE, position["x"], position["y"])
                        for building in self.parent.buildings.values():
                            if building.type == "base":
                                print("bob")
                                if building.parent.ai.civilisation == self.civilisation:
                                    self.base = building
                                    print("ok")
                        print("base créée poel")

                        


    def augmenterMoral(self):
        print("augmenter Moral")
        for batiment in self.batiments:
            if isinstance(batiment, Eglise):
                if self.ressources["bois"] >= batiment.coutRecherche1[0]:
                    batiment.recherche1()
                    return
                else:
                    self.manqueRessource = True
                    self.qteRessourceManquante = batiment.coutRecherche1[0]
                    self.ressourceManquante = "bois"
                    return

        print("pas d'église")
        for unit in self.units:
            if isinstance(unit, Paysan):
                if unit.typeRessource == 0:
                        if time.time() - self.derniereEglise >= self.cooldownBatiment:
                            position = self.trouverRessourcePlusPres(unit, self.parent.carte.GAZON)
                            self.parent.createBuilding(self.civilisation, self.parent.controller.view.EGLISE, position["x"], position["y"])
                            print("Eglise créée")
                            return

    def creerSoldat(self):
        print("creer Soldat")
        for batiment in self.batiments:
            if isinstance(batiment, Baraque):
                if not batiment.enCreation:
                    if  self.ressources["bois"] >= batiment.coutCreer1[0]:
                        batiment.creer1()
                        return
                    else:
                        self.manqueRessource = True
                        self.qteRessourceManquante = batiment.coutCreer1[0]
                        self.ressourceManquante = "bois"
                        return

        print("pas de baraque")
        for unit in self.units:
            if isinstance(unit, Paysan):
                if unit.typeRessource == 0:
                        if time.time() - self.derniereBarraque >= self.cooldownBatiment:
                            position = self.trouverRessourcePlusPres(unit, self.parent.carte.GAZON)
                            self.parent.createBuilding(self.civilisation, self.parent.controller.view.BARAQUE, position["x"], position["y"])
                            print("Baraque créée")
                            return

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
        self.derniereRecherche = time.time()


    def blackboard(self):
        #fais des test 1 fois au 30 sec pour éviter de trop répéter des taches
        if time.time() - self.lastCheck >= 30:

            self.units = []
            for unit in self.parent.units:
                if self.parent.units[unit].civilisation == self.civilisation:
                    self.units.append(self.parent.units[unit])

            self.nombrePaysans = 0
            #vérifie si tous les paysans sont occupés
            for unit in self.units:
                if isinstance(unit, Paysan):
                    self.nombrePaysans += 1
                    if unit.typeRessource == 0:
                        self.paysansOccupes = False


            #compte les soldats à nous et trouve le hp moyen de ces soldats
            #self.nombreSoldatsAllies = 0
            #hpTotal = 0
            #for unit in self.units:
                #if isinstance(unit, Soldat):
                    #self.nombreSoldatsAllies += 1
                    #hpTotal += unit.hp

            #self.hpMoyen = hpTotal/self.nombreSoldatsAllies


            #trouve le nombre de soldats de l'ennemi avec le plus de soldats
            #ennemis = [8]
            #for unit in self.parent.units:
                #if self.parent.units[unit].civilisation == 0:
                    #ennemis[0] += 1
                #elif self.parent.units[unit].civilisation == 1:
                    #ennemis[1] += 1
                #elif self.parent.units[unit].civilisation == 2:
                    #ennemis[2] += 1
                #elif self.parent.units[unit].civilisation == 3:
                    #ennemis[3] += 1
                #elif self.parent.units[unit].civilisation == 4:
                    #ennemis[4] += 1
                #elif self.parent.units[unit].civilisation == 5:
                    #ennemis[5] += 1
                #elif self.parent.units[unit].civilisation == 6:
                    #ennemis[6] += 1
                #elif self.parent.units[unit].civilisation == 7:
                    #ennemis[7] += 1
                #elif self.parent.units[unit].civilisation == 8:
                    #ennemis[8] += 1
                #else:
                    #print("erreur civilisations")

            #check nombre ennemis
            #self.nombreSoldatsEnnemis = 0
            #for i in ennemis:
                #if self.nombreSoldatsEnnemis < i:
                    #self.nombreSoldatsEnnemis = i

            self.lastCheck = time.time()

    def trouverRessourcePlusPres(self, unit, typeRessource):
        ressource = {"x" : 0 , "y" : 0}

        minX = int(unit.x)
        minY = int(unit.y)
        maxX = int(unit.x)
        maxY = int(unit.y)
        found = False

        while not found:
            print("start check")
            minX = minX - 240
            minY = minY - 240
            maxX += 240
            maxY += 240

            #si le minimum des X à vérifier est va à moins de 0, mettre à 0
            if minX < 0:
                minX = 0

            #si le minimum des Y à vérifier est va à moins de 0, mettre à 0
            if minY < 0:
                minY = 0

            #si le maximum des X à vérifier est plus grand que la taille de la map, le mettre au max de la map
            #taille de la map * 48 parceque la taille de la map est en tuiles et chaque tuile est de 48 pixels
            if maxX > self.parent.carte.size * 48:
                maxX = self.parent.carte.size * 48

            #si le maximum des Y à vérifier est plus grand que la taille de la map, le mettre au max de la map
            #taille de la map * 48 parceque la taille de la map est en tuiles et chaque tuile est de 48 pixels
            if maxY > self.parent.carte.size * 48:
                maxY = self.parent.carte.size * 48

            print(maxX)
            print(maxY)
            print(minX)
            print(minY)

            for x in range (minX, maxX, 48):
                for y in range (minY, maxY, 48):
                    casesCible = self.parent.trouverCaseMatrice(x, y)
                    caseCibleX = casesCible[0]
                    caseCibleY = casesCible[1]
                    if self.parent.carte.matrice[caseCibleX][caseCibleY].type == typeRessource:
                        ressource["x"] = x
                        ressource["y"] = y
                        return ressource





    def delaiPenser(self):
        if time.time() - self.derniereAction >= 5:
            self.derniereAction = time.time()
            self.penser()

