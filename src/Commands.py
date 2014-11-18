#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Command():
    """ Commande représentant actions d'un joueur. Utilisées pour communiquer avec le réseau et le modèle
    """
    # LES TYPES DE COMMANDES POSSIBLES

    # COMMANDES GÉNÉRALES
    START_GAME = 'sg'      # Utilisée par l'hôte lorsqu'on désire lancer la partie
    NEXT_FRAME = 'nf'      # Utilisée pour indiquer au client de changer de frame
    WAIT = 'w'             # Utilisée par le serveur pour indiquer à un client qu'il doit attendre
    DESYNC = 'dsc'         # Utilisée par le serveur pour indiquer à un client qu'il est totalement désynchronisé

    # COMMANDES POUR CIVILISATIONS
    CIVILISATION_CREATE = 'cc'          # Utilisée lorsqu'un joueur se joint à la partie
    CIVILISATION_PROMOTE = 'cp'         # Utilisée lorsqu'une unité change d'âge (évolue)
    CIVILISATION_ANNIHILATE = 'ca'      # Utilisée lorsque civilisation quitte partie pour tuer détruire ses effectifs
    CIVILISATION_INVOKE_GOD = 'cig'      # Utilisée lorsque civilisation invoque les dieux augmentant son morale++

    # COMMANDES POUR UNITÉS
    UNIT_CREATE = 'uc'         # Utilisée lorsqu'on veut créer une unité
    UNIT_DIE = 'ud'           # Utilisée lorsqu'on veut tuer une unité
    UNIT_MOVE = 'um'           # Utilisée lorsqu'on veut déplacer une unité
    UNIT_ATTACK_UNIT = 'uau'         # Utilisée lorsqu'on veut attaquer une unité

    # TODO Vérfier pertinence de la commande
    UNIT_ATTACK_BUILDING = 'uab'     # Utilisée lorsqu'une unité attaque un bâtiment

    UNIT_ENTER_BUILDING = 'ueb'      # Utilisée lorsqu'une unité entre dans un bâtiment
    UNIT_LEAVE_BUILDING = 'ulb'      # Utilisée lorsqu'une unité sort d'un bâtiment


    #  COMMANDE POUR BÂTIMENTS
    BUILDING_CREATE = 'bc'     # Utilisée lorsqu'on désire créer un bâtiment
    BUILDING_DESTROY = 'bd'    # Utilisée lorsqu'on désire détruire un bâtiment




    def __init__(self, clientId=-1, cmdType=-1):
        """
        :param clientId: ID du client envoyant la commande
        :param cmdType: Type de la commande à envoyer
        """
        self.clientId = clientId
        self.data = {'TYPE': cmdType}  # The necessary data needed by the command

    def addData(self, data_key, newData):
        """ Ajoute de nouvelles données/infos à la commande
        :param data_key: la clé d'identification de la donnée (son nom)
        :param newData: la valeur de la donnée
        :return: self
        """
        self.data[data_key] = newData
        return self

    def convertToDict(self):
        """ Fait la conversion de la commande en dictionnaire et la renvoie
        :return: la représentation en dictionnaire de la commande
        """
        return self.__dict__

    @staticmethod
    def buildFromDict(d):
        """ Construit un objet Command à partir d'un dictionnaire et le retourne
        :param d: le dictionnaire à partir duquelle on construit l'Objet Command
        :return: L'objet commande construit
        """
        cmd = Command(d['clientId'], d['data']['TYPE'])
        cmd.data = d['data']
        return cmd

    def __getitem__(self, item):
        return self.data[item]
