#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time


class Batiment:
    def __init__(self,parent, posX, posY, civilisation):
        self.pos = [posX, posY]
        self.civilisation = civilisation
        self.peutEtreOccupe = False
        self.estOccupe = False
        self.pointsDeVie = 100
        self.estSelectionne = False
        self.type = ""
        self.parent = parent
        self.recherchesCompletes = 0

    def detruire(self):
        self.sortirUnites(self.parent)
        #enlever de la liste des batiments
        #retourner un % des ressources du cout

    def sortirUnites(self):
        #verifie si le batiment peut etre occupe puis s'il y a des unites dedans et les sort
        if self.peutEtreOccupe == True:
            if self.estOccupe == True:
                for i in range(0, self.parent.unites):
                    if self.parent.unites[i].batiment == self:
                        self.parent.unites[i].batiment == 0



class Eglise(Batiment):
    def __init__(self, parent, posX, posY, civilisation):
        super().__init__(parent, posX, posY, civilisation)
        self.type = "Eglise"
        self.boostDisponible = True


    def boostMoral(self):
        if self.boostDisponible == True:
            if self.parent.epoque == 2:
                self.boostDisponible = False
                time.sleep(60)
                #a verifier si le moral fonctionnera de meme
                self.parent.moral=100
                time.sleep(120)
                self.boostDisponible = True
            else:
                self.boostDisponible = False
                time.sleep(120)
                self.parent.moral=100
                time.sleep(300)
                self.boostDisponible = True



class TourDeGuet(Batiment):
    def __init__(self, parent, posX, posY, civilisation):
        super().__init__(parent, posX, posY, civilisation)
        self.type = "Tour de guet"

    def meilleureVue(self):
        if self.parent.epoque == 2:
            if self.recherchesCompletes < 1:
                #Decouverir comment le FOW fonctionnera
                self.recherchesCompletes+=1

        else:
            if self.recherchesCompletes < 2:
                #Decouverir comment le FOW fonctionnera
                self.recherchesCompletes+=1



class Hopital(Batiment):
    def __init__(self, parent, posX, posY, civilisation):
        super().__init__(parent, posX, posY, civilisation)
        self.type = "Hopital"
        self.peutEtreOccupe = True
        self.vitesseDeCreation = 30

    def healing(self, unite):
        #decouvrir comment le healing va se faire
        2

    def regenerationAmelioree(self):
        if self.recherchesCompletes < 1:
        #decouvrir comment la regeneration va se faire
            self.recherchesCompletes+=1



class Base(Batiment):
    def __init__(self, parent, posX, posY, civilisation):
        super().__init__(parent, posX, posY, civilisation)
        self.type = "Base"
        self.vitesseDeCreation = 40


    def creerPaysan(self):
        time.sleep(self.vitesseDeCreation)
        #a decouvrir le constructeur de paysans
        self.parent.unites.add(Paysan(self.posX+4, self.posY+4, self.civilisation))

    def meilleureVitesse(self):
        if self.parent.epoque == 1:
            if self.recherchesCompletes < 1:
                self.vitesseDeCreation = self.vitesseDeCreation*0.9
                self.recherchesCompletes+=1

        elif self.parent.epoque == 2:
            if self.recherchesCompletes < 2:
                self.vitesseDeCreation = self.vitesseDeCreation*0.9
                self.recherchesCompletes+=1

        else:
            if self.recherchesCompletes < 3:
                self.vitesseDeCreation = self.vitesseDeCreation*0.9
                self.recherchesCompletes+=1



class Baraque(Batiment):
    def __init__(self, parent, posX, posY, civilisation):
        super().__init__(parent, posX, posY, civilisation)
        self.type="Baraque"
        self.vitesseDeCreation = 40

    def creerSoldatEpee(self):
        time.sleep(self.vitesseDeCreation)
        #trouver le constructeur de soldat
        self.parent.unites.add(SoldatEpee(self.posX+4, self.posY+4, self.civilisation))

    def creerSoldatLance(self):
        time.sleep(self.vitesseDeCreation)
        #trouver le constructeur de soldat
        self.parent.unites.add(SoldatLance(self.posX+4, self.posY+4, self.civilisation))

    def creerSoldatBouclier(self):
        time.sleep(self.vitesseDeCreation)
        #trouver le constructeur de soldat
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
    def __init__(self, parent, posX, posY, civilisation):
        super().__init__(parent, posX, posY, civilisation)
        self.peutEtreOccupe = True
        self.production = 10

    def Produire(self):
        #a se renseigner sur les valeurs pour la production
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
    def __init__(self, parent, posX, posY, civilisation):
        super().__init__(parent, posX, posY, civilisation)
        self.peutEtreOccupe = True
        self.production = 10

    def Produire(self):
        #a se renseigner sur les valeurs pour la production
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
    def __init__(self, parent, posX, posY, civilisation):
        super().__init__(parent, posX, posY, civilisation)
        self.peutEtreOccupe = True
        self.production = 10

    def Produire(self):
        #a se renseigner sur les valeurs pour la production
        while self.estOccupe == True:
            self.parent.metal += self.production
            time.sleep(10)

    def ameliorationPreoduction(self):
        if self.parent.epoque == 3:
            if self.recherchesCompletes < 1:
                time.sleep(60)
                self.production = self.production * 1.1
                self.recherchesCompletes += 1
