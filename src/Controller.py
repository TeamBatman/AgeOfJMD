#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Commands import Command
from Model import Model
from NetworkModule import NetworkController, ClientConnectionError
from Units import Unit
from View import View
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
            cmds = self.network.synchronizeClient()
            if cmds:
                for cmd in cmds:
                    self.model.executeCommand(cmd)
        except ClientConnectionError:
            self.shutdown()
        # TODO Faire quelque chose de plus approprié (afficher message? retour au menu principal?)



        self.model.update()

        self.view.update(self.model.units)
        self.view.after(int(1000 / self.refreshRate), self.mainLoop)

    def start(self):
        """ Starts the controller
        """
        self.network.startServer(port=47098)
        self.network.connectClient(ipAddress="10.57.100.152", port=47098)

        self.model.creerJoueur(self.network.getClientId())
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

    def onMapRClick(self, event):
        """ Appelée lorsque le joueur fait un clique droit dans la regions de la map
        """
        x2 = event.x + (self.controller.view.carte.cameraX * self.controller.view.carte.item)
        y2 = event.y + (self.controller.view.carte.cameraY * self.controller.view.carte.item)
        ledearUnit = self.controller.model.trouverPlusProche(self.controller.view.selected, (x2,y2))
        for unitSelected in self.controller.view.selected:
            cmd = Command(self.controller.network.client.id, Command.MOVE_UNIT)
            cmd.addData('ID', unitSelected.id)
            cmd.addData('X1', unitSelected.x)
            cmd.addData('Y1', unitSelected.y)
            cmd.addData('X2', x2)
            cmd.addData('Y2', y2)
            if unitSelected == ledearUnit:
                cmd.addData('LEADER', 1)
                groupe = self.controller.view.selected
                unitSelected.groupe = groupe[:]
                unitSelected.groupe.remove(unitSelected)
            else:
                cmd.addData('LEADER', 2)
            self.controller.network.client.sendCommand(cmd)

    def onMapLPress(self, event):
        """ Appelée lorsque le joueur appuie sur le bouton gauche de sa souris dans la regions de la map
        """
        self.leftClickPos = (event.x, event.y)
        self.controller.view.resetSelection()


    def onMapLRelease(self, event):
        """ Appelée lorsque le joueur lâche le bouton gauche de sa souris dans la regions de la map
        """
        clientId = self.controller.network.getClientId()
        x1, y1 = self.leftClickPos
        x2, y2 = event.x, event.y
        self.controller.view.deleteSelectionSquare()
        self.controller.view.detectSelected(x1, y1, x2, y2, self.controller.model.units, clientId)


    def unitClick(self, event):
        """
        Appelée lorsqu'on clique sur une unité
        :param event:
        """
        clientId = self.controller.network.getClientId()
        x1, y1 = event.x, event.y
        x2, y2 = event.x, event.y
        self.controller.view.detectSelected(x1, y1, x2, y2, self.controller.model.units, clientId)


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

#    def onMouseMotion(self, event):
#        if self.controller.view.width - 233 <= event.x <= self.controller.view.width - 22:
#            if 18 <= event.y <= 229:
#                self.controller.view.deleteSelectionSquare()#selection de la carte


    def onMapCenterClick(self, event):
        """ Appelée lorsque le joueur fait un clique de la mollette """
        # CRÉATION D'UNITÉ
        clientId = self.controller.network.client.id
        cmd = Command(clientId, Command.CREATE_UNIT)
        cmd.addData('ID', Unit.generateId(clientId))
        cmd.addData('X', event.x + (self.controller.view.carte.cameraX * self.controller.view.carte.item))
        cmd.addData('Y', event.y + (self.controller.view.carte.cameraY * self.controller.view.carte.item))
        cmd.addData('CIV', self.controller.model.joueur.civilisation)
        self.controller.network.client.sendCommand(cmd)

    def onMinimapLPress(self, event):
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


        #print(self.controller.view.carte.cameraX, self.controller.view.carte.cameraY)


        self.controller.view.update(self.controller.model.units, self.controller.model.carte.matrice)
        self.controller.view.frameMinimap.drawRectMiniMap(event.x, event.y)


    def onMinimapMouseMotion(self, event):
        """ Appelée lorsque le joueur bouge sa souris dans la regions de la minimap
        """
        self.onMinimapLPress(event)

    def onCloseWindow(self):
        """ Appelée lorsque le joueur ferme la fenêtre """
        self.controller.shutdown()


    def createBuilding(self, param):
        if param == 0:
            print("Create building ferme")
        elif param == 1:
            print("Create building baraque")
        elif param == 2:
            print("Create building hopital")


if __name__ == '__main__':
    app = Controller()
    app.start()
