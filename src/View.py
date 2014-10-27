#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from tkinter import *  # Python 3
except ImportError:
    from Tkinter import *  # Python 2

from GuiAwesomeness import *
from itertools import product


class FrameSide():
    def __init__(self, canvas, largeurMinimap, hauteurMinimap):
        self.canvas = canvas

        self.width = largeurMinimap
        self.height = int(self.canvas.cget('height')) - hauteurMinimap

        self.x = int(self.canvas.cget('width')) - self.width
        self.y = hauteurMinimap

        self.frame = GFrame(self.canvas, width=self.width, height=self.height)


    def draw(self):
        """ Affiche le CADRE 
        """
        self.frame.draw(self.x, self.y)


class FrameMiniMap():
    def __init__(self, canvas, eventListener):
        self.canvas = canvas
        self.eventListener = eventListener

        # LE CADRE
        self.width = 250  # Largeur du cadre en pixels
        self.height = 250  # hauteur du cadre en pixels
        self.x = int(self.canvas.cget('width')) - self.width  # en pixels
        self.y = 0  # en pixels
        self.frame = GFrame(self.canvas, width=self.width, height=self.height)


        # LA MINIMAP
        self.miniMapTag = 'miniMap'  # Le tag tkinter à utiliser pour la minimap
        self.miniMapWidth = 211  # en pixels
        self.miniMapHeight = 211  # en pixels

        # # Taille de la marge entre la cadre et la minimap en pixels
        self.minimapMargeX = int((self.width - self.miniMapWidth) / 2)
        self.minimapMargeY = int((self.height - self.miniMapHeight) / 2)

        # Position de la minimap en pixel par rapport au caneva
        self.miniMapX = self.x + self.minimapMargeX
        self.miniMapY = self.y + self.minimapMargeY

        # Position de la mini caméra en pixels selon le coins haut gauche
        self.miniCameraX = self.miniMapX
        self.miniCameraY = self.miniMapY

        self.tailleTuile = 2  # Taille d'une tuile en pixels 


    def bindEvents(self):
        """ Lie les évènements entre au eventListener
        """

        # Carré d'écoute des événèments (pour le tag)
        self.canvas.create_rectangle(self.miniMapX, self.miniMapY, self.miniMapWidth + self.miniMapX,
                                     self.miniMapHeight + self.miniMapY, fill='green', tags=self.miniMapTag)

        self.canvas.tag_bind(self.miniMapTag, '<ButtonPress-1>', self.eventListener.onMinimapLPress)
        self.canvas.tag_bind(self.miniMapTag, '<B1-Motion>', self.eventListener.onMinimapMouseMotion)

    def draw(self):
        """ Dessine le CADRE de la minimap à l'écran
        """
        self.frame.draw(self.x, self.y)

    def updateMinimap(self, carte):
        """ Met à jours, (re)dessine la carte de la minimap
        """
        self.canvas.delete(self.miniMapTag)
        # x1 = self.miniMapX
        # y1 = self.miniMapY
        #x2 = x1 + self.miniMapWidth
        #y2 = y1 + self.miniMapHeight

        size = 106  # TODO Explication de ce chiffre
        itemMini = self.tailleTuile  # La grandeur des cases pour la minimap en pixels
        couleurs = {
            View.GAZON: "#0B610B",  # vert
            View.FORET: "#BFBF00",  # jaune
            View.MINERAI: "#1C1C1C",  # gris pale
            View.CHARBON: "#BDBDBD",  # gris fonce
            View.EAU: "#2E9AFE"  # bleu
        }

        for x in range(size):
            for y in range(size):
                posX1 = self.miniMapX + x * itemMini
                posY1 = self.miniMapY + y * itemMini
                posX2 = posX1 + itemMini
                posY2 = posY1 + itemMini
                couleur = couleurs[carte[x][y].type]

                self.canvas.create_rectangle(posX1, posY1, posX2, posY2, width=0, fill=couleur, tags=self.miniMapTag)


    def updateMiniUnits(self, units):
        """ (Re)dessine les unités à l'écran
        :param units: les unités
        """
        tagUnits = 'miniUnits'
        self.canvas.delete(tagUnits)
        color = 'red'  # TODO METTRE LES COULEURS SELON LA CIVILISATION
        item = 2
        for unit in units:
            caseX, caseY = self.eventListener.controller.model.trouverCaseMatrice(unit.x, unit.y)
            x1 = self.miniMapX + (caseX * item)
            y1 = self.minimapMargeY + (caseY * item)
            x2 = x1 + item
            y2 = y1 + item
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags=tagUnits)

    def drawRectMiniMap(self, clicX=0, clicY=0, nbCasesX=16, nbCasesY=14):
        """ (Re)dessine le rectangle de caméra de la minimap
        :param clicX: position X de la souris en pixels
        :param clicY: position Y de la souris en pixels
        """

        width = self.tailleTuile * nbCasesX  # Largeur du Rectangle
        height = self.tailleTuile * nbCasesY  # Hauteur du Rectangle
        couleur = 'red'

        # On centre le rectangle par rapport au Clic de la souris

        self.miniCameraX = clicX - width / 2
        self.miniCameraY = clicY - height / 2


        # TESTER LES LIMITES

        # Limite Gauche
        if self.miniCameraX < self.miniMapX:
            self.miniCameraX = self.miniMapX

        # Limite Droite
        if self.miniCameraX + width > self.miniMapX + self.miniMapWidth:
            self.miniCameraX = self.miniMapX + self.miniMapWidth - width

            # Limite Haut
        if self.miniCameraY < self.miniMapY:
            self.miniCameraY = self.miniMapY

        # Limite Bas
        if self.miniCameraY + height > self.miniMapY + self.miniMapHeight:
            self.miniCameraY = self.miniMapY + self.miniMapHeight - height

        # On affiche le rectangle
        self.canvas.delete('rectMiniMap')
        self.canvas.create_rectangle(self.miniCameraX, self.miniCameraY,
                                     self.miniCameraX + width, self.miniCameraY + height,
                                     outline=couleur, tags='rectMiniMap')


