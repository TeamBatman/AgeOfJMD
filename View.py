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
        
        self.buttonFerme = GMediumButton(self.canvas,None,self.createBuildingFerme, GButton.BROWN)
        self.buttonFerme.draw(x=self.width - 222, y=280)
        im = Image.open("GuiAwesomeness/Gui/Buttons_Sprite/Farm.png")
        im.thumbnail((70,70), Image.ANTIALIAS)
        self.imtk = ImageTk.PhotoImage(im)
        self.canvas.create_image(self.width - 212, 285, anchor=NW,image=self.imtk)
        self.buttonBaraque = GMediumButton(self.canvas,"Baraque",self.createBuildingBaraque, GButton.GREY)
        self.buttonBaraque.draw(x=self.width - 123, y=280)
        self.buttonHopital = GMediumButton(self.canvas,"Hopital",self.createBuildingHopital, GButton.GREY)
        self.buttonHopital.draw(x=self.width - 222, y=390)

        # LE PANEL DU BAS
        self.bottomPanel = GFrame(self.canvas, width=self.width - self.sidePanel.width, height=100)
        self.bottomPanel.draw(0, self.height - self.bottomPanel.height)

        self.moraleProg = GProgressBar(self.canvas, 150, "Morale")
        self.moraleProg.setProgression(63)
        self.moraleProg.draw(x=35, y=self.height - self.bottomPanel.height+25)




    def bindEvents(self):
        self.canvas.bind("<Button-1>", self.eventListener.onLClick)
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
                self.canvas.create_rectangle(unit.x, unit.y, unit.x + 32, unit.y + 32, fill='blue', tags='unit')

    def show(self):
        self.root.mainloop()

    def after(self, ms, func):
        self.root.after(ms, func)
        
    def destroy(self):
        self.root.destroy()


