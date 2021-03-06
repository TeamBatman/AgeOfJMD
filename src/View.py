#!/usr/bin/env python
# -*- coding: utf-8 -*-
import winsound

from Batiments import Batiment
from Carte import Tuile
import Config
from GraphicsManagement import GraphicsManager
import GraphicsManagement
from Units import Unit
from Units import Paysan
from Civilisations import Civilisation
import Units


try:
    from tkinter import *  # Python 3
except ImportError:
    from Tkinter import *  # Python 2

from GuiAwesomeness import *


class Color:
    ROUGE = "#D34343"
    BLEU = "#3D99BB"
    VERT = "#26BE2E"
    MAUVE = "#5637DD"
    ORANGE = "#F39621"
    ROSE = "#CF4592"
    NOIR = "#0F0F0F"
    BLANC = "#FFFFFF"
    JAUNE = "#F5F520"


class FrameSide():
    UNITVIEW = 0
    CONSTRUCTIONVIEW = 1
    BASEVIEW = 2
    FARMVIEW = 3
    HOSPITALVIEW = 4
    BARACKVIEW = 5
    SCIERIEVIEW = 6
    FONDERIEVIEW = 7


    def __init__(self, canvas, parent, largeurMinimap, hauteurMinimap, eventListener):
        self.canvas = canvas
        self.parent = parent
        self.eventListener = eventListener

        self.width = largeurMinimap
        self.height = int(self.canvas.cget('height')) - hauteurMinimap

        self.x = int(self.canvas.cget('width')) - self.width
        self.y = hauteurMinimap

        self.frame = GFrame(self.canvas, width=self.width, height=self.height)

        self.baseButton = GMediumButton(self.canvas, text=None, command=self.createBuildingBase,
                                        iconPath="Graphics/Buildings/Age_I/Base.png")

        self.childView = None  # La vue à afficher sur ce menu
        self.unitView = None
        self.constructionView = None


    def draw(self):
        """ Affiche le CADRE 
        """
        if self.childView:
            self.childView.draw()
        self.frame.draw(self.x, self.y)

    def drawBaseButton(self):
        self.baseButton.draw(x=self.x + 25, y=self.y + 25)

    def createBuildingBase(self):
        self.eventListener.createBuilding(Batiment.BASE)
        self.destroy()

    def changeView(self, selectedView, building=None):
        if self.childView:
            self.childView.destroy()

        if selectedView == FrameSide.UNITVIEW:
            if self.parent.selected:
                unit = self.parent.selected[0]
            else:
                unit = self.unitView.unit
            self.unitView = UnitView(self.canvas, unit, self, self.eventListener)
            self.unitView.draw()
            self.childView = self.unitView

        elif selectedView == FrameSide.CONSTRUCTIONVIEW:
            self.constructionView = ConstructionView(self.canvas, self, self.eventListener)
            self.constructionView.draw()
            self.childView = self.constructionView

        elif selectedView == FrameSide.BASEVIEW:
            self.baseView = BaseView(self.canvas, building, self, self.eventListener)
            self.baseView.draw()
            self.childView = self.baseView

        elif selectedView == FrameSide.FARMVIEW:
            self.farmView = FarmView(self.canvas, building, self, self.eventListener)
            self.farmView.draw()
            self.childView = self.farmView

        elif selectedView == FrameSide.HOSPITALVIEW:
            self.hospitalView = HospitalView(self.canvas, building, self, self.eventListener)
            self.hospitalView.draw()
            self.childView = self.hospitalView

        elif selectedView == FrameSide.BARACKVIEW:
            self.barackView = BarackView(self.canvas, building, self, self.eventListener)
            self.barackView.draw()
            self.childView = self.barackView

        elif selectedView == FrameSide.SCIERIEVIEW:
            self.scierieView = ScierieView(self.canvas, building, self, self.eventListener)
            self.scierieView.draw()
            self.childView = self.scierieView

        elif selectedView == FrameSide.FONDERIEVIEW:
            self.fonderieView = FonderieView(self.canvas, building, self, self.eventListener)
            self.fonderieView.draw()
            self.childView = self.fonderieView


    def destroy(self):
        attr = self.__dict__
        for value in attr.values():
            if isinstance(value, GButton):
                value.destroy()


class UnitView():
    def __init__(self, canvas, unitSelected, frameSide, evListener):
        self.canvas = canvas
        self.eventListener = evListener
        self.frameSide = frameSide
        self.btnPassive = GMediumButton(self.canvas, command=self.onPassive,
                                        iconPath='Graphics/Icones/PassiveModeBig.png')
        self.btnActive = GMediumButton(self.canvas, command=self.onActive,
                                       iconPath='Graphics/Icones/ActiveModeBig.png')

        self.btnConstruction = GMediumButton(self.canvas, command=self.onConstruction,
                                             iconPath='Graphics/Icones/constructionBig.png')
        self.width = frameSide.width
        self.height = frameSide.height

        self.x = frameSide.x
        self.y = frameSide.y

        self.unit = unitSelected

    def onActive(self):
        self.unit.modeAttack = Unit.ACTIF

    def onPassive(self):
        self.unit.modeAttack = Unit.PASSIF

    def onConstruction(self):
        self.frameSide.changeView(FrameSide.CONSTRUCTIONVIEW)

    def draw(self):
        posX = self.x + self.width / 2 - 32
        posY = self.y + 50

        # BARRE DE VIE
        largeurBarre = self.unit.grandeur  # en pixels
        hauteurBarre = 10
        hp = int(self.unit.hp * largeurBarre / self.unit.hpMax)
        self.canvas.create_rectangle(posX, posY - 12, posX + 32, posY - hauteurBarre, fill='black', tags='unitView')
        self.canvas.create_rectangle(posX, posY - 12, posX + hp, posY - hauteurBarre, fill='red', tags='unitView')


        # ICÔNE MODE COMBAT
        ico = GraphicsManager.getPhotoImage('Icones/modeActif.png') if self.unit.modeAttack == Unit.ACTIF \
            else GraphicsManager.getPhotoImage('Icones/modePassif.png')
        self.canvas.create_image(posX - 16, posY, anchor=NW, image=ico, tags='unitView')
        self.canvas.create_image(posX, posY, anchor=NW, image=self.unit.animation.spriteSheet.frames['DOWN_1'],
                                 tags=('unitView', self.unit.id))

        # BOUTONS
        self.btnActive.draw(self.x + 25, self.y + 130)
        self.btnPassive.draw(self.x + 130, self.y + 130)
        if isinstance(self.unit, Paysan):
            self.btnConstruction.draw(self.x + 25, self.y + 235)

    def destroy(self):
        self.canvas.delete('unitView')
        attr = self.__dict__
        for value in attr.values():
            if isinstance(value, GButton):
                value.destroy()


