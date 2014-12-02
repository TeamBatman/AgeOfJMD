#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" NetworkModule.py: Ce module contient toutes les classes et fonctions nécessaires au bon fonctionnement du réseau """

import json as pickle
import random
import socket
import threading

import Pyro4
import time

from Civilisations import Civilisation
from Commands import Command





# CONFIGURATION PYRO
Pyro4.PYRO_TRACELEVEL = 0  # N'affiche pas les erreurs de PYRO4
Pyro4.config.COMMTIMEOUT = 5.0  # en sec Permet serveur de s'éteindre et de deconnecter le client après délais
# Pyro4.config.REQUIRE_EXPOSE = True      # Permet d'exposer certaines méthodes et attributs d'un Proxy Pyro


# CONSTANTE DU MODULE
SERVER_DEBUG_VERBOSE = True  # Permet d'afficher les messages de debug du serveur
CLIENT_DEBUG_VERBOSE = True  # Permet d'afficher les messages de debug du client
LOCAL_TEST = False  # Permet de mettre l'adresse IP du serveur à 127.0.0.1. Fonctionne mieux pour les tests..


def detectIP():
    return socket.gethostbyname(socket.gethostname())


class SCClient:
    """ Représentation d'un client pour le ServerController
    """

    def __init__(self, ipAddress, name, cid):
        self.civId = cid  # Identifiant de civilisation du client
        self.name = name  # Nom du client/joueur
        self.ipAddress = ipAddress  # Adresse IP du client
        self.currentFrame = 0  # la Frame de simulation actuel du client
        self.isHost = False  # Spécifie si le client est aussi l'hote (True) on Non (False)


