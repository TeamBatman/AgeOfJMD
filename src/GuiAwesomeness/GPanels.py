#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'fireraccon A.K.A Jean-William Perreault'

from PIL import Image
from PIL import ImageTk

from GuiAwesomeness.GWidgets import GWidget


try:
    # Python2
    from Tkinter import NW
except ImportError:
    # Python3
    from tkinter import NW


class GPanel(GWidget):
    """ Un panneau
    """
    # COULEURS
    BROWN = 0
    BEIGE = 1
    BEIGE_LIGHT = 2
    BLUE = 3

    # SOUS-PARTIES
    BASE = 0  # Représente l'image de base
    TOP_LEFT = 1
    TOP_CENTER = 2
    TOP_RIGHT = 3

    LEFT = 4
    CENTER = 5
    RIGHT = 6

    BOTTOM_LEFT = 7
    BOTTOM_CENTER = 8
    BOTTOM_RIGHT = 9

    FULL = 10  # L'image construite finale

    def __init__(self, parent, width, height, color=0, x=0, y=0):
        GWidget.__init__(self, parent, x, y)
        self.width = width   # Doit être un multiple de subdivise  Size
        self.height = height
        self.graphImage = None  # L'image à afficher (tkinter PhotoImage)
        # Image Data
        self.subdivSize = 32  # La taille d'une partie (ex 32x32 i.e. n x n)
        self.imageData = {}

        self._determineBaseImage(color)
        self._subdivideBaseImage()
        self._buildFullImage()

    def _subdivideBaseImage(self):
        """ Subdivise l'image principale en parties plus petites
        """
        # Sub Images
        self.imageData[GPanel.TOP_LEFT] = self.imageData[GPanel.BASE].crop(
            (0, 0, self.subdivSize, self.subdivSize))

        self.imageData[GPanel.TOP_CENTER] = self.imageData[GPanel.BASE].crop(
            (10, 0, 10 + self.subdivSize, 0 + self.subdivSize))

        self.imageData[GPanel.TOP_RIGHT] = self.imageData[GPanel.BASE].crop(
            (100 - self.subdivSize, 0, 100, self.subdivSize))

        self.imageData[GPanel.LEFT] = self.imageData[GPanel.BASE].crop(
            (0, self.subdivSize, self.subdivSize, self.subdivSize * 2))

        self.imageData[GPanel.CENTER] = self.imageData[GPanel.BASE].crop(
            (50, 50, 50 + self.subdivSize, 50 + self.subdivSize))

        self.imageData[GPanel.RIGHT] = self.imageData[GPanel.BASE].crop(
            (100 - self.subdivSize, self.subdivSize, 100, self.subdivSize * 2))

        self.imageData[GPanel.BOTTOM_LEFT] = self.imageData[GPanel.BASE].crop(
            (0, 100 - self.subdivSize, self.subdivSize, 100))

        self.imageData[GPanel.BOTTOM_CENTER] = self.imageData[GPanel.BASE].crop(
            (50, 100 - self.subdivSize, 50 + self.subdivSize, 100))

        self.imageData[GPanel.BOTTOM_RIGHT] = self.imageData[GPanel.BASE].crop(
            (100 - self.subdivSize, 100 - self.subdivSize, 100, 100))

    def _determineBaseImage(self, color):
        """ Détermine l'image de base à utiliser à l'aide du param couleur
        :param color: la couleur
        :return:
        """
        if color == GPanel.BROWN:
            img = Image.open('GuiAwesomeness/Gui/Panels/panel_brown.png')
        elif color == GPanel.BEIGE:
            img = Image.open('GuiAwesomeness/Gui/Panels/panel_beige.png')
        elif color == GPanel.BEIGE_LIGHT:
            img = Image.open('GuiAwesomeness/Gui/Panels/panel_beigeLight.png')
        elif color == GPanel.BLUE:
            img = Image.open('GuiAwesomeness/Gui/Panels/panel_blue.png')

        self.imageData[GPanel.BASE] = img

    def _adjustSubdivToSize(self):
        """ Adjust the subdivision to fit the size
        Basically it just looks for the greatest common divisor (GCD)
        of width and height starting with the object's subdivSize
        """
        sub = self.subdivSize
        isOK = False
        while not isOK:
            isOK = self.height % sub == 0
            if isOK:
                isOK = self.width % sub == 0
            if not isOK:
                sub -= 1
        return sub

    def _buildFullImage(self):
        """ Construit une image d'un panneau selon la largeur et la hauteur
        """
        # CREATE IMAGE FROM HEIGHT AND WIDTH
        finalImage = Image.new("RGBA", (self.width, self.height))

        # FIND SUBDIVISION FOR SIZE
        sub = self._adjustSubdivToSize()

        # 1. On remplie le panel ainsi que les 4 cotes
        for x in range(0, int(self.width/sub)):
            for y in range(0, int(self.height/sub)):
                if y == 0:
                    finalImage.paste(self.imageData[GPanel.TOP_CENTER], (x * sub-self.subdivSize, y))

                elif y == self.height/sub-1:  # TODO
                    finalImage.paste(self.imageData[GPanel.BOTTOM_CENTER], (x * sub, self.height - self.subdivSize))
                elif x == 0:
                    finalImage.paste(self.imageData[GPanel.LEFT], (x * sub, y * sub))

                elif x == self.width/sub - 1:
                    finalImage.paste(self.imageData[GPanel.RIGHT], (self.width-self.subdivSize, y * sub))

                else:
                    finalImage.paste(self.imageData[GPanel.CENTER], (x * sub, y * sub))

        # 3. On fait les 4 coins
        finalImage.paste(self.imageData[GPanel.TOP_LEFT], (0, 0))
        finalImage.paste(self.imageData[GPanel.TOP_RIGHT], (self.width - self.subdivSize, 0))

        finalImage.paste(self.imageData[GPanel.BOTTOM_LEFT], (0, self.height - self.subdivSize))
        finalImage.paste(self.imageData[GPanel.BOTTOM_RIGHT],
                         (self.width - self.subdivSize, self.height - self.subdivSize))
        self.imageData[GPanel.FULL] = finalImage
        self.graphImage = ImageTk.PhotoImage(self.imageData[GPanel.FULL])

    def draw(self, x, y):
        GWidget.draw(self, x, y)
        self.parent.create_image(self.x, self.y, image=self.graphImage, anchor=NW, tags=(self.id, 'GMenu'))
        GWidget.drawChildren(self)


