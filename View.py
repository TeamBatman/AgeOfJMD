#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from tkinter import *  # Python 3
except ImportError:
    from Tkinter import *  # Python 2

from GuiAwesomeness import *
from Tuile import *


class View(GWindow):
    """ Responsable de l'affichage graphique et de captuer les entrées de l'usager"""

    def __init__(self, evListener):
        GWindow.__init__(self)


        # PARAMÈTRES DE BASE
        self.width = 1020
        self.height = 772
        self.root.geometry('%sx%s' % (self.width, self.height))
        self.root.configure(background='#2B2B2B')


        # ZONE DE DESSIN
        self.canvas = Canvas(self.root, width=self.width, height=self.height, background='#91BB62', bd=0,
                             highlightthickness=0)  # higlightthickness retire la bordure par défaut blanche des canvas
        self.canvas.pack()
        # Position de la fenetre
        self.positionX = 0
        self.positionY = 0

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

    def drawMap(self, carte):
        if 'carte' in self.canvas.find_all():
            self.canvas.delete('carte')
        x1 = self.positionX
        y1 = self.positionY
        x2 = self.width-250
        y2 = self.height-100

        item = 48
        #self.canvas.create_rectangle(x1,y1,x2,y2, fill="blue")

        for x in range(x1,x1+16):
            for y in range(y1,y1+14):
                posX1 = 0+(x-x1)*item
                posY1 = 0+(y-y1)*item
                posX2 = posX1+item
                posY2 = posY1+item

                if carte[x][y].type == 0:
                    couleur = "#0B610B" #vert
                elif carte[x][y].type == 1:
                    #couleur = "#D7DF01" #jaune
                    couleur = "#BFBF00"
                elif carte[x][y].type == 2:
                    couleur = "#1C1C1C" #gris pale
                elif carte[x][y].type == 3:
                    couleur = "#BDBDBD" #gris fonce
                else:
                    couleur = "#2E9AFE" #bleu
                self.canvas.create_rectangle(posX1,posY1,posX2,posY2,width=1,fill=couleur, tags='carte')



    def drawMinimap(self, units, carte):
        if 'miniMap' in self.canvas.find_all():
            self.canvas.delete('miniMap')
        x1 = self.width - 233
        y1 = 18
        x2 = self.width - 22
        y2 = y1 + 211

        size = 106
        item = 2
        #self.canvas.create_rectangle(x1,y1,x2,y2, fill="blue", tags='miniMap')

        for x in range(0,size):
            for y in range(0,size):

                posX1 = x1+x*item
                posY1 = y1+y*item
                posX2 = posX1+item
                posY2 = posY1+item

                if carte[x][y].type == 0:
                    couleur = "#0B610B" #vert
                elif carte[x][y].type == 1:
                    #couleur = "#D7DF01" #jaune
                    couleur = "#BFBF00"
                elif carte[x][y].type == 2:
                    couleur = "#1C1C1C" #gris pale
                elif carte[x][y].type == 3:
                    couleur = "#BDBDBD" #gris fonce
                else:
                    couleur = "#2E9AFE" #bleu
                self.canvas.create_rectangle(posX1,posY1,posX2,posY2,width=0,fill=couleur, tags='miniMap')

        #self.canevasJeu.create_line(event.x-13*self.mCaisse,event.y-10*self.mCaisse, event.x+13*self.mCaisse,event.y-10*self.mCaisse,width=2,fill="white")
  		
        xr = x1+self.positionX*item
        yr = y1+self.positionY*item

        self.canvas.create_line(xr,yr,xr+17*item,yr,fill="red")
        self.canvas.create_line(xr,yr,xr,yr+15*item,fill="red")
        self.canvas.create_line(xr,yr+15*item,xr+17*item,yr+15*item,fill="red")
        self.canvas.create_line(xr+17*item,yr,xr+17*item,yr+15*item,fill="red")


        self.drawMap(carte)



    def bindEvents(self):
        self.canvas.bind("<Button-1>", self.eventListener.onLClick)
        self.canvas.bind("<Button-3>", self.eventListener.onRClick)
        
    def createBuildingFerme(self):
        self.eventListener.createBuilding(0)
        
    def createBuildingBaraque(self):
        self.eventListener.createBuilding(1)
        
    def createBuildingHopital(self):
        self.eventListener.createbuilding(2)

    def update(self, units, carte):
    	
        self.canvas.delete('unit')
        # Draw Units
        if units:
            for unit in units:
                self.canvas.create_rectangle(unit.x, unit.y, unit.x + 32, unit.y + 32, fill='blue', tags='unit')
                
        self.drawMinimap(units, carte)
        self.drawMap(carte)


    def show(self):
        self.root.mainloop()

    def after(self, ms, func):
        self.root.after(ms, func)


