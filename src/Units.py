import random
import time
import math

from Commands import Command
from GraphicsManagement import SpriteSheet, SpriteAnimation, GraphicsManager, \
    OneTimeAnimation
from SimpleTimer import Timer, FrameTimer
from Civilisations import Civilisation

class Unit():
    COUNT = 0  # Un compteur permettant d'avoir un Id unique pour chaque unité

    # MODE DE COMBAT
    ACTIF = 0
    PASSIF = 1

    def __init__(self, uid, x, y, joueur, civilisation):
        """
        :param uid: l'id unique de l'unité
        :param x: sa position initiale en x
        :param y: sa position initiale en y
        :param model: le modèle
        :param civilisation: la civilisation de l'unité
        """
        self.id = uid
        self.civilisation = int(civilisation)
        self.x = x
        self.y = y
        self.joueur = joueur
        self.model = self.joueur.model
        self.vitesse = 5
        self.grandeur = 41  # 32 donc grandeur/2 - 16
        self.cibleX = x
        self.cibleY = y
        self.cheminTrace = []
        self.cibleXTrace = x
        self.cibleXTrace = y
        self.cibleXDeplacement = x
        self.cibleYDeplacement = y
        self.mode = 0  # 1=ressource, 2 = batiment 3 = attack, 5=attack batiment

        self.trouver = True  # pour le pathfinding

        self.enDeplacement = False
        self.ancienX = self.x
        self.ancienY = self.y
        self.positionDejaVue = []
        self.casesDejaVue = []
        self.cheminAttente = []

        self.groupeID = [] #Pour le leader
        self.leader = 0
        self.finMultiSelection = None
        self.building = None # Tuple (Id, type)
        self.ancienPosEnnemi = None
        self.ressource = False
        self.ressourceEnvoye = False #Pour ne pas envoyer plein de commandes déplacement (ressource)
        self.typeRessource = 0 #0 = Rien (voir Tuile)
        self.inBuilding = False # Si l'unité est dans un bâtiment


        self.timerDeplacement = FrameTimer(1)
        self.timerDeplacement.start()

        # ANIMATION
        self.animation = None
        self.determineSpritesheet()


        # Kombat
        # Health Points, Points de Vie
        self.hpMax = 20
        self.hp = 20
        # Force à laquelle l'unité frappe
        self.attackMin = 0
        self.attackMax = 5

        self.rayonVision = 100  # la rayon de la vision en pixel
        self.ennemiCible = None

        self.modeAttack = Unit.PASSIF
        self.timerAttack = FrameTimer(8)
        self.timerAttack.start()

        self.oneTimeAnimations = []

    def getClientId(self):
        """ Retourne l'ID du propriétaire de l'unité
        :return: l'id du propriétaire (str)
        """
        return int(self.id.split('_')[0])

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
        raise Exception("La méthode determineSprite doit être surchargée par tous les sous-classes de Unit et doit ")

    @staticmethod
    def generateId(clientId):
        gId = "%s_%s" % (clientId, Unit.COUNT)
        Unit.COUNT += 1
        return gId


    def update(self, model):

        #print("update", self.id, self.mode)
        #print("update", self.id, self.leader)
        if self.hp == 0:
            return

        for anim in self.oneTimeAnimations:
            anim.animate()
            if anim.isFinished:
                self.oneTimeAnimations.remove(anim)
                
        self.determineCombatBehaviour(model)
        try:
            civDuBuilding = int(self.attackedBuildingId.split('_')[0])
            buildingViser = self.model.joueurs[civDuBuilding].buildings[self.attackedBuildingId]
            self.attaquerBuilding(self.model, buildingViser)

        except:
            pass

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


    def changerCible(self, cibleX, cibleY, groupeID, finMultiSelection, leader, ennemiCibleID = None, building = None, attackedBuildingID = None):
        #print("unit:", cibleX, cibleY , leader)
        self.leader = leader #Pour sélection multiple
        #print("leader", self.leader)
        #if leader == 1:
        #    self.mode = 0
        if self.nbRessources == 0:#S'il n'est pas en ressource
            self.mode = 0
        
        if self.ennemiCible:
            print("changement", self.id)
            self.mode = 3
        else:
            print("what!")
        print("building",building)
        if building:
            print("buildingTrue", self.leader)
            if self.leader == 1:
                self.building = building
            self.mode = 2
            
        self.attackedBuildingId = attackedBuildingID
        if attackedBuildingID:
            print("JAI UN BUILDING A ATTAQUER")
            self.mode = 5           
            
        self.cibleX = cibleX
        self.cibleY = cibleY
        self.cibleXDeplacement = cibleX
        self.cibleYDeplacement = cibleY

        #print("info unit",self.id, self.leader, self.cibleX, self.cibleY, self.cibleXDeplacement, self.cibleYDeplacement)
        self.trouver = False
        self.enDeplacement = True
        #if ennemiCibleID:
        #    self.ennemiCible = self.parent.getUnit(ennemiCibleID)
        #else:
        #    self.ennemiCible = None
        
        self.positionDejaVue = []
        self.cheminAttente = []
        self.time1 = 0
        self.nbTour = 0
        if self.leader == 1:
            self.groupeID = groupeID
            if finMultiSelection == None:
                self.finMultiSelection = None
            else:
                self.finMultiSelection = Noeud(None, finMultiSelection[0], finMultiSelection[1], None, None)

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
            self.x += self.vitesse
            self.animation.direction = SpriteSheet.Direction.RIGHT

        elif cibleX < self.x:
            self.x -= self.vitesse
            self.animation.direction = SpriteSheet.Direction.LEFT

        if cibleY > self.y:
            self.y += self.vitesse
            self.animation.direction = SpriteSheet.Direction.DOWN

        elif cibleY < self.y:
            self.y -= self.vitesse
            self.animation.direction = SpriteSheet.Direction.UP

        self.timerDeplacement.reset()


    def deplacement(self):
        """Déplacement lorsqu'on a pas trouvé notre path"""
        if not self.timerDeplacement.isDone():
            return
        if self.x == self.cibleX and self.y == self.cibleY:
            print("fix", self.x, self.cibleX, self.y, self.cibleY, self.cibleXDeplacement, self.cibleYDeplacement)
            #self.trouver = True
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
        # Garder en souvenir

        self.ancienX = self.posX
        self.ancienY = self.posY
        # Puisqu'il y a eu un déplacement
        self.animation.animate()
        self.timerDeplacement.reset()

    def eviterObstacles(self):
        """Évite les obstacles lorsqu'on n'a pas de path"""
        contact = False
        casesPossibles = [  self.model.trouverCaseMatrice(self.x, self.y),
                            self.model.trouverCaseMatrice(self.x+self.grandeur/2, self.y),
                            self.model.trouverCaseMatrice(self.x, self.y + self.grandeur/2),
                            self.model.trouverCaseMatrice(self.x+self.grandeur/2, self.y+self.grandeur/2),
                            self.model.trouverCaseMatrice(self.x-self.grandeur/2, self.y),
                            self.model.trouverCaseMatrice(self.x, self.y - self.grandeur/2),
                            self.model.trouverCaseMatrice(self.x-self.grandeur/2, self.y-self.grandeur/2)]

        for case in casesPossibles:
            if not self.model.carte.matrice[case[0]][case[1]].isWalkable or case in self.casesDejaVue:
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
                        casesPossibles = [  self.model.trouverCaseMatrice(self.x+(i*self.vitesse), self.y+(j*self.vitesse)),
                                            self.model.trouverCaseMatrice(self.x+(i*self.vitesse)+self.grandeur/2, self.y+(j*self.vitesse)),
                                            self.model.trouverCaseMatrice(self.x+(i*self.vitesse), self.y+(j*self.vitesse) + self.grandeur/2),
                                            self.model.trouverCaseMatrice(self.x+(i*self.vitesse)+self.grandeur/2, self.y+(j*self.vitesse)+self.grandeur/2),
                                            self.model.trouverCaseMatrice(self.x+(i*self.vitesse)-self.grandeur/2, self.y+(j*self.vitesse)),
                                            self.model.trouverCaseMatrice(self.x+(i*self.vitesse), self.y+(j*self.vitesse) - self.grandeur/2),
                                            self.model.trouverCaseMatrice(self.x+(i*self.vitesse)-self.grandeur/2, self.y+(j*self.vitesse)-self.grandeur/2)]

                        #Gestion des obstacles
                        for case in casesPossibles:
                            if not self.model.carte.matrice[case[0]][case[1]].isWalkable or case in self.casesDejaVue:
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
                            self.animation.direction = SpriteSheet.Direction.RIGHT
                        elif diffX < 0 and diffY == 0:
                            self.animation.direction = SpriteSheet.Direction.LEFT

                        # elif diffX > 0 and diffY < 0:

                        #    self.animDirection = 'DOWN'
                        #elif diffX > 0 and diffY > 0:
                        #    self.animDirection = 'UP'
                        else:
                            self.animation.direction = SpriteSheet.Direction.DOWN

                        # print(diffX,diffY)

                        diff = diffCoord

            if trouve == False:
                self.animation.direction = SpriteSheet.Direction.DOWN

                #print("rate !", self.x,self.posX,self.ancienX,"y;", self.y,self.posY,self.ancienY)

            if (self.x, self.y) in self.positionDejaVue:
                self.casesDejaVue.append(self.model.trouverCaseMatrice(self.x, self.y))
                nouvelleCase = self.trouverNouvelleCase(self.model.trouverCaseMatrice(self.x,self.y))
                destination = self.model.trouverCentreCase(nouvelleCase[0],nouvelleCase[1])
                self.cheminAttente.append((destination[0],destination[1]))
                self.cibleXDeplacement = destination[0]
                self.cibleYDeplacement = destination[1]
                #print("YOU FAILED !!!")
                

            self.positionDejaVue.append((self.x, self.y))


    def trouverNouvelleCase(self, case):
        """Trouve une case qui esr walkable... Lorsqu'on a pas de path"""
        casesPossibles = []
        liste = [-1,0,1]
        for i in liste:
            for j in liste:
                if not(i==0 and j==0) and not case[0]+i < 0 and not case[1]+j < 0:
                    try:
                        if self.model.carte.matrice[case[0]+i][case[1]+j].isWalkable:
                            if i==0 or j==0: # Pas de diagonale
                                if (case[0]+i,case[1]+j) not in self.casesDejaVue:
                                    casesPossibles.append((case[0]+i,case[1]+j))
                    except:
                        print("fail nouvelle case")
                        pass #Dépasse la matrice

        if casesPossibles: #Trouver la case la plus proche du but !

            caseBut = self.model.trouverCaseMatrice(self.cibleX, self.cibleY)
            caseResultat = casesPossibles[0]
            diff = abs(casesPossibles[0][0] - caseBut[0]) + abs(casesPossibles[0][1] - caseBut[1])
            for case in casesPossibles:
                diffCase = abs(case[0] - caseBut[0]) + abs(case[1] - caseBut[1])
                if diff > diffCase:
                    caseResultat = case
            return caseResultat

        print("nouvelle case no return !")
        return case  # FAIL !

    def deplacementTrace(self, chemin, mode):
        """Déplacement lorsqu'on a trouvé un path (principal ou secondaire)"""
        # TODO: Mettre les obstacles !

        if len(chemin) > 0:
            if self.x == self.cibleXDeplacement and self.y == self.cibleYDeplacement:
                del chemin[-1]
                self.nbTour += 1
                # chemin = chemin[:len(chemin)-self.nbTour]
                if len(chemin) <= 0:  #FIN
                    if mode == 0 or mode == 2:  #vrai pathfinding
                        return self.finDeplacementTraceVrai()
                    else:  # mode attente
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
                diaganoleVit = self.vitesse # vitesse normal


            if abs(self.cibleXDeplacement - self.x) <= diaganoleVit:
                self.x = self.cibleXDeplacement
            if abs(self.cibleYDeplacement - self.y) <= diaganoleVit:
                self.y = self.cibleYDeplacement

            self.deplacer(self.cibleXDeplacement,self.cibleYDeplacement,diaganoleVit)

            # self.eviterObstacles()

            # Puisqu'il y a eu un déplacement
            self.animation.animate()
            self.timerDeplacement.reset()

    def finDeplacementTraceVrai(self): #la fin du vrai pathfinding
        """La fin du déplacement"""
        print("MODE DE FIN ",self.mode)
        self.animation.setActiveFrameKey(SpriteSheet.Direction.DOWN, 1)
        self.enDeplacement = False
        if self.building:
            print("JE VEUX CONSTRUIRE!")
            self.joueur.createBuilding(self.building[0], self.x, self.y, self.building[1])
            self.building = None
        else:
            print("JE VEUX PAS CONSTRUIRE!")

        #if self.mode == 5:
           # civDuBuilding = int(self.attackedBuildingId.split('_')[0])
           # buildingViser = self.model.joueurs[civDuBuilding].buildings[self.attackedBuildingId]
           #self.attaquerBuilding(self.model,buildingViser)

        if self.mode == 4: #Rentre dans un building
            buildingDetected = self.model.controller.view.detectBuildings(self.x, self.y,self.x,self.y, self.model.getBuildings())
            if buildingDetected:
                buildingDetected = buildingDetected[0]
                if buildingDetected.peutEtreOccupe:
                    self.inBuilding = True
                    buildingDetected.unitInBuilding.append(self)
                    if len(buildingDetected.unitInBuilding) <= 1: #Il n'y avait pas d'unité avant
                    	buildingDetected.tempsProduction = time.time()
            
        return -1

    def choisirTrace(self):
        """Premier essai pour trouver un path"""
        self.distance = abs(self.x - self.cibleX) + abs(self.y - self.cibleY)
        print("distance", self.distance)
        self.tempsTotal = 0
        self.ressourceEnvoye = False
        cases = self.model.trouverCaseMatrice(self.x, self.y)
        caseX = cases[0]
        caseY = cases[1]
        if self.leader == 1 and self.typeRessource == 0 and not self.mode == 5:
            self.mode = 0
        if self.ennemiCible:
            self.mode = 3
        casesCible = self.model.trouverCaseMatrice(self.cibleX, self.cibleY)
        self.ressource = False
        
        #Ressources
        if not self.model.carte.matrice[casesCible[0]][casesCible[1]].isWalkable:
            if not self.model.carte.matrice[casesCible[0]][casesCible[1]].type == 5:# Pas sur un bâtiment (ressource)
                if isinstance(self, Paysan): #Paysan sur ressource 
                    print("ressource", len(self.groupeID))
                    if self.model.carte.matrice[casesCible[0]][casesCible[1]].revealed:
                        if self not in self.joueur.enRessource:
                            self.joueur.enRessource.append(self)
                    for unitID in self.groupeID:
                        unit = self.model.getUnit(unitID)
                        print("UNIT", unit.id)
                        if isinstance(unit, Paysan):
                            print(unit.id)
                            if unit not in unit.joueur.enRessource:
                                print("ressource choix", unit.id, self.model.carte.matrice[casesCible[0]][casesCible[1]].revealed)
                                if self.model.carte.matrice[casesCible[0]][casesCible[1]].revealed:
                                    unit.joueur.enRessource.append(unit)
                            unit.mode = 1
                    self.mode = 1  # ressource
                    print("mode",self.mode)
                    
                    #cases = self.parent.trouverCentreCase(,noeud.y)
                    #print("avant", self.posRessource.x, self.posRessource.y)
                    if not self.model.carte.matrice[casesCible[0]][casesCible[1]].type == 5:
                        for unitID in self.groupeID:
                            unit = self.model.getUnit(unitID)
                            unit.posRessource = Noeud(None, self.cibleX, self.cibleY, None, None)
                            unit.ressource = True
                            unit.typeRessource = self.model.carte.matrice[casesCible[0]][casesCible[1]].type
                        
                        self.posRessource = Noeud(None, self.cibleX, self.cibleY, None, None)
                        self.ressource = True
                        self.typeRessource = self.model.carte.matrice[casesCible[0]][casesCible[1]].type
                    #self.posRessource = Noeud(None, self.cibleX, self.cibleY, None, None)
                    #print("ressource node" , self.mode, cases[0], cases[1])

                    # TODO Changer le chemin pour aller à côté de la ressource !
                else:
                    return -1  # Ne peut pas aller sur un obstacle
            else:
                print("MODE semi", self.mode)
                if not self.mode == 1 and not self.mode == 5: #S'il ne retourne pas à la base (ressource)
                    self.mode = 4 #Rentre dans un building
        caseCibleX = casesCible[0]
        caseCibleY = casesCible[1]

        noeudInit = Noeud(None, caseX, caseY, caseCibleX, caseCibleY)
        self.open = []
        self.closed = []
        self.open.append(noeudInit)
        self.time1 = time.time()
        chemin = self.aEtoile(0.3)

        # print("Temps a*: ", time.time() - self.time1)

        n = chemin
        if not n == -1:
            cheminTrace = []
            while n.parent:
                cheminTrace.append(n)
                centreCase = self.model.trouverCentreCase(n.x, n.y)
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
        """Essai de trouver le path(après un essai)"""
        # print("traceFail", self.cibleX,self.cibleY)
        # print("avant", n.x,n.y)
        self.open = []
        self.closed = []

        self.open = self.ancienOpen
        #self.afficherList("open",self.ancienOpen)
        self.closed = self.ancienClosed
        #self.afficherList("closed",self.ancienClosed)
        #noeudInit = self.ancienN
        n = self.cheminTrace[0]
        cases = self.model.trouverCaseMatrice(n.x,n.y)
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
                    centreCase = self.model.trouverCentreCase(int(n.x),int(n.y))
                    n.x = centreCase[0]
                    n.y = centreCase[1]
                else:
                    pass
                n = n.parent
            #print(self.cheminTrace,"len", len(self.cheminTrace))
            if self.trouver == True:
                self.finTrace()

    def finTrace(self):
        """Trouver la fin du path"""
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
        """Trouver le path entre toi et le debut d'un autre path"""
        # Trouver le chemin entre le début du pathfinding et la position actuelle

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
        """Trouver un path entre la fin d'un path et un autre path"""
        # unit.afficherList("unit chemin AVANT", unit.cheminTrace)
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
        # print("toruev FIn path x", unit.x, unit.y, unit.cibleX, unit.cibleY)
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
        #unit.afficherList("unit chemin", unit.cheminTrace)
        #print("-----------")
        unit.cibleXDeplacement = unit.cheminTrace[-1].x
        unit.cibleYDeplacement = unit.cheminTrace[-1].y

    def trouverCheminMultiSelection(self):
        if self.leader == 1 and self.groupeID:
            for unitId in self.groupeID:
                unit = self.model.getUnit(unitId)
                if not unit.leader == 1:
                    self.trouverCheminMultiSelectionUnit(unit)
                    
        if self.leader == 1 and self.ennemiCible:
            self.trouverCheminMultiSelectionUnit(self)

        #self.leader = 0 #defaut
        self.groupeID = []

    def trouverCheminMultiSelectionUnit(self,unit):
        """Utilisé par trouverCheminMultiSelection"""
        unit.cheminTrace = self.cheminTrace[:]
        self.trouverDebutPath(unit)
        #print("tourver", unit.leader, unit.finMultiSelection, len(self.groupeID), self.leader)
        
        unit.cheminTrace[0] = unit.finMultiSelection
        
        try:
            self.trouverFinPath(unit)
        except:
            print("none.. mais bon !")
        try:
            unit.cibleX = unit.finMultiSelection.x
            unit.cibleY = unit.finMultiSelection.y
        except:
            if unit.ennemiCible:
                unit.cheminTrace = [Noeud(None, unit.ennemiCible.x, unit.ennemiCible.y, None, None)]
            else:
                unit.cheminTrace = [Noeud(None, unit.cibleX, unit.cibleY, None, None)]
            print("Y'a pas de finMultiSelection!")
        #print(unit.cibleX, unit.cibleY, unit.finMultiSelection.x, unit.finMultiSelection.y)
        unit.trouver = True
        

    def aEtoile(self, tempsMax):
        nbNoeud = 100
        while self.open:
            n = self.open[0]
            #print("temps", self.tempsTotal , self.distance/1000)
            if self.goal(n):
                print("Temps total: ", self.tempsTotal)
                self.trouver = True
                #print("changeent true trouver !")
                self.ancienOpen = []
                self.ancienClosed = []
                if self.ressource:
                    cases = self.model.trouverCentreCase(n.x,n.y)
                    #if not n.x == caseCibleX and n - caseCibleX:
                    for unitID in self.groupeID:
                        self.model.getUnit(unitID).posUnitRessource = Noeud(None, cases[0], cases[1], None, None)
                    self.posUnitRessource = Noeud(None, cases[0], cases[1], None, None)
                    #print("ressource node" ,cases[0], cases[1])
                #if self.mode == 1:
                    #cases = self.parent.trouverCentreCase(n.x,n.y)
                    #if not n.x == caseCibleX and n - caseCibleX:
                      #  self.posRessource = Noeud(None, cases[0], cases[1], None, None)
                       # print("ressource node" ,cases[0], cases[1])
                return n
            if self.tempsTotal > self.distance/1000 and self.tempsTotal > 1:
                    print("introuvable ", n.x, n.y, tempsMax)
                    self.trouver = True
                    return -1
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
            
                # print("Temps sort: ", tempsTotal)

            if len(self.open) > nbNoeud:
                #self.afficherList("open", self.open)
                #return -1

                self.open = self.open[:nbNoeud]
                #print(len(self.open))
                #self.parent.parent.v.afficherCourantPath(self.open)
            if time.time() - self.time1 > tempsMax:
                self.trouver = False
                self.tempsTotal += time.time()-self.time1
                #print("lol", self.tempsTotal,time.time()-self.time1 )

                # print("changeent false", n.x, n.y)
                # self.ancienClosed = self.closed
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
            if caseX - 1 >= 0 and not self.model.carte.matrice[caseX - 1][caseY - 1].isWalkable:
                return True
            if not self.model.carte.matrice[caseX][caseY - 1].isWalkable:
                return True
            if caseX + 1 < self.model.grandeurMat and not self.model.carte.matrice[caseX + 1][caseY - 1].isWalkable:
                return True

        if caseX - 1 >= 0 and not self.model.carte.matrice[caseX - 1][caseY].isWalkable:
            return True
        if caseX + 1 < self.model.grandeurMat and not self.model.carte.matrice[caseX + 1][caseY].isWalkable:
            return True

        if caseY + 1 < self.model.grandeurMat:
            if caseX - 1 >= 0 and not self.model.carte.matrice[caseX - 1][caseY + 1].isWalkable:
                return True
            if not self.model.carte.matrice[caseX][caseY + 1].isWalkable:
                return True
            if caseX + 1 < self.model.grandeurMat and not self.model.carte.matrice[caseX + 1][caseY + 1].isWalkable:
                return True

        return False

    def transition(self, n):
        caseTransition = []

        caseX = n.x
        caseY = n.y
        casesCible = self.model.trouverCaseMatrice(self.cibleX, self.cibleY)
        caseCibleX = casesCible[0]
        caseCibleY = casesCible[1]

        if caseY - 1 >= 0:
            if caseX - 1 >= 0 and self.model.carte.matrice[caseX - 1][caseY - 1].isWalkable and not self.aCoteMur(
                            caseX - 1, caseY - 1):
                caseTransition.append(Noeud(n, caseX - 1, caseY - 1, caseCibleX, caseCibleY))
            if self.model.carte.matrice[caseX][caseY - 1].isWalkable:
                caseTransition.append(Noeud(n, caseX, caseY - 1, caseCibleX, caseCibleY))
            if caseX + 1 < self.model.grandeurMat and self.model.carte.matrice[caseX + 1][
                        caseY - 1].isWalkable and not self.aCoteMur(caseX + 1, caseY - 1):
                caseTransition.append(Noeud(n, caseX + 1, caseY - 1, caseCibleX, caseCibleY))

        if caseX - 1 >= 0 and self.model.carte.matrice[caseX - 1][caseY].isWalkable:
            caseTransition.append(Noeud(n, caseX - 1, caseY, caseCibleX, caseCibleY))
        if caseX + 1 < self.model.grandeurMat and self.model.carte.matrice[caseX + 1][caseY].isWalkable:
            caseTransition.append(Noeud(n, caseX + 1, caseY, caseCibleX, caseCibleY))

        if caseY + 1 < self.model.grandeurMat:
            if caseX - 1 >= 0 and self.model.carte.matrice[caseX - 1][caseY + 1].isWalkable and not self.aCoteMur(
                            caseX - 1, caseY + 1):
                caseTransition.append(Noeud(n, caseX - 1, caseY + 1, caseCibleX, caseCibleY))
            if self.model.carte.matrice[caseX][caseY + 1].isWalkable:
                caseTransition.append(Noeud(n, caseX, caseY + 1, caseCibleX, caseCibleY))
            if caseX + 1 < self.model.grandeurMat and self.model.carte.matrice[caseX + 1][
                        caseY + 1].isWalkable and not self.aCoteMur(caseX + 1, caseY + 1):
                caseTransition.append(Noeud(n, caseX + 1, caseY + 1, caseCibleX, caseCibleY))

        return caseTransition


    def goal(self, noeud):
        casesCible = self.model.trouverCaseMatrice(self.cibleX, self.cibleY)
        caseCibleX = casesCible[0]
        caseCibleY = casesCible[1]

        if noeud.x == caseCibleX and noeud.y == caseCibleY:
            return True
        elif abs(noeud.x - caseCibleX) <= 1 and abs(
                        noeud.y - caseCibleY) <= 1 and (self.mode == 1 or self.mode == 4 or self.mode == 5):  # pour les ressources
            #cases = self.parent.trouverCentreCase(noeud.x,noeud.y)
            #print("avant", self.posRessource.x, self.posRessource.y)
            #self.posRessource = Noeud(None, cases[0], cases[1], None, None)
            #print("ressource node" , self.mode, cases[0], cases[1])
            return True
        return False


    # KOMBAT ==========================================================

    def determineCombatBehaviour(self, model):
        """ Détermine le comportement de combat à adopter
        dépendemment du mode de combat (Actif ou Passif)
        """
        if int(self.getClientId()) != model.joueur.civilisation and not self.joueur.ai:
             return     # Ce n'est pas une unité du joueur en cours ni l'AI

        if self.ennemiCible == self:
            self.ennemiCible = None

        # ACTIF
        if self.modeAttack == Unit.ACTIF and not self.mode == 3:
            # On se choisie une cible et on envoie une commande pour l'attaquer
            # vision range
            try:
                units = model.controller.view.detectUnits(self.x - self.rayonVision, self.y - self.rayonVision,
                                                          self.x + self.rayonVision, self.y + self.rayonVision,
                                                          units=self.model.getUnits())
            except:
                print("ennemi tué")

            # units = [u for u in units if not u.estUniteDe(self.getClientId()) and u.id != self.id]
            units = [u for u in units if not u.id == self.id]
            if not units:
                return

            # Prendre la plus proche
            closestDistance = 2000
            closestUnit = units[0]
            for unit in units:
                d = math.hypot(self.x - unit.x, self.y - unit.y)
                if d > closestDistance:
                    closestUnit = unit
            self.ennemiCible = closestUnit
            self.cibleX = self.ennemiCible.x
            self.cibleY = self.ennemiCible.y
            self.mode = 3
            print("leader actif", self.id, self.leader)
            if self.leader == 1:
                groupe = []
                groupe.append(self)
                for unitID in self.groupeID: 
                    groupe.append(model.getUnit(unitID))

                self.model.controller.eventListener.onUnitRClick((self.model.getUnit(self.ennemiCible.id)),groupe)

            if self.ancienPosEnnemi == None:
                self.ancienPosEnnemi = (self.ennemiCible.x,self.ennemiCible.y)
            # Chercher une cible dans sans champ de vision
            # Lancer une commande attaque vers la cible


        #ATTAQUE
        if self.ennemiCible:
            if self.ancienPosEnnemi is None:
                self.ancienPosEnnemi = (self.ennemiCible.x,self.ennemiCible.y)
            if not self.ennemiCible == self and self.mode == 3:
                self.attaquer(model)
                return
            else:
                print("NON", self.id, self.mode)

    def attaquer(self, model):
        """ Permet d'attaquer une unité
        """
        # try:
        #    self.animHurt.animate()
        #except AttributeError:
        #    pass
        if self.ennemiCible.hp == 0:
            self.ennemiCible = None
            #TODO: SI en déplacement trouver une nouvelle position...
            return

        

        # Si je suis trop loin je me rapproche de l'ennemi
        distance = self.grandeur + (model.controller.view.carte.item/2) #Car il va au centre de la case...
        if abs(self.x - self.ennemiCible.x) > distance or abs(self.y - self.ennemiCible.y) > distance: #and not self.cheminTrace:
            #print(abs(self.x - self.ennemiCible.x), abs(self.y - self.ennemiCible.y), self.grandeur)
            try:
                #print("cible", self.ennemiCible.x, self.ennemiCible.y, self.ancienPosEnnemi[0], self.ancienPosEnnemi[1])
                print("cible", self.ennemiCible.x, self.ennemiCible.y, self.ancienPosEnnemi[0], self.ancienPosEnnemi[1],self.x, self.y,self.ennemiCible.enDeplacement, self.cheminTrace)
                if self.ennemiCible.enDeplacement:
                #if abs(self.ennemiCible.x - self.ancienPosEnnemi[0]) > distance or abs(self.ennemiCible.y - self.ancienPosEnnemi[1]) > distance: #or not self.cheminTrace:
                    #x2 = self.ennemiCible.x-self.grandeur
                    #y2 = self.ennemiCible.y-self.grandeur
                    self.ancienPosEnnemi = (self.ennemiCible.x,self.ennemiCible.y)
                    if self.leader == 1:
                        print("leader deplacement attaque", self.id)
                        groupe = []
                        groupe.append(self)
                        for unitID in self.groupeID: 
                            groupe.append(model.getUnit(unitID))

                        self.model.controller.eventListener.onUnitRClick((self.model.getUnit(self.ennemiCible.id)),groupe)
                        #model.controller.eventListener.selectionnerUnit(self,True, None,x2,y2, groupe)
                        # TODO: DOIT CHANGER LUI ET SON GROUPE !
                    else:
                        print("CRY", self.leader)
                        # TODO: Trouver nouvelle position sans les unités sélectionnés (avec le groupe) FAIRE LE CHANGMENT POUR LE LEADER SEULEMENT !!! QUI CHANGERA SON GROUPE
                        
                        #posFin = model.trouverFinMultiSelection(x2, y2, 1,self.grandeur)
                        #model.controller.eventListener.selectionnerUnit(self,False, posFin,self.ennemiCible.x-self.grandeur, self.ennemiCible.y-self.grandeur, self )
                        #groupe = []
                        #groupe.append(self)
                        #model.controller.eventListener.onUnitRClick((self.model.getUnit(self.ennemiCible.id)),groupe)
                    #print("1")
                    return
                #print("2")
                return
            except:
                print("pos ennemi fail")
                return
            

        if self.timerAttack.isDone():
            attack = random.randint(self.attackMin, self.attackMax)
            # TODO ENVOYER L'ATTAQUE AU SERVEUR
            cmd = Command(cmdType=Command.UNIT_ATTACK_UNIT)
            cmd.addData('SOURCE_ID', self.id)
            cmd.addData('TARGET_ID', self.ennemiCible.id)
            cmd.addData('DMG', attack)
            model.controller.sendCommand(cmd)
            self.timerAttack.reset()

    def attaquerBuilding(self, model, building):
        if not building.estBatimentDe(self.joueur.civilisation) and self.mode == 5 and not self.enDeplacement:
            if self.timerAttack.isDone():
                attack = random.randint(self.attackMin, self.attackMax)
                cmd = Command(cmdType=Command.UNIT_ATTACK_BUILDING)
                cmd.addData('SOURCE_ID', self.id)
                cmd.addData('TARGET_ID', building.id)
                print("commande dattaque envoyer vers : "+building.id)
                cmd.addData('DMG', attack)
                model.controller.sendCommand(cmd)
                self.timerAttack.reset()


    def recevoirAttaque(self, model, attaquant, attack):
        """ Permet d'affaiblir une unité
        :param attack: Force d'attaque (int)
        """
        self.hp -= attack
        anim = OneTimeAnimation(GraphicsManager.getAnimationSheet('Animations/mayoche.png', 1, 3), 50)
        self.oneTimeAnimations.append(anim)


        if self.hp <= 0:
            self.hp = 0  # UNITÉ MORTE
            cmd = Command(self.getClientId(), Command.UNIT_DIE)

            cmd.addData('ID', self.id)
            model.controller.sendCommand(cmd)

        # RIPOSTER SEULEMENT SI ON EST LE PROPRIÉTAIRE DE L'UNITÉ
        # TODO Compatibiliser avec l'AI
        if int(self.getClientId()) == model.joueur.civilisation or self.joueur.ai:
            self.ennemiCible = attaquant
            self.mode = 3