class ConstructionView():
    def __init__(self, canvas, parent, evListener):
        self.canvas = canvas
        self.parent = parent
        self.eventListener = evListener

        self.width = parent.width
        self.height = parent.width
        self.x = parent.x
        self.y = parent.y

        self.buttonFerme = GMediumButton(self.canvas, text=None, command=self.onCreateBuildingFerme,
                                         iconPath="Graphics/Buildings/Age_I/Ferme/Ferme_noire.png")

        self.buttonBaraque = GMediumButton(self.canvas, text=None, command=self.onCreateBuildingBaraque,
                                           iconPath="Graphics/Buildings/Age_II/Barracks/barracks_noire.png")

        self.buttonHopital = GMediumButton(self.canvas, text=None, command=self.onCreateBuildingHopital,
                                           iconPath="Graphics/Buildings/Age_III/Hopital/hopital_noir.png")

        self.buttonScierie = GMediumButton(self.canvas, text=None, command=self.onCreateBuildingScierie,
                                        iconPath="Graphics/Buildings/Age_II/Scierie/scierie_noire.png")

        self.buttonFonderie = GMediumButton(self.canvas, text=None, command=self.onCreateBuildingFonderie, iconPath="Graphics/Buildings/Age_III/Fonderie/fonderie_noire.png")


        self.btnRetour = GMediumButton(self.canvas, text=None, command=self.onRetour, iconPath='Graphics/Icones/arrowBack.png')


    def onRetour(self):
        self.parent.changeView(FrameSide.UNITVIEW)

    def onCreateBuildingScierie(self):
        self.eventListener.createBuilding(Batiment.SCIERIE)

    def onCreateBuildingFonderie(self):
        self.eventListener.createBuilding(Batiment.FONDERIE)

    def onCreateBuildingBaraque(self):
        self.eventListener.createBuilding(Batiment.BARAQUE)

    def onCreateBuildingHopital(self):
        self.eventListener.createBuilding(Batiment.HOPITAL)

    def onCreateBuildingFerme(self):
        self.eventListener.createBuilding(Batiment.FERME)

    def createBuildingBase(self):
        self.eventListener.createBuilding(Batiment.BASE)

    def draw(self):
        # BTN CONSTRUCTION
        if self.parent.parent.selected:
            unit = self.parent.parent.selected[0]
            epoque = unit.joueur.epoque
        else:
            print("fail epoque")
            epoque = 1

        if epoque > 1:
            ageString = {1: 'Age_I', 2: 'Age_II', 3: 'Age_III'}
            unit = self.parent.parent.selected[0]
            epoque = unit.joueur.epoque
            age = ageString[epoque]
            img = GraphicsManager.getImage(('Buildings/%s/Ferme/ferme_noire.png' % age))
            resized = img.resize((70, 70), Image.ANTIALIAS)
            imageBonne = ImageTk.PhotoImage(resized)
            self.buttonFerme.icon = imageBonne
            self.buttonBaraque.draw(x=self.x + self.width / 2 + 5, y=self.y + 25)
            self.buttonHopital.draw(x=self.x + 25, y=self.y + 130)

        if epoque > 1:
            self.buttonScierie.draw(x=self.x + self.width / 2 + 5, y=self.y + 130)
            self.buttonFonderie.draw(x=self.x + 25, y=self.y + 235)

        self.buttonFerme.draw(x=self.x + 25, y=self.y + 25)
        self.btnRetour.draw(x=self.x + 25, y=self.y + 340)


    def destroy(self):
        attr = self.__dict__
        for value in attr.values():
            if isinstance(value, GButton):
                value.destroy()


class BaseView():
    def __init__(self, canvas, building, parent, evListener):
        self.canvas = canvas
        self.parent = parent
        self.eventListener = evListener

        self.base = building

        self.width = parent.width
        self.height = parent.width
        self.x = parent.x
        self.y = parent.y

        self.boutonCreateUnit = GMediumButton(self.canvas, 'Unit', self.onCreateUnit, GButton.GREY)
        p = Paysan(-1, -1, -1,  building.joueur, building.joueur.civilisation)
        img = p.animation.spriteSheet.frames['DOWN_1']
        self.boutonCreateUnit.icon = img


    def draw(self):
        posX = self.x + 91
        posY = self.y + 35

        # BARRE DE VIE
        largeurBarre = self.base.grandeur  # en pixels
        hauteurBarre = 10
        hp = int(self.base.pointsDeVie * largeurBarre / self.base.hpMax)
        self.canvas.create_rectangle(posX, posY - 12, posX + 32, posY - hauteurBarre, fill='black', tags='buildingView')
        self.canvas.create_rectangle(posX, posY - 12, posX + hp, posY - hauteurBarre, fill='red', tags='buildingView')


        # IMAGE DU BATIMENT
        self.canvas.create_image(posX - 25, posY - 10, anchor=NW, image=self.base.image,
                                 tags=('buildingView', self.base.id))

        self.boutonCreateUnit.draw(x=self.x + 25, y=self.y + 130)

    def onCreateUnit(self):
        self.base.creer1()
        print("created unit")

    def destroy(self):
        self.canvas.delete('buildingView')
        attr = self.__dict__
        for value in attr.values():
            if isinstance(value, GButton):
                value.destroy()


class FarmView():
    def __init__(self, canvas, building, parent, evListener):
        self.canvas = canvas
        self.parent = parent
        self.eventListener = evListener

        self.farm = building

        self.width = parent.width
        self.height = parent.width
        self.x = parent.x
        self.y = parent.y
        self.boutonReleaseUnit = GMediumButton(self.canvas, 'Ferme', self.onRemoveUnit, GButton.GREY)

    def draw(self):
        posX = self.x + 91
        posY = self.y + 35

        # BARRE DE VIE
        largeurBarre = self.farm.grandeur  # en pixels
        hauteurBarre = 10
        hp = int(self.farm.pointsDeVie * largeurBarre / self.farm.hpMax)
        self.canvas.create_rectangle(posX, posY - 12, posX + 32, posY - hauteurBarre, fill='black', tags='buildingView')
        self.canvas.create_rectangle(posX, posY - 12, posX + hp, posY - hauteurBarre, fill='red', tags='buildingView')


        # IMAGE DU BATIMENT
        self.canvas.create_image(posX - 25, posY - 10, anchor=NW, image=self.farm.image,
                                 tags=('buildingView', self.farm.id))

        self.boutonReleaseUnit.draw(x=self.x + 25, y=self.y + 130)

    def onRemoveUnit(self):
        self.farm.sortir()

    def destroy(self):
        self.canvas.delete('buildingView')
        attr = self.__dict__
        for value in attr.values():
            if isinstance(value, GButton):
                value.destroy()


