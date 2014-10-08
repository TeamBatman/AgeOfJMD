#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" NetworkModule.py: Ce module contient toutes les classes et fonctions nécessaires au bon fonctionnement du réseau """

import json as pickle
import socket
import threading
import Pyro4
from Commands import Command

# CONSTANTE DU MODULE
SERVER_DEBUG_VERBOSE = True  # Permet d'afficher les messages de debug du serveur
CLIENT_DEBUG_VERBOSE = True  # Permet d'afficher les messages de debug du client
LOCAL_TEST = True  # Permet de mettre l'adresse IP du serveur à 127.0.0.1. Fonctionne mieux pour les tests..

class ServerController:
    """ Contrôleur serveur. C'est une instance de cette classe qui sera mis à disposition des clients. Enregistrée dans
     le démon Pyro4. Ainsi, ils ne pourront avoir accès qu'aux méthodes définies ici."""

    def __init__(self):

        # Chaque clé est identifiant du client et la valeur est une liste des commandes à exécuter par le client
        self.clients = {}

        self.idIndex = 0  # À chaque attribution d'ID ce nombre est augmenté [il constitue l'identifiant unique]
        self.commands = []  # une liste des commandes reçues

    def _generateId(self):
        """ Génère un identifiant unique à être attribué à chaque utilisateur
        :return: a unique ID
        """
        genId = self.idIndex
        self.idIndex += 1
        return genId

    def join(self):
        """ Permet à un client de rejoindre le serveur et lui retoune un Identifiant unique
        :return: l'identifiant unique généré pour le client
        """
        clientId = self._generateId()
        self.clients[clientId] = []
        if SERVER_DEBUG_VERBOSE:
            print('CLIENT %s JUST JOINED' % clientId)
        return clientId

    def sendCommand(self, command):
        """ Permet à un client d'envoie une commande à tous les autres clients[dans la liste de commande à synchroniser]
        :param command: la commande à être envoyé à tous les clients
        """
        for client in self.clients:
            self.clients[client].append(command)

    def getLatestCommand(self, clientId):
        """ Permet à un client de se renseigner sur la dernière commande envoyée et non synchronisée
        :param clientId: le numéro d'identification du client
        :return: Les dernières commandes non synchronisées par le client ou []
        """
        if self.clients[clientId]:
            return self.clients[clientId].pop()
        return None


    def leave(self, clientId):
        """ Permet à un client de quitter le serveur
        :param clientId:
        """
        self.clients.pop(clientId)
        Server.outputDebug((' client: %s left the game' % clientId))


class Server:
    """ La classe Serveur principal. c'est cette classe qui sera manipulée par le contrôleur réseau
    Lorsqu'ils voudra partir ou arrêter le serveur
    """

    def __init__(self, port=3333):
        self.port = port  # Le port du serveur
        self.host = socket.gethostbyname(socket.gethostname())  # L'adresse IP du serveur. Détectée automatiquement
        if LOCAL_TEST:
            self.host = '127.0.0.1'

        self.daemon = None  # L'instance du démon Pyro4
        self.uri = ''  # L'identifiant Pyro
        self.name = 'RTS'  # Le nom du serveur
        self.running = False  # Flag spécifiant si le serveur est en marche ou non
        Pyro4.config.COMMTIMEOUT = 0.5  # Permet au serveur de pouvoir s'éteindre

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

        Server.outputDebug('SERVER STARTED AT %s' % self.uri)

        self.daemon.requestLoop(loopCondition=self.isRunning)

        Server.outputDebug('SERVER STOPPED')

    def isRunning(self):
        return self.running

    def stop(self):
        """ Met le flag "running" à False
        """
        self.running = False


    @staticmethod
    def outputDebug(msg):
        if SERVER_DEBUG_VERBOSE:
            print(msg)


class Client:
    """ Objet client
    """
    def __init__(self):
        self.uri = ''   # L'identifiant Pyro du client
        self.host = None  # L'hôte auquel on tente de se connecte
        self.id = -1    # L'identifiant logique auprès du serveur

    def connect(self, host='127.0.0.1', port=3333, hostName='RTS'):
        """ Connecte le client à son hôte
        :param host: L'addresse IP de l'hôte
        :param port: Le port ouvert de l'hôte
        """
        try:
            self.uri = "PYRO:%s@%s:%s" % (hostName, host, port)
            self.host = Pyro4.Proxy(self.uri)
            self.id = self.host.join()

            Client.outputDebug()
        except Exception as e:
            pass  # Cette erreur n'est pas nécessairement vraie...


    def synchronize(self):
        """ Vérifie s'il ya une commande non exécutée par le client
        sur le serveur
        :return: la dernière commande reçue (si il y avait une) autrement on retourne None
        """
        if not self.host:
            raise ConnectionError("Impossible de SYNCHRONISER")

        response = self.host.getLatestCommand(self.id)
        if response:
            command = pickle.loads(response)
            return Command.buildFromDict(command)
        else:
            return None


    def sendCommand(self, command):
        """ Sends a command to a host in a serialized format
        :param command: the command to send to the host
        """
        if not self.host:
            raise ConnectionError("Impossible d'ENVOYER LA COMMANDE AU SERVEUR")
        # CONVERSION DE LA COMMANDE EN DICTIONNAIRE
        command = command.convertToDict()
        # SÉRIALISATION DE LA COMMANDE
        cmd_ser = pickle.dumps(command)
        # ENVOIE DE LA COMMANDE SÉRIALISÉE VERS L'HÔTE
        self.host.sendCommand(cmd_ser)

    @staticmethod
    def outputDebug(msg):
        if CLIENT_DEBUG_VERBOSE:
            print(msg)
            
    def disconnect(self):
        self.host.leave(self.id)


class NetworkController:
    """ Objet responsable de toutes les communications réseau
        Il fait le lien entre le Contrôleur Général et les instances
        de client et serveur. Il s'occupe notamment d'établir la connection
        d'un client avec un serveur et de lancer un serveur dans un Thread séparé
     """

    def __init__(self):
        self.client = Client()  # Instance du client
        self.server = None  # Instance du serveur (Seulement lorsque le joueur décide de hoster une partie)
        self.serverThread = None  # Le Fil d'éxécution du serveur

    def connectClient(self, ipAddress='127.0.0.1', port=3333):
        """ Connecte le
        :param ipAddress: L'adresse IP du serveur auquel on veut se connecter
        :param port: Le port du serveur
        """
        self.client.connect(ipAddress, port)

    def disconnectClient(self):
        self.client.disconnect()

    def getClientId(self):
        return self.client.id if self.client else -1

    def startServer(self):
        """ Lance le serveur dans un nouveau fil d'exécution
        """
        self.serverThread = threading.Thread(target=self._startServer)
        self.serverThread.start()

    def _startServer(self):
        """ Crée l'instance du serveur et lance ce dernier
        """
        self.server = Server()
        self.server.initDaemon()
        self.server.registerController()
        self.server.start()

    def stopServer(self):
        """ Arrête le serveur
        """
        self.server.stop()


class ConnectionError(Exception):
    def __init__(self, reason):
        """ Erreur lancée lorsque qu'il y a eu une erreur de connection
        :param reason: Raison de l'erreur de connection
        """
        self.message = "[ERROR] %s : le client n'est connecté à aucun hôte" % reason
        Exception.__init__(self, self.message)