class Paysan(Unit):

    def __init__(self, clientId, x, y, model, civilisation):
        super(Paysan, self).__init__(clientId, x, y, model, civilisation)
        self.vitesseRessource = 0.1  # 0.01  # La vitesse à ramasser des ressources
        self.nbRessourcesMax = 2
        self.nbRessources = 0
        self.typeRessource = 0  # 0 = Rien 1 à 4 = Ressources
        self.compteurRessource = 0
        self.posRessource = Noeud(None, 0, 0, None, None)

    def determineSpritesheet(self):

        ageString = {1: 'Age_I', 2: 'Age_II', 3: 'Age_III'}
        age = ageString[self.joueur.epoque]

        spritesheets = {
            Civilisation.BLANC: 'Units/%s/paysans/paysan_blanc.png' % age,
            Civilisation.BLEU: 'Units/%s/paysans/paysan_bleu.png' % age,
            Civilisation.JAUNE: 'Units/%s/paysans/paysan_jaune.png' % age,

            Civilisation.MAUVE: 'Units/%s/paysans/paysan_mauve.png' % age,
            Civilisation.NOIR: 'Units/%s/paysans/paysan_noir.png' % age,
            Civilisation.ORANGE: 'Units/%s/paysans/paysan_orange.png' % age,

            Civilisation.ROUGE: 'Units/%s/paysans/paysan_rouge.png' % age,
            Civilisation.VERT: 'Units/%s/paysans/paysan_vert.png' % age,
            Civilisation.ROSE: 'Units/%s/paysans/paysan_rose.png' % age
        }
        spritesheet = GraphicsManager.getSpriteSheet(spritesheets[self.civilisation])
        self.animation = SpriteAnimation(spritesheet, 333)  # 1000/333 = 3 fois par secondes


    def chercherRessources(self):
        # print(int(self.nbRessources))
        # TODO Regarder le type de la ressource !
        # TODO Enlever nbRessources à la case ressource !
        #print(self.nbRessources)
        cases = self.model.trouverCaseMatrice(self.posRessource.x, self.posRessource.y)
        if self.model.carte.matrice[cases[0]][cases[1]].type == 0:
            print("FIN DE LA RESSOURCE")
            self.mode = 0
        if self.nbRessources + self.compteurRessource + self.vitesseRessource <= self.nbRessourcesMax:
            self.compteurRessource += self.vitesseRessource
            if self.compteurRessource >= 1:
                cmd = Command(cmdType=Command.UNIT_TAKE_RESSOURCES)
                cmd.addData('ID',self.id)
                cmd.addData('X1',cases[0])
                cmd.addData('Y1',cases[1])
                cmd.addData('NB_RESSOURCES', 1)
                self.model.controller.sendCommand(cmd)
                self.compteurRessource = 0
            #self.nbRessources += self.vitesseRessource
        else:
            if not self.ressourceEnvoye:
                cmd = Command(cmdType=Command.UNIT_TAKE_RESSOURCES)
                cmd.addData('ID',self.id)
                cmd.addData('X1',cases[0])
                cmd.addData('Y1',cases[1])
                cmd.addData('NB_RESSOURCES', self.nbRessourcesMax-self.nbRessources)
                #self.nbRessources = self.nbRessourcesMax
           
                if self.joueur.base:
                    if not self.cheminTrace:
                        #print("compare",self.x, self.posUnitRessource.x, self.y, self.posUnitRessource.y)
                        #if self.x == self.posUnitRessource.x and self.y == self.posUnitRessource.y:
                        #print(self.id, "aller à la base",self.ressourceEnvoye )
                        if not self.ressourceEnvoye:
                            print(self.id, "envoyé à la base !")
                            self.posUnitRessource = Noeud(None, self.x, self.y, None, None)
                            groupe = []
                            groupe.append(self)
                            #self.ressourceEnvoye = True
                            
                            self.model.controller.eventListener.onMapRClick(self.joueur.base, groupe)
                            self.model.controller.sendCommand(cmd)
                            #self.model.controller.eventListener.onMapRClick(self.joueur.base, groupe)#QUICK FIX
                            self.ressourceEnvoye = True
                        #else:
                         #   print("aller à la ressource", self.enDeplacement)
                            #Remettre les ressources
                        
        
                #self.mode = 2

            # print("MAX!", self.nbRessources)
            # TODO Faire retourner à la base !

