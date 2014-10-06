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
        for paysan in self.model.enRessource:
            if paysan.mode == 1:
                paysan.chercherRessources()
            else:
                del paysan
        self.view.update(self.model.units)
        self.view.after(20, self.mainLoop)

    def start(self):
        """ Starts the controller
        """
        self.network.startServer()
        self.network.client.connect()
        self.view.drawMinimap(self.model.units, self.model.carte.matrice)
        self.view.drawRectMiniMap()
        self.view.drawMap(self.model.carte.matrice)
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
        if event.x < 742 and event.y < 636:
            self.controller.view.selection()
            self.controller.view.update(self.controller.model.units, None)

        if event.x >= self.controller.view.width - 233 and event.x <= self.controller.view.width - 22:
            if event.y >= 18 and event.y <= 229:
                self.controller.view.positionX = int((event.x - self.controller.view.width-233)/2)+233
                self.controller.view.positionY = int((event.y - 18) /2)
                #self.controller.view.drawMinimap(self.controller.model.units,self.controller.model.carte.matrice)
                self.controller.view.update(self.controller.model.units, self.controller.model.carte.matrice)

    def onRClick(self, event):
        for unitSelected in self.controller.view.selected:
            cmd = Command(self.controller.network.client.id, Command.MOVE_UNIT)
            cmd.addData('X1', unitSelected.x)
            cmd.addData('Y1', unitSelected.y)
            cmd.addData('X2', event.x + (self.controller.view.positionX*self.controller.view.item))
            cmd.addData('Y2', event.y + (self.controller.view.positionY*self.controller.view.item))
            self.controller.network.client.sendCommand(cmd)

        
    #def onRClick(self, event):
        #if event.x >= self.controller.view.width - 233 and event.x <= self.controller.view.width - 22:
            #if event.y >= 18 and event.y <= 229:
            	#pass
        #self.controller.network.stopServer()



    def onCenterClick(self, event):
        cmd = Command(self.controller.network.client.id, Command.CREATE_UNIT)
        cmd.addData('X', event.x + (self.controller.view.positionX*self.controller.view.item))
        cmd.addData('Y', event.y + (self.controller.view.positionY*self.controller.view.item))
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