class GPanelInset(GPanel):
    """ Un encart, utile pour mettre à l'intérieur d'un panel
    """
    def __init__(self, parent, width, height, color=0, x=0, y=0):
        GPanel.__init__(self, parent, width, height, color=color, x=0, y=0)

    def _determineBaseImage(self, color):
        """ Détermine l'image à utiliser selon la couleur spécifiée
        :param color: la couleur à utiliser (Constantes Couleur de GPanel)
        """
        if color == GPanel.BROWN:
            img = Image.open('GuiAwesomeness/Gui/Panels/panelInset_brown.png')
        if color == GPanel.BEIGE:
            img = Image.open('GuiAwesomeness/Gui/Panels/panelInset_beige.png')
        if color == GPanel.BEIGE_LIGHT:
            img = Image.open('GuiAwesomeness/Gui/Panels/panelInset_beigeLight.png')
        if color == GPanel.BLUE:
            img = Image.open('GuiAwesomeness/Gui/Panels/panelInset_blue.png')

        self.imageData[GPanel.BASE] = img


class GFrame(GPanel):
    """ Un cadre avec un encart centré en son centre.
    Fondamentalement un GPanel plus un GPanelInset
    """

    def __init__(self, parent, width, height, color=0, x=0, y=0):
        GPanel.__init__(self, parent, width, height, color=color, x=0, y=0)

        self.margin = 15    # Marge en pixel entre la panel et son inset
        insetColor = self._determineInsetColor(color)
        insetWidth, insetHeight = self._determineInsetSize()

        self.panelInset = GPanelInset(parent, insetWidth, insetHeight, insetColor)

    def _determineInsetColor(self, color):
        """ Détermine la couleur à utiliser pour l'encart en fonction de la couleur du panneau
        (de sorte qu'ils s'agencent bien ensemble)
        :param color: the main panel color
        :return: la couleur du inset
        """
        if color == GPanel.BROWN:
            return GPanel.BEIGE

        elif color == GPanel.BEIGE:
            return GPanel.BEIGE_LIGHT

        elif color == GPanel.BEIGE_LIGHT:
            return GPanel.BROWN  # TODO see if it looks good

        elif color == GPanel.BLUE:
            return GPanel.BEIGE_LIGHT  # TODO see if it looks good

    def _determineInsetSize(self):
        """ Détermine la taille de l'encart selon celle du parent. De sorte
        à ce que l'encart soit bien centré
        :return:
        """
        insetWidth = self.width - self.margin * 2
        insetHeight = self.height - self.margin * 2
        return insetWidth, insetHeight

    def draw(self, x, y):
        GPanel.draw(self, x, y)
        # DRAW INSET
        insetX = 1 + x + self.margin
        insetY = 1 + y + self.margin
        self.panelInset.draw(insetX, insetY)
        GWidget.drawChildren(self)

    def destroy(self):
        self.panelInset.destroy()
        GPanel.destroy(self)