class Soldat(Unit):
    def __init__(self, clientId, x, y, model, civilisation):
        super(Soldat, self).__init__(clientId, x, y, model, civilisation)

class GuerrierEpee(Soldat):
    def __init__(self, clientId, x, y, model, civilisation):
        super(GuerrierEpee, self).__init__(clientId, x, y, model, civilisation)
        self.vitesse = 5
        # Kombat
        # Health Points, Points de Vie
        self.hpMax = 40
        self.hp = 40
        # Force à laquelle l'unité frappe
        self.attackMin = 1
        self.attackMax = 15

    def determineSpritesheet(self):
        spritesheets = {
            Civilisation.BLANC: 'Units/Age_II/Soldat_epee/soldat_epee_blanc.png',
            Civilisation.BLEU: 'Units/Age_II/Soldat_epee/soldat_epee_bleu.png',
            Civilisation.JAUNE: 'Units/Age_II/Soldat_epee/soldat_epee_jaune.png',

            Civilisation.MAUVE: 'Units/Age_II/Soldat_epee/soldat_epee_.png',
            Civilisation.NOIR: 'Units/Age_II/Soldat_epee/soldat_epee_noir.png',
            Civilisation.ORANGE: 'Units/Age_II/Soldat_epee/soldat_epee_orange.png',

            Civilisation.ROUGE: 'Units/Age_II/soldat_epee_rouge.png',
            Civilisation.VERT: 'Units/Age_II/soldat_epee_vert.png',
            Civilisation.ROSE: 'Units/Age_II/soldat_epee_rose.png'
        }

        spritesheet = GraphicsManager.getSpriteSheet(spritesheets[self.civilisation])
        self.animation = SpriteAnimation(spritesheet, 333)  # 1000/333 = 3 fois par secondes

