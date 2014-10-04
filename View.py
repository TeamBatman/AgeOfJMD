#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from tkinter import *  # Python 3
except ImportError:
    from Tkinter import *  # Python 2

from GuiAwesomeness import *
from PIL import Image
from PIL import ImageTk


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
        self.multiplicateur = 32
        self.grandeurCanevas = 768
        self.sizeUnit = 32

        # ZONE DE DESSIN
        self.canvas = Canvas(self.root, width=self.width, height=self.height, background='#91BB62', bd=0,
                             highlightthickness=0)  # higlightthickness retire la bordure par défaut blanche des canvas
        self.canvas.pack()

        # LE HUD
        self.drawHUD()

        #self.afficherLigne()

        # GESTION ÉVÈNEMENTS
        self.eventListener = evListener  # Une Classe d'écoute d'évènement
        self.drawRessources()
        self.bindEvents()

    def afficherLigne(self):
        # verticales
        for i in range(1, self.grandeurCanevas):
            self.canvas.create_line(i * self.multiplicateur, 0, i * self.multiplicateur,
                                    self.grandeurCanevas * self.multiplicateur)
        # horizontales
        for i in range(1, self.grandeurCanevas):
            self.canvas.create_line(0, i * self.multiplicateur, self.grandeurCanevas * self.multiplicateur,
                                    i * self.multiplicateur)

    def drawRessources(self):
        matrice = self.eventListener.controller.model.carte.matrice
        for i in range(0, self.eventListener.controller.model.carte.size):
            for j in range(0, self.eventListener.controller.model.carte.size):
                if not matrice[i][j].type == 0:
                    self.canvas.create_rectangle(i * self.multiplicateur, j * self.multiplicateur,
                                                 i * self.multiplicateur + 32, j * self.multiplicateur + 32,
                                                 fill="yellow", tags='ressource')

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

    def selection(self):
        print("selection")
        self.selected = []  # Déselection
        item = self.canvas.find_withtag(CURRENT)
        if item:  # Si on a cliqué sur quelque chose
            itemCoords = self.canvas.coords(item)
            itemCoord = (itemCoords[0] + self.sizeUnit / 2, itemCoords[1] + self.sizeUnit / 2)
            for unit in self.eventListener.controller.model.units:
                if unit.x == itemCoord[0] and unit.y == itemCoord[1]:
                    self.selected.append(unit)  # Unité sélectionné
                    break

    def bindEvents(self):
        self.canvas.bind("<Button-1>", self.eventListener.onLClick)
        self.canvas.bind("<Button-2>", self.eventListener.onCenterClick)
        self.canvas.bind("<Button-3>", self.eventListener.onRClick)
        self.root.protocol("WM_DELETE_WINDOW", self.eventListener.requestCloseWindow)

    def createBuildingFerme(self):
        self.eventListener.createBuilding(0)

    def createBuildingBaraque(self):
        self.eventListener.createBuilding(1)

    def createBuildingHopital(self):
        self.eventListener.createBuilding(2)

    def update(self, units):
        self.canvas.delete('unit')

        # Draw Units
        if units:
            for unit in units:
                color = 'blue'
                if unit in self.selected:
                    color = 'red'  # Unité sélectionné
                self.canvas.create_rectangle(unit.x - self.sizeUnit / 2, unit.y - self.sizeUnit / 2,
                                             unit.x + self.sizeUnit / 2, unit.y + self.sizeUnit / 2, fill=color,
                                             tags='unit')

    def show(self):
        self.root.mainloop()

    def after(self, ms, func):
        self.root.after(ms, func)

    def destroy(self):
        self.root.destroy()


