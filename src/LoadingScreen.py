from GraphicsManagement import GraphicsManager
from GuiAwesomeness import *

import time
import math
from PIL import Image




class LoadingScreen(GWindow):
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

        self.initMenu()



    def initMenu(self):
        self.frame = GFrame(self.canvas, 600, 100)
        self.frame.draw(self.width/2 - self.frame.width/2, self.height-150)
        self.progressBar = GProgressBar(self.canvas, self.frame.width - 60, text="Chargement...")
        self.progressBar.setProgression(0)
        self.progressBar.draw(self.frame.x + 30, self.frame.y + 30)


    def initBackground(self):
        self.title = GraphicsManager.getPhotoImage('Graphics/Screens/LoadingScreen.jpg')
        self.canvas.create_image(0, 0, anchor=NW, image=self.title)
        self.canvas.create_image(0, 0, anchor=NW, image=self.title, tags='background')




    def update(self):
        self.progressBar.setProgression(self.progressBar.progress + 10)
        self.progressBar.update()
        self.after(1000, self.update)













def main():
    t = LoadingScreen()
    t.update()
    t.show()

if __name__ == '__main__':
    main()