class ServerController:
    """ Contrôleur serveur. C'est une instance de cette classe qui sera mis à disposition des clients. Enregistrée dans
     le démon Pyro4. Ainsi, ils ne pourront avoir accès qu'aux méthodes définies ici."""

    # ÉTATS DU JEU
    WAITING_LOADING = 'wl'  # Le serveur attends que tous les joueur aient loadé les ressources du jeu
    IN_GAME = 'ig'  # La parite est en cours



    def __init__(self):
        # Chaque clé est identifiant du client et la valeur est sa progression dans l'ensemble des commandes
        # Les commandes ont toutes un ID ainsi (plus le ID est haut plus la commande est récente):
        # X : l'ID de la dernière commande
        # X-1: Valeur progression d'un client signifiant qu'il est en StandBy ,il attend de recevoir une cmd du serveur
        # X-2: La commande précédant X
        self.clients = {}
        self.idIndex = 0  # À chaque attributionID ce nombre est augmenté [constitue l'ID unique des commandes]
        self.commands = {}  # une dict des commandes reçues la clé est l'ID de la commande etl a valeur la commande

        # Les civilisations possibles
        self.civilisations = [
            Civilisation.ROUGE,
            Civilisation.BLEU,
            Civilisation.VERT,

            Civilisation.MAUVE,
            Civilisation.ORANGE,
            Civilisation.ROSE,

            Civilisation.NOIR,
            Civilisation.BLANC,
            Civilisation.JAUNE
        ]

        # Le nombre de frames dans le futur depuis le temps de sa réception qu'une commande doit être exécutée
        self.commandFrameLatency = 2

        self.syncFrameThreshold = 1  # Le nombre de frames minimum pour déclancher une synchronisation
        # Le nombre maximal de frames de retard sur le jeu. Lorsqu'un joueur est X frames derrière le
        # plus avancé, on lui renvoie Command.DESYNC lui indiquant qu'il ne peu plus joueur car il est désynchronisé
        self.desynchFrameThreshold = 40

    #@Pyro4.expose
    #@property
    def getClients(self):
        """ Retourne la liste des clients du serveu, chacun sous la forme d'un dictionnaire
        :return: une liste contenant les clients sous forme de dictionnaire
        """

        return [c.__dict__ for c in self.clients.values()]

    def join(self, ip, name='Joueur Anonyme'):
        """ Permet à un client de rejoindre le serveur et lui retoune un Identifiant unique
        :return: l'identifiant unique généré pour le client
        """
        # On choisit de aléatoirement une civilisation
        random.shuffle(self.civilisations)
        civ = self.civilisations.pop()

        newClient = SCClient(ip, name, civ)
        self.clients[civ] = newClient

        newClient.isHost = (detectIP() == ip)

        Server.outputDebug('LE CLIENT %s A REJOINT LA PARTIE' % newClient.civId)
        return newClient.civId

    def sendCommand(self, command, currentFrame):
        """ Permet à un client d'envoie une commande à tous les autres clients[dans la liste de commande à synchroniser]
        :param command: la commande à être envoyé à tous les clients
        """
        maxFrame = self.getFrameMostForwardInTime()
        targetFrame = maxFrame + self.commandFrameLatency
        try:
            self.commands[targetFrame].append(command)
        except KeyError:
            self.commands[targetFrame] = [command]

        if Command.START_GAME in command:
            self.commands[currentFrame] = [command]




    def getNextCommand(self, clientId, currentFrame):  # TODO Simplifier
        """ Permet à un client de se renseigner sur sa prochaine commande à exécuter
        afin de se synchroniser
        :param currentFrame: La frame actuelle du client ce qui veut dire qu'il désire currentFrame + 1
        :param clientId: le numéro d'identification du client
        :return: La prochaine commande à exécuter par le client
        """



        currentClient = self.clients[clientId]
        currentClient.currentFrame = currentFrame
        #print(["%s: %s" % (c.civId, c.currentFrame) for c in self.clients.values()])   # PROGRESSION CLIENTS


        # a-t-on suffisamment de joueurs pour commencer la partie?
        if len(self.clients) < 1:
            cmd = Command(-1, Command.WAIT)
            return [pickle.dumps(cmd.convertToDict())]

        # Le client est-il totalement désynchro?
        if self.getFrameMostForwardInTime() - currentClient.currentFrame >= self.desynchFrameThreshold:
            Server.outputDebug("client avec ID: %s est DÉSYNCHRONISÉ" % currentClient.civId)
            return [pickle.dumps(Command(-1, Command.DESYNC).convertToDict())]



        # Si quelqu'un est plus en retard que nous on ne peut obtenir notre prochaine frame
        # On va attendre que le(s) client(s) en retard se synchronise(nt)
        if self.isSomeoneLate():
            if self.isSomeoneMoreLate(currentClient):
                # Si différence temps entre client courant et le plus en retard > threshold on le fait attendre
                if currentFrame - self.getFrameMostBackwardInTime() >= self.syncFrameThreshold:
                    return [pickle.dumps(Command(-1, Command.WAIT).convertToDict())]

        try:
            return self.commands[currentFrame + 1]
        except KeyError:
            return []


    def getFrameMostForwardInTime(self):
        """ Retourne la frame du client le PLUS avancé dans le temps
        :return: int frame la PLUS avancée dans le temps
        """
        return max([c.currentFrame for c in self.clients.values()])

    def getFrameMostBackwardInTime(self):
        """ Retourne la frame du client le MOINS avancé dans le temps
        :return: int frame la MOINS avancée dans le temps
        """
        return min([c.currentFrame for c in self.clients.values()])


    def isSomeoneMoreLate(self, refClient):
        """ Trouves si un client est plus en retard que le client en paramètre
        :param refClient: Le client à compararer au autres
        :return: True si quelqu'un est plus en retard autrement False: Nous somme le plus en retard
        """
        for client in self.clients.values():
            if client.currentFrame < refClient.currentFrame:
                return True

        return False

    def isSomeoneLate(self):
        """ Trouves si un client est en retard
        :return: True si quelqu'un est en retard sinon False:
        """
        return len(set([c.currentFrame for c in self.clients.values()])) != 1


    def leave(self, clientId):
        """ Permet à un client de quitter le serveur
        :param clientId:
        """
        self.clients.pop(clientId)
        Server.outputDebug(('CLIENT: %s A QUITTER LA PARTIE' % clientId))


    def ping(self):
        """ Méthode permettant à un client de tester si le serveur
        existe toujours
        """
        pass


