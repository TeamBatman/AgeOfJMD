#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from Commands import Command
from Carte import Carte
from GraphicsManagement import SpriteSheet

import time
import math

class Unit():
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent
        self.vitesse = 5
        self.grandeur = 32
        self.cibleX = x
        self.cibleY = y
        self.cheminTrace = []
        self.cibleXTrace = x
        self.cibleXTrace = y
        self.cibleXDeplacement = x
        self.cibleYDeplacement = y
        self.mode = 0  # 1=ressource
        self.trouver = True #pour le pathfinding
        self.enDeplacement = False
        self.ancienX = self.x
        self.ancienY = self.y

        # ANIMATION
        self.lastAnimtaionTime = time.time()
        self.animationRate = 333  # in millisecond
        self.spriteSheet = SpriteSheet('Units/Age_I/red_caveman_1.png')

        self.animDirection = 'DOWN'
        self.animFrameIndex = 1

        activeFrameKey = '%s_%s' % (self.animDirection, self.animFrameIndex)
        self.activeFrame = self.spriteSheet.frames[activeFrameKey]
        self.activeOutline = self.spriteSheet.framesOutlines[activeFrameKey]

    def animer(self):
        """ Lance l'animation de l'unité
        """
        if not time.time() - self.lastAnimtaionTime >= self.animationRate / 1000:
            return

        self.animFrameIndex += 1

        if self.animFrameIndex == self.spriteSheet.NB_FRAME_ROW:
            self.animFrameIndex = 0
        if self.animFrameIndex == 1:  # POSITION NEUTRE ON NE VEUT PAS ÇA
            self.animFrameIndex = 2

        activeFrameKey = '%s_%s' % (self.animDirection, self.animFrameIndex)
        self.activeFrame = self.spriteSheet.frames[activeFrameKey]
        self.activeOutline = self.spriteSheet.framesOutlines[activeFrameKey]
        self.lastAnimtaionTime = time.time()

    def update(self):
        try:
            if self.enDeplacement:
                if not self.trouver:
                    self.deplacement()
                    self.choisirTraceFail()
                else:
                    self.deplacementTrace()
        except:
            print("unit fail")
            self.deplacement()
                
        #try:
        #    self.deplacementTrace()
        #except:
        #    print("unit fail")
            #self.deplacement()


    def changerCible(self, cibleX, cibleY):
        self.mode = 0
        self.cibleX = cibleX
        self.cibleY = cibleY
        self.cibleXDeplacement = cibleX
        self.cibleYDeplacement = cibleY
        self.trouver = False
        self.enDeplacement = True
        self.time1 = 0
        self.nbTour = 0
        self.choisirTrace()
        

    def deplacement(self):
        self.posX = self.x
        self.posY = self.y
        if abs(self.cibleX - self.x) <= self.vitesse:
            self.x = self.cibleX
        if abs(self.cibleY - self.y) <= self.vitesse:
            self.y = self.cibleY

        if self.cibleX > self.x:
            self.x += self.vitesse
            self.animDirection = 'RIGHT'

        elif self.cibleX < self.x:
            self.x -= self.vitesse
            self.animDirection = 'LEFT'

        if self.cibleY > self.y:
            self.y += self.vitesse
            self.animDirection = 'DOWN'

        elif self.cibleY < self.y:
            self.y -= self.vitesse
            self.animDirection = 'UP'

        cases1 = self.parent.trouverCaseMatrice(self.x , self.y)
        cases2 = self.parent.trouverCaseMatrice(self.x + self.grandeur , self.y)
        cases3 = self.parent.trouverCaseMatrice(self.x , self.y+ self.grandeur)
        cases4 = self.parent.trouverCaseMatrice(self.x+ self.grandeur , self.y+ self.grandeur)
        if not self.parent.carte.matrice[cases1[0]][cases1[1]].type == 0 or not self.parent.carte.matrice[cases2[0]][cases2[1]].type == 0 or not self.parent.carte.matrice[cases3[0]][cases3[1]].type == 0 or not self.parent.carte.matrice[cases4[0]][cases4[1]].type == 0:
            trouve = False
            self.x = self.posX
            self.y = self.posY
            #cases = self.parent.trouverCaseMatrice(self.x+self.grandeur, self.y+self.grandeur)
            self.choixPossible = []
            liste = [-1,0,1]
            #print("----", self.x, self.y)
            for i in liste:
                for j in liste:
                    if not(i==0 and j==0):
                        #print(i,j)
                        cases1 = self.parent.trouverCaseMatrice(self.x+(i*self.vitesse), self.y+(j*self.vitesse))
                        cases2 = self.parent.trouverCaseMatrice(self.x+(i*self.vitesse)+self.grandeur, self.y+(j*self.vitesse))
                        cases3 = self.parent.trouverCaseMatrice(self.x+(i*self.vitesse), self.y+(j*self.vitesse) + self.grandeur)
                        cases4 = self.parent.trouverCaseMatrice(self.x+(i*self.vitesse)+self.grandeur, self.y+(j*self.vitesse)+self.grandeur)
                       # print(cases2[0],cases2[1])
                        if (self.parent.carte.matrice[cases1[0]][cases1[1]].type == 0 and self.parent.carte.matrice[cases2[0]][cases2[1]].type == 0 and self.parent.carte.matrice[cases3[0]][cases3[1]].type == 0 and self.parent.carte.matrice[cases4[0]][cases4[1]].type == 0):
                            #print(self.parent.carte.matrice[cases1[0]][cases1[1]].type == 0, self.parent.carte.matrice[cases2[0]][cases2[1]].type == 0,  self.parent.carte.matrice[cases3[0]][cases3[1]].type == 0 ,self.parent.carte.matrice[cases4[0]][cases4[1]].type == 0)
                            if not self.ancienX == self.x+(i*self.vitesse) and not self.ancienY == self.y+(j*self.vitesse):
                                self.x = self.posX
                                self.y = self.posY
                                self.x += (i*self.vitesse)
                                self.y += (j*self.vitesse)
                                self.choixPossible.append([self.x,self.y])
                                #cases0 = self.parent.trouverCaseMatrice(self.posX , self.posY)
                                #print(cases0,cases1,cases2,cases3,cases4)
                                trouve = True
                                #break
                        #if trouve == False:
                        #    print("ouais")
           # print(len(self.choixPossible))
            if self.choixPossible: #Choisir le meilleur point sur les points possibles
                self.x = self.choixPossible[0][0]
                self.y = self.choixPossible[0][1]
                diff = abs(self.x - self.cibleX) + abs(self.y - self.cibleY)
                for coord in self.choixPossible:
                    #print(coord[0],coord[1])
                    diffCoord = abs(coord[0] - self.cibleX) + abs(coord[1] - self.cibleY)
                    if diff > diffCoord:
                        self.x = coord[0]
                        self.y = coord[1]
                        diff = diffCoord
                        #TODO: Mettre les animations !
            if trouve == False:
                print("rate !", self.x,self.ancienX, self.y,self.ancienY)
                self.x = self.ancienX
                self.y = self.ancienY
                
                

        self.ancienX = self.posX
        self.ancienY = self.posY

        # Puisqu'il y a eu un déplacement
        self.animer()


    def deplacementTrace(self):
        #TODO: Mettre les animations ! Mettre les obstacles !
        
        #self.afficherList("chemin", self.cheminTrace)
        #print("courant", self.x, self.y, self.cibleXDeplacement, self.cibleYDeplacement)
        if len(self.cheminTrace) > 0:
            if self.x == self.cibleXDeplacement and self.y == self.cibleYDeplacement:
                del self.cheminTrace[-1]
                self.nbTour += 1
                #self.cheminTrace = self.cheminTrace[:len(self.cheminTrace)-self.nbTour]
                if len(self.cheminTrace) <= 0: #FIN
                    self.animFrameIndex = 1
                    self.animDirection = 'DOWN'
                    activeFrameKey = 'DOWN_1'
                    self.activeFrame = self.spriteSheet.frames[activeFrameKey]
                    self.activeOutline = self.spriteSheet.framesOutlines[activeFrameKey]
                    self.enDeplacement = False
                    return -1
                self.cibleXDeplacement = self.cheminTrace[-1].x
                self.cibleYDeplacement = self.cheminTrace[-1].y

            if not abs(self.cibleXDeplacement - self.x) == 0 and not abs(self.cibleYDeplacement - self.y) == 0:
                diaganoleVit = math.sqrt(math.pow(self.vitesse,2) + math.pow(self.vitesse,2))
                diaganoleVit /= 2
            else:
                diaganoleVit = self.vitesse #vitesse normal

            if abs(self.cibleXDeplacement - self.x) <= diaganoleVit:
                self.x = self.cibleXDeplacement
            if abs(self.cibleYDeplacement - self.y) <= diaganoleVit:
                self.y = self.cibleYDeplacement

            if self.cibleXDeplacement > self.x:
                self.x += diaganoleVit
                self.animDirection = 'RIGHT'

            elif self.cibleXDeplacement < self.x:
                self.x -= diaganoleVit
                self.animDirection = 'LEFT'

            if self.cibleYDeplacement > self.y:
                self.y += diaganoleVit
                self.animDirection = 'DOWN'

            elif self.cibleYDeplacement < self.y:
                self.y -= diaganoleVit
                self.animDirection = 'UP'

            # Puisqu'il y a eu un déplacement
            self.animer()

            #if self.x == self.cheminTrace[-1].x and self.y == self.cheminTrace[-1].y:
                #print("DELETE!!!")
             #   self.nbTour += 1
                #self.afficherList("chemin", self.cheminTrace)
                #del self.cheminTrace[-1]
                #self.cheminTrace = self.cheminTrace[:len(self.cheminTrace)-self.nbTour]
                #print("dernier",self.cheminTrace[-1].x, self.cheminTrace[-1].y)

            #if self.trouver == False and len(self.cheminTrace) < 20:
            #if self.trouver == False:
                #print("pas trouver")
                #self.choisirTraceFail()


    def choisirTrace(self):
        cases = self.parent.trouverCaseMatrice(self.x, self.y)
        caseX = cases[0]
        caseY = cases[1]
        self.mode = 0
        casesCible = self.parent.trouverCaseMatrice(self.cibleX, self.cibleY)
        if not self.parent.carte.matrice[casesCible[0]][casesCible[1]].type == 0:
            if isinstance(self, Paysan):
                print("ressource")
                self.parent.enRessource.append(self)
                self.mode = 1  # ressource
                # TODO Changer le chemin pour aller à côté de la ressource !
            else:
                return -1  # Ne peut pas aller sur un obstacle
        caseCibleX = casesCible[0]
        caseCibleY = casesCible[1]

        noeudInit = Noeud(None, caseX, caseY, caseCibleX, caseCibleY)
        self.open = []
        self.closed = []
        self.open.append(noeudInit)
        self.time1 = time.time()
        chemin = self.aEtoile(0.3)
        #print("Temps a*: ", time.time() - self.time1)
        n = chemin
        if not n == -1:
            self.cheminTrace = []
            while n.parent:
                self.cheminTrace.append(n)
                centreCase = self.parent.trouverCentreCase(n.x, n.y)
                n.x = centreCase[0]
                n.y = centreCase[1]
                n = n.parent
            # print(self.cheminTrace,"len", len(self.cheminTrace))
            if self.cheminTrace:
                #Pour ne pas finir sur le centre de la case (Pour finir sur le x,y du clic)
                if not self.mode == 1:  #pas en mode ressource
                    self.cheminTrace[0] = Noeud(None, self.cibleX, self.cibleY, None, None)
            else:
                if not self.mode == 1:  #pas en mode ressource
                    self.cheminTrace.append(Noeud(None, self.cibleX, self.cibleY, None, None))
                else:
                    self.cheminTrace.append(Noeud(None, self.x, self.y, None, None))

            self.cibleXDeplacement = self.cheminTrace[-1].x
            self.cibleYDeplacement = self.cheminTrace[-1].y


    def choisirTraceFail(self):
        #print("traceFail", self.cibleX,self.cibleY)
        #print("avant", n.x,n.y)
        self.open = []
        self.closed = []

        self.open = self.ancienOpen
        #self.afficherList("open",self.ancienOpen)
        self.closed = self.ancienClosed
        #self.afficherList("closed",self.ancienClosed)
        #noeudInit = self.ancienN
        n = self.cheminTrace[0]
        cases = self.parent.trouverCaseMatrice(n.x,n.y)
        n.x = cases[0]
        n.y = cases[1]
        noeudInit = n
        
        #print("x,y",n.x,n.y)
        #print("cibleself", self.cibleX,self.cibleY)
        #print("debut a*")
        self.time1= time.time()
        chemin = self.aEtoile(0.01)
       # print("Temps a*: ", time.time()-self.time1)
        n = chemin
        if not n == -1:
            self.cheminTrace = []
            while(not n.parent== None):
                self.cheminTrace.append(n)
                #print("boucle", n.x, n.y)
                if isinstance(n.x, int):
                    centreCase = self.parent.trouverCentreCase(int(n.x),int(n.y))
                    n.x = centreCase[0]
                    n.y = centreCase[1]
                else:
                    pass
                
                n = n.parent
            #print(self.cheminTrace,"len", len(self.cheminTrace))
            if self.trouver == True:
                if self.cheminTrace:
                    print("DUDE !",self.cibleX,self.cibleY)
                    #Pour ne pas finir sur le centre de la case (Pour finir sur le x,y du clic)
                    self.cheminTrace[0] = Noeud(None,self.cibleX,self.cibleY,None ,None)
                else:
                    print("DUDE !",self.cibleX,self.cibleY)
                    self.cheminTrace.append(Noeud(None,self.cibleX,self.cibleY,None ,None))

            #print("chemin", len(self.cheminTrace),self.cheminTrace[-1].x,self.cheminTrace[-1].y )
           # print("courant", self.x,self.y , self.nbTour)
            #self.afficherList("chemin", self.cheminTrace)
            #self.afficherList("chemin", self.cheminTrace)
           
                self.cheminTrace = self.cheminTrace[:len(self.cheminTrace)-self.nbTour]
                while abs(self.x - self.cibleX) + abs(self.y - self.cibleY) < abs(self.cheminTrace[-1].x - self.cibleX) + abs(self.cheminTrace[-1].y - self.cibleY):
                #print(self.x, self.cheminTrace[-1].x,self.y , self.cheminTrace[-1].y)
                #if self.x == self.cheminTrace[-1].x and self.y == self.cheminTrace[-1].y:
                    #print("DELETE!!!")
                    #self.nbTour += 1
                   # self.afficherList("chemin", self.cheminTrace)
                    del self.cheminTrace[-1]
                   # print("dernier",self.cheminTrace[-1].x, self.cheminTrace[-1].y)
                    
                    
                #for n in self.cheminTrace:
                #    if self.x == n.x and self.y == n.y:
                #        print("DELETE!!!")
                 #       self.afficherList("chemin", self.cheminTrace)
                #        index = self.cheminTrace.index(n)
                #        self.cheminTrace = self.cheminTrace[:index]
                 #       print("dernier",self.cheminTrace[-1].x, self.cheminTrace[-1].y, "index", index)
                 #       break

                 
                self.cibleXDeplacement = self.cheminTrace[-1].x
                self.cibleYDeplacement = self.cheminTrace[-1].y

    def aEtoile(self, tempsMax):
        nbNoeud = 100
        while self.open:
            n = self.open[0]
            if self.goal(n):
                self.trouver = True
                print("changeent true trouver !")
                self.ancienOpen = []
                self.ancienClosed = []
                return n
            self.open.remove(n)
            self.closed.append(n)

            successeurN = self.transition(n)

            for nPrime in successeurN:
                if nPrime in self.closed:
                    print("lol")
                aAjouter = True
                for i in range(len(self.open)):
                    if nPrime.x == self.open[i].x and nPrime.y == self.open[i].y:
                        if nPrime.cout <= self.open[i].cout:
                            del self.open[i]
                        else:
                            aAjouter = False
                        break
                if aAjouter:
                    self.open.append(nPrime)
                    
                    # Mettre dans le if aAjouter ?
                    #  time1= time.time()

            self.open.sort(key=lambda x: x.cout)
                # tempsTotal += time.time()-time1
                # print("Temps sort: ", tempsTotal)
            if len(self.open) > nbNoeud:
                #self.afficherList("open", self.open)
                #return -1
                self.open = self.open[:nbNoeud]
                #print(len(self.open))
                #self.parent.parent.v.afficherCourantPath(self.open)
            if time.time() - self.time1 > tempsMax:
                self.trouver = False
                #print("changeent false", n.x, n.y)
                #self.ancienClosed = self.closed
                self.ancienClosed = []
                #self.ancienOpen = self.open[:int((nbNoeud/2))]
                self.ancienOpen = self.open
                self.ancienN = n
                return n
        return -1

    def afficherList(self, nom, liste):
        for i in range(0, len(liste)):
            print(i, nom, liste[i].x, liste[i].y, "cout", liste[i].cout)

    def aCoteMur(self, caseX, caseY):  # Pour ne pas aller en diagonale et rentrer dans un mur
        #TODO BUG traverse un mur en diagonale
        if caseY - 1 >= 0:
            if caseX - 1 >= 0 and not self.parent.carte.matrice[caseX - 1][caseY - 1].type == 0:
                return True
            if not self.parent.carte.matrice[caseX][caseY - 1].type == 0:
                return True
            if caseX + 1 < self.parent.grandeurMat and not self.parent.carte.matrice[caseX + 1][caseY - 1].type == 0:
                return True

        if caseX - 1 >= 0 and not self.parent.carte.matrice[caseX - 1][caseY].type == 0:
            return True
        if caseX + 1 < self.parent.grandeurMat and not self.parent.carte.matrice[caseX + 1][caseY].type == 0:
            return True

        if caseY + 1 < self.parent.grandeurMat:
            if caseX - 1 >= 0 and not self.parent.carte.matrice[caseX - 1][caseY + 1].type == 0:
                return True
            if not self.parent.carte.matrice[caseX][caseY + 1].type == 0:
                return True
            if caseX + 1 < self.parent.grandeurMat and not self.parent.carte.matrice[caseX + 1][caseY + 1].type == 0:
                return True

        return False

    def transition(self, n):
        caseTransition = []

        caseX = n.x
        caseY = n.y
        casesCible = self.parent.trouverCaseMatrice(self.cibleX, self.cibleY)
        caseCibleX = casesCible[0]
        caseCibleY = casesCible[1]

        if caseY - 1 >= 0:
            if caseX - 1 >= 0 and self.parent.carte.matrice[caseX - 1][caseY - 1].type == 0 and not self.aCoteMur(
                            caseX - 1, caseY - 1):
                caseTransition.append(Noeud(n, caseX - 1, caseY - 1, caseCibleX, caseCibleY))
            if self.parent.carte.matrice[caseX][caseY - 1].type == 0:
                caseTransition.append(Noeud(n, caseX, caseY - 1, caseCibleX, caseCibleY))
            if caseX + 1 < self.parent.grandeurMat and self.parent.carte.matrice[caseX + 1][
                        caseY - 1].type == 0 and not self.aCoteMur(caseX + 1, caseY - 1):
                caseTransition.append(Noeud(n, caseX + 1, caseY - 1, caseCibleX, caseCibleY))

        if caseX - 1 >= 0 and self.parent.carte.matrice[caseX - 1][caseY].type == 0:
            caseTransition.append(Noeud(n, caseX - 1, caseY, caseCibleX, caseCibleY))
        if caseX + 1 < self.parent.grandeurMat and self.parent.carte.matrice[caseX + 1][caseY].type == 0:
            caseTransition.append(Noeud(n, caseX + 1, caseY, caseCibleX, caseCibleY))

        if caseY + 1 < self.parent.grandeurMat:
            if caseX - 1 >= 0 and self.parent.carte.matrice[caseX - 1][caseY + 1].type == 0 and not self.aCoteMur(
                            caseX - 1, caseY + 1):
                caseTransition.append(Noeud(n, caseX - 1, caseY + 1, caseCibleX, caseCibleY))
            if self.parent.carte.matrice[caseX][caseY + 1].type == 0:
                caseTransition.append(Noeud(n, caseX, caseY + 1, caseCibleX, caseCibleY))
            if caseX + 1 < self.parent.grandeurMat and self.parent.carte.matrice[caseX + 1][
                        caseY + 1].type == 0 and not self.aCoteMur(caseX + 1, caseY + 1):
                caseTransition.append(Noeud(n, caseX + 1, caseY + 1, caseCibleX, caseCibleY))

        return caseTransition


    def goal(self, noeud):
        casesCible = self.parent.trouverCaseMatrice(self.cibleX, self.cibleY)
        caseCibleX = casesCible[0]
        caseCibleY = casesCible[1]

        if noeud.x == caseCibleX and noeud.y == caseCibleY:
            return True
        elif abs(noeud.x - caseCibleX) <= 1 and abs(
                        noeud.y - caseCibleY) <= 1 and self.mode == 1:  # pour les ressources
            return True
        return False


