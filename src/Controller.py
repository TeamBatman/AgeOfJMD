#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import sys
from tkinter import ALL

from Batiments import Batiment
from Commands import Command
import GraphicsManagement
from LoadingScreen import ResourceLoader, LoadingScreen
from Model import Model
from NetworkModule import NetworkController, ClientConnectionError, Client
import NetworkModule
from TitleScreen import TitleScreen
from Units import Unit
from Units import Noeud
from View import GameView, FrameSide
from GameWindow import GameWindow
from SimpleTimer import Timer

import Config

import MenuDebut


SKIP_MENU = False  # Permet de skipper les menus
LOAD_RESSOURCE_ON_START = True  # Si on load les ressources au démarrage du jeu ou non


try:
    from tkinter import Event  # Python 3
except ImportError:
    from Tkinter import Event  # Python 2



class Controller:
    """ Responsable des communications entre le module réseau, la Vue et le Modèle
        de sorte à ce qu'ils n'aient pas accès entre eux directement.
    """


    def __init__(self):
        self.model = Model(self)
        self.network = NetworkController()
        self.eventListener = EventListener(self)
        self.window = GameWindow()
        self.view = None


        self.currentFrame = -1
        self.nbFramesPerSecond = 15
        self.refreshRate = int(1000 / self.nbFramesPerSecond)

        self.displayTimer = Timer(1000 / 60)  # Pour limiter nombre de rafraichissement du GUI (60 FPS ~ 16ms)
        self.loadingThread = None

        self.gameStarted = False

    def updateRefreshRate(self):
        self.refreshRate = int(1000 / self.nbFramesPerSecond)

    def mainLoop(self):
        if self.network.client is not None:
            cmd = []
            try:
                #print(self.currentFrame)
                cmd = self.network.synchronizeClient(self.currentFrame)
            except (ClientConnectionError, KeyError):
                self.gameStarted = False
            # TODO Faire quelque chose de plus approprié (afficher message? retour au menu principal?)

            for c in cmd:
                print(c['TYPE'])
                if c['TYPE'] == Command.START_GAME:
                    self.startGame()

        if not self.gameStarted:
            self.titleScreenLoop()
        else:
            self.gameLoop(cmd)

        self.window.after(self.refreshRate, self.mainLoop)

    def gameLoop(self, cmd):
        self.doLogic(cmd)
        self.renderGraphics()


    def startGame(self):

        self.window.canvas.delete(ALL)
        print(self.window.root.update())
        #self.view = GameView(self.window, self.eventListener,)

        cmd = Command(self.network.getClientId(), Command.CIVILISATION_CREATE)
        cmd.addData('ID', self.network.getClientId())
        self.sendCommand(cmd)
        self.model.creerJoueur(self.network.getClientId())
        self.model.joueur = self.model.joueurs[self.network.getClientId()]
        self.model.civNumber = self.network.getClientId()

        self.gameStarted = True


        self.view = GameView(self.window, self.eventListener, joueur=self.model.joueurs[self.model.civNumber])
        self.view.drawMinimap(self.model.carte.matrice)
        self.view.drawRectMiniMap()
        self.view.drawMap(self.model.carte.matrice)






    def doLogic(self, commands):
        """ Une itération sur cette fonction constitue une FRAME
        :return:
        """
        doUpdate = True
        for command in commands:
            if command['TYPE'] == Command.WAIT:
                doUpdate = False
            elif command['TYPE'] == Command.DESYNC:
                Client.outputDebug("Votre client est DÉSYNCHRONISÉ")
                self.shutdown()  # TODO Afficher message
            else:
                self.model.executeCommand(command)

        if doUpdate:
            self.model.update()
            # print("Finnished %s" % self.currentFrame)
            self.currentFrame += 1

    def renderGraphics(self):
        """ Méthode principale d'affichage des Graphics
        :return:
        """
        joueur = self.model.joueurs[self.model.civNumber]
        if self.displayTimer.isDone():
            #if self.view.needUpdateCarte():
            #    self.view.update(self.model.getUnits(), self.model.getBuildings(),self.model.carte.matrice, joueur=joueur)
            #else:
            try:
                self.view.update(self.model.getUnits(), self.model.getBuildings(), joueur=joueur)
            except TypeError:
                pass

            self.displayTimer.reset()

    def startSoloGame(self):
         # INITIALISATION RÉSEAU
        self.network.startServer(port=33333)
        self.network.connectClient(ipAddress=NetworkModule.detectIP(), port=33333, playerName='Batman')

        # INITIALISATION MODEL
        cmd = Command(cmdType=Command.START_GAME)
        cmd.addData('SEED', random.randint(0, 2000))
        self.sendCommand(cmd)


        cmd = Command(self.network.getClientId(), Command.CIVILISATION_CREATE)
        cmd.addData('ID', self.network.getClientId())
        self.sendCommand(cmd)
        self.model.creerJoueur(self.network.getClientId())
        self.model.joueur = self.model.joueurs[self.network.getClientId()]
        self.model.civNumber = self.network.getClientId()

        self.gameStarted = True



        aiId = self.model.civNumber + 1
        if aiId > 8:
             aiId = 0

        self.model.creerAI(aiId)
        self.model.creerbaseAI(aiId)

        # INITIALISATION AFFICHAGE
        self.view = GameView(self.window, self.eventListener, self.model.joueurs[self.model.civNumber])
        self.view.drawMinimap(self.model.carte.matrice)
        self.view.drawRectMiniMap()
        self.view.drawMap(self.model.carte.matrice)

    def start(self):
        """ Starts the controller
        """

        # TIMERS
        self.displayTimer.start()

        # FRAMES
        self.currentFrame = 0

        if not Config.SKIP_LOADING:
            self.view = LoadingScreen(self.window, self)
            self.graphicsLoader = ResourceLoader(GraphicsManagement.detectGraphics(), self.view)
        else:
            if Config.SKIP_MENU:
               self.startSoloGame()
            else:
                self.graphicsLoader = ResourceLoader(GraphicsManagement.detectGraphics(), self.view)
                self.graphicsLoader.isDone = True
                self.view = TitleScreen(self.window, self)
                self.catchMenuEvent(MenuDebut.TitleEvent.VOIR_MENU_PRINCIPAL)
        self.mainLoop()
        self.window.show()







    def catchMenuEvent(self, event, additionalData=None):
        """ Événement actionné par l'usager durant l'écran titre
        :param event: L'évenement à gérer
        :param additionalData: paramètre additionnel accompagnant l'action
        """
        # Affichage Menus
        if event == MenuDebut.TitleEvent.VOIR_MENU_PRINCIPAL:
            self.view.changerMenu(MenuDebut.MenuPrincipal(self.window, self))
            self.view.drawMenu()

        elif event == MenuDebut.TitleEvent.VOIR_MENU_MULTIJOUEUR:
            self.view.changerMenu(MenuDebut.MenuMultijoueur(self.window, self))
            self.view.drawMenu()

        elif event == MenuDebut.TitleEvent.VOIR_MENU_CREER_SERVEUR:
            print(NetworkModule.detectIP())
            self.view.changerMenu(MenuDebut.MenuServeur(self.window, self, NetworkModule.detectIP()))
            self.view.drawMenu()

        elif event == MenuDebut.TitleEvent.VOIR_MENU_REJOINDRE_SERVEUR:
            self.view.changerMenu(MenuDebut.MenuRejoindreServeur(self.window, self))
            self.view.drawMenu()


        elif event == MenuDebut.TitleEvent.VOIR_MENU_SOLO:
            self.view.changerMenu(MenuDebut.MenuSolo(self.window, self))
            self.view.drawMenu()

        elif event == MenuDebut.TitleEvent.LANCER_PARTIE_SOLO:
            self.nbFramesPerSecond *= int(additionalData)
            self.updateRefreshRate()
            self.view.destroy()
            self.startSoloGame()

        elif event == MenuDebut.TitleEvent.QUITTER_JEU:
            self.shutdown()

        elif event == MenuDebut.TitleEvent.CREER_SERVEUR:
            nomJoueur = self.view.menuActif.nomJoueur

            self.network.startServer(port=33333)
            self.network.connectClient(ipAddress=NetworkModule.detectIP(), port=33333, playerName=nomJoueur)
            self.view.changerMenu(MenuDebut.MenuLobby(self.window, self, self.network.isClientHost()))
            self.view.drawMenu()

        elif event == MenuDebut.TitleEvent.REJOINDRE_SERVEUR:
            IPJoueur = self.view.menuActif.IPJoueur
            nomJoueur = self.view.menuActif.nomJoueur
            self.network.connectClient(ipAddress=IPJoueur, port=33333, playerName=nomJoueur)
            self.view.changerMenu(MenuDebut.MenuLobby(self.window, self, self.network.isClientHost()))
            self.view.drawMenu()

        elif event == MenuDebut.TitleEvent.ARRETER_SERVEUR:
            if self.network.client:
                self.network.disconnectClient()
            if self.network.server:
                self.network.stopServer()
            self.catchMenuEvent(MenuDebut.TitleEvent.VOIR_MENU_MULTIJOUEUR)

        elif event == MenuDebut.TitleEvent.LANCER_PARTIE_MULTIJOUEUR:
            print("PARTIE MULTI")
            cmd = Command(cmdType=Command.START_GAME)
            cmd.addData('SEED', random.randint(0, 2000))
            self.sendCommand(cmd)



    def titleScreenLoop(self):
        if not self.graphicsLoader.isDone:
            if self.window.isShown:
                self.graphicsLoader.run()
                if Config.SKIP_MENU:
                    self.view.destroy()
                    self.startSoloGame()
                    return
                else:
                    self.view = TitleScreen(self.window, self)

                    self.catchMenuEvent(MenuDebut.TitleEvent.VOIR_MENU_PRINCIPAL)

        if self.displayTimer.isDone():
                if isinstance(self.view, LoadingScreen):
                    self.view.update(self.graphicsLoader.progression)
                else:
                    self.view.update()
                    if isinstance(self.view.menuActif, MenuDebut.MenuLobby):
                        self.view.menuActif.update(self.network.client.host.getClients())
                self.displayTimer.reset()



    def shutdown(self):

        self.window.destroy()

        if self.network.client:
            self.network.disconnectClient()
        if self.network.server:
            self.network.stopServer()
        sys.exit(0)


    def sendCommand(self, command):
        """ Raccourci permettant d'envoyer une commande au serveur
        en passant par le network module
        """
        if command.clientId == -1:
            command.clientId = self.network.client.id
        self.network.client.sendCommand(command, self.currentFrame)


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

    def onMapRClick(self, event, groupe=None, building = None, attackedBuildingId = None):
        """ Appelée lorsque le joueur fait un clique droit dans la regions de la map
        :param event: Tkinter Event
        :param groupe: l'ensemble des unités qui veulent se déplacer
        :param building: le building à construire
        """
        try:
            if isinstance(event,Event): #Savoir si l'event vient de Tkinter ou du programme
                eventTkinter = True
                x2 = event.x + (self.controller.view.carte.cameraX * self.controller.view.carte.item)
                y2 = event.y + (self.controller.view.carte.cameraY * self.controller.view.carte.item)
            else:
                eventTkinter = False
                x2 = event.x
                y2 = event.y

            print("DEPLACEMENT !!!!:::", x2, y2, " vs ", event.x, event.y, event)
            if not groupe:
                groupe = self.controller.view.selected[:]
                if isinstance(groupe[0], Batiment):
                    print("batiment")
                    return
                print(groupe)
            leaderUnit = self.controller.model.trouverPlusProche(groupe, (x2, y2))

            #Pour aller sur un batiment
            posFin = None
            carte = self.model.carte.matrice
            cases = self.model.trouverCaseMatrice(x2,y2)
            if not carte[cases[0]][cases[1]].isWalkable and carte[cases[0]][cases[1]].type == 5:
                buildingDetected = self.controller.view.detectBuildings(x2, y2, x2, y2, self.model.getBuildings(),eventTkinter)[0]
                if buildingDetected.peutEtreOccupe:
                    posFin = []
                    for i in range(len(groupe)-1):
                        posFin.append((x2,y2))
            if posFin == None:
                posFin = self.controller.model.trouverFinMultiSelection(x2, y2, len(groupe) - 1,
                                                                    groupe[0].grandeur)

            groupeSansLeader = groupe[:]
            groupeSansLeader.remove(leaderUnit)
        except IndexError:  # Il n'y rien à l'endroit ou l'on a cliqué
            print("index !")
            groupeSansLeader = []
            pass
        # TODO François Check ça
        for unitSelected in groupeSansLeader:
            self.selectionnerUnit(unitSelected, False, posFin, x2, y2, groupe, None, building, attackedBuildingId, eventTkinter)

        self.selectionnerUnit(leaderUnit, True, posFin, x2, y2, groupe[:], None, building, attackedBuildingId, eventTkinter)  # Faire le leader en dernier

    def selectionnerUnit(self, unitSelected, leaderUnit, posFin, x2, y2,groupe, targetUnit = None, building = None, attackedBuildingId = None, eventTkinter = False):
        """Pour la fonction onMapRClick !!!"""
        # print("select", leaderUnit)
        cmd = Command(self.controller.network.client.id, Command.UNIT_MOVE)
        cmd.addData('ID', unitSelected.id)
        cmd.addData('X1', unitSelected.x)
        cmd.addData('Y1', unitSelected.y)
        cmd.addData('X2', x2)
        cmd.addData('Y2', y2)
        cmd.addData('BTYPE', building)
        cmd.addData('ABID', attackedBuildingId)
        cmd.addData('ISEVENT', eventTkinter)
        if targetUnit:
            cmd.addData('ENNEMI', targetUnit.id)
        else:
            cmd.addData('ENNEMI', None)
        #print("leader selection", leaderUnit)
        if leaderUnit:
            cmd.addData('LEADER', 1)

            if posFin:
                posLeader = posFin.pop(0)
                print("leader KOMBAT!", posLeader)
                cmd.addData('FIN', posLeader)
            else:
                cmd.addData('FIN', None)
            #groupe = self.controller.view.selected[:]
            groupeID = []
            for unit in groupe:
                groupeID.append(unit.id)
            try:
                groupeID.remove(unitSelected.id)
            except:
                print("leader pas dans la list !")
            cmd.addData('GROUPE', groupeID)
        else:
            if unitSelected.leader == 1:
                print("changement leader")
            else:
                print("pas changment leader", unitSelected.id, unitSelected.leader)

            cmd.addData('LEADER', 2)
            cmd.addData('FIN', posFin.pop(0))
            cmd.addData('GROUPE', None)
        self.controller.sendCommand(cmd)


    def onMapLPress(self, event):
        """ Appelée lorsque le joueur appuie sur le bouton gauche de sa souris dans la regions de la map
        """
        print("PRESS")
        self.leftClickPos = (event.x, event.y)
        if not self.controller.view.modeConstruction:
            self.controller.view.resetSelection()
        else:
            self.onMapLRelease(event) #QUICK FIX


    def onMapLRelease(self, event):
        """ Appelée lorsque le joueur lâche le bouton gauche de sa souris dans la regions de la map
        """
        print("RELEASE")
        clientId = self.controller.network.getClientId()
        x1, y1 = self.leftClickPos
        x2, y2 = event.x, event.y

        self.controller.view.deleteSelectionSquare()

        # SÉLECTION BUILDINGS
        buildings = self.controller.view.detectBuildings(x1, y1, x2, y2, self.model.getBuildings())
        if buildings:
            for b in buildings:
                print("building", b.type)
                if b.estBatimentDe(clientId):
                    if b.type == Batiment.BASE:
                        self.controller.view.frameSide.changeView(FrameSide.BASEVIEW, b)
                    elif b.type == Batiment.FERME:
                        self.controller.view.frameSide.changeView(FrameSide.FARMVIEW, b)
                    elif b.type == Batiment.BARAQUE:
                        self.controller.view.frameSide.changeView(FrameSide.BARACKVIEW, b)
            self.controller.view.selected = [b for b in buildings if b.estBatimentDe(clientId)]
        print("modeConstruct", self.controller.view.modeConstruction)
        if self.controller.view.modeConstruction:
            currentX = event.x + (self.controller.view.carte.cameraX * self.controller.view.carte.item)
            currentY = event.y + (self.controller.view.carte.cameraY * self.controller.view.carte.item)
            clientId = self.controller.network.getClientId()

            idBatiment = Batiment.generateId(clientId)
            civ =  self.model.civNumber
            bType =  self.controller.view.lastConstructionType

            self.envoyerCommandBatiment(idBatiment, currentX, currentY, self.controller.view.selected[:], bType, civ)
            self.controller.view.modeConstruction = False
            print("MODE SELECTION")
            return

        # SÉLECTION UNITÉS
        units = self.controller.view.detectUnits(x1, y1, x2, y2, self.model.getUnits())
        if units:
            self.controller.view.selected = [u for u in units if u.estUniteDe(clientId)]
            self.controller.view.frameSide.changeView(FrameSide.UNITVIEW)
            return


    def envoyerCommandBatiment(self,idBatiment, posX, posY, unitsSelected, bType, civ = None):
        print("ENVOYER BATIMENT")
        caseX, caseY = self.model.trouverCaseMatrice(posX, posY)
        if self.model.validPosBuilding(caseX, caseY) and unitsSelected:
            tropProche = False
            caseUnitX, caseUnitY = self.model.trouverCaseMatrice(unitsSelected[0].x, unitsSelected[0].y)
            if abs(caseUnitX - caseX) + abs(caseUnitY - caseY) <= 1:
                tropProche = True
            else:
                self.controller.eventListener.onMapRClick(Noeud(None, posX, posY, None, None), unitsSelected, (idBatiment, bType))

        if bType == 0 or tropProche: #Base TEMPORAIRE !
            clientId = self.controller.network.getClientId()
            cmd = Command(clientId, Command.BUILDING_CREATE)
            cmd.addData('ID', idBatiment)
            cmd.addData('X', posX)
            cmd.addData('Y', posY)
            cmd.addData('CIV', clientId)
            cmd.addData('UNITS', [])
            cmd.addData('BTYPE', bType)
            self.controller.sendCommand(cmd)

    def onUnitRClick(self, event, groupeSansLeader=None):
        """
        Appelée lorsqu'on clique sur une unité avec le bouton droit de la souris
        :param event: Tkinter Event
        """
        print(event)
        clientId = self.controller.network.getClientId()

        x1, y1 = event.x, event.y
        # x2, y2 = event.x, event.y
        if isinstance(event,Event): #Savoir si l'event vient de Tkinter ou du programme
            eventTkinter = True
            x2 = event.x + (self.controller.view.carte.cameraX * self.controller.view.carte.item)
            y2 = event.y + (self.controller.view.carte.cameraY * self.controller.view.carte.item)
        else:
            eventTkinter = False
            x2 = event.x
            y2 = event.y
        # print("dude!", x2, y2)
        targetUnit = self.controller.view.detectUnits(x1, y1, x2, y2, self.controller.model.getUnits())[0]
        if targetUnit.civilisation == self.model.joueur.civilisation:
            return #Ne peux pas attaquer sa civilisation
        #TODO: Merge avec onMapRClick !!!
        try:
            groupe = groupeSansLeader
            if not groupeSansLeader:
                groupeSansLeader = self.controller.view.selected[:]
                groupe = None

            #x2 = event.x + (self.controller.view.carte.cameraX * self.controller.view.carte.item)
            #y2 = event.y + (self.controller.view.carte.cameraY * self.controller.view.carte.item)
            leaderUnit = self.controller.model.trouverPlusProche(groupeSansLeader, (x2, y2))
            posFin = self.controller.model.trouverFinMultiSelection(x2, y2, len(groupeSansLeader),
                                                                    groupeSansLeader[0].grandeur)
            if groupe == None:
                groupeSansLeader.remove(leaderUnit)

                #groupeSansLeader = self.controller.view.selected[:]

        except IndexError:  # Il n'y rien à l'endroit ou l'on a cliqué
            print("index 2 !")
            groupeSansLeader = []
        #    pass
        # TODO François Check ça
        for unitSelected in groupeSansLeader:
            unitSelected.ennemiCible = targetUnit
            unitSelected.ancienPosEnnemi = (targetUnit.x, targetUnit.y)
            unitSelected.mode = 3
            #print("-----posFIn",len(posFin))
            #print("posFin", posFin)
            self.selectionnerUnit(unitSelected, False, posFin, x2, y2,None, unitSelected.ennemiCible, None, None, eventTkinter)

        leaderUnit.ennemiCible = targetUnit
        leaderUnit.ancienPosEnnemi = (targetUnit.x, targetUnit.y)
        leaderUnit.mode = 3
        #print("posFIn leader", posFin)
        self.selectionnerUnit(leaderUnit, True, posFin, x2, y2, groupeSansLeader,
                              leaderUnit.ennemiCible, None, None, eventTkinter)  # Faire le leader en dernier

        # if not targetUnit.estUniteDe(clientId):
        #leaderUnit = self.controller.model.trouverPlusProche(self.controller.view.selected, (x2, y2))
        #for unitSelected in self.controller.view.selected:
        #    unitSelected.ennemiCible = targetUnit
        #    if unitSelected == leaderUnit:
        #        print("leader KOMBAT !!")
        #        #self.selectionnerUnit(unitSelected, True, None, x2, y2)
        #    else:
        #        print("KOMBAT PAS LEADER !!")
        #        self.selectionnerUnit(unitSelected, False, None, x2, y2)
        #self.selectionnerUnit(leaderUnit, True, [0], x2, y2)

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
        if unit.estUniteDe(clientId):
            self.controller.view.selected.append(unit)
            self.controller.view.frameSide.changeView(FrameSide.UNITVIEW)
        # TODO REMOVE C'EST JUSTE POUR DES TEST

    def onBuildingRClick(self, event):
        """
        Appelée lorsqu'on clique sur un bâtiment avec le bouton droite de la souris
        :param event: Tkinter Event
        """
        if isinstance(event,Event): #Savoir si l'event vient de Tkinter ou du programme
            eventTkinter = True
        else:
            eventTkinter = False
        building = self.controller.view.detectBuildings(event.x, event.y,event.x, event.y, self.controller.model.getBuildings(),eventTkinter)[0]
        if not building.estBatimentDe(self.model.joueur.civilisation):
            print("click sur building ennemi")
            self.onMapRClick(event, attackedBuildingId=building.id)

        elif building.type == Batiment.FERME:
            print("Rentre dans batiment")
            self.onMapRClick(event)


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
            cmd = Command(clientId, Command.UNIT_CREATE)
            cmd.addData('ID', Unit.generateId(clientId))
            cmd.addData('X', event.x + (self.controller.view.carte.cameraX * self.controller.view.carte.item))
            cmd.addData('Y', event.y + (self.controller.view.carte.cameraY * self.controller.view.carte.item))
            cmd.addData('CIV', self.controller.model.joueur.civilisation)
            self.controller.sendCommand(cmd)


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

        if self.controller.view.modeConstruction:
            currentX = event.x + (self.controller.view.carte.cameraX * self.controller.view.carte.item)
            currentY = event.y + (self.controller.view.carte.cameraY * self.controller.view.carte.item)
            clientId = self.controller.network.getClientId()

            cmd = Command(clientId, Command.BUILDING_CREATE)
            cmd.addData('ID', Batiment.generateId(clientId))
            cmd.addData('X', currentX)
            cmd.addData('Y', currentY)
            cmd.addData('CIV', self.model.joueur.civilisation)
            cmd.addData('BTYPE', self.controller.view.lastConstructionType)
            self.controller.sendCommand(cmd)
            self.controller.view.modeConstruction = False
            print("MODE SELECTION")



        # CONVERTIR POSITION DE LA MINI CAMÉRA EN COORDONNÉES TUILES ET L'ATTRIBUER À CAMÉRA CARTE
        # Numéro de tuile à afficher dans coin haut gauche de carte en X et Y
        self.controller.view.carte.cameraX = int((miniCamX - miniMapX) / tailleMiniTuile)
        self.controller.view.carte.cameraY = int((miniCamY - MiniMapY) / tailleMiniTuile)

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
            cmd = Command(clientId, Command.UNIT_CREATE)
            cmd.addData('ID', Unit.generateId(clientId))
            cmd.addData('X', event.x + (self.controller.view.carte.cameraX * self.controller.view.carte.item))
            cmd.addData('Y', event.y + (self.controller.view.carte.cameraY * self.controller.view.carte.item))
            cmd.addData('CIV', self.controller.model.joueur.civilisation)
            self.controller.sendCommand(cmd)


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
        if redo == 0:  # QUICK FIX
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
            self.controller.view.lastConstructionType = Batiment.BARAQUE
            self.controller.view.modeConstruction = True


        elif param == Batiment.HOPITAL:
            print("Create building hopital")
            self.controller.view.lastConstructionType = Batiment.HOPITAL
            self.controller.view.modeConstruction = True


        elif param == Batiment.BASE:
            print("Create building base")
            self.controller.view.lastConstructionType = Batiment.BASE
            self.controller.view.modeConstruction = True

            if not self.controller.view.modeConstruction:
                print("oups")
            else:
                print("MODE CONSTRUCTION")

    def onSurrender(self):
        self.controller.view = TitleScreen(self.controller.window, self.controller)
        self.controller.catchMenuEvent(MenuDebut.TitleEvent.VOIR_MENU_PRINCIPAL)
        self.controller.network.disconnectClient()
        if self.controller.network.server:
            self.controller.network.stopServer()
        self.controller.gameStarted = False






if __name__ == '__main__':
    app = Controller()
    app.start()

