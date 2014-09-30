#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Commands import Command
from Carte import Carte
import time

class Unit():
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent
        self.vitesse = 5
        self.grandeur = 30
        self.cibleX = x
        self.cibleY = y
        self.cheminTrace = []
        self.cibleXTrace = x
        self.cibleXTrace = y

    def changerCible(self,cibleX ,cibleY):
        self.cibleX = cibleX
        self.cibleY = cibleY
        self.choisirTrace()
    
    def deplacement(self):
        if abs(self.cibleX - self.x) <= self.vitesse:
            self.x = self.cibleX
        if abs(self.cibleY - self.y) <= self.vitesse:
            self.y = self.cibleY
        if self.cibleX > self.x:
            self.x = self.x + self.vitesse
        elif self.cibleX < self.x:
            self.x = self.x - self.vitesse
        if self.cibleY > self.y:
            self.y = self.y + self.vitesse
        elif self.cibleY < self.y:
            self.y = self.y - self.vitesse

    def deplacementTrace(self):
        if len(self.cheminTrace) > 0:
            if self.x == self.cibleX and self.y == self.cibleY:
                del self.cheminTrace[-1]
                if len(self.cheminTrace) <= 0:
                    return -1
                self.cibleX = self.cheminTrace[-1].x
                self.cibleY = self.cheminTrace[-1].y

            if abs(self.cibleX - self.x) <= self.vitesse:
                self.x = self.cibleX
            if abs(self.cibleY - self.y) <= self.vitesse:
                self.y = self.cibleY
            if self.cibleX > self.x:
                self.x = self.x + self.vitesse
            elif self.cibleX < self.x:
                self.x = self.x - self.vitesse
            if self.cibleY > self.y:
                self.y = self.y + self.vitesse
            elif self.cibleY < self.y:
                self.y = self.y - self.vitesse

    def choisirTrace(self):
        cases = self.parent.trouverCaseMatrice(self.x,self.y)
        caseX = cases[0]
        caseY = cases[1]
        casesCible = self.parent.trouverCaseMatrice(self.cibleX,self.cibleY)
        if not self.parent.carte.matrice[casesCible[0]][casesCible[1]].type == 0 :
            if isinstance(self, Paysan):
                print("ressource")
                #TODO Changer le chemin pour aller à côté de la ressource !
            return -1 # Ne peut pas aller sur un obstacle
        caseCibleX = casesCible[0]
        caseCibleY = casesCible[1]
        
        noeudInit = Noeud(None,caseX,caseY,caseCibleX ,caseCibleY)
        self.open = []
        self.closed = []
        self.open.append(noeudInit)
        time1= time.time()
        chemin = self.aEtoile()
        print("Temps a*: ", time.time()-time1)
        n = chemin
        if not n == -1:
            self.cheminTrace = []
            while(not n.parent== None):
                self.cheminTrace.append(n)
                centreCase = self.parent.trouverCentreCase(n.x,n.y)
                n.x = centreCase[0]
                n.y = centreCase[1]
                n = n.parent
            #print(self.cheminTrace,"len", len(self.cheminTrace)) 
            self.cibleX = self.cheminTrace[-1].x
            self.cibleY = self.cheminTrace[-1].y

    def aEtoile(self):
        nbTour = 0
        nbNoeud = 400
        tempsTotal = 0
        while self.open:
            n = self.open[0]
            if self.goal(n) == True:
                return n
            self.open.remove(n)
            self.closed.append(n)
            
            successeurN = self.transition(n)
            
            for nPrime in successeurN:
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

               #Mettre dans le if aAjouter ?
             #  time1= time.time() 
               self.open.sort(key=lambda x: x.cout)
               #tempsTotal += time.time()-time1
              # print("Temps sort: ", tempsTotal)
               if len(self.open) > nbNoeud:
                   #self.afficherList("open", self.open)
                   #return -1
                   self.open = self.open[:nbNoeud]
               #print(len(self.open))
               #self.parent.parent.v.afficherCourantPath(self.open)
        return -1

    def afficherList(self,nom,liste):
        for i in range(0,len(liste)):
            print(i, nom, liste[i].x, liste[i].y, "cout", liste[i].cout)

    def aCoteMur(self,caseX,caseY): #Pour ne pas aller en diagonale est rentrer dans un mur
        #TODO BUG traverse un mur en diagonale
        if caseY-1 >= 0 :
            if caseX-1 >= 0 and not self.parent.carte.matrice[caseX-1][caseY-1].type == 0 :
                return True
            if not self.parent.carte.matrice[caseX][caseY-1].type  == 0:
                return True
            if caseX+1 < self.parent.grandeurMat and not self.parent.carte.matrice[caseX+1][caseY-1].type  == 0:
                return True

        #if caseX-1 >= 0 and not self.parent.carte.matrice[caseX-1][caseY]  == 0 :
        #    return False
        #if caseX+1 < self.parent.grandeurMat and not self.parent.carte.matrice[caseX+1][caseY]  == 0:
        #    return False

        if caseY+1 < self.parent.grandeurMat:
            if caseX-1 >= 0 and not self.parent.carte.matrice[caseX-1][caseY+1].type  == 0 :
                return True
            if not self.parent.carte.matrice[caseX][caseY+1].type  == 0:
                return True
            if caseX+1 < self.parent.grandeurMat and not  self.parent.carte.matrice[caseX+1][caseY+1].type  == 0 :
                return True

        return False
    
    def transition(self,n):
        caseTransition = []
        
        caseX = n.x
        caseY = n.y
        casesCible = self.parent.trouverCaseMatrice(self.cibleX,self.cibleY)
        caseCibleX = casesCible[0]
        caseCibleY = casesCible[1]
        
        if caseY-1 >= 0 :
            if caseX-1 >= 0 and self.parent.carte.matrice[caseX-1][caseY-1].type == 0 and not self.aCoteMur(caseX-1,caseY-1) :
                caseTransition.append(Noeud(n,caseX-1,caseY-1,caseCibleX,caseCibleY))
            if self.parent.carte.matrice[caseX][caseY-1].type  == 0:
                caseTransition.append(Noeud(n,caseX,caseY-1,caseCibleX,caseCibleY))
            if caseX+1 < self.parent.grandeurMat and self.parent.carte.matrice[caseX+1][caseY-1].type  == 0 and not self.aCoteMur(caseX+1,caseY-1):
                caseTransition.append(Noeud(n,caseX+1,caseY-1,caseCibleX,caseCibleY))
            
        if caseX-1 >= 0 and self.parent.carte.matrice[caseX-1][caseY].type  == 0 :
            caseTransition.append(Noeud(n,caseX-1,caseY,caseCibleX,caseCibleY))
        if caseX+1 < self.parent.grandeurMat and self.parent.carte.matrice[caseX+1][caseY].type == 0:
            caseTransition.append(Noeud(n,caseX+1,caseY,caseCibleX,caseCibleY))

        if caseY+1 < self.parent.grandeurMat:
            if caseX-1 >= 0 and self.parent.carte.matrice[caseX-1][caseY+1].type  == 0 and not self.aCoteMur(caseX-1,caseY+1) :
                caseTransition.append(Noeud(n,caseX-1,caseY+1,caseCibleX,caseCibleY))
            if self.parent.carte.matrice[caseX][caseY+1].type == 0:
                caseTransition.append(Noeud(n,caseX,caseY+1,caseCibleX,caseCibleY))
            if caseX+1 < self.parent.grandeurMat and self.parent.carte.matrice[caseX+1][caseY+1].type == 0 and not self.aCoteMur(caseX+1,caseY+1):
                caseTransition.append(Noeud(n,caseX+1,caseY+1,caseCibleX,caseCibleY))

        return caseTransition
  

    def goal(self,noeud):
        casesCible = self.parent.trouverCaseMatrice(self.cibleX,self.cibleY)
        caseCibleX = casesCible[0]
        caseCibleY = casesCible[1]
        
        if noeud.x == caseCibleX and noeud.y == caseCibleY:
            return True
        return False


