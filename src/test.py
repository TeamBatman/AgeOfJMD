#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fireraccon A.K.A Jean-William Perreault'




try:
    from tkinter import *
except ImportError:
    from Tkinter import *

from GuiAwesomeness import *


class SpriteSheet():
    """ A representation of a spritesheet. It is able to split
        a sprite sheet into an array of character images
    """

    def __init__(self, imgPath):
        """
        :param imgPath: the path to the image ressource
        """
        self.NB_FRAME_ROW = 3  # Nombre de frames par rangee
        self.NB_FRAME_COL = 4  # Nombre de frames par colonne

        self.imgPath = imgPath
        self.sheet = Image.open(self.imgPath)

        self.width, self.height = self.sheet.size

        self.CELL_WIDTH = int(self.width / self.NB_FRAME_ROW)
        self.CELL_HEIGHT = int(self.height / self.NB_FRAME_COL)

        self.frames = {}

        self.splitSheet()

    def splitRow(self, rowNb, rowTag):
        """ Splits a row from the sprite sheet image
        and adds each slice to the frame dictionary as a
        ImageTk.PhotoImage(frame)
        :param rowNb: The number of the row to split
        :param rowTag: The tag we want to give to the row
        """
        for x in range(0, self.NB_FRAME_ROW):
            x1 = x * self.CELL_WIDTH
            y1 = rowNb * self.CELL_HEIGHT
            x2 = x1 + self.CELL_WIDTH
            y2 = y1 + self.CELL_HEIGHT

            frameTag = "%s_%s" % (rowTag, x)
            rectangle = (x1, y1, x2, y2)
            self.frames[frameTag] = ImageTk.PhotoImage(self.sheet.crop(rectangle))

    def splitSheet(self):
        """
            splits the whole character sheet
        """
        self.splitRow(0, 'DOWN')
        self.splitRow(1, 'LEFT')
        self.splitRow(2, 'RIGHT')
        self.splitRow(3, 'UP')


class Unit:
    def __init__(self):
        self.spriteSheet = SpriteSheet('char.png')
        self.sprite = self.spriteSheet.frames['DOWN_1']


class Tile():
    def __init__(self, walkable=True):
        self.isWalkable = walkable


class Controller():
    def __init__(self):
        self.gui = Window()
        self.map = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ]

    def mainloop(self):
        self.gui.after(100, self.mainloop)

    def run(self):
        self.mainloop()
        self.gui.show()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Window(GWindow):
    def __init__(self):
        GWindow.__init__(self)
        self.root.geometry('800x600')
        self.canvas = None
        self.UserInterface()
        self.updateGUI()

    def UserInterface(self):
        CANVAS_WIDTH = 800
        CANVAS_HEIGHT = 600

        self.canvas = Canvas(self.root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="#91BB62")
        self.canvas.pack()
        # self.panel = GChoiceDialogue(self.canvas, "Do you really want to quit?", command=self.btnClick)
        # self.panel.draw(200, 100)



    def updateGUI(self):
        self.unit = Unit()
        self.canvas.create_image(800/2, 600/2, anchor=NW, image=self.unit.sprite)

    def show(self):
        self.root.mainloop()


def main():
    game = Controller()
    game.run()


if __name__ == '__main__':
    main()