class FrameBottom():
    def __init__(self, canvas, largeurMinimap):
        self.canvas = canvas
        self.width = int(self.canvas.cget('width')) - largeurMinimap
        self.height = 100

        self.x = 0
        self.y = int(self.canvas.cget('height')) - self.height

        self.frame = GFrame(self.canvas, width=self.width, height=self.height)

        # TODO COMPLETER
        self.moraleProg = GProgressBar(self.canvas, 150, "Morale")
        self.moraleProg.setProgression(63)


    def draw(self):
        """ Dessine le cadre
        """
        self.frame.draw(self.x, self.y)
        self.moraleProg.draw(x=self.frame.x + 35, y=self.frame.y + 25)


class CarteView():
    def __init__(self, canvas, eventListener, largeurEcran, hauteurEcran, largeurCadreDroit, hauteurCadreBas):
        self.canvas = canvas
        self.eventListener = eventListener

        self.width = largeurEcran - largeurCadreDroit
        self.height = hauteurEcran - hauteurCadreBas


        # CASES
        self.sizeUnit = 32  # Taille des unités en pixels
        self.item = 48  # Grandeur d'un bloc (Carte) en pixel
        # Nombre de cases Visibles en X et En Y
        self.nbCasesX = 16  # Nombre de case (de taille item) en X à afficher
        self.nbCasesY = 14  # Nombre de case (de taille item) en Y à afficher

        # Position de la caméra En terme de case (de taille item) dans la matrice de la map
        self.cameraX = 0
        self.cameraY = 0

        self.tagName = 'carte'



    def bindEvents(self):
        """ Lis les événements à la carte
        """
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill='green', tags=self.tagName)
        self.canvas.tag_lower('carte')  # Pour que ce soit derrière le HUD
        self.canvas.tag_bind('carte', '<Button-2>', self.eventListener.onMapCenterClick)
        self.canvas.tag_bind('carte', '<Button-3>', self.eventListener.onMapRClick)

        self.canvas.tag_bind('carte', '<ButtonPress-1>', self.eventListener.onMapLPress)
        self.canvas.tag_bind('carte', '<B1-Motion>', self.eventListener.onMapMouseMotion)
        self.canvas.tag_bind('carte', '<ButtonRelease-1>', self.eventListener.onMapLRelease)

        self.canvas.tag_bind('unit', '<Button-1>', self.eventListener.unitClick)

        self.canvas.tag_bind('building', '<ButtonPress-1>', self.eventListener.onMapLRelease)
        self.canvas.tag_bind('building', '<ButtonRelease-1>', self.eventListener.onMapLRelease)


    def draw(self, carte):
        """ Dessine la carte à l'écran
        :param carte: la carte
        """
        self.canvas.delete(self.tagName)
        # TODO OPTIMISER C'EST TROP LONG
        x1 = self.cameraX
        y1 = self.cameraY
        x2 = self.width
        y2 = self.height

        couleurs = {
            View.GAZON: "#0B610B",  # vert
            View.FORET: "#BFBF00",  # jaune
            View.MINERAI: "#1C1C1C",  # gris pale
            View.CHARBON: "#BDBDBD",  # gris fonce
            View.EAU: "#2E9AFE"  # bleu
        }

        for x in range(x1, x1 + self.nbCasesX):
            for y in range(y1, y1 + self.nbCasesY):
                posX1 = 0 + (x - x1) * self.item
                posY1 = 0 + (y - y1) * self.item
                posX2 = posX1 + self.item
                posY2 = posY1 + self.item

                couleur = couleurs[carte[x][y].type]

                self.canvas.create_rectangle(posX1, posY1, posX2, posY2, width=1, fill=couleur, tags=self.tagName)
        self.canvas.tag_lower(self.tagName)  # Pour que ce soit derrière le HUD


    def drawUnits(self, units, selectedUnits):
        """ Dessine les unités dans la map
        :param selectedUnits: une liste des unités sélectionnées
        :param units: une liste d'unités
        """
        self.canvas.delete('unit')
        for unit in units:
            if self.isUnitShown(unit):
                img = unit.activeOutline if unit in selectedUnits else unit.activeFrame
                posX = (unit.x - self.sizeUnit / 2) - (self.cameraX * self.item)
                posY = (unit.y - self.sizeUnit / 2) - (self.cameraY * self.item)
                self.canvas.create_image(posX, posY, anchor=NW, image=img, tags='unit')

    def isUnitShown(self, unit):
        """ Renvoie si une unité est visible par la caméra ou non
        :param unit:
        :return: True si l'unité doit être dessiner sinon False
        """
        x1 = self.cameraX * self.item
        y1 = self.cameraY * self.item
        x2 = x1 + (self.nbCasesX * self.item)
        y2 = y1 + (self.nbCasesY * self.item)

        # minimap
        unitX1 = unit.x - self.sizeUnit / 2
        unitY1 = unit.y - self.sizeUnit / 2
        unitX2 = unit.x + self.sizeUnit / 2
        unitY2 = unit.y + self.sizeUnit / 2

        if unitX1 > x1 and unitX2 < x2 and unitY1 > y1 and unitY2 < y2:
            return True

        return False