class GuerrierLance(Soldat):
    def __init__(self, clientId, x, y, model, civilisation):
        super(GuerrierLance, self).__init__(clientId, x, y, model, civilisation)
        self.vitesse = 5
        # Kombat
        # Health Points, Points de Vie
        self.hpMax = 30
        self.hp = 30
        # Force à laquelle l'unité frappe
        self.attackMin = 1
        self.attackMax = 25

    def determineSpritesheet(self):
        spritesheets = {
            Civilisation.BLANC: 'Units/Age_II/Soldat_lance/soldat_lance_blanc.png',
            Civilisation.BLEU: 'Units/Age_II/Soldat_lance/soldat_lance_bleu.png',
            Civilisation.JAUNE: 'Units/Age_II/Soldat_lance/soldat_lance_jaune.png',

            Civilisation.MAUVE: 'Units/Age_II/Soldat_lance/soldat_lance_mauve.png',
            Civilisation.NOIR: 'Units/Age_II/Soldat_lance/soldat_lance_noir.png',
            Civilisation.ORANGE: 'Units/Age_II/Soldat_lance/soldat_lance_orange.png',

            Civilisation.ROUGE: 'Units/Age_II/Soldat_lance/soldat_lance_rouge.png',
            Civilisation.VERT: 'Units/Age_II/Soldat_lance/soldat_lance_vert.png',
            Civilisation.ROSE: 'Units/Age_II/Soldat_lance/soldat_lance_rose.png'
        }

        spritesheet = GraphicsManager.getSpriteSheet(spritesheets[self.civilisation])
        self.animation = SpriteAnimation(spritesheet, 333)  # 1000/333 = 3 fois par secondes

