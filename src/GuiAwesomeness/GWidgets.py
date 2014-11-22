#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'fireraccon A.K.A Jean-William Perreault'

try:
    # Python2
    from Tkinter import Tk, NW, Canvas
except ImportError:
    # Python3
    from tkinter import Tk, NW, Canvas

from PIL import Image
from PIL import ImageTk


CURRENT_ID_INDEX = 0  # ID COUNTER USED FOR WIDGETS

class GWidget():
    """Base for all widgets"""

    def __init__(self, parent, x=0, y=0):
        self.id = GWidget.newID()
        self.parent = parent
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.children = []

    def addWidget(self, widget):
        """ Ajoute un Widget à la liste des widgets enfants.
        :param widget: le widget à ajouter
        """
        widget.parent = self
        self.children.append(widget)
        return self

    def getCanvas(self):
        """ Va remonter tous les parents jusqu'à trouver le Canvas
        :return: Canvas
        """
        p = self.parent
        while not isinstance(p, Canvas):
            p = p.parent
        return p




    def setPosition(self, x, y):
        """
        :param x: position en x
        :param y: position en y
        """
        self.x = x
        self.y = y

    def destroy(self):
        """ Détruit un widget (le ferme, le rend invisible)
        """
        self.parent.delete(self.id)
        for w in self.children:
            w.destroy()

    def draw(self, x, y):  # TODO Compléter Docstring
        """ Permet de dessiner le Widget à sa position x et y relativement à son parent
        Les valeurs par défaut xy(-1,-1) signifie que le widget sera d
        :param x: valeur position en x où dessiner
        :param y: valeur position en y où dessiner
        """
        # On s'assure qu'on essaie pas d'utiliser des paramètres de Canvas n'existant pas
        if isinstance(self.parent, Canvas):
            self.x = x
            self.y = y
        else: # On dessine en relatif
            print(x, y)
            self.x = self.parent.x + self.x
            self.y = self.parent.y + self.y


    def drawChildren(self):
        # Le positionnement des widgets enfants est relatif au parent
        for widget in self.children:
            widget.draw(self.x, self.y)




    @staticmethod
    def newID():
        """ Génère un identifiant unique à être attribué à un widget
        :return: str(identifiant unique)
        """
        global CURRENT_ID_INDEX
        str_id = "GID_%s" % CURRENT_ID_INDEX
        CURRENT_ID_INDEX += 1
        return str_id


class GWindow():
    """Une fenêtre Tkinter bien rudimentaire"""

    def __init__(self):
        self.root = Tk()

    def after(self, ms, func):
        """ Appelle une fonction après un certain temps

        :param ms: durée en millisecondes entre les appels de la fonction
        :param func: la fonction à appeler
        """
        self.root.after(ms, func)

    def afterCancel(self):
        """
        Annule un after
        """
        self.root.after_cancel()

    def show(self):
        """ Permet d'afficher la fenêtre
        """
        self.root.mainloop()