class Server:
    """ La classe Serveur principal. c'est cette classe qui sera manipulée par le contrôleur réseau
    Lorsqu'ils voudra partir ou arrêter le serveur
    """

    def __init__(self, port=3333):
        self.port = port  # Le port du serveur
        self.host = detectIP()  # L'adresse IP du serveur. Détectée automatiquement
        if LOCAL_TEST:
            self.host = '127.0.0.1'

        self.daemon = None  # L'instance du démon Pyro4
        self.uri = ''  # L'identifiant Pyro
        self.name = 'RTS'  # Le nom du serveur
        self.running = False  # Flag spécifiant si le serveur est en marche ou non


    def initDaemon(self):
        """ Initialise le démon Pyro
        """
        self.daemon = Pyro4.Daemon(host=self.host, port=self.port)

    def registerController(self):
        """  Enregistre le contrôleur de Serveur auprès du démon
        """
        self.uri = self.daemon.register(ServerController(), self.name)

    def start(self):
        """ Part le Démon pyro du serveur et boucle tant que le flag "running" sera à True
        """
        self.running = True

        Server.outputDebug('SERVEUR DÉMARRÉ À %s' % self.uri)

        self.daemon.requestLoop(loopCondition=self.isRunning)

        Server.outputDebug('SERVEUR ARRÊTÉ')

    def isRunning(self):
        return self.running

    def stop(self):
        """ Met le flag "running" à False
        """
        self.running = False


    @staticmethod
    def outputDebug(msg):
        if SERVER_DEBUG_VERBOSE:
            print('[SERVER]: %s' % msg)


class Client:
    """ Objet client
    """

    def __init__(self):
        self.uri = ''  # L'identifiant Pyro du client
        self.host = None  # L'hôte auquel on tente de se connecte
        self.id = -1  # L'identifiant logique auprès du serveur

    def connect(self, host='127.0.0.1', port=3333, hostName='RTS', playerName='Batman'):
        """ Connecte le client à son hôte
        :param host: L'addresse IP de l'hôte
        :param port: Le port ouvert de l'hôte
        """

        self.uri = "PYRO:%s@%s:%s" % (hostName, host, port)
        self.host = Pyro4.Proxy(self.uri)
        self.id = self.host.join(detectIP(), playerName)  # TODO Ajouter le nom

        Client.outputDebug("Connecté à %s avec ID: %s" % (self.uri, self.id))


    def synchronize(self, currentFrame):
        """ Vérifie s'il ya une commande non exécutée par le client
        sur le serveur
        :return: la dernière commande reçue (si il y avait une) autrement on retourne None
        """
        try:
            response = self.host.getNextCommand(self.id, currentFrame)
            if response:
                return [Command.buildFromDict(pickle.loads(chunk)) for chunk in response]
            else:
                return []
        except Pyro4.errors.CommunicationError:  # Pyro4.errors.CommunicationError:
            raise ClientConnectionError("Impossible de SYNCHRONISER")


    def attemptReconnect(self):
        """ Utilisée lorsque le
        :return:
        """
        try:
            Client.outputDebug('Tentative de reconnection auprès du serveur ...')
            self.host.ping()
            self.host.pyroReconnect()
            Client.outputDebug('Reconnecté!')
            return True
        except Pyro4.errors.CommunicationError:  # Pyro4.errors.CommunicationError:
            return False  # Échec de la tentative... le serveur n'existe peut-être plus


    def sendCommand(self, command, currentFrame):
        """ Envoie un objet commande à l'hôte dans un format sérialisé JSON
        :param command: la commande à envoyer [OBJET]
        """
        try:
            # CONVERSION DE LA COMMANDE EN DICTIONNAIRE
            command = command.convertToDict()
            # SÉRIALISATION DE LA COMMANDE
            cmd_ser = pickle.dumps(command)
            # ENVOIE DE LA COMMANDE SÉRIALISÉE VERS L'HÔTE
            self.host.sendCommand(cmd_ser, currentFrame)
        except Pyro4.errors.CommunicationError:
            raise ClientConnectionError("Impossible d'ENVOYER LA COMMANDE AU SERVEUR")

    @staticmethod
    def outputDebug(msg):
        if CLIENT_DEBUG_VERBOSE:
            print('[CLIENT]: %s' % msg)

    def disconnect(self):
        try:
            self.host.leave(self.id)
        except Pyro4.errors.CommunicationError:  # Pyro4.errors.CommunicationError
            raise ClientConnectionError('Échec lors de la tentative d\'abandon de la partie')


