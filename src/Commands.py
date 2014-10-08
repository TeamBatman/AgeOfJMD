#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Command():
    # LES TYPES DE COMMANDES POSSIBLES
    CREATE_UNIT = 0
    DELETE_UNIT = 1
    MOVE_UNIT = 2

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