class HospitalView():
    def __init__(self, canvas, building, parent, evListener):
        self.canvas = canvas
        self.parent = parent
        self.eventListener = evListener

        self.hospital = building

        self.width = parent.width
        self.height = parent.width
        self.x = parent.x
        self.y = parent.y
        self.healUnit = GMediumButton(self.canvas, 'Regenerer', self.onHealingUnit, GButton.GREY)

    def draw(self):
        posX = self.x + 91
        posY = self.y + 35

        # BARRE DE VIE
        largeurBarre = self.hospital.grandeur  # en pixels
        hauteurBarre = 10
        hp = int(self.hospital.pointsDeVie * largeurBarre / self.hospital.hpMax)
        self.canvas.create_rectangle(posX, posY - 12, posX + 32, posY - hauteurBarre, fill='black', tags='buildingView')
        self.canvas.create_rectangle(posX, posY - 12, posX + hp, posY - hauteurBarre, fill='red', tags='buildingView')


        # IMAGE DU BATIMENT
        self.canvas.create_image(posX - 25, posY - 10, anchor=NW, image=self.hospital.image,
                                 tags=('buildingView', self.hospital.id))

        self.healUnit.draw(x=self.x + 25, y=self.y + 130)

    def onHealingUnit(self):
        self.hospital.healing()

    def destroy(self):
        self.canvas.delete('buildingView')
        attr = self.__dict__
        for value in attr.values():
            if isinstance(value, GButton):
                value.destroy()


class BarackView():
    def __init__(self, canvas, building, parent, evListener):
        self.canvas = canvas
        self.parent = parent
        self.eventListener = evListener

        self.barack = building

        self.width = parent.width
        self.height = parent.width
        self.x = parent.x
        self.y = parent.y
        self.createPrivate = GMediumButton(self.canvas, 'Soldat', self.onCreatePrivate, GButton.GREY)
        p = Units.GuerrierEpee(-1, -1, -1,  building.joueur, building.joueur.civilisation)
        img = p.animation.spriteSheet.frames['DOWN_1']
        self.createPrivate.icon = img


        p = Units.GuerrierLance(-1, -1, -1,  building.joueur, building.joueur.civilisation)
        img = p.animation.spriteSheet.frames['DOWN_1']
        self.createUpgradedPrivate = GMediumButton(self.canvas, 'Soldat 2', self.onCreateUpgradedPrivate, GButton.GREY)
        self.createUpgradedPrivate.icon = img




        p = Units.GuerrierBouclier(-1, -1, -1,  building.joueur, building.joueur.civilisation)
        img = p.animation.spriteSheet.frames['DOWN_1']
        self.createShieldPrivate = GMediumButton(self.canvas, 'Soldat 3', self.onCreateShieldPrivate, GButton.GREY)
        self.createShieldPrivate.icon = img


        p = Units.Scout(-1, -1, -1,  building.joueur, building.joueur.civilisation)
        img = p.animation.spriteSheet.frames['DOWN_1']
        self.createScout = GMediumButton(self.canvas, 'Scout', self.onCreateScoutPrivate, GButton.GREY)
        self.createScout.icon = img


    def draw(self):
        posX = self.x + 91
        posY = self.y + 35

        # BARRE DE VIE
        largeurBarre = self.barack.grandeur  # en pixels
        hauteurBarre = 10
        hp = int(self.barack.pointsDeVie * largeurBarre / self.barack.hpMax)
        self.canvas.create_rectangle(posX, posY - 12, posX + 32, posY - hauteurBarre, fill='black', tags='buildingView')
        self.canvas.create_rectangle(posX, posY - 12, posX + hp, posY - hauteurBarre, fill='red', tags='buildingView')


        # IMAGE DU BATIMENT
        self.canvas.create_image(posX - 25, posY - 10, anchor=NW, image=self.barack.image,
                                 tags=('buildingView', self.barack.id))

        self.createPrivate.draw(x=self.x + 25, y=self.y + 130)
        self.createUpgradedPrivate.draw(x=self.x + self.width / 2 + 5, y=self.y + 130)
        self.createShieldPrivate.draw(x=self.x + 25, y=self.y + 235)
        self.createScout.draw(x=self.x + self.width / 2 + 5, y=self.y + 235)

    def onCreatePrivate(self):
        self.barack.creer1()

    def onCreateUpgradedPrivate(self):
        self.barack.creer2()

    def onCreateShieldPrivate(self):
        self.barack.creer3()

    def onCreateScoutPrivate(self):
        self.barack.creer4()

    def destroy(self):
        self.canvas.delete('buildingView')
        attr = self.__dict__
        for value in attr.values():
            if isinstance(value, GButton):
                value.destroy()


class ScierieView():
    def __init__(self, canvas, building, parent, evListener):
        self.canvas = canvas
        self.parent = parent
        self.eventListener = evListener

        self.scierie = building

        self.width = parent.width
        self.height = parent.width
        self.x = parent.x
        self.y = parent.y
        self.boutonReleaseUnit = GMediumButton(self.canvas, 'Scierie', self.onRemoveUnit, GButton.GREY)


    def draw(self):
        posX = self.x + 91
        posY = self.y + 35

        # BARRE DE VIE
        largeurBarre = self.scierie.grandeur  # en pixels
        hauteurBarre = 10
        hp = int(self.scierie.pointsDeVie * largeurBarre / self.scierie.hpMax)
        self.canvas.create_rectangle(posX, posY - 12, posX + 32, posY - hauteurBarre, fill='black', tags='buildingView')
        self.canvas.create_rectangle(posX, posY - 12, posX + hp, posY - hauteurBarre, fill='red', tags='buildingView')


        # IMAGE DU BATIMENT
        self.canvas.create_image(posX - 25, posY - 10, anchor=NW, image=self.scierie.image,
                                 tags=('buildingView', self.scierie.id))

        self.boutonReleaseUnit.draw(x=self.x + 25, y=self.y + 130)

    def onRemoveUnit(self):
        self.scierie.sortir()

    def destroy(self):
        self.canvas.delete('buildingView')
        attr = self.__dict__
        for value in attr.values():
            if isinstance(value, GButton):
                value.destroy()


class FonderieView():
    def __init__(self, canvas, building, parent, evListener):
        self.canvas = canvas
        self.parent = parent
        self.eventListener = evListener

        self.fonderie = building

        self.width = parent.width
        self.height = parent.width
        self.x = parent.x
        self.y = parent.y
        self.boutonReleaseUnit = GMediumButton(self.canvas, 'Fonderie', self.onRemoveUnit, GButton.GREY)


    def draw(self):
        posX = self.x + 91
        posY = self.y + 35

        # BARRE DE VIE
        largeurBarre = self.fonderie.grandeur  # en pixels
        hauteurBarre = 10
        hp = int(self.fonderie.pointsDeVie * largeurBarre / self.fonderie.hpMax)
        self.canvas.create_rectangle(posX, posY - 12, posX + 32, posY - hauteurBarre, fill='black', tags='buildingView')
        self.canvas.create_rectangle(posX, posY - 12, posX + hp, posY - hauteurBarre, fill='red', tags='buildingView')


        # IMAGE DU BATIMENT
        self.canvas.create_image(posX - 25, posY - 10, anchor=NW, image=self.fonderie.image,
                                 tags=('buildingView', self.fonderie.id))

        self.boutonReleaseUnit.draw(x=self.x + 25, y=self.y + 130)

    def onRemoveUnit(self):
        self.fonderie.sortir()

    def destroy(self):
        self.canvas.delete('buildingView')
        attr = self.__dict__
        for value in attr.values():
            if isinstance(value, GButton):
                value.destroy()


