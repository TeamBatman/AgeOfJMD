#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" NetworkModule.py: Ce module contient toutes les classes et fonctions nécessaires au bon fonctionnement du réseau """

import json as pickle
import random
import socket
import threading
import Pyro4
from Commands import Command





# CONFIGURATION PYRO
from Joueurs import Joueur

Pyro4.PYRO_TRACELEVEL = 0  # N'affiche pas les erreurs de PYRO4
Pyro4.config.COMMTIMEOUT = 5.0  # en sec Permet au serveur de pouvoir s'éteindre et deconnecte le client après ce délais

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

        # Les civilisations possibles
        self.civilisations = [
            Joueur.ROUGE,
            Joueur.BLEU,
            Joueur.VERT,

            Joueur.MAUVE,
            Joueur.ORANGE,
            Joueur.ROSE,

            Joueur.NOIR,
            Joueur.BLANC,
            Joueur.JAUNE
        ]




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

        random.shuffle(self.civilisations)
        clientId = self.civilisations.pop()
        self.clients[clientId] = []
        Server.outputDebug('CLIENT %s JUST JOINED' % clientId)
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
            cmds = self.clients[clientId]
            self.clients[clientId] = []  # Flush les vieilles commandes
            return cmds
        return []


    def leave(self, clientId):
        """ Permet à un client de quitter le serveur
        :param clientId:
        """
        self.clients.pop(clientId)
        Server.outputDebug((' client: %s left the game' % clientId))


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
        self.host = socket.gethostbyname(socket.gethostname())  # L'adresse IP du serveur. Détectée automatiquement
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
            print('[SERVER]: %s' % msg)


class Client:
    """ Objet client
    """

    def __init__(self):
        self.uri = ''  # L'identifiant Pyro du client
        self.host = None  # L'hôte auquel on tente de se connecte
        self.id = -1  # L'identifiant logique auprès du serveur

    def connect(self, host='127.0.0.1', port=3333, hostName='RTS'):
        """ Connecte le client à son hôte
        :param host: L'addresse IP de l'hôte
        :param port: Le port ouvert de l'hôte
        """

        self.uri = "PYRO:%s@%s:%s" % (hostName, host, port)
        self.host = Pyro4.Proxy(self.uri)
        self.id = self.host.join()

        Client.outputDebug("Connecté à %s avec ID: %s" % (self.uri, self.id))


    def synchronize(self):
        """ Vérifie s'il ya une commande non exécutée par le client
        sur le serveur
        :return: la dernière commande reçue (si il y avait une) autrement on retourne None
        """
        try:
            response = self.host.getLatestCommand(self.id)
            if response:
                commands = []
                for chunk in response:
                    commands.append(Command.buildFromDict(pickle.loads(chunk)))
                return commands
            else:
                return []
        except Exception:   # Pyro4.errors.CommunicationError:
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
        except Exception:  # Pyro4.errors.CommunicationError:
            return False  # Échec de la tentative... le serveur n'existe surement plus





    def sendCommand(self, command):
        """ Envoie un objet commande à l'hôte dans un format sérialisé JSON
        :param command: la commande à envoyer [OBJET]
        """
        try:
            # CONVERSION DE LA COMMANDE EN DICTIONNAIRE
            command = command.convertToDict()
            # SÉRIALISATION DE LA COMMANDE
            cmd_ser = pickle.dumps(command)
            # ENVOIE DE LA COMMANDE SÉRIALISÉE VERS L'HÔTE
            self.host.sendCommand(cmd_ser)
        except Exception:
            raise ClientConnectionError("Impossible d'ENVOYER LA COMMANDE AU SERVEUR")

    @staticmethod
    def outputDebug(msg):
        if CLIENT_DEBUG_VERBOSE:
            print('[CLIENT]: %s' % msg)

    def disconnect(self):
        try:
            self.host.leave(self.id)
        except Exception:  # Pyro4.errors.CommunicationError
            raise ClientConnectionError('Échec lors de la tentative d\'abandon de la partie')


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
        try:
            self.client.disconnect()
        except Exception:
            pass

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
        try:
            self.server.initDaemon()
            self.server.registerController()
            self.server.start()
        except Exception:
            Server.outputDebug('Un serveur est déjà ouvert sur le port %s, le serveur ne sera pas lancer' %
                               self.server.port)

    def synchronizeClient(self):
        """ Méthode synchronisant le client et retournant
         les commandes reçu par ce dernier s'il en a reçu
        :return: les commandes du client (une liste d'Objet Commande)
        """
        try:
            return self.client.synchronize()
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


class ClientConnectionError(Exception):
    def __init__(self, reason=''):
        """ Erreur lancée lorsque qu'il y a eu une erreur de connection
        :param reason: Raison de l'erreur de connection
        """
        self.message = "[ERREUR CLIENT] %s : la connection avec le serveur à été perdue" % reason
        Exception.__init__(self, self.message)