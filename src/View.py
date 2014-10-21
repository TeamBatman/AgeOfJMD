#!/usr/bin/env python
# -*- coding: utf-8 -*-
from GraphicsManagement import GraphicsManager

try:
    from tkinter import *  # Python 3
except ImportError:
    from Tkinter import *  # Python 2

from GuiAwesomeness import *

from Tuile import *
from PIL import Image
from PIL import ImageTk


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
        # TODO mettre une référence au parent

        # PARAMÈTRES DE BASE

        self.width = 1024
        self.height = 768
        self.selected = []  # Liste qui contient ce qui est selectionné

        # PARAMÈTRES CRÉATION BATIMENTS
        self.modeConstruction = False

        # POUR LES CASES
        self.sizeUnit = 32
        self.item = 48  # Grandeur d'un bloc (Carte)
        self.nbCasesX = 16
        self.nbCasesY = 14

        # ZONE DE DESSIN
        self.canvas = Canvas(self.root, width=self.width, height=self.height, background='#91BB62', bd=0,
                             highlightthickness=0)  # higlightthickness retire la bordure par défaut blanche des canvas
        self.canvas.pack()
        # Position de la Caméra
        self.positionX = 0
        self.positionY = 0

        # LE HUD
        self.drawHUD()

        # self.afficherLigne()

        # GESTION ÉVÈNEMENTS
        self.eventListener = evListener  # Une Classe d'écoute d'évènement
        self.bindEvents()


    def drawHUD(self):
        # LA MINIMAP
        self.miniMap = GFrame(self.canvas, width=250, height=250)
        self.miniMap.draw(self.width - 250, 0)

        # LE PANEL DROIT
        self.sidePanel = GFrame(self.canvas, width=250, height=self.height - 250)
        self.sidePanel.draw(self.width - 250, 250)

        self.buttonFerme = GMediumButton(self.canvas, text=None, command=self.createBuildingFerme,
                                         iconPath="Graphics/Buildings/Age_I/Farm.png")
        self.buttonFerme.draw(x=self.width - 222, y=280)

        self.buttonBaraque = GMediumButton(self.canvas, "Baraque", self.createBuildingBaraque, GButton.GREY)
        self.buttonBaraque.draw(x=self.width - 123, y=280)
        self.buttonHopital = GMediumButton(self.canvas, "Hopital", self.createBuildingHopital, GButton.GREY)
        self.buttonHopital.draw(x=self.width - 222, y=390)

        # LE PANEL DU BAS
        self.bottomPanel = GFrame(self.canvas, width=self.width - self.sidePanel.width, height=100)
        self.bottomPanel.draw(0, self.height - self.bottomPanel.height)

        self.moraleProg = GProgressBar(self.canvas, 150, "Morale")
        self.moraleProg.setProgression(63)
        self.moraleProg.draw(x=35, y=self.height - self.bottomPanel.height + 25)

    def drawMap(self, carte):
        try:
            self.canvas.delete('carte')
        except:
            pass
        x1 = self.positionX
        y1 = self.positionY
        x2 = self.width - 250
        y2 = self.height - 100

        for x in range(x1, x1 + self.nbCasesX):
            for y in range(y1, y1 + self.nbCasesY):
                posX1 = 0 + (x - x1) * self.item
                posY1 = 0 + (y - y1) * self.item
                posX2 = posX1 + self.item
                posY2 = posY1 + self.item

                if carte[x][y].type == View.GAZON:
                    couleur = "#0B610B"  # vert
                    #self.canvas.create_image(posX1, posY1,
                    #                         image=ImageTk.PhotoImage(GraphicsManager.get('Graphics/World/grass.png')))
                    #continue
                elif carte[x][y].type == View.FORET:
                    # couleur = "#D7DF01" #jaune
                    couleur = "#BFBF00"
                elif carte[x][y].type == View.MINERAI:
                    couleur = "#1C1C1C"  # gris pale
                elif carte[x][y].type == View.CHARBON:
                    couleur = "#BDBDBD"  # gris fonce
                else:
                    couleur = "#2E9AFE"  # bleu
                self.canvas.create_rectangle(posX1, posY1, posX2, posY2, width=1, fill=couleur, tags='carte')


    def drawMinimap(self, units, carte):
        try:
            self.canvas.delete('miniMap')
        except:
            pass
        x1 = self.width - 233
        y1 = 18
        x2 = self.width - 22
        y2 = y1 + 211

        size = 106
        itemMini = 2  # La grandeur des cases pour la minimap

        for x in range(0, size):
            for y in range(0, size):

                posX1 = x1 + x * itemMini
                posY1 = y1 + y * itemMini
                posX2 = posX1 + itemMini
                posY2 = posY1 + itemMini

                if carte[x][y].type == 0:
                    couleur = "#0B610B"  # vert
                elif carte[x][y].type == 1:
                    # couleur = "#D7DF01" #jaune
                    couleur = "#BFBF00"
                elif carte[x][y].type == 2:
                    couleur = "#1C1C1C"  # gris pale
                elif carte[x][y].type == 3:
                    couleur = "#BDBDBD"  # gris fonce
                else:
                    couleur = "#2E9AFE"  # bleu
                self.canvas.create_rectangle(posX1, posY1, posX2, posY2, width=0, fill=couleur, tags='miniMap')


    def drawMiniUnits(self, units):
        try:
            self.canvas.delete('miniUnits')
        except:
            pass
        color = 'red'
        item = 2
        for unit in units:
            caseX, caseY = self.eventListener.controller.model.trouverCaseMatrice(unit.x,unit.y)
            x1 = (self.width - 233) + (caseX * item)
            y1 = 18 + (caseY * item)
            x2 = x1+item
            y2 = y1+item
            self.canvas.create_rectangle(x1,y1,x2,y2, fill=color, tags='miniUnits')


    def drawRectMiniMap(self):
        try:
            self.canvas.delete('rectMiniMap')
        except:
            pass

        x1 = self.width - 233
        y1 = 18
        itemMini = 2  # La grandeur des cases pour la minimap
        xr = x1 + self.positionX * itemMini
        yr = y1 + self.positionY * itemMini

        self.canvas.create_line(xr, yr, xr + 17 * itemMini, yr, fill="red", tags='rectMiniMap')
        self.canvas.create_line(xr, yr, xr, yr + 15 * itemMini, fill="red", tags='rectMiniMap')
        self.canvas.create_line(xr, yr + 15 * itemMini, xr + 17 * itemMini, yr + 15 * itemMini, fill="red",
                                tags='rectMiniMap')
        self.canvas.create_line(xr + 17 * itemMini, yr, xr + 17 * itemMini, yr + 15 * itemMini, fill="red",
                                tags='rectMiniMap')

    def addBuildingToCursor(self,posX,posY):
        #self.buildingSprite =
        pass


    def resetSelection(self):
        """ Met la sélection à 0 (désélection
        """
        self.selected = []


    def detectSelected(self, x1, y1, x2, y2, units):
        """ Ajoute toutes les unités sélectionné dans le carré spécifié
        :param units: All the possible units
        :param x1: coord x du point haut gauche
        :param y1: coord y du point haut gauche
        :param x2: coord x du point bas droite
        :param y2: coord y du point bas droite
        """
        items = self.canvas.find_overlapping(x1, y1, x2, y2)
        for item in items:
            itemCoords = self.canvas.coords(item)
            itemCoord = (itemCoords[0] + self.sizeUnit / 2 + (self.positionX * self.item),
                         itemCoords[1] + self.sizeUnit / 2 + (self.positionY * self.item))
            for unit in units:
                if unit.x == itemCoord[0] and unit.y == itemCoord[1]:
                    self.selected.append(unit)  # Unité sélectionné








    def carreSelection(self, x1, y1, x2, y2):
        self.deleteSelectionSquare()
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='blue', tags='selection_square')

    def deleteSelectionSquare(self):
        self.canvas.delete('selection_square')





    def bindEvents(self):
        self.canvas.bind("<Button-2>", self.eventListener.onCenterClick)
        self.canvas.bind("<Button-3>", self.eventListener.onRClick)

        self.canvas.bind('<ButtonPress-1>', self.eventListener.onLPress)
        self.canvas.bind('<B1-Motion>', self.eventListener.onMouseMotion)
        self.canvas.bind('<ButtonRelease-1>', self.eventListener.onLRelease)

        self.root.protocol("WM_DELETE_WINDOW", self.eventListener.requestCloseWindow)


    def createBuildingFerme(self):
        self.eventListener.createBuilding(View.FERME)

    def createBuildingBaraque(self):
        self.eventListener.createBuilding(View.BARAQUE)

    def createBuildingHopital(self):
        self.eventListener.createBuilding(View.HOPITAL)

    def update(self, units, buildings, carte=None):

        self.canvas.delete('unit')

        # Draw Units
        if carte:
            # self.drawMinimap(units, carte)
            self.drawRectMiniMap()
            self.drawBuildings(buildings)


        self.drawMiniUnits(units)
        for unit in units:
            if self.isUnitShow(unit):
                img = unit.activeFrame
                if unit in self.selected:
                    img = unit.activeOutline,

                self.canvas.create_image((unit.x - self.sizeUnit / 2) - (self.positionX * self.item),
                                         (unit.y - self.sizeUnit / 2) - (self.positionY * self.item),
                                         anchor=NW,
                                         image=img,
                                         tags='unit')

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


    def isUnitShow(self, unit):
        x1 = self.positionX * self.item
        y1 = self.positionY * self.item
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


    def show(self):
        self.root.mainloop()

    def after(self, ms, func):
        self.root.after(ms, func)

    def destroy(self):
        self.root.destroy()


