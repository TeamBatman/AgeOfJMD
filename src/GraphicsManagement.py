#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Timer import Timer

DEBUG_VERBOSE = True  # Permet d'afficher les messages de debug du GraphicsManager

from PIL import Image
from PIL import ImageTk
from PIL import ImageEnhance


def colorizeImage(pilImg):
    """ Augmente l'intensité des couleur de l'image
    :param pilImg: l'image PIL
    :return: l'image PIl en rouge
    """

    # COLORIZE
    converter = ImageEnhance.Color(pilImg)
    pilImg = converter.enhance(3)  # n* les couleurs de l'image de base
    return pilImg




class AnimationSheet():
    """ Permet de splitter une image et d'en retournant les sous parties
    """
    def __init__(self, imgPath, nbFrameCol, nbFrameRow):
        """
        :param imgPath:  Le chemin vers l'image de la feuille d'Animation
        """
        self.NB_FRAME_COL = nbFrameCol
        self.NB_FRAME_ROW = nbFrameRow


        self.imgPath = imgPath  # Le chemin vers la feuille d'animation
        self.sheet = GraphicsManager.get(imgPath)   # La feuille de sprite en tant qu'image
        self.sheet.convert('RGBA')

        width, height = self.sheet.size
        self.CELL_WIDTH = int(width / self.NB_FRAME_ROW)  # La largeur d'une frame d'animation
        self.CELL_HEIGHT = int(height / self.NB_FRAME_COL)  # La hauteur d'une frame d'animation


        self.frames = []
        self._splitSheet()

    def _splitSheet(self):
        for y in range(self.NB_FRAME_COL):
            for x in range(self.NB_FRAME_ROW):
                x1 = x * self.CELL_WIDTH
                y1 = y * self.CELL_HEIGHT
                x2 = x1 + self.CELL_WIDTH
                y2 = y1 + self.CELL_HEIGHT
                rectangle = (x1, y1, x2, y2)
                img = self.sheet.crop(rectangle)
                self.frames.append(ImageTk.PhotoImage(img))

class SpriteSheet():

    class Direction:
        UP = 'UP'
        DOWN = 'DOWN'
        LEFT = 'LEFT'
        RIGHT = 'RIGHT'

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
        self.framesOutlines = {}    # Le dictionnaire contenant toutes les frames en version sélectionnées
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
        self._splitRow(0, SpriteSheet.Direction.DOWN)
        self._splitRow(1, SpriteSheet.Direction.LEFT)
        self._splitRow(2, SpriteSheet.Direction.RIGHT)
        self._splitRow(3, SpriteSheet.Direction.UP)


class Animation():
    """ Représente une animation Générique
    """
    def __init__(self, animationSheet, frameDelay):
        self.sheet = animationSheet
        self.frameIndex = 0
        self.activeFrame = None


        self.timer = Timer(frameDelay)
        self.timer.start()

    def animate(self):
        if not self.timer.isDone():
            return

        self.frameIndex += 1
        try:
            self.activeFrame = self.sheet.frames[self.frameIndex]
        except IndexError:  # On est allé trop loin
            self.activeFrame = 0

        self.timer.reset()


class SpriteAnimation():
    """ Correspond à l'animation d'un sprite et l'anime au besoin (manuellement via animate() )
    """
    def __init__(self, spriteSheet, frameDelay):
        """
        :param frameDelay: the delay between frames
        :param spriteSheet: the spriteSheet to use
        """
        self.spriteSheet = spriteSheet
        self.timer = Timer(frameDelay)

        self.direction = SpriteSheet.Direction.DOWN
        self.frameIndex = 1

        self.activeFrame = None
        self.activeOutline = None

        self._updateActiveFrameKey()
        self.timer.start()


    def _updateActiveFrameKey(self):
        activeFrameKey = '%s_%s' % (self.direction, self.frameIndex)
        self.activeFrame = self.spriteSheet.frames[activeFrameKey]
        self.activeOutline = self.spriteSheet.framesOutlines[activeFrameKey]

    def setActiveFrameKey(self, direction, frameIndex):
        self.frameIndex = frameIndex
        self.direction = direction
        self._updateActiveFrameKey()

    def animate(self):
        if not self.timer.isDone():
            return

        self.frameIndex += 1
        if self.frameIndex == self.spriteSheet.NB_FRAME_ROW:
            self.frameIndex = 0
        if self.frameIndex == 1:  # POSITION NEUTRE ON NE VEUT PAS ÇA DURANT L'ANIMATION
            self.frameIndex = 2

        self._updateActiveFrameKey()
        self.timer.reset()



class GraphicsManager():
    """ Objet à une instance seulement puisqu'il doit être disponible pour la totalité
        de l'instance du programme
    """

    # Types de ressources
    UNIT = 0
    ICONS = 1
    BUILDINGS = 2


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





