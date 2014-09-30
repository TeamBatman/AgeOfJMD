#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Commands import Command
from Model import Model
from NetworkModule import NetworkController
from View import View


class Controller:
    """ Responsable des communications entre le module réseau, la Vue et le Modèle
        de sorte à ce qu'ils n'aient pas accès entre eux directement.
    """
    def __init__(self):
        self.model = Model()
        self.network = NetworkController()
        self.eventListener = EventListener(self)
        self.view = View(self.eventListener)

    def mainLoop(self):
        cmd = self.network.client.synchronize()
        if cmd:

            self.model.executeCommand(cmd)
            self.view.update(self.model.units, self.model.carte.matrice)

        #else:
        #    self.view.canvas.delete('miniMap')
        #    self.view.drawMinimap(self.model.units, self.model.carte.matrice)
        
        self.view.after(20, self.mainLoop)

    def start(self):
        """ Starts the controller
        """
        self.network.startServer()
        self.network.client.connect()
        self.view.drawMinimap(self.model.units, self.model.carte.matrice)
        self.mainLoop()
        self.view.show()

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

    def onLClick(self, event):
        if event.x < 742 and event.y < 636:
            cmd = Command(self.controller.network.client.id, Command.CREATE_UNIT)
            cmd.addData('X', event.x)
            cmd.addData('Y', event.y)
            self.controller.network.client.sendCommand(cmd)

        if event.x >= self.controller.view.width - 233 and event.x <= self.controller.view.width - 22:
            if event.y >= 18 and event.y <= 229:
                self.controller.view.positionX = int((event.x - self.controller.view.width-233)/2)+233
                self.controller.view.positionY = int((event.y - 18) /2)

                print(self.controller.view.positionX)

                self.controller.view.drawMinimap(self.controller.model.units,self.controller.model.carte.matrice)

    def onRClick(self, event):
        print("R-CLICK")

        if event.x >= self.controller.view.width - 233 and event.x <= self.controller.view.width - 22:
            if event.y >= 18 and event.y <= 229:
                print("YES")

        #self.controller.network.stopServer()
        
    def createBuilding(self,param):
        if param == 0:
            print("Create building ferme")
        elif param == 1:
            print("Create building baraque")
        elif param == 2:
            print("Create building hopital")










if __name__ == '__main__':
    app = Controller()
    app.start()
