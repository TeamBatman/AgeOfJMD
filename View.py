#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from tkinter import *  # Python 3
except ImportError:
    from Tkinter import *  # Python 2

from GuiAwesomeness import *


class View(GWindow):
    """ Responsable de l'affichage graphique et de captuer les entrées de l'usager"""

    def __init__(self, evListener):
        GWindow.__init__(self)


        # PARAMÈTRES DE BASE
        self.width = 1024
        self.height = 768
        self.root.geometry('%sx%s' % (self.width, self.height))
        self.root.configure(background='#2B2B2B')


        # ZONE DE DESSIN
        self.canvas = Canvas(self.root, width=self.width, height=self.height, background='#91BB62', bd=0,
                             highlightthickness=0)  # higlightthickness retire la bordure par défaut blanche des canvas
        self.canvas.pack()

        # LE HUD
        self.drawHUD()

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
        
        self.buttonFerme = GButton(self.canvas,"Ferme",self.createBuildingFerme,0)
        self.buttonFerme.draw(x=self.width - 225, y=280)
        self.buttonBaraque = GButton(self.canvas,"Baraque",self.createBuildingBaraque,2)
        self.buttonBaraque.draw(x=self.width - 225, y=335)
        self.buttonHopital = GButton(self.canvas,"Hopital",self.createBuildingHopital,2)
        self.buttonHopital.draw(x=self.width - 225, y=390)

        # LE PANEL DU BAS
        self.bottomPanel = GFrame(self.canvas, width=self.width - self.sidePanel.width, height=100)
        self.bottomPanel.draw(0, self.height - self.bottomPanel.height)

        self.moraleProg = GProgressBar(self.canvas, 150, "Morale")
        self.moraleProg.setProgression(63)
        self.moraleProg.draw(x=35, y=self.height - self.bottomPanel.height+25)




    def bindEvents(self):
        self.canvas.bind("<Button-1>", self.eventListener.onRClick)
        self.canvas.bind("<Button-3>", self.eventListener.onLClick)
        
    def createBuildingFerme(self):
        self.eventListener.createBuilding(0)
        
    def createBuildingBaraque(self):
        self.eventListener.createBuilding(1)
        
    def createBuildingHopital(self):
        self.eventListener.createbuilding(2)

    def update(self, units):
        self.canvas.delete('unit')
        # Draw Units
        if units:
            for unit in units:
                self.canvas.create_rectangle(unit.x, unit.y, unit.x + 32, unit.y + 32, fill='blue', tags='unit')

    def show(self):
        self.root.mainloop()

    def after(self, ms, func):
        self.root.after(ms, func)


