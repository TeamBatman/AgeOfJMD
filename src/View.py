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


        # LA MINIMAP
        self.miniMapWidth = 211
        self.miniMapHeight = 211

        self.minimapMargeX = int((self.width - self.miniMapWidth) / 2)
        self.minimapMargeY = int((self.height - self.miniMapHeight) / 2)

        self.miniMapX = self.x + self.minimapMargeX
        self.miniMapY = self.y + self.minimapMargeY

        self.regionEcouteImage = ImageTk.PhotoImage(Image.new('RGBA', (self.miniMapWidth, self.miniMapHeight)))
        self.regionEcoute = self.canvas.create_image(self.miniMapX, self.miniMapY,
                                                     image=self.regionEcouteImage, anchor=NW)


    def bindEvents(self):
        self.canvas.tag_bind(self.regionEcoute, '<ButtonPress-1>', self.eventListener.onMinimapLPress)
        self.canvas.tag_bind(self.regionEcoute, '<B1-Motion>', self.eventListener.onMinimapMouseMotion)

    def draw(self):
        """ Dessine le CADRE de la minimap à l'écran
        """
        self.frame.draw(self.x, self.y)

    def updateMinimap(self, carte):
        """ Dessine toutes les composantes du cadre
        dans le cas présent la minimap
        """
        try:
            self.canvas.delete('miniMap')
        except Exception:
            pass

        x1 = self.miniMapX
        y1 = self.miniMapY
        x2 = x1 + self.miniMapWidth
        y2 = y1 + self.miniMapHeight

        size = 106
        itemMini = 2  # La grandeur des cases pour la minimap
        for x in range(0, size):
            for y in range(0, size):
                posX1 = x1 + x * itemMini
                posY1 = y1 + y * itemMini
                posX2 = posX1 + itemMini
                posY2 = posY1 + itemMini

                couleurs = {
                    0: "#0B610B",  # vert
                    1: "#BFBF00",  # jaune
                    2: "#1C1C1C",  # gris pale
                    3: "#BDBDBD",  # gris fonce
                    4: "#2E9AFE"  # bleu
                }
                couleur = couleurs[carte[x][y].type]
                self.canvas.create_rectangle(posX1, posY1, posX2, posY2, width=0, fill=couleur, tags='miniMap')
        self.canvas.tag_raise(self.regionEcoute)

    def updateMiniUnits(self, units):
        """ Dessine les unités à l'écran
        :param units: les unités
        :return:
        """
        try:
            self.canvas.delete('miniUnits')
        except:
            pass
        color = 'red'  # TODO METTRE LES COULEURS SELON LA CIVILISATION
        item = 2
        for unit in units:
            caseX, caseY = self.eventListener.controller.model.trouverCaseMatrice(unit.x, unit.y)
            x1 = self.miniMapX + (caseX * item)
            y1 = self.minimapMargeY + (caseY * item)
            x2 = x1 + item
            y2 = y1 + item
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags='miniUnits')


    def drawRectMiniMap(self, positionCameraX, positionCameraY):
        """ Dessine le rectangle de caméra de la minimap
        :param positionCameraX: position de la caméra en X
        :param positionCameraY: position de la caméra en Y
        :return:
        """
        self.canvas.delete('rectMiniMap')

        itemMini = 2  # La grandeur des cases pour la minimap
        xr = self.miniMapX + positionCameraX * itemMini
        yr = self.miniMapY + positionCameraY * itemMini

        self.canvas.create_rectangle(xr, yr, xr + 17 * itemMini, yr + 15 * itemMini, outline='red', tags='rectMiniMap')


class FrameBottom():  # TODO COMPLETER
    def __init__(self, canvas, largeurMinimap):
        self.canvas = canvas
        self.width = int(self.canvas.cget('width')) - largeurMinimap
        self.height = 100

        self.x = 0
        self.y = int(self.canvas.cget('height')) - self.height

        self.frame = GFrame(self.canvas, width=self.width, height=self.height)





        # self.moraleProg = GProgressBar(self.canvas, 150, "Morale")
        # self.moraleProg.setProgression(63)
        #self.moraleProg.draw(x=self.bottomPanel.x + 35, y=self.height - self.bottomPanel.height + 25)


    def draw(self):
        """ Dessine le cadre
        """
        self.frame.draw(self.x, self.y)


