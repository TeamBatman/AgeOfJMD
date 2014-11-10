#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Command():
    """ La classe commande n'est en réalité qu'un wrapper pour dictionnaire """
    # LES TYPES DE COMMANDES POSSIBLES

    # COMMANDES GÉNÉRALES
    START_GAME = 'sg'                   # Utilisée par l'hôte lorsqu'on désire lancer la partie

    # COMMANDES POUR CIVILISATIONS
    CREATE_CIVILISATION = 'cp'          # Utilisée lorsqu'un joueur se joint à la partie
    PROMOTE_CIVILISATION = 'pc'         # Utilisée lorsqu'une unité change d'âge (évolue)
    ANNIHILATE_CIVILISATION = 'ac'      # Utilisée lorsque civilisation quitte partie pour tuer détruire ses effectifs



    # COMMANDES POUR UNITÉS
    CREATE_UNIT = 'cu'         # Utilisée lorsqu'on veut créer une unité
    KILL_UNIT = 'ku'           # Utilisée lorsqu'on veut tuer une unité
    MOVE_UNIT = 'mu'           # Utilisée lorsqu'on veut déplacer une unité
    ATTACK_UNIT = 'au'         # Utilisée lorsqu'on veut attaquer une unité
    ATTACK_BUILDING = 'ab'     # Utilisée lorsqu'une unité attaque un bâtiment  # TODO Vérfier pertinence de la commande

    #  COMMANDE POUR BÂTIMENTS
    CREATE_BUILDING = 'cb'     # Utilisée lorsqu'on désire créer un bâtiment
    DESTROY_BUILDING = 'db'    # Utilisée lorsqu'on désire détruire un bâtiment







    def __init__(self, clientId=-1, cmdType=-1):
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