class Noeud:
    def __init__(self, parent, x, y, cibleX, cibleY):
        self.parent = parent
        self.x = x
        self.y = y
        self.cout = 0
        if not (parent == None):
            self.calculerCout(cibleX, cibleY)

    def calculerCout(self, cibleX, cibleY):
        g = self.parent.cout + self.coutTransition(self.parent)
        h = abs(self.x - cibleX) + abs(self.y - cibleY)
        self.cout = g + h

    def coutTransition(self, n2):
        if abs(self.x - n2.x) == 1 and abs(self.y - n2.y) == 1:
            return 14  # Diagonale
        else:
            return 10


class Paysan(Unit):
    def __init__(self, x, y, parent):
        Unit.__init__(self, x, y, parent)
        self.vitesseRessource = 0.01  # La vitesse à ramasser des ressources
        self.nbRessourcesMax = 10
        self.nbRessources = 0
        self.typeRessource = 0  # 0 = Rien 1 à 4 = Ressources

    def chercherRessources(self):
        #print(int(self.nbRessources))
        #TODO Regarder le type de la ressource !
        #TODO Enlever nbRessources à la case ressource !
        if self.nbRessources + self.vitesseRessource <= self.nbRessourcesMax:
            self.nbRessources = self.nbRessources + self.vitesseRessource
        else:
            self.nbRessources = self.nbRessourcesMax
            #print("MAX!", self.nbRessources)
            #TODO Faire retourner à la base !        


