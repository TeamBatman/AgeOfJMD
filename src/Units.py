import random
import sys
import time
from GraphicsManagement import SpriteSheet, AnimationSheet, SpriteAnimation
from Joueurs import Joueur
from Timer import Timer


class Unit():
    COUNT = 0  # Un compteur permettant d'avoir un Id unique pour chaque unité


    # COMBAT
    ACTIF = 0
    PASSIF = 0


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
        self.grandeur = 30
        self.cibleX = x
        self.cibleY = y
        self.cheminTrace = []
        self.cibleXTrace = x
        self.cibleXTrace = y
        self.mode = 0  # 1=ressource

        self.timerDeplacement = Timer(60)
        self.timerDeplacement.start()

        # ANIMATION
        self.spriteSheet = None
        self.animation = SpriteAnimation(self.determineSpritesheet(), 333)  # 1000/333 = 3 fois par secondes

        # Kombat
        # Health Points, Points de Vie
        self.hpMax = 20
        self.hp = 20
        # Force à laquelle l'unité frappe
        self.attackMin = 0
        self.attackMax = 5
        self.ennemiCible = None
        self.modeAttack = Unit.PASSIF
        self.timerAttack = Timer(900)
        self.timerAttack.start()

        self.animHurtSheet = AnimationSheet('Graphics/Animations/003-Attack01.png', 2, 5)
        self.animHurt = None

        self.animHurtIndex = 0




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
        raise Exception("La méthode determineSprite doit être surchargée par tous les sous-classes de Unit et doit "
                        "retourner la sprite sheet")

    @staticmethod
    def generateId(clientId):
        gId = "%s_%s" % (clientId, Unit.COUNT)
        Unit.COUNT += 1
        return gId


    def update(self):
        if self.hp == 0:
            return
        self.determineCombatBehaviour()

        try:
            self.deplacementTrace()
        except:
            print("unit fail")
            self.deplacement()


    def changerCible(self, cibleX, cibleY):
        self.mode = 0
        self.cibleX = cibleX
        self.cibleY = cibleY
        self.choisirTrace()


    def deplacer(self):

        if not self.timerDeplacement.isDone():
            return

        if self.cibleX > self.x:
            self.x += self.vitesse
            self.animation.direction = SpriteSheet.Direction.RIGHT

        elif self.cibleX < self.x:
            self.x -= self.vitesse
            self.animation.direction = SpriteSheet.Direction.LEFT

        if self.cibleY > self.y:
            self.y += self.vitesse
            self.animation.direction = SpriteSheet.Direction.DOWN

        elif self.cibleY < self.y:
            self.y -= self.vitesse
            self.animation.direction = SpriteSheet.Direction.UP

        # Puisqu'il y a eu un déplacement
        self.animation.animate()
        self.timerDeplacement.reset()


    def deplacement(self):
        if abs(self.cibleX - self.x) <= self.vitesse:
            self.x = self.cibleX
        if abs(self.cibleY - self.y) <= self.vitesse:
            self.y = self.cibleY

        self.deplacer()

    def deplacementTrace(self):
        if len(self.cheminTrace) > 0:
            if self.x == self.cibleX and self.y == self.cibleY:
                del self.cheminTrace[-1]
                if len(self.cheminTrace) <= 0:
                    self.animation.setActiveFrameKey(SpriteSheet.Direction.DOWN, 1)
                    return -1
                self.cibleX = self.cheminTrace[-1].x
                self.cibleY = self.cheminTrace[-1].y

            if abs(self.cibleX - self.x) <= self.vitesse:
                self.x = self.cibleX
            if abs(self.cibleY - self.y) <= self.vitesse:
                self.y = self.cibleY
            self.deplacer()


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
        time1 = time.time()
        chemin = self.aEtoile()
        # print("Temps a*: ", time.time() - time1)
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
                # Pour ne pas finir sur le centre de la case (Pour finir sur le x,y du clic)
                if not self.mode == 1:  # pas en mode ressource
                    self.cheminTrace[0] = Noeud(None, self.cibleX, self.cibleY, None, None)
            else:
                if not self.mode == 1:  # pas en mode ressource
                    self.cheminTrace.append(Noeud(None, self.cibleX, self.cibleY, None, None))
                else:
                    self.cheminTrace.append(Noeud(None, self.x, self.y, None, None))

            self.cibleX = self.cheminTrace[-1].x
            self.cibleY = self.cheminTrace[-1].y

    def aEtoile(self):
        nbNoeud = 400
        while self.open:
            n = self.open[0]
            if self.goal(n):
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

                    # Mettre dans le if aAjouter ?
                    # time1= time.time()
                self.open.sort(key=lambda x: x.cout)
                # tempsTotal += time.time()-time1
                # print("Temps sort: ", tempsTotal)
                if len(self.open) > nbNoeud:
                    # self.afficherList("open", self.open)
                    # return -1
                    self.open = self.open[:nbNoeud]
                    # print(len(self.open))
                    # self.parent.parent.v.afficherCourantPath(self.open)
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

        if caseX - 1 >= 0 and not self.parent.carte.matrice[caseX - 1][caseY] == 0:
            return False
        if caseX + 1 < self.parent.grandeurMat and not self.parent.carte.matrice[caseX + 1][caseY] == 0:
            return False

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


    # KOMBAT ==========================================================

    def determineCombatBehaviour(self):
        """ Détermine le comportement de combat à adopter
        dépendemment du mode de combat (Actif ou Passif)
        """
        # PASSIF
        if self.modeAttack == Unit.PASSIF:
            if self.ennemiCible:
                self.attaquer()

        # ACTIF
        if self.modeAttack == Unit.ACTIF:
            pass     # TODO
            # Chercher une cible dans sans champ de vision
            # Lancer une commande attaque vers la cible



    def attaquer(self):
        """ Permet d'attaquer une unité
        """
        if self.ennemiCible.hp == 0:
            self.ennemiCible = None
            return

        # Si je suis trop loin je me rapproche de l'ennemi

        if abs(self.x - self.ennemiCible.x) > self.grandeur or abs(self.y - self.ennemiCible.y) > self.grandeur:
            self.changerCible(self.ennemiCible.x - self.grandeur, self.ennemiCible.y - self.grandeur)
            return

        if self.timerAttack.isDone():
            attack = random.randint(self.attackMin, self.attackMax)
            self.ennemiCible.recevoirAttaque(self, attack)
            self.timerAttack.reset()

    def recevoirAttaque(self, attaquant, attack):
        """ Permet d'affaiblir une unité
        :param attack: Force d'attaque (int)
        """
        self.hp -= attack
        if self.hp <= 0:
            self.hp = 0  # UNITÉ MORTE

        try:
            self.animHurt = self.animHurtSheet.frames[0][self.animHurtIndex]
        except KeyError:
            self.animHurtIndex = 0

        # RIPOSTER
        self.ennemiCible = attaquant


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
        return SpriteSheet(spritesheets[self.civilisation])


    def chercherRessources(self):
        # print(int(self.nbRessources))
        # TODO Regarder le type de la ressource !
        # TODO Enlever nbRessources à la case ressource !
        if self.nbRessources + self.vitesseRessource <= self.nbRessourcesMax:
            self.nbRessources += self.vitesseRessource
        else:
            self.nbRessources = self.nbRessourcesMax
            # print("MAX!", self.nbRessources)
            # TODO Faire retourner à la base !


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