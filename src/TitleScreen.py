from GraphicsManagement import GraphicsManager
from GuiAwesomeness import *

import time
import math
from PIL import Image



class Cloud:
    def __init__(self, pI, x, y, speed):
        self.pI = pI
        self.x = x
        self.y = y
        self.vx = speed
        

    def update(self):
        self.x += self.vx


class Wave:
    def __init__(self, pI, x, y):
        self.pI = pI
        self.x = x
        self.y = y
        self.vx = 1

        self.center = y
        self.offset = 0
        self.radius = 5
        self.invert = 5


    def update(self):
        # TODO fixerl le rate avec des Frame en remplaçant
        # msElapsed par un frameTick auxquel on fait ++ à chaque call de update
        msElapsed = time.time() * self.vx
        offset = math.sin(msElapsed) * self.radius * self.invert
        #self. y = offset
        self.x = offset





class TitleScreen(GWindow):
    def __init__(self):
        GWindow.__init__(self)
        self.width = 1024
        self.height = 768
        self.root.geometry('%sx%s' % (self.width, self.height))
        self.root.configure(background='#000')

        # ZONE DE DESSIN
        self.canvas = Canvas(self.root, width=self.width, height=self.height, background='#000', bd=0,
                             highlightthickness=0)  # higlightthickness retire la bordure par défaut blanche des canvas
        self.canvas.pack()


        self.initBackground()
        self.initClouds()
        self.initWaves()

        self.initMenu()


       



    def initMenu(self):
        self.frame = GFrame(self.canvas, 300, 250)
        self.frame.draw(500, 270)

        self.btnCommencer = GButton(self.canvas, text="Jouer Solo")
        self.btnCommencer.draw(550, 320)

        self.btnCommencer = GButton(self.canvas, text="Jouer Multijoueur")
        self.btnCommencer.draw(550, 380)

        self.btnCommencer = GButton(self.canvas, text="Quitter")
        self.btnCommencer.draw(550, 440)


    def initBackground(self):
        self.title = GraphicsManager.getPhotoImage('Graphics/Screens/title.jpg')
        self.canvas.create_image(0, 0, anchor=NW, image=self.title)

        self.canvas.create_image(0, 0, anchor=NW, image=self.title, tags=('background'))



    def initClouds(self):
        self.clouds = []
        for c in range(8):
            image = GraphicsManager.getPhotoImage("Graphics/Screens/Cloud_%s.png" % c)
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
        self.clouds[2].vx = 1

        self.clouds[3].x = 185
        self.clouds[3].y = 350
        self.clouds[3].vx = 1

        self.clouds[4].x = 654
        self.clouds[4].y = 373
        self.clouds[4].vx = 0.75

        self.clouds[5].x = 80
        self.clouds[5].y = 400
        self.clouds[5].vx = 1

        self.clouds[6].x = 430
        self.clouds[6].y = 415
        self.clouds[6].vx = 0.75

        self.clouds[7].x = -200
        self.clouds[7].y = 400
        self.clouds[7].vx = 0.5





    def initWaves(self):
        self.waves = []
        for w in range(4):
            image = GraphicsManager.getPhotoImage("Graphics/Screens/wave_%s.png" % w)
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
        self.canvas.delete('cloud')
        self.canvas.delete('wave')

        # UPDATE CLOUDS
        for c in self.clouds:
            c.update()
            if c.x > self.width:
                c.x = 0 - 100
            self.canvas.create_image(c.x, c.y, anchor=NW, image=c.pI, tags=('cloud'))
        

        # UPDATE WAVES
        for wave in reversed(self.waves):
            wave.update()
            self.canvas.create_image(wave.x, wave.y, anchor=NW, image=wave.pI, tags=('wave'))

        self.canvas.tag_raise('cloud', 'background')
        self.canvas.tag_raise('wave', 'background')
        self.after(100, self.update)






def main():
    t = TitleScreen()
    t.update()
    t.show()

if __name__ == '__main__':
    main()