class Model:
    def __init__(self, controller):
        self.controller = controller
        self.units = []
        self.grandeurMat = 106
        self.carte = Carte(self.grandeurMat)
        self.enRessource = []  # TODO ?À mettre dans Joueur?


    def update(self):
        self.updateUnits()

    def updateUnits(self):
        for unit in self.units:
            unit.update()


    def deleteUnit(self, x, y):  # TODO utiliser un tag ou un identifiant à la place des positions x et y (plus rapide)
        """ Supprime une unité à la liste d'unités
        :param x: position x de l'unité
        :param y: position y de l'unité
        """
        for unit in self.units:
            if unit.x == x and unit.y == y:
                self.units.remove(unit)

    def createUnit(self, x, y):
        """ Crée et ajoute une nouvelle unité à la liste des unités
        :param x: position x de l'unité
        :param y: position y de l'unité
        """
        # self.units.append(Unit(x, y, self))
        self.units.append(Paysan(x, y, self))

    def executeCommand(self, command):
        """ Exécute une commande
        :param command: la commande à exécuter
        """
        if command.data['TYPE'] == Command.CREATE_UNIT:
            self.createUnit(command.data['X'], command.data['Y'])

        elif command.data['TYPE'] == Command.DELETE_UNIT:
            self.deleteUnit(command.data['X'], command.data['Y'])
        elif command.data['TYPE'] == Command.MOVE_UNIT:
            for unit in self.units:
                if unit.x == command.data['X1'] and unit.y == command.data['Y1']:
                    unit.changerCible(command.data['X2'], command.data['Y2'])

    def trouverCaseMatrice(self, x, y):
        # TODO ? Mettre dans la vue ?

        grandeurCanevasRelle = self.grandeurMat * self.controller.view.item
        grandeurCase = grandeurCanevasRelle / self.grandeurMat
        caseX = int(x / grandeurCase)
        caseY = int(y / grandeurCase)

        return (caseX, caseY)

    def trouverCentreCase(self, caseX, caseY):
        # TODO ? Mettre dans la vue ?

        grandeurCanevasRelle = self.grandeurMat * self.controller.view.item
        grandeurCase = grandeurCanevasRelle / self.grandeurMat
        centreX = (grandeurCase * caseX) + grandeurCase / 2
        centreY = (grandeurCase * caseY) + grandeurCase / 2

        return (centreX, centreY)