class StatsView():
    def __init__(self, canvas, joueur, tkRoot):
        self.canvas = canvas
        self.joueur = joueur
        self.root = tkRoot

        self.width = 450
        self.height = 500
        self.x = 225
        self.y = 100
        self.frame = GFrame(self.canvas, width=self.width, height=self.height)

        self.labelStatisques = GLabel(self.canvas, "Statistiques", fontSize=24)
        self.labelTempsJeux = GLabel(self.canvas, "Temps de jeu: ", self.x + 30, self.y + 30)
        self.labelAge = GLabel(self.canvas, "Age: ")
        self.labelNbBuilding = GLabel(self.canvas, "Nombre de Bâtiments: ")
        self.labelNbUnits = GLabel(self.canvas, "Nombre d'unités: ")
        self.labelNbUnitsDead = GLabel(self.canvas, "Nombre d'unités mortes au combat: ")

        self.okButton = GCheckButton(self.canvas, command=self.destroy)



    def draw(self):
        self.frame.draw(self.x, self.y)

        self.labelStatisques.draw(self.x + self.width/2-70, self.y + 20)

        self.labelTempsJeux.text = "Temps de jeu: %s" % self.joueur.baseVivante
        self.labelTempsJeux.draw(self.x + 20, self.y + 70)

        self.labelAge.text = "Âge: %s" % self.joueur.epoque
        self.labelAge.draw(self.x + 20, self.labelTempsJeux.y + 30)

        self.labelNbBuilding.text = "Nombre de Bâtiments: %s" % len(self.joueur.buildings)
        self.labelNbBuilding.draw(self.x + 20, self.labelAge.y + 30)

        self.labelNbUnits.text = "Nombre d'unités: %s" % len(self.joueur.buildings)
        self.labelNbUnits.draw(self.x + 20, self.labelNbBuilding.y + 30)

        self.labelNbUnitsDead.text = "Nombre d'unités mortes au combat: %s" % self.joueur.nbDeadUnits
        self.labelNbUnitsDead.draw(self.x + 20, self.labelNbUnits.y + 30)

        self.okButton.draw(self.x + self.width/2-self.okButton.width/2, self.y + self.height-80)



    def destroy(self):
        attr = self.__dict__
        for value in attr.values():
            if isinstance(value, GWidget):
                value.destroy()







class GameMenu():
    def __init__(self, canvas, mainView):
        self.canvas = canvas
        self.mainView = mainView

        self.width = 250
        self.height = 315
        self.x = 300
        self.y = 100
        self.frame = GFrame(self.canvas, width=self.width, height=self.height)

        self.lblMenu = GLabel(self.canvas, "Menu", fontSize=24)

        self.btnStats = GButton(self.canvas, "Statistiques", command=self.onStats)
        self.btnSurrender = GButton(self.canvas, "Abandonner", command=self.onSurrender)
        self.btnBack = GButton(self.canvas, "Retour", command=self.onBack)


    def draw(self):
        self.frame.draw(self.x, self.y)
        self.lblMenu.draw(self.x + self.width/2-40, self.y + 20)

        self.btnStats.draw(self.x + 30, self.y + 70)
        self.btnSurrender.draw(self.x + 30, self.btnStats.y + self.btnStats.height + 30)
        self.btnBack.draw(self.x + 30, self.btnSurrender.y + self.btnSurrender.height + 30)



    def destroy(self):
        attr = self.__dict__
        for value in attr.values():
            if isinstance(value, GWidget):
                value.destroy()

    def onStats(self):
        self.statWindow = StatsView(self.canvas, self.mainView.joueur, self.mainView.window.root)
        self.statWindow.draw()

    def onSurrender(self):
        self.dialog = GChoiceDialogue(self.canvas, "Voulez-vous vraiment abandonner   \n la partie?", command=self.onConfirmSurrender)
        self.destroy()
        self.dialog.draw(self.x, self.y)

    def onConfirmSurrender(self, result):
        if result == GChoiceDialogue.NO:
            self.dialog.destroy()
            self.draw()
            return

        self.destroy()
        self.mainView.eventListener.onSurrender()




    def onBack(self):
        self.destroy()









