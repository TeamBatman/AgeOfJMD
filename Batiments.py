#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time



#TODO Remplacer les sleep par un test du temps
#TODO les bons constructeurs pour les unités et la bonne variable

class Batiment:
    def __init__(self,parent, posX, posY):
        self.pos = [posX, posY]
        self.peutEtreOccupe = False
        self.estOccupe = False
        self.pointsDeVie = 100
        self.estSelectionne = False
        self.type = ""
        self.parent = parent
        self.recherchesCompletes = 0
        self.enRecherche = False
        self.enCreation = False
        self.tempsDepartRecherche = 0
        self.tempsDepartCreation = 0

    def detruire(self):
        self.sortirUnites(self.parent)
        #TODO enlever de la liste des batiments
        #TODO retourner un % des ressources du cout

    def sortirUnites(self):
        #verifie si le batiment peut etre occupe puis s'il y a des unites dedans et les sort
        if self.peutEtreOccupe == True:
            if self.estOccupe == True:
                for i in range(0, self.parent.unites):
                    if self.parent.unites[i].batiment == self:
                        self.parent.unites[i].batiment == 0



class Eglise(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "Eglise"


    def boostMoral(self):
        if self.parent.epoque == 2:
            if self.enRecherche == False:
                self.enRecherche = True
                self.tempsDepartRecherche = time.time()
            if roundtime.time() - self.tempsDepartRecherche <= 60:
                self.parent.moral=100
                self.enRecherche = False
        else:
            if self.enRecherche == False:
                self.enRecherche = True
                self.tempsDepartRecherche = time.time()
            if time.time() - self.tempsDepartRecherche <= 120:
                self.parent.moral=100
                self.enRecherche = False



class TourDeGuet(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "Tour de guet"

    def meilleureVue(self):
        if self.parent.epoque == 2:
            if self.recherchesCompletes < 1:
                #TODO Decouverir comment le FOW fonctionnera
                #TODO ajouter le temps de recherche
                self.recherchesCompletes+=1

        else:
            if self.recherchesCompletes < 2:
                #TODO Decouverir comment le FOW fonctionnera
                #TODO ajouter le temps de recherche
                self.recherchesCompletes+=1



class Hopital(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "Hopital"
        self.peutEtreOccupe = True
        self.vitesseDeCreation = 30

    def healing(self, unite):
        #TODO decouvrir comment le healing va se faire
        #TODO ajouter le temps de recherche
        2

    def regenerationAmelioree(self):
        if self.recherchesCompletes < 1:
        #TODO decouvrir comment la regeneration va se faire
        #TODO ajouter le temps de recherche
            self.recherchesCompletes+=1



class Base(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "Base"
        self.vitesseDeCreation = 40


    def creerPaysan(self):
        if self.enCreation == False:
            self.enCreation = True
            self.tempsDepartCreation = round(time.time(), 0)
        elif time.time() - self.tempsDepartCreation <= 30:
            self.parent.units.add(Paysan(self.posX+4, self.posY+4, self.parent))


    def meilleureVitesse(self):
        if self.parent.epoque == 1:
            if self.recherchesCompletes < 1:
                #TODO ajouter le temps de recherche
                self.vitesseDeCreation = self.vitesseDeCreation*0.9
                self.recherchesCompletes+=1

        elif self.parent.epoque == 2:
            if self.recherchesCompletes < 2:
                #TODO ajouter le temps de recherche
                self.vitesseDeCreation = self.vitesseDeCreation*0.9
                self.recherchesCompletes+=1

        else:
            if self.recherchesCompletes < 3:
                #TODO ajouter le temps de recherche
                self.vitesseDeCreation = self.vitesseDeCreation*0.9
                self.recherchesCompletes+=1



class Baraque(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type="Baraque"
        self.vitesseDeCreation = 40

    def creerSoldatEpee(self):
        time.sleep(self.vitesseDeCreation)
        #TODO trouver le constructeur de soldat
        self.parent.unites.add(SoldatEpee(self.posX+4, self.posY+4, self.civilisation))

    def creerSoldatLance(self):
        time.sleep(self.vitesseDeCreation)
        #TODO trouver le constructeur de soldat
        self.parent.unites.add(SoldatLance(self.posX+4, self.posY+4, self.civilisation))

    def creerSoldatBouclier(self):
        time.sleep(self.vitesseDeCreation)
        #TODO trouver le constructeur de soldat
        self.parent.unites.add(SoldatBouclier(self.posX+4, self.posY+4, self.civilisation))

    def meilleureAttaque(self):
        if self.parent.epoque == 2:
            if self.recherchesCompletes < 1:
                time.sleep(60)
                for unite in self.parent.unites:
                    if unite.instanceof(Soldat):
                        unite.attaque = unite.attaque*1.1
                        self.recherchesCompletes += 1

        else:
            if self.recherchesCompletes < 2:
                time.sleep(60)
                for unite in self.parent.unites:
                    if unite.instanceof(Soldat):
                        unite.attaque = unite.attaque*1.1
                        self.recherchesCompletes += 1

    def meilleureVitesse(self):
        if self.parent.epoque == 2:
            if self.recherchesCompletes < 2:
                self.vitesseDeCreation = self.vitesseDeCreation*0.9
                self.recherchesCompletes+=1

        else:
            if self.recherchesCompletes < 3:
                self.vitesseDeCreation = self.vitesseDeCreation*0.9
                self.recherchesCompletes+=1



class Ferme(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.peutEtreOccupe = True
        self.production = 10

    def Produire(self):
        #TODO a se renseigner sur les valeurs pour la production
        while self.estOccupe == True:
            self.parent.nourriture += self.production
            time.sleep(10)

    def ameliorationPreoduction(self):
        if self.parent.epoque == 1:
            if self.recherchesCompletes < 1:
                time.sleep(60)
                self.production = self.production * 1.1
                self.recherchesCompletes += 1

        elif self.parent.epoque == 2:
            if self.recherchesCompletes < 2:
                time.sleep(60)
                self.production = self.production * 1.1
                self.recherchesCompletes += 1

        else :
            if self.recherchesCompletes < 3:
                time.sleep(60)
                self.production = self.production * 1.1
                self.recherchesCompletes += 1



class Scierie(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.peutEtreOccupe = True
        self.production = 10

    def Produire(self):
        #TODO a se renseigner sur les valeurs pour la production
        while self.estOccupe == True:
            self.parent.bois += self.production
            time.sleep(10)

    def ameliorationPreoduction(self):
        if self.parent.epoque == 2:
            if self.recherchesCompletes < 1:
                time.sleep(60)
                self.production = self.production * 1.1
                self.recherchesCompletes += 1

        else :
            if self.recherchesCompletes < 2:
                time.sleep(60)
                self.production = self.production * 1.1
                self.recherchesCompletes += 1



class Fonderie(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.peutEtreOccupe = True
        self.production = 10

    def Produire(self):
        #TODO a se renseigner sur les valeurs pour la production
        while self.estOccupe == True:
            self.parent.metal += self.production
            time.sleep(10)

    def ameliorationPreoduction(self):
        if self.parent.epoque == 3:
            if self.recherchesCompletes < 1:
                time.sleep(60)
                self.production = self.production * 1.1
                self.recherchesCompletes += 1