class GuerrierBouclier(Soldat):
    def __init__(self, clientId, x, y, model, civilisation):
        super(GuerrierBouclier, self).__init__(clientId, x, y, model, civilisation)
        self.vitesse = 5
        # Kombat
        # Health Points, Points de Vie
        self.hpMax = 50
        self.hp = 50
        # Force à laquelle l'unité frappe
        self.attackMin = 1
        self.attackMax = 10

    def determineSpritesheet(self):
        spritesheets = {
            Civilisation.BLANC: 'Units/Age_II/Soldat_bouclier/soldat_bouclier_blanc.png',
            Civilisation.BLEU: 'Units/Age_II/Soldat_bouclier/soldat_bouclier_bleu.png',
            Civilisation.JAUNE: 'Units/Age_II/Soldat_bouclier/soldat_bouclier_jaune.png',

            Civilisation.MAUVE: 'Units/Age_II/Soldat_bouclier/soldat_bouclier_mauve.png',
            Civilisation.NOIR: 'Units/Age_II/Soldat_bouclier/soldat_bouclier_noir.png',
            Civilisation.ORANGE: 'Units/Age_II/Soldat_bouclier/soldat_bouclier_orange.png',

            Civilisation.ROUGE: 'Units/Age_II/Soldat_bouclier/soldat_bouclier_rouge.png',
            Civilisation.VERT: 'Units/Age_II/Soldat_bouclier/soldat_bouclier_vert.png',
            Civilisation.ROSE: 'Units/Age_II/Soldat_bouclier/soldat_bouclier_rose.png'
        }
        spritesheet = GraphicsManager.getSpriteSheet(spritesheets[self.civilisation])
        self.animation = SpriteAnimation(spritesheet, 333)  # 1000/333 = 3 fois par secondes

