import sys
import time
from GraphicsManagement import SpriteSheet
from Joueurs import Joueur
from Timer import Timer

import time
import math

class Unit():
    COUNT = 0  # Un compteur permettant d'avoir un Id unique pour chaque unité

    def __init__(self, uid, x, y, parent, civilisation):
        """
        :param uid: l'id unique de l'unité
        :param x: sa position initiale en x
        :param y: sa position initiale en y
        :param parent: le modèle
        :param civilisation: la civilisation de l'unité
        """
        self.id = uid
        self.civilisation = civilisation
        self.x = x
        self.y = y
        self.parent = parent
        self.vitesse = 5
        self.grandeur = 41 #32 donc grandeur/2 - 16
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
        self.positionDejaVue = []
        self.casesDejaVue = []
        self.cheminAttente = []
        self.groupeID = [] #Pour le leader
        self.leader = 0
        self.finMultiSelection = None

        self.timerDeplacement = Timer(60)
        self.timerDeplacement.start()

        # ANIMATION
        self.timerAnimation = Timer(333)   # 1000/333 = 3 fois par secondes
        self.timerAnimation.start()
        self.spriteSheet = None
        self.determineSpritesheet()

        self.animDirection = 'DOWN'
        self.animFrameIndex = 1

        activeFrameKey = '%s_%s' % (self.animDirection, self.animFrameIndex)
        self.activeFrame = self.spriteSheet.frames[activeFrameKey]
        self.activeOutline = self.spriteSheet.framesOutlines[activeFrameKey]

        # Kombat
        self.hp = 100       # Health Points, Points de Vie
        self.damage = 50    # Force à laquelle l'unité frappe


    def getClientId(self):
        """ Returns the Id of the client using the id of the unit
        :return: the id of the clients
        """
        return self.id.split('_')[0]

    def estUniteDe(self, clientId):
        """ Vérifie si l'unité appartient au client ou non
        :param clientId: le client à tester
        :return: True si elle lui appartient Sinon False
        """
        masterId = int(self.getClientId())
        clientId = int(clientId)
        return masterId == clientId

    def determineSpritesheet(self):
        """ permet de déterminer le spritesheet à utiliser
        selon la civilisation de l'unité
        """
        raise Exception("La méthode determineSprite doit être surchargée par tous les sous-classes de Unit")
        sys.exit(1)

    @staticmethod
    def generateId(clientId):
        gId = "%s_%s" % (clientId, Unit.COUNT)
        Unit.COUNT += 1
        return gId


    def animer(self):
        """ Lance l'animation de l'unité
        """
        if not self.timerAnimation.isDone():
            return

        self.animFrameIndex += 1
        if self.animFrameIndex == self.spriteSheet.NB_FRAME_ROW:
            self.animFrameIndex = 0
        if self.animFrameIndex == 1:  # POSITION NEUTRE ON NE VEUT PAS ÇA
            self.animFrameIndex = 2

        activeFrameKey = '%s_%s' % (self.animDirection, self.animFrameIndex)
        self.activeFrame = self.spriteSheet.frames[activeFrameKey]
        self.activeOutline = self.spriteSheet.framesOutlines[activeFrameKey]
        self.timerAnimation.reset()

    def update(self):
        #print(len(self.groupeID))
        if self.enDeplacement:
            #print("---", self.leader, self.enDeplacement, self.trouver)
            #self.afficherList("cheminTrace", self.cheminTrace)
            if not self.trouver:
                if not self.cheminAttente:
                    self.deplacement()
                else:
                    self.deplacementTrace(self.cheminAttente, 1)
                if self.leader == 1:
                    self.choisirTraceFail()
            else:
                self.deplacementTrace(self.cheminTrace,0)


    def changerCible(self, cibleX, cibleY, groupeID, finMultiSelection, leader):
        #print("unit:", cibleX, cibleY , leader)
        self.leader = leader #Pour sélection multiple
        #print("leader", self.leader)
        self.mode = 0
        self.cibleX = cibleX
        self.cibleY = cibleY
        self.cibleXDeplacement = cibleX
        self.cibleYDeplacement = cibleY
        self.trouver = False
        self.enDeplacement = True
        
        self.positionDejaVue = []
        self.cheminAttente = []
        self.time1 = 0
        self.nbTour = 0
        if self.leader == 1:
            self.groupeID = groupeID
            self.finMultiSelection = None
            self.cheminTrace = self.choisirTrace()
            #self.afficherList("cheminTrace", self.cheminTrace)
            if self.trouver:
                self.trouverCheminMultiSelection()
        else:
            #print("NOEUD", finMultiSelection)
            self.finMultiSelection = Noeud(None, finMultiSelection[0], finMultiSelection[1], None, None)
            #print("NOEUD", self.finMultiSelection.x, self.finMultiSelection.y )

    def deplacer(self, cibleX, cibleY, vitesse):
        if not self.timerDeplacement.isDone():
            return

        if cibleX > self.x:
            self.x += vitesse
            self.animDirection = 'RIGHT'

        elif cibleX < self.x:
            self.x -= vitesse
            self.animDirection = 'LEFT'

        if cibleY > self.y:
            self.y += vitesse
            self.animDirection = 'DOWN'

        elif cibleY < self.y:
            self.y -= vitesse
            self.animDirection = 'UP'

        # Puisqu'il y a eu un déplacement
        #self.animer()
        #self.timerDeplacement.reset()

    def deplacement(self):
        if not self.timerDeplacement.isDone():
            return
        if self.x == self.cibleX and self.y == self.cibleY:
            print("fix", self.x, self.cibleX, self.y, self.cibleY)
            return self.finDeplacementTraceVrai() #Quick Fix
	#ATTENTION: POSX EST LE 1er ancien et ancien le 2ieme !!! 
        self.posX = self.x
        self.posY = self.y
        if abs(self.cibleX - self.x) <= self.vitesse:
            self.x = self.cibleX
        if abs(self.cibleY - self.y) <= self.vitesse:
            self.y = self.cibleY

        self.deplacer(self.cibleX, self.cibleY, self.vitesse)

        self.eviterObstacles()
        
        #Garder en souvenir
        self.ancienX = self.posX
        self.ancienY = self.posY
        # Puisqu'il y a eu un déplacement
        self.animer()
        self.timerDeplacement.reset()

    def eviterObstacles(self):
        contact = False
        casesPossibles = [  self.parent.trouverCaseMatrice(self.x, self.y),
                            self.parent.trouverCaseMatrice(self.x+self.grandeur/2, self.y),
                            self.parent.trouverCaseMatrice(self.x, self.y + self.grandeur/2),
                            self.parent.trouverCaseMatrice(self.x+self.grandeur/2, self.y+self.grandeur/2),
                            self.parent.trouverCaseMatrice(self.x-self.grandeur/2, self.y),
                            self.parent.trouverCaseMatrice(self.x, self.y - self.grandeur/2),
                            self.parent.trouverCaseMatrice(self.x-self.grandeur/2, self.y-self.grandeur/2)]

        for case in casesPossibles:
            if not self.parent.carte.matrice[case[0]][case[1]].type == 0 or case in self.casesDejaVue:
                contact = True
                break

        if contact:
            trouve = False
            self.x = self.posX
            self.y = self.posY
            self.choixPossible = []
            liste = [-1,0,1]
            for i in liste:
                for j in liste:
                    if not(i==0 and j==0):
                        deplacementPossible = True
                        casesPossibles = [  self.parent.trouverCaseMatrice(self.x+(i*self.vitesse), self.y+(j*self.vitesse)),
                                            self.parent.trouverCaseMatrice(self.x+(i*self.vitesse)+self.grandeur/2, self.y+(j*self.vitesse)),
                                            self.parent.trouverCaseMatrice(self.x+(i*self.vitesse), self.y+(j*self.vitesse) + self.grandeur/2),
                                            self.parent.trouverCaseMatrice(self.x+(i*self.vitesse)+self.grandeur/2, self.y+(j*self.vitesse)+self.grandeur/2),
                                            self.parent.trouverCaseMatrice(self.x+(i*self.vitesse)-self.grandeur/2, self.y+(j*self.vitesse)),
                                            self.parent.trouverCaseMatrice(self.x+(i*self.vitesse), self.y+(j*self.vitesse) - self.grandeur/2),
                                            self.parent.trouverCaseMatrice(self.x+(i*self.vitesse)-self.grandeur/2, self.y+(j*self.vitesse)-self.grandeur/2)]

                        #Gestion des obstacles
                        for case in casesPossibles:
                            if not self.parent.carte.matrice[case[0]][case[1]].type == 0 or case in self.casesDejaVue:
                                deplacementPossible = False
                                break
                            
                        if deplacementPossible:
                            #print("deplacement possible !")
                            if (self.x+(i*self.vitesse), self.y+(j*self.vitesse)) not in self.positionDejaVue:
                                self.x = self.posX
                                self.y = self.posY
                                self.x += (i*self.vitesse)
                                self.y += (j*self.vitesse)
                                self.choixPossible.append([self.x,self.y])

                                trouve = True

            if self.choixPossible: #Choisir le meilleur point sur les points possibles
                self.x = self.choixPossible[0][0]
                self.y = self.choixPossible[0][1]
                diff = abs(self.x - self.cibleX) + abs(self.y - self.cibleY)
                for coord in self.choixPossible:
                    diffCoord = abs(coord[0] - self.cibleX) + abs(coord[1] - self.cibleY)
                    if diff > diffCoord:
                        self.x = coord[0]
                        self.y = coord[1]
                        diffX = self.x - self.posX
                        diffY = self.y - self.posY
                        
                        if diffX > 0 and diffY == 0:
                            self.animDirection = 'RIGHT'
                        elif diffX < 0 and diffY == 0:
                            self.animDirection = 'LEFT'
                        #elif diffX > 0 and diffY < 0:
                        #    self.animDirection = 'DOWN'
                        #elif diffX > 0 and diffY > 0:
                        #    self.animDirection = 'UP'
                        else:
                            self.animDirection = 'DOWN'
                            
                        #print(diffX,diffY)
                        diff = diffCoord

            if trouve == False:
                self.animDirection = 'DOWN'
                #print("rate !", self.x,self.posX,self.ancienX,"y;", self.y,self.posY,self.ancienY)

            if (self.x, self.y) in self.positionDejaVue:
                self.casesDejaVue.append(self.parent.trouverCaseMatrice(self.x, self.y))
                nouvelleCase = self.trouverNouvelleCase(self.parent.trouverCaseMatrice(self.x,self.y))
                destination = self.parent.trouverCentreCase(nouvelleCase[0],nouvelleCase[1])
                self.cheminAttente.append((destination[0],destination[1]))
                self.cibleXDeplacement = destination[0]
                self.cibleYDeplacement = destination[1]
                #print("YOU FAILED !!!")
                
            self.positionDejaVue.append((self.x, self.y))


    def trouverNouvelleCase(self, case):
        casesPossibles = []
        liste = [-1,0,1]
        for i in liste:
            for j in liste:
                if not(i==0 and j==0):
                    try:
                        if self.parent.carte.matrice[case[0]+i][case[1]+j].type == 0:
                            if i==0 or j==0: # Pas de diagonale
                                if (case[0]+i,case[1]+j) not in self.casesDejaVue:
                                    casesPossibles.append((case[0]+i,case[1]+j))
                    except:
                        print("fail nouvelle case")
                        pass #Dépasse la matrice

        if casesPossibles: #Trouver la case la plus proche du but !
            caseBut = self.parent.trouverCaseMatrice(self.cibleX, self.cibleY)
            caseResultat = casesPossibles[0]
            diff = abs(casesPossibles[0][0] - caseBut[0]) + abs(casesPossibles[0][1] - caseBut[1])
            for case in casesPossibles:
                diffCase = abs(case[0] - caseBut[0]) + abs(case[1] - caseBut[1])
                if diff > diffCase:
                    caseResultat = case
            return caseResultat
            
        print("nouvelle case no return !")
        return case #FAIL !

    def deplacementTrace(self, chemin, mode):
        #TODO: Mettre les obstacles !
        if len(chemin) > 0:
            if self.x == self.cibleXDeplacement and self.y == self.cibleYDeplacement:
                del chemin[-1]
                self.nbTour += 1
                #chemin = chemin[:len(chemin)-self.nbTour]
                if len(chemin) <= 0: #FIN
                    if mode == 0: #vrai pathfinding
                        return self.finDeplacementTraceVrai()
                    else: # mode attente
                        chemin = []
                        return -1

                self.cibleXDeplacement = chemin[-1].x
                self.cibleYDeplacement = chemin[-1].y

            if not self.timerDeplacement.isDone():
                return

            if not abs(self.cibleXDeplacement - self.x) == 0 and not abs(self.cibleYDeplacement - self.y) == 0:
                diaganoleVit = math.sqrt(math.pow(self.vitesse,2) + math.pow(self.vitesse,2))
                diaganoleVit /= 2
            else:
                diaganoleVit = self.vitesse #vitesse normal

            if abs(self.cibleXDeplacement - self.x) <= diaganoleVit:
                self.x = self.cibleXDeplacement
            if abs(self.cibleYDeplacement - self.y) <= diaganoleVit:
                self.y = self.cibleYDeplacement

            self.deplacer(self.cibleXDeplacement,self.cibleYDeplacement,diaganoleVit)

            #self.eviterObstacles()
            # Puisqu'il y a eu un déplacement
            self.animer()
            self.timerDeplacement.reset()

    def finDeplacementTraceVrai(self): #la fin du vrai pathfinding
        self.animFrameIndex = 1
        self.animDirection = 'DOWN'
        activeFrameKey = 'DOWN_1'
        self.activeFrame = self.spriteSheet.frames[activeFrameKey]
        self.activeOutline = self.spriteSheet.framesOutlines[activeFrameKey]
        self.enDeplacement = False
        
        return -1

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
            cheminTrace = []
            while n.parent:
                cheminTrace.append(n)
                centreCase = self.parent.trouverCentreCase(n.x, n.y)
                n.x = centreCase[0]
                n.y = centreCase[1]
                n = n.parent
            # print(cheminTrace,"len", len(cheminTrace))
            if cheminTrace:
                #Pour ne pas finir sur le centre de la case (Pour finir sur le x,y du clic)
                if not self.mode == 1:  #pas en mode ressource
                    cheminTrace[0] = Noeud(None, self.cibleX, self.cibleY, None, None)
            else:
                if not self.mode == 1:  #pas en mode ressource
                    cheminTrace.append(Noeud(None, self.cibleX, self.cibleY, None, None))
                else:
                    cheminTrace.append(Noeud(None, self.x, self.y, None, None))

            self.cibleXDeplacement = cheminTrace[-1].x
            self.cibleYDeplacement = cheminTrace[-1].y
            
        return cheminTrace
    
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
                self.finTrace()

    def finTrace(self):
        if self.cheminTrace:
            print("DUDE !",self.cibleX,self.cibleY)
            #Pour ne pas finir sur le centre de la case (Pour finir sur le x,y du clic)
            self.cheminTrace[0] = Noeud(None,self.cibleX,self.cibleY,None ,None)                    
        else:
            print("DUDE !",self.cibleX,self.cibleY)
            self.cheminTrace.append(Noeud(None,self.cibleX,self.cibleY,None ,None))
           
        self.cheminTrace = self.cheminTrace[:len(self.cheminTrace)-self.nbTour]
        while abs(self.x - self.cibleX) + abs(self.y - self.cibleY) < abs(self.cheminTrace[-1].x - self.cibleX) + abs(self.cheminTrace[-1].y - self.cibleY):
            del self.cheminTrace[-1]
                
        self.trouverDebutPath(self)
        self.trouverCheminMultiSelection()

    def trouverDebutPath(self, unit):
        #Trouver le chemin entre le début du pathfinding et la position actuelle
        unit.cibleX = self.cheminTrace[-1].x
        unit.cibleY = self.cheminTrace[-1].y
        unit.cibleXDeplacement = self.cheminTrace[-1].x
        unit.cibleYDeplacement = self.cheminTrace[-1].y
        cheminDebutTrace = unit.choisirTrace()
        
        for case in cheminDebutTrace:
            unit.cheminTrace.append(case)
            
        unit.cibleXDeplacement = unit.cheminTrace[-1].x
        unit.cibleYDeplacement = unit.cheminTrace[-1].y

    def trouverFinPath(self, unit):
        #self.afficherList("unit chemin AVANT", unit.cheminTrace)
        unit.cibleX = unit.cheminTrace[0].x
        unit.cibleY = unit.cheminTrace[0].y
        xSave = unit.x
        ySave = unit.y
        try:
            unit.x = unit.cheminTrace[1].x
            unit.y = unit.cheminTrace[1].y
        except:
            print("petit chemin")
            pass
        unit.cibleXDeplacement = unit.cheminTrace[0].x
        unit.cibleYDeplacement = unit.cheminTrace[0].y
        #print("toruev FIn path x", unit.x, unit.y, unit.cibleX, unit.cibleY)
        cheminFinTrace = unit.choisirTrace()
        
        unit.cheminTrace.reverse()
        unit.cheminTrace.pop()

        cheminFinTrace.reverse()
        for case in cheminFinTrace:
            #print(case.x,case.y)
            unit.cheminTrace.append(case)

        unit.cheminTrace.reverse()

        unit.x = xSave
        unit.y = ySave
        #self.afficherList("unit chemin", unit.cheminTrace)
        #print("-----------")
        unit.cibleXDeplacement = unit.cheminTrace[-1].x
        unit.cibleYDeplacement = unit.cheminTrace[-1].y

    def trouverCheminMultiSelection(self):
        if self.leader == 1 and self.groupeID:
            for id in self.groupeID:
                unit = self.parent.getUnit(id)
                unit.cheminTrace = self.cheminTrace[:]
                self.trouverDebutPath(unit)
                #print("tourver", unit.leader, unit.finMultiSelection, len(self.groupeID), self.leader)
                unit.cheminTrace[0] = unit.finMultiSelection
                self.trouverFinPath(unit)
                unit.cibleX = unit.finMultiSelection.x
                unit.cibleY = unit.finMultiSelection.y
                #print(unit.cibleX, unit.cibleY, unit.finMultiSelection.x, unit.finMultiSelection.y)
                unit.trouver = True

        #self.leader = 0 #defaut
        self.groupeID = []

    def aEtoile(self, tempsMax):
        nbNoeud = 100
        while self.open:
            n = self.open[0]
            if self.goal(n):
                self.trouver = True
                #print("changeent true trouver !")
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
        # TODO BUG traverse un mur en diagonale
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


