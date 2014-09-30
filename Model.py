#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Commands import Command


class Unit():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Model:
    def __init__(self):
        self.units = []

    def deleteUnit(self, x, y):  # TODO utiliser un tag ou un identifiant à la place des positions x et y (plus rapide)
        """ Supprime une unité à la liste d'unités
        :param x: position x de l'unité
        :param y: position y de l'unité
        """
        for unit in self.units:
            if unit.x == x and unit.y == y:
                self.units.remove(unit)

    def createUnit(self, x, y):
        """ Crée et ajoute une nouvelle unité à la liste des unités
        :param x: position x de l'unité
        :param y: position y de l'unité
        """
        self.units.append(Unit(x, y))

    def executeCommand(self, command):
        """ Exécute une commande
        :param command: la commande à exécuter
        """
        if command.data['TYPE'] == Command.CREATE_UNIT:
            self.createUnit(command.data['X'], command.data['Y'])

        elif command.data['TYPE'] == Command.DELETE_UNIT:
            self.deleteUnit(command.data['X'], command.data['Y'])