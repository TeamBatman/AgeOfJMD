#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'fireraccon A.K.A Jean-William Perreault'

from GuiAwesomeness.GWidgets import GWidget
from PIL import Image
from PIL import ImageTk

try:
    # Python2
    from Tkinter import NW
except ImportError:
    # Python3
    from tkinter import NW


class GButton(GWidget):
    """ Un bouton custom utilisant une image. A etre palcer sur un canvas"""

    # ÉTATS D'UN BOUTON
    NORMAL = 0
    PRESSED = 1
    FOCUS = 2
    EMPTY = 3

    # COULEURS
    BROWN = 0
    BEIGE = 1
    GREY = 2
    BLUE = 3

    def __init__(self, parent, text="", command=None, color=0):
        GWidget.__init__(self, parent)
        self.text = text
        self.command = command

        # Images
        self.imageData = {}
        self.textColor = "white"
        self._determineColor(color)

        # Image vide sur le dessus utilisée pour obtnie les événements de la souris (Event Monitor)
        self.graphImage = ImageTk.PhotoImage(self.imageData[GButton.NORMAL])
        self.eventMonitorImage = ImageTk.PhotoImage(self.imageData[GButton.EMPTY])

        # Tkitner Canvas Items
        self.eventMonitor = None
        self.btnItem = None

    def _determineColor(self, color):
        """ Détermine les images à utiliser en fonction de la couleur donnée
        :param color: la couleur (Constante de GButton)
        :return:
        """
        if color == GButton.BROWN:
            color = "brown"
        elif color == GButton.BEIGE:
            color = "beige"
        elif color == GButton.GREY:
            color = "grey"
            self.textColor = "black"
        elif color == GButton.BLUE:
            color = "blue"

        self.imageData[GButton.NORMAL] = Image.open("GuiAwesomeness/Gui/Buttons/buttonLong_%s.png" % color)
        self.imageData[GButton.PRESSED] = Image.open("GuiAwesomeness/Gui/Buttons/buttonLong_%s_pressed.png" % color)
        self.imageData[GButton.FOCUS] = Image.open('GuiAwesomeness/Gui/Buttons/buttonLong_focus.png')

        self.width, self.height = self.imageData[GButton.NORMAL].size
        self.imageData[GButton.EMPTY] = Image.new('RGBA', (self.width, self.height))

    def draw(self, x, y):
        self.btnItem = self.parent.create_image(x, y, image=self.graphImage, anchor=NW, tags=self.id)

        self.parent.create_text(x + 10, y + 12, text=self.text, anchor=NW, font="Arial", fill=self.textColor,
                                tags=self.id)

        self.eventMonitor = self.parent.create_image(x, y, image=self.eventMonitorImage, anchor=NW, tags=self.id)
        self._bindEvents()

    def drawState(self, state):
        """  Dessine le bouton en fonction de son état
        :param state: l'état du bouton à afficher (Constante de GButton)
        """
        if state == GButton.FOCUS:
            self.eventMonitorImage = ImageTk.PhotoImage(self.imageData[state])
            # self.parent.itemconfig(self.eventMonitor, image=self.eventMonitorImage)
        else:
            self.graphImage = ImageTk.PhotoImage(self.imageData[state])
            self.parent.itemconfig(self.btnItem, image=self.graphImage)

            self.eventMonitorImage = ImageTk.PhotoImage(self.imageData[GButton.EMPTY])
            self.parent.itemconfig(self.eventMonitor, image=self.eventMonitorImage)

    def _bindEvents(self):
        """ Lie les événements de la souris à l'EventMonitor (Moniteur événementiel)
        """
        # BIND EVENTS
        self.parent.tag_bind(self.eventMonitor, '<Enter>', self.onFocus)
        self.parent.tag_bind(self.eventMonitor, '<Leave>', self.onLeave)
        self.parent.tag_bind(self.eventMonitor, '<ButtonPress-1>', self.onClick)
        self.parent.tag_bind(self.eventMonitor, '<ButtonRelease-1>', self.onRelease)

    def onFocus(self, event):
        self.drawState(GButton.FOCUS)

    def onLeave(self, event):
        self.drawState(GButton.NORMAL)

    def onClick(self, event):
        self.drawState(GButton.PRESSED)

    def onRelease(self, event):
        self.drawState(GButton.NORMAL)
        self.drawState(GButton.FOCUS)
        if self.command:
            self.command()