class FrameMiniMap():  # TODO AFFICHER LES BUILDINGS
    def __init__(self, mainView, canvas, eventListener):
        self.canvas = canvas
        self.eventListener = eventListener
        self.mainView = mainView

        # LE CADRE
        self.width = 250  # Largeur du cadre en pixels
        self.height = 250  # hauteur du cadre en pixels
        self.x = int(self.canvas.cget('width')) - self.width  # en pixels
        self.y = 0  # en pixels
        self.frame = GFrame(self.canvas, width=self.width, height=self.height)


        # LA MINIMAP
        self.miniMapTag = 'miniMap'  # Le tag tkinter à utiliser pour la minimap
        self.miniMapWidth = 211  # en pixels
        self.miniMapHeight = 211  # en pixels

        # # Taille de la marge entre la cadre et la minimap en pixels
        self.minimapMargeX = int((self.width - self.miniMapWidth) / 2) - 2
        self.minimapMargeY = int((self.height - self.miniMapHeight) / 2) - 1

        # Position de la minimap en pixel par rapport au caneva
        self.miniMapX = self.x + self.minimapMargeX
        self.miniMapY = self.y + self.minimapMargeY

        # Position de la mini caméra en pixels selon le coins haut gauche
        self.miniCameraX = self.miniMapX
        self.miniCameraY = self.miniMapY

        self.tailleTuile = 2  # Taille d'une tuile en pixels 


    def bindEvents(self):
        """ Lie les évènements entre au eventListener
        """

        # Carré d'écoute des événèments (pour le tag)
        self.canvas.create_rectangle(self.miniMapX, self.miniMapY, self.miniMapWidth + self.miniMapX,
                                     self.miniMapHeight + self.miniMapY, fill='green', tags=self.miniMapTag)

        self.canvas.tag_bind(self.miniMapTag, '<ButtonPress-1>', self.eventListener.onMinimapLPress)
        self.canvas.tag_bind(self.miniMapTag, '<B1-Motion>', self.eventListener.onMinimapMouseMotion)

    def draw(self):
        """ Dessine le CADRE de la minimap à l'écran
        """
        self.frame.draw(self.x, self.y)

    def updateMinimap(self, carte):
        """ Met à jours, (re)dessine la carte de la minimap
        """
        self.canvas.delete(self.miniMapTag)
        # x1 = self.miniMapX
        # y1 = self.miniMapY
        # x2 = x1 + self.miniMapWidth
        # y2 = y1 + self.miniMapHeight

        size = 106  # TODO Explication de ce chiffre
        itemMini = self.tailleTuile  # La grandeur des cases pour la minimap en pixels
        # couleurs = {
        # 0: "#0B610B",  # vert
        # 1: "#BFBF00",  # jaune
        # 2: "#1C1C1C",  # gris pale
        # 3: "#BDBDBD",  # gris fonce
        # 4: "#2E9AFE"  # bleu
        # }

        for x in range(size):
            for y in range(size):
                posX1 = self.miniMapX + x * itemMini
                posY1 = self.miniMapY + y * itemMini
                posX2 = posX1 + itemMini
                posY2 = posY1 + itemMini
                #couleur = couleurs[carte[x][y].type]
                couleur = "#333"

                self.canvas.create_rectangle(posX1, posY1, posX2, posY2, width=0, fill=couleur, tags=self.miniMapTag)


    def updateMiniUnits(self, units):
        """ (Re)dessine les unités à l'écran
        :param units: les unités
        """
        # TODO METTRE CONSTANTE JOUEUR
        couleursCiv = {
            Civilisation.ROUGE: Color.ROUGE,
            Civilisation.BLEU: Color.BLEU,
            Civilisation.VERT: Color.VERT,
            Civilisation.MAUVE: Color.MAUVE,
            Civilisation.ORANGE: Color.ORANGE,
            Civilisation.ROSE: Color.ROSE,
            Civilisation.NOIR: Color.NOIR,
            Civilisation.BLANC: Color.BLANC,
            Civilisation.JAUNE: Color.JAUNE
        }

        tagUnits = 'miniUnits'
        self.canvas.delete(tagUnits)

        item = 2

        for unit in units.values():

            color = couleursCiv[unit.civilisation]
            if unit.civilisation == self.eventListener.controller.model.civNumber:
                self.updateFog(unit)

            caseX, caseY = self.eventListener.controller.model.trouverCaseMatrice(unit.x, unit.y)

            if self.eventListener.controller.model.carte.matrice[caseX][caseY].revealed:
                x1 = self.miniMapX + (caseX * item)
                y1 = self.minimapMargeY + (caseY * item)
                x2 = x1 + item
                y2 = y1 + item
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags=(tagUnits, self.miniMapTag))


    def updateFog(self, unit):
        carte = self.eventListener.controller.model.carte.matrice

        caseX, caseY = self.eventListener.controller.model.trouverCaseMatrice(unit.x, unit.y)
        radius = 5
        couleurs = {
            Tuile.GAZON: "#0B610B",  # vert
            Tuile.FORET: "#BFBF00",  # jaune
            Tuile.MINERAI: "#1C1C1C",  # gris pale
            Tuile.CHARBON: "#BDBDBD",  # gris fonce
            Tuile.EAU: "#2E9AFE"  # bleu
        }

        for x in range(caseX - radius, caseX + radius):
            if 0 <= x <= 106:
                for y in range(caseY - radius, caseY + radius):
                    if 0 <= y <= 106:
                        try:
                            if not carte[x][y].revealed:
                                posX1 = self.miniMapX + x * self.tailleTuile
                                posY1 = self.miniMapY + y * self.tailleTuile
                                posX2 = posX1 + self.tailleTuile
                                posY2 = posY1 + self.tailleTuile

                                if not carte[x][y].type == 5:  # bâtiment
                                    couleur = couleurs[carte[x][y].type]
                                else:
                                    couleur = couleurs[0]

                                self.canvas.create_rectangle(posX1, posY1, posX2, posY2, width=0, fill=couleur,
                                                             tags=self.miniMapTag)

                                self.eventListener.controller.model.carte.matrice[x][y].revealed = 1
                                try:
                                    self.canvas.tag_lower(str(x) + ":" + str(y))
                                except:
                                    pass

                                self.canvas.tag_raise('rectMiniMap')
                        except IndexError:
                            pass
                            # print("index map fog!")


    def drawRectMiniMap(self, clicX=0, clicY=0, nbCasesX=16, nbCasesY=14):
        """ (Re)dessine le rectangle de caméra de la minimap
        :param clicX: position X de la souris en pixels
        :param clicY: position Y de la souris en pixels
        """

        width = self.tailleTuile * nbCasesX  # Largeur du Rectangle
        height = self.tailleTuile * nbCasesY  # Hauteur du Rectangle
        couleur = 'red'

        # On centre le rectangle par rapport au Clic de la souris

        self.miniCameraX = clicX - width / 2
        self.miniCameraY = clicY - height / 2


        # TESTER LES LIMITES

        # Limite Gauche
        if self.miniCameraX < self.miniMapX:
            self.miniCameraX = self.miniMapX

        # Limite Droite
        if self.miniCameraX + width > self.miniMapX + self.miniMapWidth:
            self.miniCameraX = self.miniMapX + self.miniMapWidth - width

        # Limite Haut
        if self.miniCameraY < self.miniMapY:
            self.miniCameraY = self.miniMapY

        # Limite Bas
        if self.miniCameraY + height > self.miniMapY + self.miniMapHeight:
            self.miniCameraY = self.miniMapY + self.miniMapHeight - height

        # On affiche le rectangle
        self.canvas.delete('rectMiniMap')
        self.canvas.create_rectangle(self.miniCameraX, self.miniCameraY,
                                     self.miniCameraX + width, self.miniCameraY + height,
                                     outline=couleur, tags='rectMiniMap')


class FrameBottom():
    def __init__(self, gameView, canvas, largeurMinimap):
        self.gameView = gameView
        self.canvas = canvas
        self.width = int(self.canvas.cget('width')) - largeurMinimap
        self.height = 100

        self.x = 0
        self.y = int(self.canvas.cget('height')) - self.height

        self.frame = GFrame(self.canvas, width=self.width, height=self.height)
        self.canvas.tag_raise(self.frame.id, 'GButton')

        # TODO COMPLETER
        self.moraleProg = GProgressBar(self.canvas, 150, "Morale")
        self.moraleProg.setProgression(63)


        self.texteNourriture = GLabel(self.canvas,text=" "+str(40))
        self.texteBois = GLabel(self.canvas,text=" "+str(0))
        self.texteMinerai = GLabel(self.canvas,text=" "+str(0))
        self.texteCharbon = GLabel(self.canvas,text=" "+str(0))


        self.btnSettings = GSmallButton(self.canvas, command=self.onSettings, iconPath="Graphics/Icones/menuIcon.png")


    def draw(self):
        """ Dessine le cadre
        """
        self.frame.draw(self.x, self.y)
        #self.moraleProg.draw(x=self.frame.x + 35, y=self.frame.y + 25)
        self.canvas.delete('infoRes')
        self.texteNourriture.destroy()
        self.texteBois.destroy()
        self.texteMinerai.destroy()
        self.texteCharbon.destroy()




        self.texteNourriture.draw(x=self.frame.x + 300, y=self.frame.y + 35)
        self.canvas.create_image(self.frame.x + 225, self.frame.y + 20, anchor=NW, image=GraphicsManager.getPhotoImage("Icones/foodInfo.png"), tags='infoRes')

        self.texteBois.draw(x=self.frame.x + 410, y=self.frame.y + 35)
        self.canvas.create_image(self.frame.x + 350, self.frame.y + 20, anchor=NW, image=GraphicsManager.getPhotoImage("Icones/woodInfo.png"), tags='infoRes')



        self.texteMinerai.draw(x=self.frame.x + 555, y=self.frame.y + 35)
        self.canvas.create_image(self.frame.x + 450, self.frame.y + 20, anchor=NW, image=GraphicsManager.getPhotoImage("Icones/mineraiInfo.png"), tags='infoRes')


        self.texteCharbon.draw(x=self.frame.x + 675, y=self.frame.y + 35)
        self.canvas.create_image(self.frame.x + 600, self.frame.y + 20, anchor=NW, image=GraphicsManager.getPhotoImage("Icones/charbonInfo.png"), tags='infoRes')






        self.btnSettings.draw(self.x + 20, self.y + 20)


    def updateResources(self, joueur):
        attr = self.__dict__
        for value in attr.values():
            if isinstance(value, GLabel):
                value.destroy()
        ressources = joueur.ressources
        self.texteNourriture.text = " "+str(ressources['nourriture'])
        self.texteBois.text = " "+str(ressources['bois'])
        self.texteMinerai.text = " "+str(ressources['minerai'])
        self.texteCharbon.text = " "+str(ressources['charbon'])
        self.draw()


    def onSettings(self):
        self.gmenu = GameMenu(self.canvas, self.gameView)
        self.gmenu.draw()

