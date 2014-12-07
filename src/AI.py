#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Batiments import *

#TODO mode rechercher
#TODO implémentation du moral

from Joueurs import Joueur
from Units import *
from Batiments import *
from Carte import Tuile



class AI(Joueur):
    def __init__(self, civilisation, model):
        super().__init__(civilisation, model)
        self.ai = True
        self.manqueRessource = False
        self.ressourceManquante = None
        self.qteRessourceManquante = 0
        self.ressources = {'bois' : 0, 'minerai' : 0, 'charbon' : 0, 'nourriture' : 10}
        self.paix = True
        self.paysansOccupes = False
        self.nombreSoldatsAllies = 0
        self.nombreSoldatsEnnemis = 0
        self.hpMoyen = 0
        self.ennemiPlusFort = None
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
        self.cooldownEpoque = 60#60
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
        self.tempsDepart = time.time() - 55
        self.nombrePaysans = 0
        self.epoque = 1
        self.lastHPBase = 0
        self.defense = False

    def penser(self):
        #fais des test requis pour savoir quel mode prendre
        self.blackboard()
        #premier test pour savoir si on est en paix
        if self.paix:
            #print("paix")
            if not self.paysansOccupes:
                for unitID in self.units:
                    unit = self.model.getUnit(unitID)
                    if isinstance(unit, Paysan):
                        if unit.typeRessource == 0:
                            position = {"x" : 0, "y" : 0}
                            position = self.trouverRessourcePlusPres(unit, Tuile.FORET)
                            self.deplacerUnite(position["x"], position["y"], unit, None)

            #si tous les paysans sont occupés et que l'on en a moins de 10, créer un nouveau paysan
            if time.time() - self.dernierPaysan >= self.cooldownUnite and (self.paysansOccupes or self.nombrePaysans < 10):
                print("besoin Paysan")
                self.creerPaysan()
                self.dernierPaysan = time.time()
                return
            #print("paysans libres")

            #si on manque de ressources, aller les miner
            if self.manqueRessource:
                print("manque ressource")
                self.chercherRessource(self.ressourceManquante)
                if self.ressourceManquante == 'bois':
                    if self.qteRessourceManquante <= self.ressources['bois']:
                        self.manqueRessource = False
                    else:
                        self.chercherRessource('bois')
                        return
                elif self.ressourceManquante == "minerais":
                    if self.qteRessourceManquante <= self.ressources['minerai']:
                        self.manqueRessource = False
                    else:
                        self.chercherRessource("minerais")
                        return
                elif self.ressourceManquante == "nourriture":
                    if self.qteRessourceManquante <= self.ressources['nourriture']:
                        self.manqueRessource = False
                    else:
                        self.chercherRessource("nourriture")
                        return
                elif self.ressourceManquante == 'charbon':
                    if self.qteRessourceManquante <= self.ressources['charbon']:
                        self.manqueRessource = False
                    else:
                        self.chercherRessource('charbon')
                        return

            #si l'on peut changer d'époque, le faire
            if time.time() - self.departEpoque >= self.cooldownEpoque and self.epoque < 3:
                print("peux changer époque")
                self.changerEpoque()
                self.departEpoque = time.time()
                return
            #print("peux pas changer d'époque")

            #TODO Implémenter le moral
            #si le moral est trop bas, faire une fête
            #if self.morale < 50 and time.time() - self.derniereFete >= self.cooldownRecherche:
                #print("moral bas")
                #self.augmenterMoral()
                #self.derniereFete = time.time()
                #return
            #print("moral assez haut")

            #si un ennemi a plus de soldats que nous, creer des soldats
            if self.nombreSoldatsAllies < self.nombreSoldatsEnnemis and time.time() - self.dernierSoldat >= self.cooldownUnite:
                print("besoin soldats !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                self.creerSoldat()
                self.dernierSoldat = time.time()
                return
            #print("soldats suffisants")

            #si un ennemi a moins de soldats que nous, attaquer
            if self.nombreSoldatsAllies > self.nombreSoldatsEnnemis and time.time() - self.derniereAttaque >= self.cooldownAttaque:
                print("a l'attaque!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                self.attaquer()
                self.derniereAttaque = time.time()
                self.paix = False
                return
            #print("peux pas attaquer")

            #si rien d'autre, faire des recherches
            #TODO implémenter les recherches
            #if time.time() - self.derniereRecherche >= self.cooldownRecherche:
                #print("démarrer recherche")
                #self.rechercher()
                #return
            #print("cooldown recherche")


        #sinon on est en guerre
        else:
            if self.defense:
                self.defendre()
                return

            if self.hpMoyen < 50 :
                self.retraite()
                return

            self.attaquer()
            #print("pas besoin retraite")


    def chercherRessource(self, ressource):
        print(ressource)
        if ressource == 'bois':
            print("chercherBois")
            self.chercherBois()
        elif ressource == 'minerai':
            self.chercherminerais()
        elif ressource == 'charbon':
            self.cherchercharbon()
        elif ressource == "nourriture":
            self.chercherNourriture()

    def chercherBois(self):
        unit = self.trouverUniteLibre(Tuile.FORET)
        if unit != None:
            if self.epoque >= 2:
                if time.time() - self.derniereScierie >= self.cooldownAutomatisation:
                    self.batirBatiment(Batiment.SCIERIE, unit)
                    self.derniereScierie = time.time()
                    print("scierie créée?")
                    return
            if time.time() - self.derniereRessourceBois >= self.cooldownRessource:
                print("not cd")
                position = self.trouverRessourcePlusPres(unit,Tuile.FORET)
                self.deplacerUnite(position["x"], position["y"], unit, None)
                self.derniereRessourceBois = time.time()
                return
            else:
                print("en cooldown bois")
                return
        self.creerPaysan()

    def chercherminerais(self):
        unit = self.trouverUniteLibre(Tuile.MINERAI)
        if unit != None:
            if self.epoque >= 3:
                if time.time() - self.derniereFonderie >= self.cooldownAutomatisation:
                    self.batirBatiment(Batiment.FONDERIE, unit)
                    self.derniereFonderie = time.time()
                    print("fonderie créée?")
                    return
            if time.time() - self.derniereRessourceMinerai >= self.cooldownRessource:
                position = self.trouverRessourcePlusPres(unit, Tuile.MINERAI)
                self.deplacerUnite(position["x"], position["y"], unit, None)
                self.derniereRessourceBois = time.time()
                return
        self.creerPaysan()

    def cherchercharbon(self):
        unit = self.trouverUniteLibre(Tuile.CHARBON)
        if unit != None:
            if time.time() - self.derniereRessourceCharbon >= self.cooldownRessource:
                for x in range(unit.x, unit.x+20):
                    for y in range(unit.y, unit.y+20):
                        if time.time() - self.derniereRessourceBois >= self.cooldownRessource:
                            position = self.trouverRessourcePlusPres(unit, Tuile.CHARBON)
                            self.deplacerUnite(position["x"], position["y"], unit, None)
                            self.derniereRessourceBois = time.time()
                            return
        self.creerPaysan()

    def chercherNourriture(self):
        unit = self.trouverUniteLibre("")
        ferme = self.trouverBatiment(Batiment.FERME, "", self.civilisation)

        if unit != None:
            if not ferme:
                if time.time() - self.derniereFerme >= self.cooldownAutomatisation:
                    self.batirBatiment(Batiment.FERME, unit)
                    print("ferme créée?")
                    self.derniereFerme = time.time()
                    return
            else:
                print("help",ferme.posX, ferme.posY)
                batiment = self.model.trouverCentreCase(ferme.posX, ferme.posY)
                print(batiment[0], batiment[1])
                self.deplacerUnite(batiment[0], batiment[1], unit, None)

        self.creerPaysan()

    def changerEpoque(self):
        base = self.trouverBatiment(Batiment.BASE, "", self.civilisation)
        if base != None:
            if self.epoque == 1:
                if self.ressources['bois'] >= base.coutRecherche2['bois']:
                    base.recherche2()
                else:
                    self.manqueRessource = True
                    self.qteRessourceManquante = base.coutRecherche2['bois']
                    self.ressourceManquante = 'bois'
                return

            elif self.epoque == 2:
                if self.ressources['bois'] >= base.coutRecherche2['bois']:
                    if self.ressources['minerai'] >= base.coutRecherche2['minerai']:
                        base.recherche2()
                    else:
                        self.manqueRessource = True
                        self.qteRessourceManquante = base.coutRecherche2['minerai']
                        self.ressourceManquante = 'minerai'
                else:
                    self.manqueRessource = True
                    self.qteRessourceManquante = base.coutRecherche2['bois']
                    self.ressourceManquante = 'bois'
                return
            return

        print("pas de base")
        if time.time() - self.derniereBase >= self.cooldownBatiment:
            unit = self.trouverUniteLibre("")
            #position = self.trouverRessourcePlusPres(unit, Tuile.GAZON)
            self.batirBatiment(Batiment.BASE, unit)

            print("base créée poel")

    def creerPaysan(self):
        print("creer Paysan")
        base = self.trouverBatiment(Batiment.BASE, "", self.civilisation)
        if base != None:
            if self.ressources['nourriture'] >= base.coutCreer1['nourriture']:
                base.creer1()
                print("départ création")
                return
            else:
                self.manqueRessource = True
                self.qteRessourceManquante = base.coutCreer1['nourriture']
                self.ressourceManquante = 'nourriture'
                print("il manque" + " " + str(self.qteRessourceManquante) + ":" + str(self.ressourceManquante))
                return

        print("pas de base")
        if time.time() - self.derniereBase >= self.cooldownBatiment:
            unit = self.trouverUniteLibre("")
            if unit == None:
                print("AI DEAD")
                return
            else:
                position = self.trouverRessourcePlusPres(unit, Tuile.GAZON)
                self.batirBatiment(Batiment.BASE, unit)

                print("base créée poel")

                        


    def augmenterMoral(self):
        print("augmenter Moral")
        eglise = self.trouverBatiment(Batiment.LIEU_CULTE, "", self.civilisation)
        if eglise != None:
            if self.ressources['bois'] >= eglise.coutRecherche1[0]:
                eglise.recherche1()
                return
            else:
                self.manqueRessource = True
                self.qteRessourceManquante = eglise.coutRecherche1[0]
                self.ressourceManquante = 'bois'
                return

        print("pas d'église")
        unit = self.trouverUniteLibre("")
        if self.epoque >= 2:
            if time.time() - self.derniereEglise >= self.cooldownBatiment:
                position = self.trouverRessourcePlusPres(unit, Tuile.GAZON)
                self.batirBatiment(Batiment.LIEU_CULTE, unit)
                print("Eglise créée")
                return
        else:
            print("pas la bonne époque pour crééer un église")

    def creerSoldat(self):
        print("creer Soldat")
        baraque = self.trouverBatiment(Batiment.BARAQUE, "creation", self.civilisation)
        if baraque != None:
            if isinstance(baraque, Baraque):
                if not baraque.enCreation:
                    if  self.ressources['nourriture'] >= baraque.coutCreer1['nourriture']:
                        baraque.creer1()
                        return
                    else:
                        self.manqueRessource = True
                        self.qteRessourceManquante = baraque.coutCreer1['nourriture']
                        self.ressourceManquante = 'nourriture'
                        print("en création soldat")
                        return

        print("pas de baraque")
        unit = self.trouverUniteLibre("")
        if self.epoque >= 2:
            if time.time() - self.derniereBarraque >= self.cooldownBatiment:
                self.batirBatiment(Batiment.BARAQUE, unit)
                self.derniereBarraque = time.time()
                print("Baraque créée")
                return
        else:
            print("!pas la bonne époque pour créer une baraque!")

    def attaquer(self):
        print("attaquer")
        self.creerSoldat()
        destination = self.trouverBatiment(Batiment.BASE, "", self.ennemiPlusFort)
        if destination == None:
            destination = self.trouverPremierBatiment(self.ennemiPlusFort)
        for unitID in self.units:
            unit = self.model.getUnit(unitID)
            if isinstance(unit, Soldat):
                unit.modeAttack = Unit.ACTIF
                batiment = self.model.trouverCentreCase(destination.posX, destination.posY)
                self.deplacerUnite(batiment[0], batiment[1], unit, None)


    def retraite(self):
        print("retraite")
        destination = self.trouverBatiment(Batiment.HOPITAL, "", self.civilisation)
        if destination == None:
            destination = self.trouverBatiment(Batiment.BASE, "", self.civilisation)
        if destination == None:
            destination = self.trouverPremierBatiment( self.civilisation)

        for unitID in self.units:
            unit = self.model.getUnit(unitID)
            if isinstance(unit, Soldat):
                unit.modeAttack = Unit.PASSIF
                batiment = self.model.trouverCentreCase(destination.posX, destination.posY)
                self.deplacerUnite(batiment[0], batiment[1], unit, None)
        self.paix = True

    def defendre(self):
        print("défense")
        destination = self.trouverBatiment(Batiment.BASE, "", self.civilisation)
        if destination == None:
            destination = self.trouverPremierBatiment( self.civilisation)

        for unitID in self.units:
            unit = self.model.getUnit(unitID)
            unit.modeAttack = Unit.ACTIF
            batiment = self.model.trouverCentreCase(destination.posX+1, destination.posY+1)
            self.deplacerUnite(batiment[0], batiment[1], unit, None)

    def rechercher(self):
        print("rechercher")
        #TODO figurer comment rechercher
        self.derniereRecherche = time.time()


    def blackboard(self):
        #fais des test 1 fois au 30 sec pour éviter de trop répéter des taches

        if time.time() - self.lastCheck >= 30:


            self.nombrePaysans = 0
            #vérifie si tous les paysans sont occupés
            self.paysansOccupes = True
            for unit in self.units.values():
                if isinstance(unit, Paysan):
                    self.nombrePaysans += 1
                    if unit.typeRessource == 0:
                        self.paysansOccupes = False


            #compte les soldats à nous et trouve le hp moyen de ces soldats
            self.nombreSoldatsAllies = 0
            hpTotal = 0
            for unitID in self.units:
                unit = self.model.getUnit(unitID)
                if isinstance(unit, Soldat):
                    self.nombreSoldatsAllies += 1
                    hpTotal += unit.hp

            if self.nombreSoldatsAllies > 0:
                self.hpMoyen = hpTotal/self.nombreSoldatsAllies
            else:
                self.hpMoyen = 100
                self.paix = True


            #trouve le nombre de soldats de l'ennemi avec le plus de soldats
            self.nombreSoldatsEnnemis = 0
            for joueur in self.model.joueurs.values():
                nombreSoldatsCiv = 0
                if joueur.civilisation != self.civilisation:
                    for unitID in joueur.units:
                        unit = self.model.getUnit(unitID)
                        if isinstance(unit, Soldat):
                            nombreSoldatsCiv += 1
                    if nombreSoldatsCiv > self.nombreSoldatsEnnemis:
                        self.nombreSoldatsEnnemis = nombreSoldatsCiv
                        self.ennemiPlusFort = joueur.civilisation
                    #print(nombreSoldatsCiv," soldats de civ " ,joueur.civilisation)
            #print(self.nombreSoldatsEnnemis, " soldats pour civ ", self.ennemiPlusFort)

            #determine si la base est sous attaque
            base = self.trouverBatiment(Batiment.BASE, "", self.civilisation)
            if base:
                if self.lastHPBase > base.pointsDeVie:
                    self.paix = False
                    self.defendre()
                else:
                    self.paix = True
                    for unitID in self.units:
                        unit = self.model.getUnit(unitID)
                        unit.modeAttack = unit.PASSIF

                print(base.pointsDeVie)
                self.lastHPBase = base.pointsDeVie

            else:
                unit = self.trouverUniteLibre("")
                if unit == None:
                    print("AI DEAD")
                    return
                else:
                    self.paix = True
                    for unitID in self.units:
                        unit = self.model.getUnit(unitID)
                        unit.modeAttack = unit.PASSIF

                    self.batirBatiment(Batiment.BASE, unit)



            self.lastCheck = time.time()

    def trouverRessourcePlusPres(self, unit, typeRessource):
        ressource = {"x" : 0 , "y" : 0}
        if unit == None:
            self.creerPaysan()
            return
        
        return self.model.trouverRessourcePlusPres(unit, typeRessource)
        

    def update(self):

        self.updateUnits()
        self.updatePaysans()
        self.updateBuildings()

        if time.time() > self.tempsDepart + 1:
            if time.time() - self.derniereAction >= 5:
                self.derniereAction = time.time()
                self.penser()


    def deplacerUnite(self, butX, butY, unite, building):
        print(butX, butY, unite.x, unite.y)
        self.model.controller.eventListener.onMapRClick(Noeud(None, butX, butY, None, None), [unite], building, None, True)
        #cmd = Command(self.civilisation, Command.MOVE_UNIT)
        #cmd.addData('ID', unite.id)
        #cmd.addData('X1', unite.x)
        #cmd.addData('Y1', unite.y)
        #cmd.addData('X2', butX)
        #cmd.addData('Y2', butY)
        #self.model.controller.network.client.sendCommand(cmd)

    def batirBatiment(self, type, unite):
        if unite == None:
            self.creerPaysan()
            print("no unit selected for build")
            return
        else:
            position = self.trouverZoneLibrePourBatir(unite)
            unite.building = []
            unite.building.append(Batiment.generateId(self.civilisation))
            unite.building.append(type)

            self.deplacerUnite(position["x"], position["y"], unite, unite.building)

    def trouverBatiment(self, type, raison, civilisation):
        if civilisation == self.civilisation:
            if raison == "creation":
                for building in self.buildings.values():
                    if building.type == type:
                        if not building.enCreation:
                            return building

            if raison == "recherche":
                for building in self.buildings.values():
                    if building.type == type:
                        if not building.enRecherche:
                            return building

            else:
                for building in self.buildings.values():
                    if building.type == type:
                        return building

            return None

        else:
            for joueur in self.model.joueurs.values():
                if joueur.civilisation == civilisation:
                    for batimentID in joueur.buildings:
                        if isinstance(self.model.getBuilding(batimentID), Base):
                            return self.model.getBuilding(batimentID)

    def trouverPremierBatiment(self, civilisation):
        for joueur in self.model.joueurs.values():
            if joueur.civilisation == civilisation:
                for batimentID in joueur.buildings:
                    return self.model.getBuilding(batimentID)

    def trouverUniteLibre(self, typeRessource):
        #cherche d'abord une unité libre
        for unitID in self.units:
            unit = self.model.getUnit(unitID)
            if isinstance(unit, Paysan):
                if unit.typeRessource == 0:
                    print("found libre")
                    return unit
        print("none free")
        bois = True
        minerai = True
        charbon = True
        nourriture = True

        if self.ressources['bois'] >= 150:
            bois = False
        if self.ressources['minerai'] >= 100:
            minerai = False
        if self.ressources['charbon'] >= 50:
            charbon = False
        if self.ressources['nourriture'] >= 200:
            nourriture = False
        #ensuite cherche une unité que amasse des ressources non requises
        for unitID in self.units:
            unit = self.model.getUnit(unitID)
            if isinstance(unit, Paysan):
                if unit.typeRessource != typeRessource:
                    if unit.nbRessources != unit.nbRessourcesMax:
                        if unit.typeRessource == Tuile.FORET and not bois:
                            print("found wood for nothing")
                            return unit
                        elif unit.typeRessource == Tuile.MINERAI and not minerai:
                            print("found mieral for nothing")
                            return unit
                        elif unit.typeRessource == Tuile.CHARBON and not charbon:
                            print("found coal for nothing")
                            return unit
                        else:
                            print(unit.typeRessource)
        print("none doing something else unless stuck from empty ressource")

        #reset toutes les unités avec la ressource voulue à type 0 pour unstick
        for unitID in self.units:
            unit = self.model.getUnit(unitID)
            if isinstance(unit, Paysan):
                if unit.nbRessources != unit.nbRessourcesMax:
                    if unit.typeRessource == typeRessource:
                        unit.typeRessource = 0

        print("ok all set to 0")

        #cherche d'abord une unité libre
        for unitID in self.units:
            unit = self.model.getUnit(unitID)
            if isinstance(unit, Paysan):
                if unit.nbRessources != unit.nbRessourcesMax:
                    if unit.typeRessource == 0:
                        print("found libre")
                        return unit


        #for unitID in self.units:
         #   unit = self.model.getUnit(unitID)
          #  if isinstance(unit, Paysan):
           #     if unit.nbRessources != unit.nbRessourcesMax:
            #        print("found 1st not full ressource")
             #       return unit
        print("ok wtf why none found")
        return None

    def trouverZoneLibrePourBatir(self, unit):

        position = {'x' : 0, 'y' : 0}


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
            if maxX > self.model.carte.size * 48:
                maxX = self.model.carte.size * 48

            #si le maximum des Y à vérifier est plus grand que la taille de la map, le mettre au max de la map
            #taille de la map * 48 parceque la taille de la map est en tuiles et chaque tuile est de 48 pixels
            if maxY > self.model.carte.size * 48:
                maxY = self.model.carte.size * 48

            print(maxX)
            print(maxY)
            print(minX)
            print(minY)

            for x in range (minX, maxX, 48):
                for y in range (minY, maxY, 48):
                    casesCible = self.model.trouverCaseMatrice(x, y)
                    caseCibleX = casesCible[0]
                    caseCibleY = casesCible[1]
                    if self.model.carte.matrice[caseCibleX][caseCibleY].type == Tuile.GAZON:
                        if self.model.validPosBuilding(caseCibleX, caseCibleY):

                            position["x"] = x
                            position["y"] = y
                            print("!", x,y)
                            return position