class GProgressBar(GWidget):
    """ Une barre de progression
    Pour le moment UNIQUEMENT l'orientation HORIZONTALE est fonctionnelle
    """
    # ORIENTATION
    HORIZONTAL = 0
    VERTICAL = 0

    # COLORS
    BLUE = 0
    GREEN = 1
    ORANGE = 3
    YELLOW = 4

    # IMAGES (PARTS)
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

    BACK_LEFT = 3
    BACK_MIDDLE = 4
    BACK_RIGHT = 5

    FULL = 6

    def __init__(self, parent, width, text="", progress=0, orientation=0, color=BLUE, x=0, y=0):
        GWidget.__init__(self, parent, x, y)
        self.width = width
        self.height = 0  # TODO DEFINE
        self.text = text
        self.imageData = {}
        self.graphImage = None
        self.subdivSize = 18  # The size of a part (ex 18x18 i.e. n x n)
        self.progress = progress
        self._determineImages(color, orientation)
        # Determine Height
        width, height = self.imageData[GProgressBar.MIDDLE].size
        self.height = 2 * height

        self._buildFullImage()

    def setProgression(self, progress):
        """
        Completion sur 100
        :param pourcentage:
        """
        if progress <= 100:
            self.progress = progress
            self._buildFullImage()

    def _determineImages(self, color, orientation):
        """ Détermine l'image à utiliser selon la couleur de l'objet
        :param color: couleur désirée pour l'objet
        """
        if color == GProgressBar.BLUE:
            color = 'Blue'
        elif color == GProgressBar.GREEN:
            color = 'Green'
        elif color == GProgressBar.ORANGE:
            color = 'Orange'
        elif color == GProgressBar.YELLOW:
            color = 'Yellow'

        if orientation == GProgressBar.HORIZONTAL:
            orientation = 'horizontal'
        elif orientation == GProgressBar.VERTICAL:
            orientation = 'vertical'

        self.imageData[GProgressBar.LEFT] = Image.open(
            'GuiAwesomeness/Gui/ProgressBars/bar%s_%sLeft.png' % (color, orientation))
        self.imageData[GProgressBar.MIDDLE] = Image.open(
            'GuiAwesomeness/Gui/ProgressBars/bar%s_%sMid.png' % (color, orientation))
        self.imageData[GProgressBar.RIGHT] = Image.open(
            'GuiAwesomeness/Gui/ProgressBars/bar%s_%sRight.png' % (color, orientation))

        self.imageData[GProgressBar.BACK_LEFT] = Image.open(
            'GuiAwesomeness/Gui/ProgressBars/barBack_%sLeft.png' % orientation)

        self.imageData[GProgressBar.BACK_MIDDLE] = Image.open(
            'GuiAwesomeness/Gui/ProgressBars/barBack_%sMid.png' % orientation)

        self.imageData[GProgressBar.BACK_RIGHT] = Image.open(
            'GuiAwesomeness/Gui/ProgressBars/barBack_%sRight.png' % orientation)

    def _adjustSubdivToSize(self):
        """Ajuste la subdivision pour s'addapter à la taille de l'objet.
        Fondamentalement, la fonction cherche le diviseur le plus près
        de la valeur de subDiv de la taille
        """
        sub = self.subdivSize
        isOK = False
        while not isOK:
            isOK = self.width % sub == 0
            if not isOK:
                sub -= 1
        return sub

    def _buildFullImage(self):
        """ Construit l'image complète selon les paramètres
        actuels de l'objet
        """
        # CREATE IMAGE FROM HEIGHT AND WIDTH
        finalImage = Image.new("RGBA", (self.width, int(self.height / 2)))

        # FIND SUBDIVISION FOR SIZE
        sub = self._adjustSubdivToSize()

        # 1. On remplie l'espace du "Back"
        for x in range(0, int(self.width / sub)):
            finalImage.paste(self.imageData[GProgressBar.BACK_MIDDLE], (x * sub - self.subdivSize, 0))

        finalImage.paste(self.imageData[GProgressBar.BACK_LEFT], (0, 0))
        finalImage.paste(self.imageData[GProgressBar.BACK_RIGHT], (self.width - 19, 0))



        # 2. On remplie l'espace du "Back"
        progress = self.progress * self.width / 100
        if self.progress > 5:
            for x in range(0, int(progress / sub)):
                posX = x * sub - self.subdivSize
                finalImage.paste(self.imageData[GProgressBar.MIDDLE], (x * sub - self.subdivSize, 0))
                finalImage.paste(self.imageData[GProgressBar.RIGHT], (x * sub - self.subdivSize + 18, 0),
                                 self.imageData[GProgressBar.RIGHT])
                if posX <= 9:
                    finalImage.paste(self.imageData[GProgressBar.LEFT], (0, 0))

        self.imageData[GProgressBar.FULL] = finalImage
        self.graphImage = ImageTk.PhotoImage(self.imageData[GProgressBar.FULL])

    def draw(self, x, y):
        GWidget.draw(self, x, y)
        self.getCanvas().delete(self.id)
        self.parent.create_text(x, y, text=self.text, anchor=NW, font="Helvetica",
                                fill="#575246", tags=self.id)
        self.parent.create_image(x, y + self.height / 2 + 5, image=self.graphImage, anchor=NW, tags=self.id)

    def update(self):
        """ Met la progress bar à jour (redessine la progress bar)
        """
        self.getCanvas().delete(self.id)
        self.draw(self.x, self.y)


class GLabel(GWidget):
    def __init__(self, parent, text="", color="", x=0, y=0):
        """ Permet d'afficher du texte (Label)
        :param parent: le parent de l'objet
        :param text:
        :param color:
        """
        super(GLabel, self).__init__(parent, x, y)
        self.color = color
        self.text = text


    def draw(self, x, y):
        super(GLabel, self).draw(x, y)
        self.getCanvas().create_text(self.x, self.y, text=self.text, anchor=NW, font="Helvetica", fill=self.color,
                                tags=self.id)