class CarteView():
    def __init__(self, canvas, eventListener, largeurEcran, hauteurEcran, largeurCadreDroit, hauteurCadreBas):
        self.canvas = canvas
        self.eventListener = eventListener

        self.width = largeurEcran - largeurCadreDroit
        self.height = hauteurEcran - hauteurCadreBas


        # CASES
        # self.sizeUnit = 32  # Taille des unités en pixels

        self.item = 48  # Grandeur d'un bloc (Carte) en pixel
        # Nombre de cases Visibles en X et En Y
        self.nbCasesX = 16  # Nombre de case (de taille item) en X à afficher
        self.nbCasesY = 14  # Nombre de case (de taille item) en Y à afficher

        # Position de la caméra En terme de case (de taille item) dans la matrice de la map
        self.cameraX = 0
        self.cameraY = 0

        self.tagName = 'carte'


    def bindEvents(self):
        """ Lis les événements à la carte
        """
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill='green', tags=self.tagName)
        self.canvas.tag_lower('carte')  # Pour que ce soit derrière le HUD
        self.canvas.tag_bind('carte', '<Button-2>', self.eventListener.onMapRClick)
        self.canvas.tag_bind('carte', '<Button-3>', self.eventListener.onMapRClick)
        self.canvas.tag_bind('unitVision', '<Button-3>', self.eventListener.onMapRClick)

        self.canvas.tag_bind('carte', '<ButtonPress-1>', self.eventListener.onMapLPress)
        self.canvas.tag_bind('carte', '<B1-Motion>', self.eventListener.onMapMouseMotion)
        self.canvas.tag_bind('carte', '<ButtonRelease-1>', self.eventListener.onMapLRelease)

        self.canvas.tag_bind('unit', '<Button-1>', self.eventListener.onUnitLClick)
        self.canvas.tag_bind('unit', '<Button-3>', self.eventListener.onUnitRClick)

        self.canvas.tag_bind('building', '<ButtonPress-1>', self.eventListener.onMapLRelease)
        self.canvas.tag_bind('building', '<ButtonRelease-1>', self.eventListener.onMapLRelease)
        self.canvas.tag_bind('building', '<Button-3>', self.eventListener.onBuildingRClick)


    def draw(self, carte):
        """ Dessine la carte à l'écran
        :param carte: la carte 
        """
        self.canvas.delete(self.tagName)
        # TODO OPTIMISER C'EST TROP LONG
        x1 = self.cameraX
        y1 = self.cameraY
        x2 = self.width
        y2 = self.height

        images = {
            Tuile.GAZON: GraphicsManager.getPhotoImage('World/grass.png'),  # vert
            Tuile.FORET: GraphicsManager.getPhotoImage('World/foret.png'),  # jaune
            Tuile.MINERAI: GraphicsManager.getPhotoImage('World/minerai.png'),  # gris pale
            Tuile.CHARBON: GraphicsManager.getPhotoImage('World/charbon.png'),  # gris fonce
            Tuile.EAU: GraphicsManager.getPhotoImage('World/water.png'),  # bleu
            Tuile.BATIMENT: GraphicsManager.getPhotoImage('World/grass.png'),
        }

        foretImage = {

        }

        for x in range(x1, x1 + self.nbCasesX + 1):
            for y in range(y1, y1 + self.nbCasesY):
                posX1 = 0 + (x - x1) * self.item
                posY1 = 0 + (y - y1) * self.item
                self.canvas.create_image(posX1, posY1, anchor=NW, image=images[Tuile.GAZON], tags=self.tagName)

                # for x in range(x1, x1 + self.nbCasesX + 1):
                #    for y in range(y1, y1 + self.nbCasesY):
                #        posX1 = 0 + (x - x1) * self.item
                #       posY1 = 0 + (y - y1) * self.item
                posX2 = posX1 + self.item
                posY2 = posY1 + self.item
                tuile = carte[x][y]

                if tuile.type != Tuile.GAZON:
                    img = images[tuile.type]
                    tag = self.tagName
                    self.canvas.create_image(posX1, posY1, anchor=NW, image=img, tags=tag)

                if not carte[x][y].revealed:
                    img = GraphicsManager.getPhotoImage('World/fog.png')
                    self.canvas.create_image(posX1, posY1, anchor=NW, image=img,
                                             tags=(self.tagName, str(x) + ":" + str(y)))
                    continue

                # TODO raise Fog and Forest

                """if carte[x][y].revealed and (carte[x][y].type == Tuile.GAZON or carte[x][y].type == Tuile.BATIMENT):
                    self.canvas.create_image(posX1, posY1, anchor=NW,
                                            image=,
                                            tags=self.tagName)"""

        self.canvas.tag_lower(self.tagName)  # Pour que ce soit derrière le HUD
        self.canvas.tag_raise('foret', self.tagName)
        self.canvas.tag_raise('fog')

    def drawUnits(self, units, selectedUnits, carte):
        """ Dessine les unités dans la map
        :param selectedUnits: une liste des unités sélectionnées
        :param units: une liste d'unités
        """
        self.canvas.delete('unit')
        self.canvas.delete('unitHP')
        self.canvas.delete('unitVision')
        self.canvas.delete('unitAttackMode')

        couleursCiv = {
            Civilisation.ROUGE: Color.ROUGE,
            Civilisation.BLEU: Color.BLEU,
            Civilisation.VERT: Color.VERT,
            Civilisation.MAUVE: Color.MAUVE,
            Civilisation.ORANGE: Color.ORANGE,
            Civilisation.ROSE: Color.ROSE,
            Civilisation.NOIR: Color.NOIR,
            Civilisation.BLANC: Color.BLANC,
            Civilisation.JAUNE: Color.JAUNE
        }

        for unit in units.values():
            x, y = self.eventListener.controller.model.trouverCaseMatrice(unit.x, unit.y)
            if self.isUnitShown(unit) and carte[x][y].revealed == 1:
                unitImage = unit.animation.activeFrame
                posX = (unit.x ) - (self.cameraX * self.item)
                posY = (unit.y ) - (self.cameraY * self.item)

                if unit in selectedUnits:
                    unitImage = unit.animation.activeOutline


                    selColor = GraphicsManagement.hex_to_rgba(couleursCiv[unit.civilisation])


                    try:
                        vision = GraphicsManager.getPhotoImage('unitVision_%s' % couleursCiv[unit.civilisation])
                    except KeyError:
                        vision = GraphicsManagement.generateCircle(unit.rayonVision, selColor)
                        GraphicsManager.addPhotoImage(ImageTk.PhotoImage(vision), 'unitVision')
                        vision = GraphicsManager.getPhotoImage('unitVision')
                    self.canvas.create_image(posX, posY, anchor=CENTER, image=vision, tags='unitVision')



                # BARRE DE VIE
                if unit.hp != unit.hpMax or unit in selectedUnits:
                    tailleBarre = unit.grandeur  # en pixels
                    hp = int(unit.hp * tailleBarre / unit.hpMax)

                    bx1 = posX - unit.grandeur / 2
                    by1 = posY - unit.grandeur / 2 - 8
                    bx2 = bx1 + tailleBarre
                    by2 = by1 + 4

                    self.canvas.create_rectangle(bx1, by1, bx2, by2, fill='black', tags='unitHP')
                    self.canvas.create_rectangle(bx1, by1, bx1 + hp, by2, fill='red', tags='unitHP')


                # ICÔNE MODE COMBAT
                if self.eventListener.controller.model.joueur.civilisation == unit.civilisation:
                    ico = GraphicsManager.getPhotoImage(
                        'Icones/modeActif.png') if unit.modeAttack == Unit.ACTIF else GraphicsManager.getPhotoImage(
                        'Icones/modePassif.png')
                    self.canvas.create_image(posX - 16, posY, anchor=CENTER, image=ico, tags='unitAttackMode')

                self.canvas.create_image(posX, posY, anchor=CENTER, image=unitImage, tags=('unit', unit.id))


                # ANIMATION BLESSURES ET AUTRES
                for anim in unit.oneTimeAnimations:
                    imgAnim = anim.activeFrame
                    self.canvas.create_image(posX, posY, anchor=CENTER, image=imgAnim, tags=('unit', unit.id))
                    #winsound.PlaySound("Sounds/Punch1", winsound.SND_ASYNC | winsound.SND_FILENAME)



                """if unit.leader == 1:
                    self.canvas.create_rectangle(posX, posY, posX+10, posY+10, width=1, fill='red', tags='unit')
                elif unit.leader == 2:
                    self.canvas.create_rectangle(posX, posY, posX+10, posY+10, width=1, fill='green', tags='unit')
                elif unit.leader == 0:
                    self.canvas.create_rectangle(posX, posY, posX+10, posY+10, width=1, fill='yellow', tags='unit')
                """

                try:
                    self.canvas.tag_raise('unit')
                    self.canvas.tag_lower('unit', 'GMenu')
                    self.canvas.tag_lower('unitHP', 'GMenu')
                    self.canvas.tag_lower('unitVision', 'GMenu')
                    self.canvas.tag_lower('unitVision', 'building')
                    self.canvas.tag_lower('unitAttackMode', 'GMenu')
                    self.canvas.tag_raise('unit', 'unitAttackMode')
                except:
                    pass  # un des tags n'existait pas (e.g. unitAttackMode si ennemi)

    def drawBuildings(self, buildings):  # TODO JULIEN DOCSTRING
        self.canvas.delete("ferme")
        self.canvas.delete("base")
        self.canvas.delete("building")  # QUICK FIX

        for building in buildings.values():
            if self.isBuildingShown(building):
                img = building.image
                posX = (building.posX * 48) - (self.cameraX * self.item)
                posY = (building.posY * 48) - (self.cameraY * self.item)
                self.canvas.create_image(posX,
                                         posY,
                                         anchor=NW,
                                         image=img,
                                         tags=('building', building.type, building.id))
                # self.lowerAllItemsOnMap()


                # ANIMATION BLESSURES ET AUTRES
                for anim in building.oneTimeAnimations:
                    imgAnim = anim.activeFrame
                    self.canvas.create_image(posX, posY, anchor=CENTER, image=imgAnim, tags=('building', building.id))
        self.canvas.tag_lower('building', 'GMenu')


    def drawSpecificBuilding(self, building):  # TODO JULIEN DOCSTRING
        img = building.image
        posX = (building.posX * 48) - (self.cameraX * self.item)
        posY = (building.posY * 48) - (self.cameraY * self.item)
        self.canvas.create_image(posX,
                                 posY,
                                 anchor=NW,
                                 image=img,
                                 tags=('building', building.type, building.id))


    def isUnitShown(self, unit):
        """ Renvoie si une unité est visible par la caméra ou non
        :param unit:
        :return: True si l'unité doit être dessiner sinon False
        """
        x1 = self.cameraX * self.item
        y1 = self.cameraY * self.item
        x2 = x1 + (self.nbCasesX * self.item)
        y2 = y1 + (self.nbCasesY * self.item)

        # minimap
        unitX1 = unit.x - unit.grandeur / 2 + unit.grandeur
        unitY1 = unit.y - unit.grandeur / 2 + unit.grandeur
        unitX2 = unit.x + unit.grandeur / 2 - unit.grandeur
        unitY2 = unit.y + unit.grandeur / 2 - unit.grandeur

        if unitX1 > x1 and unitX2 < x2 and unitY1 > y1 and unitY2 < y2 and not unit.inBuilding:
            return True

        return False

    def isBuildingShown(self, building):
        x1 = self.cameraX * self.item
        y1 = self.cameraY * self.item
        x2 = x1 + (self.nbCasesX * self.item)
        y2 = y1 + (self.nbCasesY * self.item)

        cases = self.eventListener.model.trouverCentreCase(building.posX, building.posY)

        batimentX1 = cases[0] - building.tailleX / 2 + building.tailleX
        batimentY1 = cases[1] - building.tailleY / 2 + building.tailleY
        batimentX2 = cases[0] + building.tailleX / 2 - building.tailleX
        batimentY2 = cases[1] + building.tailleY / 2 - building.tailleY

        if batimentX1 > x1 and batimentX2 < x2 and batimentY1 > y1 and batimentY2 < y2:
            return True

        return False