class Noeud:
    def __init__(self,parent,x,y,cibleX,cibleY):
        self.parent = parent
        self.x = x
        self.y = y
        self.cout = 0
        if not(parent == None):
            self.calculerCout(cibleX,cibleY)

    def calculerCout(self,cibleX,cibleY):
        g = self.parent.cout + self.coutTransition(self.parent)
        h = abs(self.x - cibleX) + abs(self.y - cibleY)
        self.cout = g+h

    def coutTransition(self,n2):
        if abs(self.x - n2.x) == 1 and abs(self.y - n2.y) == 1:
            return 14 #Diagonale
        else:
            return 10

class Paysan(Unit):
    def __init__(self, x, y, parent):
        Unit.__init__(self,x,y,parent)
        self.vitesseRessource = 1 #La vitesse à ramasser des ressources
        self.nbRessourcesMax = 10
        self.nbRessources = 0
        self.typeRessource = 0 #0 = Rien 1 à 4 = Ressources

    def chercherRessources(self):
        #TODO Regarder le type de la ressource !
        if self.nbRessources + vitesseRessource <= self.nbRessourcesMax:
            self.nbRessources = self.nbRessources + vitesseRessource
        else:
            self.nbRessources = self.nbRessourcesMax
            #TODO Faire retourner à la base !        


class Model:
    def __init__(self):
        self.units = []
        self.grandeurMat = 20
        self.carte = Carte(self.grandeurMat)
        self.carte.createRessources()

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
        #self.units.append(Unit(x, y, self))
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

    def trouverCaseMatrice(self,x,y):
        #TODO Linker avec la vue
        #grandeurCanevasRelle = self.parent.v.grandeurCanevasRelle
        grandeurCanevasRelle = self.grandeurMat * 32
        grandeurCase = grandeurCanevasRelle / self.grandeurMat
        caseX = int(x/grandeurCase)
        caseY = int(y/grandeurCase)
        
        return (caseX, caseY)

    def trouverCentreCase(self,caseX,caseY):
        #TODO Linker avec la vue
        #grandeurCanevasRelle = self.parent.v.grandeurCanevasRelle
        grandeurCanevasRelle = self.grandeurMat * 32
        grandeurCase = grandeurCanevasRelle / self.grandeurMat
        centreX = (grandeurCase * caseX) + grandeurCase/2
        centreY = (grandeurCase * caseY) + grandeurCase/2
        
        return (centreX,centreY)
