#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Batiments import Batiment

from Commands import Command
from Model import Model
from NetworkModule import NetworkController, ClientConnectionError

from Units import Unit
from View import View, MenuUnit

import sys


class Controller:
    """ Responsable des communications entre le module réseau, la Vue et le Modèle
        de sorte à ce qu'ils n'aient pas accès entre eux directement.
    """

    def __init__(self):
        self.model = Model(self)
        self.network = NetworkController()
        self.eventListener = EventListener(self)
        self.view = View(self.eventListener)
        self.refreshRate = 64  # Nombre de fois par seconde

    def mainLoop(self):

        try:
            cmd = self.network.synchronizeClient()
            if cmd:
                self.model.executeCommand(cmd)
        except ClientConnectionError:
            self.shutdown()
        # TODO Faire quelque chose de plus approprié (afficher message? retour au menu principal?)


        self.model.update()

        self.view.update(self.model.getUnits(), self.model.getBuildings())
        self.view.after(int(1000 / self.refreshRate), self.mainLoop)

    def start(self):
        """ Starts the controller
        """

        self.network.startServer(port=33333)
        self.network.connectClient(ipAddress='127.0.0.1', port=33333)

        cmd = Command(self.network.getClientId(), Command.CREATE_CIVILISATION)
        cmd.addData('ID', self.network.getClientId())
        self.model.creerJoueur(self.network.getClientId())
        self.model.joueur = self.model.joueurs[self.network.getClientId()]



        self.network.client.sendCommand(cmd)
        self.view.drawMinimap(self.model.carte.matrice)
        self.view.drawRectMiniMap()
        self.view.drawMap(self.model.carte.matrice)
        self.mainLoop()



        self.view.show()

    def shutdown(self):
        self.view.destroy()
        if self.network.client:
            self.network.disconnectClient()
        if self.network.server:
            self.network.stopServer()
        sys.exit(0)