class NetworkController:
    """ Objet responsable de toutes les communications réseau
        Il fait le lien entre le Contrôleur Général et les instances
        de client et serveur. Il s'occupe notamment d'établir la connection
        d'un client avec un serveur et de lancer un serveur dans un Thread séparé
     """

    def __init__(self):
        self.client = None #Client()  # Instance du client
        self.server = None  # Instance du serveur (Seulement lorsque le joueur décide de hoster une partie)
        self.serverThread = None  # Le Fil d'éxécution du serveur

    def connectClient(self, ipAddress, port, playerName):
        """ Connecte le
        :param ipAddress: L'adresse IP du serveur auquel on veut se connecter
        :param port: Le port du serveur
        """
        if self.serverThread:
            ipAddress = detectIP()
        if not self.client:
            self.client = Client()
        try:
            self.client.connect(ipAddress, port, playerName=playerName)
        except Pyro4.errors.CommunicationError:
            raise ClientConnectionError("IMPOSSIBLE DE SE CONNECTER À L'HOTE AUCUN OBJET PYRO DÉTECTER À L'ADRESSE"
                                        "ET AU PORT SPÉCIFIÉ")

    def disconnectClient(self):
        try:
            self.client.disconnect()
        except Pyro4.errors.CommunicationError:
            pass

    def getClientId(self):
        return self.client.id if self.client else -1

    def startServer(self, port):
        """ Lance le serveur dans un nouveau fil d'exécution
        """
        self.serverThread = threading.Thread(target=lambda: self._startServer(port))
        self.serverThread.start()

    def _startServer(self, port):
        """ Crée l'instance du serveur et lance ce dernier
        """
        self.server = Server(port=port)
        try:
            self.server.initDaemon()
            self.server.registerController()
            self.server.start()
        except OSError:
            Server.outputDebug('Un serveur est déjà ouvert sur le port %s, le serveur ne sera pas lancer' %
                               self.server.port)

    def synchronizeClient(self, currentFrame):
        """ Méthode synchronisant le client et retournant
         les commandes reçu par ce dernier s'il en a reçu
        :return: les commandes du client (une liste d'Objet Commande)
        """
        try:
            return self.client.synchronize(currentFrame)
        except ClientConnectionError as e:
            # TENTATIVE DE RECONNECTION
            Client.outputDebug(e.message)
            if self.client.attemptReconnect():
                self.synchronizeClient()
            else:
                self.client = None
                message = "Impossible de se reconnecter au serveur... l'hôte n'existe plus"
                Client.outputDebug(message)
                raise ClientConnectionError(message)


    def stopServer(self):
        """ Arrête le serveur
        """
        self.server.stop()
        self.server = None

    def isClientHost(self):
        """ Retourne si le client en cours est un HOST
        :return: booléen True si le client est host autrement false
        """
        return self.serverThread is not None


class ClientConnectionError(Exception):
    def __init__(self, reason=''):
        """ Erreur lancée lorsque qu'il y a eu une erreur de connection
        :param reason: Raison de l'erreur de connection
        """
        self.message = "[ERREUR CLIENT] %s : la connection avec le serveur à été perdue" % reason
        Exception.__init__(self, self.message)
