#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time



#TODO les bons constructeurs pour les unités
#TODO L'hopital ne fait rien avec le healing
#TODO La fonction détruire batiment
#TODO le FOW pour la tour de guet


class Batiment:
    def __init__(self,parent, posX, posY):
        self.posX = posX
        self.posY = posY
        self.peutEtreOccupe = False
        self.estOccupe = False
        self.pointsDeVie = 100
        self.estSelectionne = False
        self.type = ""
        self.parent = parent
        self.recherchesCompletes = 0  #compte le nombre de recherches completées pour savoir si l'on peux en faire une nouvelle
        self.enRecherche = False #booléen pour empecher de recommencer la fonction de recherche si l'on est déjà en recherche
        self.enCreation = False #booléen pour empecher de recommencer la fonction de création si l'on est déjà en création
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
            elif time.time() - self.tempsDepartRecherche <= 60:
                self.parent.moral=100
                self.enRecherche = False
        else:
            if self.enRecherche == False:
                self.enRecherche = True
                self.tempsDepartRecherche = time.time()
            elif time.time() - self.tempsDepartRecherche <= 120:
                self.parent.moral=100
                self.enRecherche = False

    def miseAJour(self):
        if self.enRecherche:
            self.boostMoral()



class TourDeGuet(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "Tour de guet"

    def meilleureVue(self):
        if self.parent.epoque == 2:
            if self.recherchesCompletes < 1:
                if self.enRecherche == False:
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche <= 60:
                    #TODO Decouverir comment le FOW fonctionnera
                    self.recherchesCompletes += 1
                    self.enRecherche = False

        else:
            if self.recherchesCompletes < 2:
                if self.enRecherche == False:
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche <= 60:
                    #TODO Decouverir comment le FOW fonctionnera
                    self.recherchesCompletes += 1
                    self.enRecherche = False

    def miseAJour(self):
        if self.enRecherche:
            self.meilleureVue()


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

    def regenerationAmelioree(self):
        if self.recherchesCompletes < 1:
            if self.recherchesCompletes < 1:
                if self.enRecherche == False:
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche <= 60:
                    self.recherchesCompletes += 1
                    self.enRecherche = False
                    #TODO decouvrir comment la regeneration va se faire

    def miseAJour(self):
        if self.enRecherche:
            self.regenerationAmelioree()


class Base(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type = "Base"
        self.vitesseDeCreation = 40


    def creerPaysan(self):
        if self.enCreation == False:
            self.enCreation = True
            self.tempsDepartCreation = time.time()

        elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
            self.parent.units.append(Paysan(self.posX+4, self.posY+4, self.parent))
            self.enCreation = False


    def meilleureVitesse(self):
        if self.parent.epoque == 1:
            if self.recherchesCompletes < 1:
                if self.enRecherche == False:
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche <= 60:
                    self.recherchesCompletes += 1
                    self.enRecherche = False
                    self.vitesseDeCreation = self.vitesseDeCreation*0.9
                    self.recherchesCompletes += 1

        elif self.parent.epoque == 2:
            if self.recherchesCompletes < 2:
               if self.enRecherche == False:
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
               elif time.time() - self.tempsDepartRecherche >= 60:
                    self.recherchesCompletes += 1
                    self.enRecherche = False
                    self.vitesseDeCreation = self.vitesseDeCreation*0.9
                    self.recherchesCompletes += 1

        else:
            if self.recherchesCompletes < 3:
                if self.enRecherche == False:
                    self.enRecherche = True
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.recherchesCompletes += 1
                    self.enRecherche = False
                self.vitesseDeCreation = self.vitesseDeCreation*0.9
                self.recherchesCompletes+=1

    def miseAJour(self):
        if self.enCreation:
            self.creerPaysan()
        if self.enRecherche:
            self.meilleureVitesse()


class Baraque(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.type="Baraque"
        self.vitesseDeCreation = 40
        self.typeCreation = ""
        self.typeRecherche = ""
        self.recherchesCompletesvitesse = 0
        self.recherchesCompletesAttaque = 0

    def creerSoldatEpee(self):
        if self.enCreation == False:
            self.enCreation = True
            self.typeCreation = "Epee"
            self.tempsDepartCreation = time.time()
        elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
            self.parent.unites.add(SoldatEpee(self.posX+4, self.posY+4))
            self.enCreation = False

    def creerSoldatLance(self):
        if self.enCreation == False:
            self.enCreation = True
            self.typeCreation = "Lance"
            self.tempsDepartCreation = time.time()
        elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
            self.parent.unites.add(SoldatLance(self.posX+4, self.posY+4))
            self.enCreation = False

    def creerSoldatBouclier(self):
        if self.enCreation == False:
            self.enCreation = True
            self.typeCreation = "Bouclier"
            self.tempsDepartCreation = time.time()
        elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
            self.parent.unites.add(SoldatBouclier(self.posX+4, self.posY+4))
            self.enCreation = False

    def meilleureAttaque(self):
        if self.parent.epoque == 2:
            if self.recherchesCompletesAttaque < 1:
               if self.enRecherche == False:
                   self.enRecherche = True
                   self.tempsDepartRecherche = time.time()
                   self.typeRecherche = "Attaque"

               elif time.time() - self.tempsDepartRecherche >= 60:
                   self.enRecherche = False
                   for unite in self.parent.units:
                        if isinstance(unite, Soldat):
                            unite.attaque = unite.attaque*1.1
                   self.recherchesCompletesAttaque += 1

        elif self.recherchesCompletesAttaque <2:
            if self.enRecherche == False:
                 self.enRecherche = True
                 self.tempsDepartRecherche = time.time()
                 self.typeRecherche = "Attaque"

            elif time.time() - self.tempsDepartRecherche >= 60:
                self.enRecherche = False
                for unite in self.parent.units:
                    if isinstance(unite, Soldat):
                        unite.attaque = unite.attaque*1.1
                self.recherchesCompletesAttaque += 1


    def meilleureVitesse(self):
        if self.parent.epoque == 2:
            if self.recherchesCompletesvitesse < 1:
                if self.enRecherche == False:
                    self.enRecherche = True
                    self.typeRecherche = "Vitesse"
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >=60:
                    self.vitesseDeCreation = self.vitesseDeCreation*0.9
                    self.recherchesCompletesvitesse += 1
                    self.enRecherche = False

        else:
            if self.recherchesCompletesvitesse < 2:
                if self.enRecherche == False:
                    self.enRecherche = True
                    self.typeRecherche = "Vitesse"
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >=60:
                    self.vitesseDeCreation = self.vitesseDeCreation*0.9
                    self.recherchesCompletesvitesse += 1
                    self.enRecherche = False

    def miseAJour(self):
        if self.enCreation:
            if self.typeCreation == "Epee":
                self.creerSoldatEpee()
            elif self.typeCreation == "Lance":
                self.creerSoldatLance()
            else:
                self.creerSoldatBouclier()
        if self.enRecherche:
            if self.typeRecherche == "Attaque":
                self.meilleureAttaque()
            else:
                self.meilleureVitesse()



class Ferme(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.peutEtreOccupe = True
        self.production = 10
        self.tempsProduction = 10

    def produire(self):
        #TODO a se renseigner sur les valeurs pour la production
        if self.estOccupe:
            if time.time() - self.tempsProduction >= 10:
                self.parent.nourriture += self.production
                self.tempsProduction = time.time()


    def ameliorationPreoduction(self):
        if self.parent.epoque == 1:
            if self.recherchesCompletes < 1:
                if self.enRecherche == False:
                    self.enRecherche = True;
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.recherchesCompletes += 1
                    self.enRecherche = False

        elif self.parent.epoque == 2:
            if self.recherchesCompletes < 2:
                if self.enRecherche == False:
                    self.enRecherche = True;
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.recherchesCompletes += 1
                    self.enRecherche = False

        else :
            if self.recherchesCompletes < 3:
                if self.enRecherche == False:
                    self.enRecherche = True;
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.recherchesCompletes += 1
                    self.enRecherche = False

    def miseAJour(self):
        if self.enRecherche:
            self.ameliorationPreoduction()

        self.produire()



class Scierie(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.peutEtreOccupe = True
        self.production = 10
        self.tempsProduction = 10

    def Produire(self):
        #TODO a se renseigner sur les valeurs pour la production
        if self.estOccupe:
            if time.time() - self.tempsProduction >= 10:
                self.parent.bois += self.production
                self.tempsProduction = time.time()

    def ameliorationPreoduction(self):
        if self.parent.epoque == 1:
            if self.recherchesCompletes < 1:
                if self.enRecherche == False:
                    self.enRecherche = True;
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.recherchesCompletes += 1
                    self.enRecherche = False

        elif self.parent.epoque == 2:
            if self.recherchesCompletes < 2:
                if self.enRecherche == False:
                    self.enRecherche = True;
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.recherchesCompletes += 1
                    self.enRecherche = False

        else :
            if self.recherchesCompletes < 3:
                if self.enRecherche == False:
                    self.enRecherche = True;
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.recherchesCompletes += 1
                    self.enRecherche = False

    def miseAJour(self):
        if self.enRecherche:
            self.ameliorationPreoduction()

        self.produire()



class Fonderie(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.peutEtreOccupe = True
        self.production = 10
        self.tempsProduction = 10

    def Produire(self):
        #TODO a se renseigner sur les valeurs pour la production
        if self.estOccupe:
            if time.time() - self.tempsProduction >= 10:
                self.parent.metal += self.production
                self.tempsProduction = time.time()

    def ameliorationPreoduction(self):
        if self.parent.epoque == 1:
            if self.recherchesCompletes < 1:
                if self.enRecherche == False:
                    self.enRecherche = True;
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.recherchesCompletes += 1
                    self.enRecherche = False

        elif self.parent.epoque == 2:
            if self.recherchesCompletes < 2:
                if self.enRecherche == False:
                    self.enRecherche = True;
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.recherchesCompletes += 1
                    self.enRecherche = False

        else :
            if self.recherchesCompletes < 3:
                if self.enRecherche == False:
                    self.enRecherche = True;
                    self.tempsDepartRecherche = time.time()
                elif time.time() - self.tempsDepartRecherche >= 60:
                    self.production = self.production * 1.1
                    self.recherchesCompletes += 1
                    self.enRecherche = False

    def miseAJour(self):
        if self.enRecherche:
            self.ameliorationPreoduction()

        self.produire()


class Garage(Batiment):
    def __init__(self, parent, posX, posY):
        super().__init__(parent, posX, posY)
        self.vitesseDeCreation = 60
        self.rechercheVitesse = 0
        self.rechercheHP = 0
        self.typeRecherche = ""

    def creerTanks(self):
        if self.enCreation == False:
            self.enCreation = True
            self.tempsDepartCreation = time.time()
        elif time.time() - self.tempsDepartCreation >= self.vitesseDeCreation:
            self.enCreation = False
            self.parent.units.append(Tank(self.posX+4, self.posY+4))

    def ameliorationVitesse(self):
        if self.rechercheVitesse < 1:
            if self.enRecherche == False:
                self.enRecherche = True
                self.tempsDepartRecherche = time.time()
                self.typeRecherche = "Vitesse"
            elif time.time() - self.tempsDepartRecherche >= 60:
                self.rechercheVitesse += 1
                self.enRecherche = False
                self.vitesseDeCreation = self.vitesseDeCreation * 0.8

    def ameliorationHP(self):
        if self.rechercheHP < 1:
            if self.enRecherche == False:
                self.enRecherche = True
                self.tempsDepartRecherche = time.time()
                self.typeRecherche = "HP"
            elif time.time() - self.tempsDepartRecherche >= 60:
                self.rechercheHP += 1
                self.enRecherche = False
                for tank in self.parent.units:
                    if isinstance(tank, Tank):
                        tank.hpMax = 120

    def miseSJour(self):
        if self.enCreation:
            self.creerTanks()
        if self.enRecherche:
            if self.typeRecherche == "Vitesse":
                self.ameliorationVitesse()
            else:
                self.ameliorationHP()