class EventListener:
    """ Écoute les évènement de la Vue (en pratique la vue appelle les méthodes de cette classe)
        Et
    """

    def __init__(self, controller):
        self.controller = controller
        self.view = None
        self.model = controller.model

        # Position du dernier clic Gauche sur la carte
        self.leftClickPos = None

    def onMapRClick(self, event, pos2=None):
        """ Appelée lorsque le joueur fait un clique droit dans la regions de la map
        """
        try:
            if pos2:
                x2 = pos2[0]
                y2 = pos2[1]
            else:
                x2 = event.x + (self.controller.view.carte.cameraX * self.controller.view.carte.item)
                y2 = event.y + (self.controller.view.carte.cameraY * self.controller.view.carte.item)
            leaderUnit = self.controller.model.trouverPlusProche(self.controller.view.selected, (x2, y2))
            posFin = self.controller.model.trouverFinMultiSelection(x2, y2, len(self.controller.view.selected) - 1,
                                                                    self.controller.view.selected[0].grandeur)

            groupeSansLeader = self.controller.view.selected[:]
            groupeSansLeader.remove(leaderUnit)
        except IndexError:  # Il n'y rien à l'endroit ou l'on a cliqué
            pass
        # TODO François Check ça
        for unitSelected in groupeSansLeader:
            self.selectionnerUnit(unitSelected, False, posFin, x2, y2)

        self.selectionnerUnit(leaderUnit, True, posFin, x2, y2)  # Faire le leader en dernier

    def selectionnerUnit(self, unitSelected, leaderUnit, posFin, x2, y2):
        """Pour la fonction onMapRClick !!!"""
        cmd = Command(self.controller.network.client.id, Command.MOVE_UNIT)
        cmd.addData('ID', unitSelected.id)
        cmd.addData('X1', unitSelected.x)
        cmd.addData('Y1', unitSelected.y)
        cmd.addData('X2', x2)
        cmd.addData('Y2', y2)
        if leaderUnit:
            cmd.addData('LEADER', 1)
            cmd.addData('FIN', None)
            groupe = self.controller.view.selected[:]
            groupeID = []
            for unit in groupe:
                groupeID.append(unit.id)

            groupeID.remove(unitSelected.id)
            cmd.addData('GROUPE', groupeID)
        else:
            cmd.addData('LEADER', 2)
            cmd.addData('FIN', posFin.pop(0))
            cmd.addData('GROUPE', None)
        self.controller.network.client.sendCommand(cmd)


    def onMapLPress(self, event):
        """ Appelée lorsque le joueur appuie sur le bouton gauche de sa souris dans la regions de la map
        """
        self.leftClickPos = (event.x, event.y)
        self.controller.view.resetSelection()

        if self.controller.view.modeConstruction:
            currentX = event.x + (self.controller.view.carte.cameraX * self.controller.view.carte.item)
            currentY = event.y + (self.controller.view.carte.cameraY * self.controller.view.carte.item)
            clientId = self.controller.network.getClientId()

            cmd = Command(clientId, Command.CREATE_BUILDING)
            cmd.addData('ID', Batiment.generateId(clientId))
            cmd.addData('X', currentX)
            cmd.addData('Y', currentY)
            cmd.addData('CIV', self.model.joueur.civilisation)
            cmd.addData('BTYPE', self.controller.view.lastConstructionType)
            self.controller.network.client.sendCommand(cmd)
            self.controller.view.modeConstruction = False
            print("MODE SELECTION")


    def onMapLRelease(self, event):
        """ Appelée lorsque le joueur lâche le bouton gauche de sa souris dans la regions de la map
        """
        clientId = self.controller.network.getClientId()
        x1, y1 = self.leftClickPos
        x2, y2 = event.x, event.y
        self.controller.view.deleteSelectionSquare()

        # SÉLECTION UNITÉS
        units = self.controller.view.detectUnits(x1, y1, x2, y2, self.model.getUnits())
        if units:
            self.controller.view.selected = [u for u in units if u.estUniteDe(clientId)]
            return

        # SÉLECTION BUILDINGS
        buildings = self.controller.view.detectBuildings(x1, y1, x2, y2, self.model.getBuildings())
        if buildings:
            print("OK")
            self.controller.view.selected = [b for b in buildings if b.estBatimentDe(clientId)]


    def onUnitRClick(self, event):
        """
        Appelée lorsqu'on clique sur une unité avec le bouton droit de la souris
        :param event: Tkinter Event
        """
        clientId = self.controller.network.getClientId()
        x1, y1 = event.x, event.y
        x2, y2 = event.x, event.y
        targetUnit = self.controller.view.detectUnits(x1, y1, x2, y2, self.controller.model.getUnits())[0]
        # if not targetUnit.estUniteDe(clientId):
        for unitSelected in self.controller.view.selected:
            unitSelected.ennemiCible = targetUnit


    def onUnitLClick(self, event):
        """
        Appelée lorsqu'on clique sur une unité avec le bouton gauche de la souris
        :param event: Tkinter Event
        """
        self.controller.view.resetSelection()
        clientId = self.controller.network.getClientId()
        x1, y1 = event.x, event.y
        x2, y2 = event.x, event.y
        unit = self.controller.view.detectUnits(x1, y1, x2, y2, self.controller.model.getUnits())[0]
        self.controller.view.selected.append(unit)
        # TODO REMOVE C'EST JUSTE POUR DES TEST

        try:
            can = self.controller.view.canvas
            unit = self.controller.view.selected[0]
            v = MenuUnit(can, unit, self.controller.view.frameSide, self)
            v.draw()
        except IndexError:
            pass


    def onMapMouseMotion(self, event):
        """ Appelée lorsque le joueur bouge sa souris dans la regions de la map
        """
        x1, y1 = self.leftClickPos
        x2, y2 = event.x, event.y

        if x2 > self.controller.view.carte.width:
            x2 = self.controller.view.carte.width

        if y2 > self.controller.view.carte.height:
            y2 = self.controller.view.carte.height

        self.controller.view.carreSelection(x1, y1, x2, y2)


    def onMapCenterClick(self, event):
        """ Appelée lorsque le joueur fait un clique de la mollette """

        if self.controller.view.modeConstruction:
            self.controller.view.modeConstruction = False
            print("MODE SELECTION")
            self.controller.view.frameSide.draw()
            # self.controller.view.frameSide.drawSideButton()
        else:
            # CRÉATION D'UNITÉ
            clientId = self.controller.network.client.id
            cmd = Command(clientId, Command.CREATE_UNIT)
            cmd.addData('ID', Unit.generateId(clientId))
            cmd.addData('X', event.x + (self.controller.view.carte.cameraX * self.controller.view.carte.item))
            cmd.addData('Y', event.y + (self.controller.view.carte.cameraY * self.controller.view.carte.item))
            cmd.addData('CIV', self.controller.model.joueur.civilisation)
            self.controller.network.client.sendCommand(cmd)


    def onMinimapLPress(self, event, redo=0):
        """ Appelée lorsque le joueur appuis sur le bouton gauche de sa souris 
        dans la regions de la minimap
        """
        self.controller.view.deleteSelectionSquare()  # déselection des unités de la carte

        # BOUGER LA CAMÉRA

        miniMapX = self.controller.view.frameMinimap.miniMapX
        MiniMapY = self.controller.view.frameMinimap.miniMapY
        miniCamX = self.controller.view.frameMinimap.miniCameraX
        miniCamY = self.controller.view.frameMinimap.miniCameraY
        tailleMiniTuile = self.controller.view.frameMinimap.tailleTuile

        # CONVERTIR POSITION DE LA MINI CAMÉRA EN COORDONNÉES TUILES ET L'ATTRIBUER À CAMÉRA CARTE
        # Numéro de tuile à afficher dans coin haut gauche de carte en X et Y
        self.controller.view.carte.cameraX = int((miniCamX - miniMapX) / tailleMiniTuile)
        self.controller.view.carte.cameraY = int((miniCamY - MiniMapY) / tailleMiniTuile)


        # print(self.controller.view.carte.cameraX, self.controller.view.carte.cameraY)


        self.controller.view.update(self.controller.model.getUnits(), self.controller.model.getBuildings(),
                                    self.controller.model.carte.matrice)
        self.controller.view.frameMinimap.drawRectMiniMap(event.x, event.y)
        if redo == 0:  #QUICK FIX
            #print("cam",self.controller.view.carte.cameraX , self.controller.view.carte.cameraY)
            self.onMinimapLPress(event, -1)

    def onMinimapMouseMotion(self, event):
        """ Appelée lorsque le joueur bouge sa souris dans la regions de la minimap
        """
        self.onMinimapLPress(event)

    def onCloseWindow(self):
        """ Appelée lorsque le joueur ferme la fenêtre """
        self.controller.shutdown()


    def createBuilding(self, param):
        if param == Batiment.FERME:
            print("Create building ferme")
            self.controller.view.lastConstructionType = Batiment.FERME
            self.controller.view.modeConstruction = True

            if not self.controller.view.modeConstruction:
                print("oups")
            else:
                print("MODE CONSTRUCTION")


        elif param == Batiment.BARAQUE:
            print("Create building baraque")


        elif param == Batiment.HOPITAL:
            print("Create building hopital")


        elif param == Batiment.BASE:
            print("Create building base")
            self.controller.view.lastConstructionType = Batiment.BASE
            self.controller.view.modeConstruction = True

            if not self.controller.view.modeConstruction:
                print("oups")
            else:
                print("MODE CONSTRUCTION")


if __name__ == '__main__':
    app = Controller()
    app.start()