class GameView():
    """ Responsable de l'affichage graphique et de captuer les entrées de l'usager"""

    def __init__(self, window, evListener, joueur):
        self.window = window
        self.canvas = self.window.canvas
        self.joueur = joueur


        # PARAMÈTRES DE BASE
        self.width = self.window.width
        self.height = self.window.height
        self.selected = []  # Liste qui contient ce qui est selectionné (unités ou bâtiments)

        self.width = 1024
        self.height = 768
        self.selected = []  # Liste qui contient ce qui est selectionné (unités ou bâtiments)


        # ZONE DE DESSIN
        self.canvas = self.window.canvas


        # GESTION ÉVÈNEMENTS
        self.eventListener = evListener  # Une Classe d'écoute d'évènement


        # LE HUD
        self.drawHUD()
        self.carte = CarteView(self.canvas, evListener, self.width, self.height, self.frameSide.width,
                               self.frameBottom.height)

        # LIAISON DES ÉVÉNEMENTS
        self.bindEvents()

        self.modeConstruction = False

        # Musique Principale
        if Config.PLAY_MUSIC:
            winsound.PlaySound("Sounds/AgeI.wav", winsound.SND_ASYNC | winsound.SND_LOOP | winsound.SND_FILENAME)







    def drawHUD(self):
        """ Dessine la base du HUD
        """
        # LE CADRE DE LA MINIMAP
        self.frameMinimap = FrameMiniMap(self, self.canvas, self.eventListener)
        self.frameMinimap.draw()

        # LE CADRE DROIT
        self.frameSide = FrameSide(self.canvas, self, self.frameMinimap.width, self.frameMinimap.height,
                                   self.eventListener)
        self.frameSide.draw()
        self.frameSide.drawBaseButton()

        # LE CADRE DU BAS
        self.frameBottom = FrameBottom(self, self.canvas, self.frameMinimap.width)
        self.frameBottom.draw()


    def drawMap(self, carte):
        """ Dessine la carte à l'écran
        :param carte: la carte
        :return:
        """
        self.carte.draw(carte)

    def drawUnits(self, units, carte):
        """ Affiche les unités sur la carte 
        """
        self.carte.drawUnits(units, self.selected, carte)

    def drawMinimap(self, carte):
        """ Permet de dessiner la carte
        :param carte: la carte
        """
        self.frameMinimap.updateMinimap(carte)

    def drawMiniUnits(self, units):
        """ Permet de dessiner les unités sur la minimap
        :param units: les unités
        """
        self.frameMinimap.updateMiniUnits(units)

    def drawBuildings(self, buildings):
        self.carte.drawBuildings(buildings)

    def addBuildingToCursor(self, posX, posY):
        pass


    def drawRectMiniMap(self, clicX=0, clicY=0):
        """ Permet de dessiner la caméra de la MINIMAP
        """
        self.frameMinimap.drawRectMiniMap(clicX, clicY)


    def resetSelection(self):
        """ Met la sélection à 0 (désélection)
        """
        self.selected = []
        if self.frameSide.childView:
            self.frameSide.childView.destroy()

    # TODO ? mettre dans carte ?




    def detectUnits(self, x1, y1, x2, y2, units):
        """ Retourne une liste d'unités faisant partie de la region passé en paramètre
        :param x1: coord x du point haut gauche
        :param y1: coord y du point haut gauche
        :param x2: coord x du point bas droite
        :param y2: coord y du point bas droite
        :return: une liste d'unités
        """
        items = [item for item in self.canvas.find_overlapping(x1, y1, x2, y2) if 'unit' in self.canvas.gettags(item)]
        units = [units[self.canvas.gettags(i)[1]] for i in items]  # Le duexième tag est toujours l'id de l'unité
        return units

    def detectClosestUnitID(self, x, y, rayon=None):
        """ Permet de retourner l'unité la plus proche du point spécifié dans un certain rayon
        :param x: point x
        :param y: point y
        :param rayon: rayon dans lequel on veut chercher le plus proche
        :param units: une listes d'unités potentielles
        :return: l'ID de l'unité la plus proche sinon None
        """
        item = self.canvas.find_closest(x, y, halo=rayon)
        if 'unit' in self.canvas.gettags(item):
            a = self.canvas.gettags(item)

        return None

    def detectBuildings(self, x1, y1, x2, y2, buildings, eventTkinter=True):
        """ Retourne une liste de buildings faisant partie de la region passé en paramètre
        :param x1: coord x du point haut gauche
        :param y1: coord y du point haut gauche
        :param x2: coord x du point bas droite
        :param y2: coord y du point bas droite
        :return: une liste de buildings
        """
        if not eventTkinter:  # Si le x1,y1,x2 et y2 ne viennnent pas d'un event (e.g.: unit.x, unit.y)
            #On converti pour avoir le x/y du canevas
            x1 = x1 - (self.carte.cameraX * self.carte.item)
            y1 = y1 - (self.carte.cameraY * self.carte.item)
            x2 = x2 - (self.carte.cameraX * self.carte.item)
            y2 = y2 - (self.carte.cameraY * self.carte.item)

        items = [item for item in self.canvas.find_overlapping(x1, y1, x2, y2) if
                 'building' in self.canvas.gettags(item)]
        buildings = [buildings[self.canvas.gettags(i)[2]] for i in
                     items]  # Le premier tag est toujours l'id du buildings
        return buildings


    def detectSelected(self, x1, y1, x2, y2, units, buildings, clientId):  # TODO CLEAN UP
        """ Ajoute toutes les unités sélectionné dans le rectangle spécifié
        à la liste d'unité sélectionnées
        :param units: All the possible units
        :param buildings: All the possible buildings
        :param x1: coord x du point haut gauche
        :param y1: coord y du point haut gauche
        :param x2: coord x du point bas droite
        :param y2: coord y du point bas droite
        """
        items = self.canvas.find_overlapping(x1, y1, x2, y2)

        for item in items:
            # :param allTags: devrait avoir l'air de ('type_de_item', 'id_unique')
            allTags = self.canvas.gettags(item)
            if allTags[0] == "base":
                building = buildings[allTags[1]]
                if building.estBatimentDe(self.eventListener.controller.network.getClientId()):
                    print(building.type + ": " + building.id)
                    building.estSelectionne = True
                    return

            elif allTags[0] == "ferme":
                building = buildings[allTags[1]]
                if building.estBatimentDe(self.eventListener.controller.network.getClientId()):
                    print(building.type + ": " + building.id)
                    building.estSelectionne = True
                    return
            elif allTags[0] == "unit":
                unit = units[allTags[1]]
                if unit.estUniteDe(self.eventListener.controller.network.getClientId()):
                    self.selected.append(unit)


    # TODO ? Mettre fonctions du rectangle de sélection dans la classe map ?

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
        """ Lie les évènements de chacun des composantes du gui """

        self.frameMinimap.bindEvents()
        self.carte.bindEvents()

        self.window.root.protocol("WM_DELETE_WINDOW", self.eventListener.onCloseWindow)


    def update(self, units, buildings, carte=None, joueur=None):  # CLEAN UP
        """ Met à jours la carte et la minimap (et leurs unités) (au besoin)"""
        self.joueur = joueur
        if carte:
            self.drawMap(carte)

        self.drawBuildings(buildings)
        self.drawMiniUnits(units)
        self.drawUnits(units, self.eventListener.controller.model.carte.matrice)
        # self.drawBuildings
        # self.frameBottom.updateResources(joueur.ressources)

    def needUpdateCarte(self):
        # print(len(self.eventListener.controller.model.joueurs[self.eventListener.controller.model.civNumber].units))
        try:
            for unite in self.eventListener.controller.model.joueurs[
                self.eventListener.controller.model.civNumber].units.values():
                if self.carte.isUnitShown(unite):
                    if unite.enDeplacement:
                        return True
            return False
        except KeyError:
            pass


    def destroy(self):
        """ Détruit la fenêtre de jeu
        """
        winsound.PlaySound("*", winsound.SND_ALIAS)
        self.window.destroy()


