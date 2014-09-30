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
        self.model = Model()
        self.network = NetworkController()
        self.eventListener = EventListener(self)
        self.view = View(self.eventListener)

    def mainLoop(self):
        cmd = self.network.client.synchronize()
        if cmd:
            self.model.executeCommand(cmd)
        for unit in self.model.units:
            try:
                unit.deplacementTrace()
            except:
                print("fail")
                unit.deplacement()
        self.view.update(self.model.units)
        self.view.after(20, self.mainLoop)

    def start(self):
        """ Starts the controller
        """
        self.network.startServer()
        self.network.client.connect()
        self.mainLoop()
        self.view.show()
    
    def shutdown(self):
        self.view.destroy()
        self.network.client.disconnect()
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

    def onLClick(self, event):
        self.controller.view.selection()

    def onRClick(self, event):
        print("R-CLICK")
        #self.controller.network.stopServer()
        print(self.controller.view.selected)
        for unitSelected in self.controller.view.selected:
            cmd = Command(self.controller.network.client.id, Command.MOVE_UNIT)
            cmd.addData('X1', unitSelected.x)
            cmd.addData('Y1', unitSelected.y)
            cmd.addData('X2', event.x)
            cmd.addData('Y2', event.y)
            self.controller.network.client.sendCommand(cmd)
            #cmd.addData('Unit', unit)
            #unit.changerCible(event.x,event.y)



    def onCenterClick(self, event):
        cmd = Command(self.controller.network.client.id, Command.CREATE_UNIT)
        cmd.addData('X', event.x)
        cmd.addData('Y', event.y)
        self.controller.network.client.sendCommand(cmd)
    
        
    def requestCloseWindow(self):
        self.controller.shutdown()
        
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
