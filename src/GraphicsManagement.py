#!/usr/bin/env python
# -*- coding: utf-8 -*-


DEBUG_VERBOSE = True  # Permet d'afficher les messages de debug du GraphicsManager
from PIL import Image
from PIL import ImageTk
from PIL import ImageOps
from PIL import ImageFilter


class SpriteSheet():
    def __init__(self, imgPath):
        """
        :param imgPath: Le chemin vers l'image de la feuille de sprite
        """
        self.NB_FRAME_ROW = 3  # Nombre de frames par rangee
        self.NB_FRAME_COL = 4  # Nombre de frames par colonne

        self.imgPath = imgPath  # Le chemin vers la Sprite Sheet
        self.sheet = GraphicsManager.get(imgPath)  # La feuille de sprite en tant qu'image
        self.sheet.convert('RGBA')

        width, height = self.sheet.size
        self.CELL_WIDTH = int(width / self.NB_FRAME_ROW)  # La largeur d'une frame d'animation
        self.CELL_HEIGHT = int(height / self.NB_FRAME_COL)  # La hauteur d'une frame d'animation

        self.frames = {}  # Le dictionnaire contenant toute les frames
        self.framesOutlines = {}
        self._splitSheet()

    def _splitRow(self, rowNb, rowTag):
        """ Divise une rangée et l'ajoute au dictionnaire de frames en tant que ImageTk.PhotoImage
        :param rowNb: le numero de la rangée à diviser
        :param rowTag: l'étiquette à attribuer à cette rangée
        """
        for x in range(0, self.NB_FRAME_ROW):
            x1 = x * self.CELL_WIDTH
            y1 = rowNb * self.CELL_HEIGHT
            x2 = x1 + self.CELL_WIDTH
            y2 = y1 + self.CELL_HEIGHT

            frameTag = "%s_%s" % (rowTag, x)
            rectangle = (x1, y1, x2, y2)

            img = self.sheet.crop(rectangle)
            self.frames[frameTag] = ImageTk.PhotoImage(img)
            self.framesOutlines[frameTag] = ImageTk.PhotoImage(colorizeImage(img))

    def _splitSheet(self):
        """ divise une feuille de sprite en chacune de ses partie
        et de ses frames d'animation la numérotation se fait à partir de 0
        """
        self._splitRow(0, "DOWN")
        self._splitRow(1, "LEFT")
        self._splitRow(2, "RIGHT")
        self._splitRow(3, "UP")


def colorizeImage(pilImg):
    """ Met une image PIL en bleu
    :param pilImg: l'image PIL
    :return: l'image PIl en rouge
    """
    # get an image that is greyscale with alpha
    pilImg = pilImg.convert('LA')
    # get the two bands
    L, A = pilImg.split()
    # a fully saturated band
    S, = Image.new('L', pilImg.size, 255).split()
    # re-combine the bands
    # this keeps tha alpha channel in the new image

    # GREY SCALE L L L A
    pilImg = Image.merge('RGBA', (L, L, S, A))

    # save
    return pilImg


class GraphicsManager():
    """ Objet à une instance seulement puisqu'il doit être disponible pour la totalité
        de l'instance du programme
    """

    # Types de ressources
    UNIT = 0
    ICONS = 0
    BUILDINGS = 0


    # VARIALBES D'INSTANCE
    directories = []  # Une liste de dossiers dans lesquels chercher les ressources
    graphics = {}  # Les ressources chargées

    @classmethod
    def initialize(cls):
        cls.addDirectory('Graphics/')

    @classmethod
    def addDirectory(cls, directory):
        """ Ajoute un dossier à la liste de dossiers
        :param directory: le dossier
        """
        if directory not in cls.directories:
            cls.directories.append(directory)

    @classmethod
    def get(cls, filename):  # TODO subdiviser en plus petites fonctions

        # Vérifie si on a la ressource de charger en mémoire
        """ Permet d'obtenir une ressource par son nom
        :param filename: le nom du fichier de la ressource
        :return: la ressource
        """
        if filename in cls.graphics:
            return cls.graphics.get(filename)

        # À ce stade la ressource n'est pas déjà en mémoire,
        # on va donc la charger à partir de son chemin
        try:
            graphics = Image.open(filename)
            graphics.convert('RGBA')
            cls.graphics[filename] = graphics
            GraphicsManager.outputDebug('chargement de %s' % filename)
            return cls.graphics[filename]
        except FileNotFoundError:
            pass


        # À ce stade son chemin n'était pas complet alros on va chercher dans la liste
        # de nos dossiers
        for directory in cls.directories:
            try:
                loadPath = directory + filename
                graphics = Image.open(loadPath)
                print(loadPath)
                graphics.convert('RGBA')
                cls.graphics[filename] = graphics
                GraphicsManager.outputDebug('chargement de %s' % filename)
                return cls.graphics[filename]
            except FileNotFoundError:
                pass

        # On a pas trouvé l'image ni en mémoire, ni dans aucun dossier on va donc
        # retourner une image vide (Noire)
        GraphicsManager.outputDebug('"%s" est introuvable. Une image vide sera utilisée.' % filename)
        cls.graphics[filename] = Image.new('RGB', (32, 32), 'black')
        return cls.graphics[filename]


    @staticmethod
    def outputDebug(msg):
        if DEBUG_VERBOSE:
            print("Graphics Manager :: %s" % msg)


GraphicsManager.addDirectory('Graphics/')





