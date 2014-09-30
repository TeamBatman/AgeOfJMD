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

        else:
        	self.view.drawMinimap(self.model.units, self.model.carte.matrice)
        
        self.view.after(20, self.mainLoop)

    def start(self):
        """ Starts the controller
        """
        self.network.startServer()
        self.network.client.connect()
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

    def onRClick(self, event):
        if event.x < 742 and event.y < 636:
            cmd = Command(self.controller.network.client.id, Command.CREATE_UNIT)
            cmd.addData('X', event.x)
            cmd.addData('Y', event.y)
            self.controller.network.client.sendCommand(cmd)

    def onLClick(self, event):
        print("R-CLICK")
        self.controller.network.stopServer()
        
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
