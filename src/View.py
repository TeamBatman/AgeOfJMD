#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from tkinter import *  # Python 3
except ImportError:
    from Tkinter import *  # Python 2

from GuiAwesomeness import *


class FrameSide():
    def __init__(self, canvas, largeurMinimap, hauteurMinimap):
        self.canvas = canvas

        self.width = largeurMinimap
        self.height = int(self.canvas.cget('height')) - hauteurMinimap

        self.x = int(self.canvas.cget('width')) - self.width
        self.y = hauteurMinimap

        self.frame = GFrame(self.canvas, width=self.width, height=self.height)


    def draw(self):
        self.frame.draw(self.x, self.y)


class FrameMiniMap():
    def __init__(self, canvas, eventListener):
        self.canvas = canvas
        self.eventListener = eventListener
        self.width = 250
        self.height = 250
        self.x = int(self.canvas.cget('width')) - self.width
        self.y = 0
        self.frame = GFrame(self.canvas, width=self.width, height=self.height)

        # TODO AJOUTER LA MINIMAP EN TANT QUE TELLE
        self.miniMapWidth = 200
        self.miniMapHeight = 200



        # TODO BINDER LES ÉVÉNEMENTS


    def draw(self):
        """ Dessine le CADRE de la minimap à l'écran
        """
        self.frame.draw(self.x, self.y)

    def updateMinimap(self, units, carte):
        """ Dessine toutes les composantes du cadre
        dans le cas présent la minimap
        """
        try:
            self.canvas.delete('miniMap')
        except Exception:
            pass

        margeX = int((self.width - self.miniMapWidth)/2)
        margeY = int((self.height - self.miniMapHeight)/2)
        print(margeX)
        x1 = self.x + margeX
        y1 = self.y + margeY
        x2 = self.x + self.miniMapWidth
        y2 = y1 + self.miniMapHeight

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

    def updateMiniUnits(self, units):
        try:
            self.canvas.delete('miniUnits')
        except:
            pass
        color = 'red'  # TODO METTRE LES COULEURS SELON LA CIVILISATION
        item = 2
        for unit in units:
            caseX, caseY = self.eventListener.controller.model.trouverCaseMatrice(unit.x, unit.y)
            x1 = self.width + (caseX * item)
            y1 = 18 + (caseY * item)
            x2 = x1 + item
            y2 = y1 + item
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags='miniUnits')


class FrameBottom():  # TODO COMPLETER
    def __init__(self, canvas, largeurMinimap):
        self.canvas = canvas
        self.width = int(self.canvas.cget('width')) - largeurMinimap
        self.height = 100

        self.x = 0
        self.y = int(self.canvas.cget('height')) - self.height

        self.frame = GFrame(self.canvas, width=self.width, height=self.height)





        # self.moraleProg = GProgressBar(self.canvas, 150, "Morale")
        #self.moraleProg.setProgression(63)
        #self.moraleProg.draw(x=self.bottomPanel.x + 35, y=self.height - self.bottomPanel.height + 25)


    def draw(self):
        """ Dessine le cadre
        """
        self.frame.draw(self.x, self.y)


class View(GWindow):
    """ Responsable de l'affichage graphique et de captuer les entrées de l'usager"""

    def __init__(self, evListener):
        GWindow.__init__(self)
        # TODO mettre une référence au parent

        # PARAMÈTRES DE BASE

        self.width = 1024
        self.height = 768
        self.selected = []  # Liste qui contient ce qui est selectionné

        self.root.geometry('%sx%s' % (self.width, self.height))
        self.root.configure(background='#2B2B2B')

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

        # GESTION ÉVÈNEMENTS
        self.eventListener = evListener  # Une Classe d'écoute d'évènement
        self.bindEvents()

        # LE HUD
        self.drawHUD()


    def drawHUD(self):
        """ Dessine la base du HUD
        """
        # LA MINIMAP
        self.frameMinimap = FrameMiniMap(self.canvas, self.eventListener)
        self.frameMinimap.draw()


        # LE CADRE DROIT
        self.frameSide = FrameSide(self.canvas, self.frameMinimap.width, self.frameMinimap.height)
        self.frameSide.draw()

        # LE CADRE DU BAS
        self.bottomFrame = FrameBottom(self.canvas, self.frameMinimap.width)
        self.bottomFrame.draw()


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

                if carte[x][y].type == 0:
                    couleur = "#0B610B"  # vert
                    # self.canvas.create_image(posX1, posY1,
                    #                         image=ImageTk.PhotoImage(GraphicsManager.get('Graphics/World/grass.png')))
                    #continue
                elif carte[x][y].type == 1:
                    # couleur = "#D7DF01" #jaune
                    couleur = "#BFBF00"
                elif carte[x][y].type == 2:
                    couleur = "#1C1C1C"  # gris pale
                elif carte[x][y].type == 3:
                    couleur = "#BDBDBD"  # gris fonce
                else:
                    couleur = "#2E9AFE"  # bleu
                self.canvas.create_rectangle(posX1, posY1, posX2, posY2, width=1, fill=couleur, tags='carte')


    def drawMinimap(self, units, carte):
        self.frameMinimap.updateMinimap(units, carte)


    def drawMiniUnits(self, units):
        self.frameMinimap.updateMiniUnits(units)


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
        self.eventListener.createBuilding(0)

    def createBuildingBaraque(self):
        self.eventListener.createBuilding(1)

    def createBuildingHopital(self):
        self.eventListener.createBuilding(2)

    def update(self, units, carte=None):

        self.canvas.delete('unit')

        # Draw Units
        if carte:
            # self.drawMinimap(units, carte)
            self.drawRectMiniMap()
            self.drawMap(carte)

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