class Scout(Soldat):
    def __init__(self, clientId, x, y, model, civilisation):
        super(Scout, self).__init__(clientId, x, y, model, civilisation)
        self.vitesse = 10
        # Kombat
        # Health Points, Points de Vie
        self.hpMax = 20
        self.hp = 20
        # Force à laquelle l'unité frappe
        self.attackMin = 0
        self.attackMax = 8

    def determineSpritesheet(self):
        spritesheets = {
            Civilisation.BLANC: 'Units/Age_I/paysan_blanc.png',
            Civilisation.BLEU: 'Units/Age_I/paysan_bleu.png',
            Civilisation.JAUNE: 'Units/Age_I/paysan_jaune.png',

            Civilisation.MAUVE: 'Units/Age_I/paysan_mauve.png',
            Civilisation.NOIR: 'Units/Age_I/paysan_noir.png',
            Civilisation.ORANGE: 'Units/Age_I/paysan_orange.png',

            Civilisation.ROUGE: 'Units/Age_I/paysan_rouge.png',
            Civilisation.VERT: 'Units/Age_I/paysan_vert.png',
            Civilisation.ROSE: 'Units/Age_I/paysan_rose.png'
        }

        spritesheet = GraphicsManager.getSpriteSheet(spritesheets[self.civilisation])
        self.animation = SpriteAnimation(spritesheet, 333)  # 1000/333 = 3 fois par secondes

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