class GMediumButton(GButton):
    def __init__(self, parent, text="", command=None, color=0, iconPath=None):
        super(GMediumButton, self).__init__(parent, text, command, color)

        self.imageData['ICON'] = Image.open(iconPath) if iconPath else Image.new('RGBA', (70, 70))
        self.imageData['ICON'].thumbnail((70, 70), Image.ANTIALIAS)
        self.icon = ImageTk.PhotoImage(self.imageData['ICON'])



    def _determineColor(self, color):
        self.imageData[GButton.NORMAL] = Image.open("GuiAwesomeness/Gui/Buttons/buttonSquare_med.png")
        self.imageData[GButton.PRESSED] = Image.open("GuiAwesomeness/Gui/Buttons/buttonSquare_med_pressed.png")
        self.imageData[GButton.FOCUS] = Image.open('GuiAwesomeness/Gui/Buttons/buttonSquare_focus.png')

        self.width, self.height = self.imageData[GButton.NORMAL].size
        self.imageData[GButton.EMPTY] = Image.new('RGBA', (self.width, self.height))

    def draw(self, x, y):
        self.btnItem = self.parent.create_image(x, y, image=self.graphImage, anchor=NW, tags=self.id)

        height, width = self.imageData["ICON"].size
        check_x = x + self.width / 2 - width / 2
        check_y = y + self.height / 2 - height / 2
        self.getCanvas().create_image(check_x, check_y, anchor=NW, image=self.icon, tags=self.id)

        self.eventMonitor = self.getCanvas().create_image(x, y, image=self.eventMonitorImage, anchor=NW, tags=self.id)
        self._bindEvents()


class GCheckButton(GButton):
    def __init__(self, parent, command=None, color=0):
        self.checkImage = None
        GButton.__init__(self, parent=parent, command=command, color=color)

    def _determineColor(self, color):
        color = "green"

        self.imageData[GButton.NORMAL] = Image.open("GuiAwesomeness/Gui/Buttons/buttonSquare_%s.png" % color)
        self.imageData[GButton.PRESSED] = Image.open("GuiAwesomeness/Gui/Buttons/buttonSquare_%s_pressed.png" % color)
        self.imageData[GButton.FOCUS] = Image.open('GuiAwesomeness/Gui/Buttons/buttonSquare_focus.png')

        self.imageData['ICON'] = Image.open('GuiAwesomeness/Gui/Icons/iconCheck.png')
        self.checkImage = ImageTk.PhotoImage(self.imageData['ICON'])

        self.width, self.height = self.imageData[GButton.NORMAL].size
        self.imageData[GButton.EMPTY] = Image.new('RGBA', (self.width, self.height))

    def draw(self, x, y):
        self.btnItem = self.parent.create_image(x, y, image=self.graphImage, anchor=NW, tags=self.id)

        height, width = self.imageData["ICON"].size
        check_x = x + self.width / 2 - width / 2
        check_y = y + self.height / 2 - height / 2
        self.parent.create_image(check_x, check_y, anchor=NW, image=self.checkImage, tags=self.id)

        self.eventMonitor = self.parent.create_image(x, y, image=self.eventMonitorImage, anchor=NW, tags=self.id)
        self._bindEvents()


class GCrossButton(GButton):
    def __init__(self, parent, command=None, color=0):
        self.checkImage = None
        GButton.__init__(self, parent=parent, command=command, color=color)

    def _determineColor(self, color):
        color = 'red'

        self.imageData[GButton.NORMAL] = Image.open('GuiAwesomeness/Gui/Buttons/buttonSquare_%s.png' % color)
        self.imageData[GButton.PRESSED] = Image.open('GuiAwesomeness/Gui/Buttons/buttonSquare_%s_pressed.png' % color)
        self.imageData[GButton.FOCUS] = Image.open("GuiAwesomeness/Gui/Buttons/buttonSquare_focus.png")

        self.imageData['ICON'] = Image.open('GuiAwesomeness/Gui/Icons/iconCross.png')
        self.checkImage = ImageTk.PhotoImage(self.imageData['ICON'])

        self.width, self.height = self.imageData[GButton.NORMAL].size
        self.imageData[GButton.EMPTY] = Image.new('RGBA', (self.width, self.height))

    def draw(self, x, y):
        self.btnItem = self.parent.create_image(x, y, image=self.graphImage, anchor=NW, tags=self.id)

        height, width = self.imageData['ICON'].size
        check_x = x + self.width / 2 - width / 2
        check_y = y + self.height / 2 - height / 2
        self.parent.create_image(check_x, check_y, anchor=NW, image=self.checkImage, tags=self.id)

        self.eventMonitor = self.parent.create_image(x, y, image=self.eventMonitorImage, anchor=NW, tags=self.id)
        self._bindEvents()


# TODO FIX THIS
class GCheckBox(GButton):
    """Un bouton custom utilisant une image. A etre palcer sur un canvas"""

    def __init__(self, parent, command=None, color=0):
        GButton.__init__(self, parent, None, command, color=color)
        self.width, self.height = self.imageData[GButton.NORMAL].size
        self.isChecked = False

    def _determineColor(self, color):
        if color == GButton.BROWN:
            color = "brown"
        elif color == GButton.BEIGE:
            color = "beige"
        elif color == GButton.BLUE:
            color = "blue"

        self.imageData[GButton.NORMAL] = Image.open('GuiAwesomeness/Gui/Buttons/buttonSquare_%s.png' % color)
        self.imageData[GButton.PRESSED] = Image.open('GuiAwesomeness/Gui/Buttons/buttonSquare_%s_pressed.png' % color)
        self.imageData[GButton.FOCUS] = Image.open('GuiAwesomeness/Gui/Buttons/buttonLong_focus.png')

    def onClick(self, event):
        self.isChecked = not self.isChecked
        if self.isChecked:
            self.drawState(GButton.NORMAL)
        else:
            self.drawState(GButton.PRESSED)