from tkinter import ALL
from GraphicsManagement import GraphicsManager
from GuiAwesomeness import *

import time
import math
from PIL import Image
from PIL import ImageTk
from PIL import ImageEnhance
import SimpleTimer


class Cloud:
    """ Représentation d'un nuage
    """
    def __init__(self, pI, x, y, speed):
        self.pI = pI
        self.x = x
        self.y = y
        self.vx = speed
        

    def update(self):
        self.x += self.vx


class Wave:
    """ Représentation d'une vague
    """
    def __init__(self, pI, x, y):
        self.pI = pI
        self.x = x
        self.y = y
        self.vx = 1

        self.radius = 10
        self.invert = 1

    def update(self):
        # TODO fixerl le rate avec des Frame en remplaçant
        # msElapsed par un frameTick auxquel on fait ++ à chaque call de update
        msElapsed = time.time()
        newX = self.invert * math.sin(self.vx*msElapsed) * self.radius
        self.x = newX






class TitleScreen():
    """ Écran titre et ses Menus
    """
    def __init__(self, window, controller):

        self.waves = []
        self.title = GraphicsManager.getPhotoImage('Graphics/Screens/TitleScreen/title.jpg')
        self.clouds = []
        self.canvas = window.canvas
        self.width = window.width
        self.controller = controller

        self.initBackground()
        self.initClouds()
        self.initWaves()

        self.castle = GraphicsManager.getPhotoImage('Graphics/Screens/TitleScreen/castle.png')
        self.canvas.create_image(327, 457, anchor=NW, image=self.castle, tags='castle')
        self.canvas.tag_raise('castle')

        self.cloudTimer = SimpleTimer.FrameTimer(1)
        self.cloudTimer.start()

        self.waveTimer = SimpleTimer.FrameTimer(1)
        self.waveTimer.start()


        self.menuActif = None


    def changerMenu(self, menu):
        if self.menuActif:
            self.menuActif.destroy()
        self.menuActif = menu

    def drawMenu(self):
        self.menuActif.draw()

    def updateMenu(self):
        self.menuActif.update()


    def initBackground(self):
        self.canvas.create_image(0, 0, anchor=NW, image=self.title, tags=('background'))

        """
        self.titleNight = GraphicsManager.getImage('Graphics/Screens/TitleScreen/titleNight.jpg')
        self.nightOpacity = 0
        night = ImageTk.PhotoImage(reduceOpacity(self.titleNight, self.nightOpacity))
        self.canvas.create_image(0, 0, anchor=NW, image=night, tags=('backgroundNight'))
        """

    def initClouds(self):
        """ Initialise les nuages
        """
        for c in range(8):
            image = GraphicsManager.getPhotoImage("Graphics/Screens/TitleScreen/Cloud_%s.png" % c)
            x = 0
            y = 0
            self.clouds.append(Cloud(image, x, y, 1))

        self.clouds[0].x = 850
        self.clouds[0].y = 450
        self.clouds[0].vx = 1

        self.clouds[1].x = 108
        self.clouds[1].y = 192
        self.clouds[1].vx = 0.75

        self.clouds[2].x = 522
        self.clouds[2].y = 270
        self.clouds[2].vx = 0.85

        self.clouds[3].x = 185
        self.clouds[3].y = 350
        self.clouds[3].vx = 0.85

        self.clouds[4].x = 654
        self.clouds[4].y = 373
        self.clouds[4].vx = 0.75

        self.clouds[5].x = 80
        self.clouds[5].y = 400
        self.clouds[5].vx = 0.85

        self.clouds[6].x = 430
        self.clouds[6].y = 415
        self.clouds[6].vx = 0.75

        self.clouds[7].x = -200
        self.clouds[7].y = 400
        self.clouds[7].vx = 0.5

    def initWaves(self):
        """ Initialise les vagues
        """
        for w in range(4):
            image = GraphicsManager.getPhotoImage("Graphics/Screens/TitleScreen/wave_%s.png" % w)
            x = 0
            y = 0
            self.waves.append(Wave(image, x, y))

        self.waves[0].x = 0
        self.waves[0].y = 735

        self.waves[1].x = 0
        self.waves[1].y = 703
        self.waves[1].invert = -1

        self.waves[2].x = 7
        self.waves[2].y = 694

        self.waves[3].x = 7
        self.waves[3].y = 693
        self.waves[3].invert = -1.2

    def update(self):
        """ Permet de m'ettre à jour les images et aniamtions
        """
        #self.canvas.delete('backgroundNight')

        # NUIT
        """self.nightOpacity += 0.1
        print(self.nightOpacity)
        self.night = ImageTk.PhotoImage(reduceOpacity(self.titleNight, self.nightOpacity))
        self.canvas.create_image(0, 0, anchor=NW, image=self.night, tags=('backgroundNight'))
        self.canvas.tag_raise('backgroundNight', 'background')"""

        # UPDATE CLOUDS
        if self.cloudTimer.isDone():
            self.cloudTimer.reset()
            self.canvas.delete('cloud')
            for c in self.clouds:
                c.update()
                if c.x > self.width:
                    c.x = 0 - 100
                self.canvas.create_image(c.x, c.y, anchor=NW, image=c.pI, tags='cloud')
            self.canvas.tag_raise('cloud', 'background')

        # UPDATE WAVES
        if self.waveTimer.isDone():
            self.waveTimer.reset()
            self.canvas.delete('wave')
            for wave in reversed(self.waves):
                wave.update()
                self.canvas.create_image(wave.x, wave.y, anchor=NW, image=wave.pI, tags='wave')
                self.canvas.tag_raise('wave', 'background')


    def destroy(self):
        """ Permet d'effacer l'écran Titre
        """
        self.canvas.delete(ALL)
        self.menuActif.destroy()









def main():
    t = TitleScreen()
    t.update()
    t.show()

if __name__ == '__main__':
    main()