class Paysan(Unit):
    def __init__(self, clientId, x, y, parent, civilisation):
        Unit.__init__(self, clientId, x, y, parent, civilisation)
        self.vitesseRessource = 0.01  # La vitesse à ramasser des ressources
        self.nbRessourcesMax = 10
        self.nbRessources = 0
        self.typeRessource = 0  # 0 = Rien 1 à 4 = Ressources

    def determineSpritesheet(self):

        spritesheets = {
            Joueur.BLANC: 'Units/Age_I/paysan_blanc.png',
            Joueur.BLEU: 'Units/Age_I/paysan_bleu.png',
            Joueur.JAUNE: 'Units/Age_I/paysan_jaune.png',

            Joueur.MAUVE: 'Units/Age_I/paysan_mauve.png',
            Joueur.NOIR: 'Units/Age_I/paysan_noir.png',
            Joueur.ORANGE: 'Units/Age_I/paysan_orange.png',

            Joueur.ROUGE: 'Units/Age_I/paysan_rouge.png',
            Joueur.VERT: 'Units/Age_I/paysan_vert.png',
            Joueur.ROSE: 'Units/Age_I/paysan_rose.png'
        }
        self.spriteSheet = SpriteSheet(spritesheets[self.civilisation])



    def update(self):
        Unit.update(self)


    def chercherRessources(self):
        # print(int(self.nbRessources))
        # TODO Regarder le type de la ressource !
        # TODO Enlever nbRessources à la case ressource !
        print(self.nbRessources)
        if self.nbRessources + self.vitesseRessource <= self.nbRessourcesMax:
            self.nbRessources += self.vitesseRessource
        else:
            self.nbRessources = self.nbRessourcesMax
            #print("MAX!", self.nbRessources)
            #TODO Faire retourner à la base !


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