class Carte():
    def __init__(self, canvas, eventListener, largeurEcran, hauteurEcran, largeurCadreDroit, hauteurCadreBas):
        self.canvas = canvas
        self.eventListener = eventListener

        self.width = largeurEcran - largeurCadreDroit
        self.height = hauteurEcran - hauteurCadreBas


        # CASES
        self.sizeUnit = 32  # Taille des unités
        self.item = 48  # Grandeur d'un bloc (Carte)
        # Nombre de cases Visibles en X et En Y
        self.nbCasesX = 16
        self.nbCasesY = 14

        # Position de la caméra
        self.cameraX = 0
        self.cameraY = 0

        self.regionEcouteImage = ImageTk.PhotoImage(Image.new('RGBA', (self.width, self.height)), 'black')
        self.regionEcoute = self.canvas.create_image(0, 0, image=self.regionEcouteImage, anchor=NW)

    def bindEvents(self):
        """ Lis les événements à la carte
        """
        self.canvas.tag_bind(self.regionEcoute, '<Button-2>', self.eventListener.onMapCenterClick)
        self.canvas.tag_bind(self.regionEcoute, '<Button-3>', self.eventListener.onMapRClick)

        self.canvas.tag_bind(self.regionEcoute, '<ButtonPress-1>', self.eventListener.onMapLPress)
        self.canvas.tag_bind(self.regionEcoute, '<B1-Motion>', self.eventListener.onMapMouseMotion)
        self.canvas.tag_bind(self.regionEcoute, '<ButtonRelease-1>', self.eventListener.onMapLRelease)






    def draw(self, carte):
        """ Affiche la carte à l'écran
        :param carte: la carte
        """
        x1 = self.cameraX
        y1 = self.cameraY
        x2 = self.width
        y2 = self.height

        for x in range(x1, x1 + self.nbCasesX):
            for y in range(y1, y1 + self.nbCasesY):
                posX1 = 0 + (x - x1) * self.item
                posY1 = 0 + (y - y1) * self.item
                posX2 = posX1 + self.item
                posY2 = posY1 + self.item

                couleurs = {
                    0: "#0B610B",  # vert
                    1: "#BFBF00",  # jaune
                    2: "#1C1C1C",  # gris pale
                    3: "#BDBDBD",  # gris fonce
                    4: "#2E9AFE"  # bleu
                }
                couleur = couleurs[carte[x][y].type]

                """
                if carte[x][y].type == 0:
                    couleur = "#0B610B"  # vert
                    # self.canvas.create_image(posX1, posY1,
                    # image=ImageTk.PhotoImage(GraphicsManager.get('Graphics/World/grass.png')))
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
                """
                self.canvas.create_rectangle(posX1, posY1, posX2, posY2, width=1, fill=couleur, tags='carte')
        self.canvas.tag_lower('carte')
        self.canvas.tag_raise(self.regionEcoute)


    def drawUnits(self, units, selectedUnits):
        """ Dessine les unités dans la map
        :param selectedUnits: une liste des unités sélectionnées
        :param units: une liste d'unités
        """
        for unit in units:
            if self.isUnitShow(unit):
                img = unit.activeOutline if unit in selectedUnits else unit.activeFrame
                posX = (unit.x - self.sizeUnit / 2) - (self.cameraX * self.item)
                posY = (unit.y - self.sizeUnit / 2) - (self.cameraY * self.item)
                self.canvas.create_image(posX, posY, anchor=NW, image=img, tags='unit')

    def isUnitShow(self, unit):
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

    def __init__(self, evListener):
        GWindow.__init__(self)
        # TODO mettre une référence au parent

        # PARAMÈTRES DE BASE

        self.width = 1024
        self.height = 768
        self.selected = []  # Liste qui contient ce qui est selectionné

        self.root.geometry('%sx%s' % (self.width, self.height))
        self.root.configure(background='#2B2B2B')

        # ZONE DE DESSIN
        self.canvas = Canvas(self.root, width=self.width, height=self.height, background='#91BB62', bd=0,
                             highlightthickness=0)  # higlightthickness retire la bordure par défaut blanche des canvas
        self.canvas.pack()


        # Position de la Caméra
        self.positionX = 0
        self.positionY = 0

        # GESTION ÉVÈNEMENTS
        self.eventListener = evListener  # Une Classe d'écoute d'évènement

        # LE HUD
        self.drawHUD()
        self.carte = Carte(self.canvas, evListener, self.width, self.height, self.frameSide.width, self.frameBottom.height)

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
        self.carte.drawUnits(units, self.selected)


    def drawMinimap(self, carte):
        """ Permet de dessiner la carte
        :param carte: la carte
        """
        self.frameMinimap.updateMinimap(carte)

    def drawMiniUnits(self, units):
        """ Permet de dessiner les unités sur la minimap
        :param units:
        """
        self.frameMinimap.updateMiniUnits(units)


    def drawRectMiniMap(self):
        """ Permet de dessiner la caméra de la minimap
        """
        self.frameMinimap.drawRectMiniMap(self.positionX, self.positionY)


    def resetSelection(self):
        """ Met la sélection à 0 (désélection)
        """
        self.selected = []


    def detectSelected(self, x1, y1, x2, y2, units):
        """ Ajoute toutes les unités sélectionné dans le rectangle spécifié
        :param units: All the possible units
        :param x1: coord x du point haut gauche
        :param y1: coord y du point haut gauche
        :param x2: coord x du point bas droite
        :param y2: coord y du point bas droite
        """
        items = self.canvas.find_overlapping(x1, y1, x2, y2)
        for item in items:
            itemCoords = self.canvas.coords(item)
            itemCoord = (itemCoords[0] + self.carte.sizeUnit / 2 + (self.carte.cameraX * self.carte.item),
                         itemCoords[1] + self.carte.sizeUnit / 2 + (self.carte.cameraY * self.carte.item))
            for unit in units:
                if unit.x == itemCoord[0] and unit.y == itemCoord[1]:
                    self.selected.append(unit)  # Unité sélectionné


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

        self.frameMinimap.bindEvents()
        self.carte.bindEvents()



        self.root.protocol("WM_DELETE_WINDOW", self.eventListener.onCloseWindow)


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
        self.drawUnits(units)




    def show(self):
        """ Affiche la fenêtre de jeu à l'écran
        """
        self.root.mainloop()

    def after(self, ms, func):
        self.root.after(ms, func)

    def destroy(self):
        """ Détruit la fenêtre de jeu
        """
        self.root.destroy()