class View(GWindow):
    """ Responsable de l'affichage graphique et de captuer les entrées de l'usager"""

    GAZON    = 0
    FORET    = 1
    MINERAI  = 2
    CHARBON  = 3
    EAU      = 4

    FERME    = 0
    BARAQUE  = 1
    HOPITAL  = 2

    def __init__(self, evListener):
        GWindow.__init__(self)

        # PARAMÈTRES DE BASE

        self.width = 1024
        self.height = 768
        self.selected = []  # Liste qui contient ce qui est selectionné (unités ou bâtiments)

        self.root.geometry('%sx%s' % (self.width, self.height))
        self.root.configure(background='#2B2B2B')

        # ZONE DE DESSIN
        self.canvas = Canvas(self.root, width=self.width, height=self.height, background='#91BB62', bd=0,
                             highlightthickness=0)  # higlightthickness retire la bordure par défaut blanche des canvas
        self.canvas.pack()


        # GESTION ÉVÈNEMENTS
        self.eventListener = evListener  # Une Classe d'écoute d'évènement

        # LE HUD
        self.drawHUD()
        self.carte = CarteView(self.canvas, evListener, self.width, self.height, self.frameSide.width,
                               self.frameBottom.height)

        # LIAISON DES ÉVÉNEMENTS
        self.bindEvents()


    def drawHUD(self):
        """ Dessine la base du HUD
        """
        # LE CADRE DE LA MINIMAP
        self.frameMinimap = FrameMiniMap(self.canvas, self.eventListener)
        self.frameMinimap.draw()

        # LE CADRE DROIT
        self.frameSide = FrameSide(self.canvas, self.frameMinimap.width, self.frameMinimap.height)
        self.frameSide.draw()

        self.buttonFerme = GMediumButton(self.canvas, text=None, command=self.createBuildingFerme,
                                         iconPath="Graphics/Buildings/Age_I/Farm.png")
        self.buttonFerme.draw(x=self.width - 222, y=280)

        self.buttonBaraque = GMediumButton(self.canvas, "Baraque", self.createBuildingBaraque, GButton.GREY)
        self.buttonBaraque.draw(x=self.width - 123, y=280)
        self.buttonHopital = GMediumButton(self.canvas, "Hopital", self.createBuildingHopital, GButton.GREY)
        self.buttonHopital.draw(x=self.width - 222, y=390)

        # LE CADRE DU BAS
        self.frameBottom = FrameBottom(self.canvas, self.frameMinimap.width)
        self.frameBottom.draw()


    def drawMap(self, carte):
        """ Dessine la carte à l'écran
        :param carte: la carte
        :return:
        """
        self.carte.draw(carte)

    def drawUnits(self, units):
        """ Affiche les unités sur la carte 
        """
        self.carte.drawUnits(units, self.selected)


    def drawMinimap(self, carte):
        """ Permet de dessiner la carte
        :param carte: la carte
        """
        self.frameMinimap.updateMinimap(carte)

    def drawMiniUnits(self, units):
        """ Permet de dessiner les unités sur la minimap
        :param units: les unités
        """
        self.frameMinimap.updateMiniUnits(units)


    def drawRectMiniMap(self, clicX=0, clicY=0):
        """ Permet de dessiner la caméra de la MINIMAP
        """
        self.frameMinimap.drawRectMiniMap(clicX, clicY)

    def drawBuildings(self,buildings):
        for building in buildings:
            img = building.image
            self.canvas.create_image(building.posX,
                                         building.posY,
                                         anchor=NW,
                                         image=img,
                                         tags='ferme')

    def drawSpecificBuilding(self,building):
        img = building.image
        self.canvas.create_image(building.posX,
                                     building.posY,
                                     anchor=NW,
                                     image=img,
                                     tags='ferme')

    def addBuildingToCursor(self,posX,posY):
        #self.buildingSprite =
        pass

    def resetSelection(self):
        """ Met la sélection à 0 (désélection)
        """
        self.selected = []

    # TODO ? mettre dans carte ? 
    def detectSelected(self, x1, y1, x2, y2, units, clientId):
        """ Ajoute toutes les unités sélectionné dans le rectangle spécifié
        à la liste d'unité sélectionnées
        :param units: All the possible units
        :param x1: coord x du point haut gauche
        :param y1: coord y du point haut gauche
        :param x2: coord x du point bas droite
        :param y2: coord y du point bas droite
        """
        # TODO utiliser l'identifiant de l'unité comme tag et détecter ceci
        items = self.canvas.find_overlapping(x1, y1, x2, y2)
        for item in items:
            itemCoords = self.canvas.coords(item)
            itemCoord = (itemCoords[0] + self.carte.sizeUnit / 2 + (self.carte.cameraX * self.carte.item),
                         itemCoords[1] + self.carte.sizeUnit / 2 + (self.carte.cameraY * self.carte.item))

            for unit in units:
                if unit.estUniteDe(clientId):
                    if unit.x == itemCoord[0] and unit.y == itemCoord[1]:
                        self.selected.append(unit)  # Unité sélectionné


    # TODO ? Mettre fonctions du rectangle de sélection dans la classe map ?

    def carreSelection(self, x1, y1, x2, y2):
        """ Dessine un rectangle de selection
        :param x1: position coin haut-gauche en x
        :param y1: position coin haut-gauche en y
        :param x2: position coin bas-droit en x
        :param y2: position coin bas-droit en y
        """
        self.deleteSelectionSquare()
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='blue', tags='selection_square')

    def deleteSelectionSquare(self):
        """ Efface le rectangle de sélection à l'écran
        """
        self.canvas.delete('selection_square')


    def bindEvents(self):
        """ Lie les évènements de chacun des composantes du gui """

        self.frameMinimap.bindEvents()
        self.carte.bindEvents()

        self.root.protocol("WM_DELETE_WINDOW", self.eventListener.onCloseWindow)


    def update(self, units, buildings, carte=None):
        """ Met à jours la carte et la minimap (et leurs unités) (au besoin)"""

        # Draw Units
        if carte:
            # self.drawMinimap(units, carte)
            self.drawRectMiniMap()
            self.drawMap(carte)
            self.drawBuildings(buildings)

        self.drawMiniUnits(units)
        self.drawUnits(units)


    def show(self):
        """ Affiche la fenêtre de jeu à l'écran
        """
        self.root.mainloop()

    def after(self, ms, func):
        """ Raccourci vers la méthode de root after
        """
        self.root.after(ms, func)

    def destroy(self):
        """ Détruit la fenêtre de jeu
        """
        self.root.destroy()


    def createBuildingFerme(self):
        self.eventListener.createBuilding(View.FERME)

    def createBuildingBaraque(self):
        self.eventListener.createBuilding(View.BARAQUE)

    def createBuildingHopital(self):
        self.eventListener.createBuilding(View.HOPITAL)
