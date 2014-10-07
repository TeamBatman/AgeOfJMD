#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Commands import Command
from Model import Model
from NetworkModule import NetworkController
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
        command = self.network.client.synchronize()
        if command:
            self.model.executeCommand(command)

        self.model.update()

        self.view.update(self.model.units)
        self.view.after(int(1000 / self.refreshRate), self.mainLoop)

    def start(self):
        """ Starts the controller
        """
        self.network.startServer()
        self.network.connectClient()
        self.view.drawMinimap(self.model.units, self.model.carte.matrice)
        self.view.drawRectMiniMap()
        self.view.drawMap(self.model.carte.matrice)
        self.mainLoop()
        self.view.show()

    def shutdown(self):
        self.view.destroy()
        self.network.disconnectClient()
        if self.network.server:
            self.network.stopServer()
        sys.exit(0)


    def actionListener(self, userInput, info):
        """ Méthode utilisée par la vue pour notifier le contrôleur des

        :param userInput:
        :param info:
        """


class EventListener:
    """ Écoute les évènement de la Vue (en pratique la vue appelle les méthodes de cette classe)
        Et
    """

    def __init__(self, controller):
        self.controller = controller
        self.leftClickPos = None


    def onRClick(self, event):
        # print(self.controller.view.selected)
        for unitSelected in self.controller.view.selected:
            cmd = Command(self.controller.network.client.id, Command.MOVE_UNIT)
            cmd.addData('X1', unitSelected.x)
            cmd.addData('Y1', unitSelected.y)
            cmd.addData('X2', event.x + (self.controller.view.positionX * self.controller.view.item))
            cmd.addData('Y2', event.y + (self.controller.view.positionY * self.controller.view.item))
            self.controller.network.client.sendCommand(cmd)

    def onLPress(self, event):
        self.leftClickPos = (event.x, event.y)
        self.controller.view.resetSelection()

    def onLRelease(self, event):

        if self.controller.view.width - 233 <= event.x <= self.controller.view.width - 22:
            if 18 <= event.y <= 229:
                self.controller.view.positionX = int((event.x - self.controller.view.width - 233) / 2) + 233
                self.controller.view.positionY = int((event.y - 18) / 2)
                # self.controller.view.drawMinimap(self.controller.model.units,self.controller.model.carte.matrice)
                self.controller.view.update(self.controller.model.units, self.controller.model.carte.matrice)
        else:
            x1, y1 = self.leftClickPos
            x2, y2 = event.x, event.y
            self.controller.view.deleteSelectionSquare()
            self.controller.view.detectSelected(x1, y1, x2, y2, self.controller.model.units)

    def onMouseMotion(self, event):
        x1, y1 = self.leftClickPos
        x2, y2 = event.x, event.y

        # TODO Mettre maximum en x et en y pour ne pas prolonger la sélection dans les panneaux
        self.controller.view.carreSelection(x1, y1, x2, y2)




    def onCenterClick(self, event):
        cmd = Command(self.controller.network.client.id, Command.CREATE_UNIT)
        cmd.addData('X', event.x + (self.controller.view.positionX * self.controller.view.item))
        cmd.addData('Y', event.y + (self.controller.view.positionY * self.controller.view.item))
        self.controller.network.client.sendCommand(cmd)

    def requestCloseWindow(self):
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
