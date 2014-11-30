import threading
from GraphicsManagement import GraphicsManager
import GraphicsManagement
from GuiAwesomeness import *

from GameView import Color


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
        self.frame.draw(self.width / 2 - self.frame.width / 2, self.height - 150)
        self.progressBar = GProgressBar(self.canvas, self.frame.width - 60, text="Chargement...")
        self.progressBar.setProgression(0)
        self.progressBar.draw(self.frame.x + 30, self.frame.y + 30)

    def initBackground(self):
        self.title = GraphicsManager.getPhotoImage('Graphics/Screens/LoadingScreen.jpg')
        self.canvas.create_image(0, 0, anchor=NW, image=self.title)
        self.canvas.create_image(0, 0, anchor=NW, image=self.title, tags='background')



class ResourceLoaderThread(threading.Thread):
    def __init__(self, resources, progressBar):
        threading.Thread.__init__(self)
        self.progressBar = progressBar

        self.resources = resources
        self.sprites = [r for r in self.resources if 'Units' in r]
        self.couleursHEX = [Color.BLANC, Color.BLEU, Color.JAUNE, Color.MAUVE,
                            Color.NOIR, Color.ORANGE, Color.ROSE, Color.ROUGE,
                            Color.VERT]

        self.nbResTotal = len(self.resources) + len(self.sprites) + len(self.couleursHEX) * 2  # *2 =>units + tours guet
        self.nbLoadedRes = 0


    def run(self):
        """ Charge toutes les images nécessaire à une partie dans le graphics manager
        :return:
        """

        # Loading Rayon Vision
        for c in self.couleursHEX:
            selColor = GraphicsManagement.hex_to_rgba(c)
            vision = GraphicsManagement.generateCircle(5, selColor)  # Pour tous les rayons possibles par défaut
            GraphicsManager.addPhotoImage(ImageTk.PhotoImage(vision), 'unitVision')
            self.loadSomething()

        for c in self.couleursHEX:
            selColor = GraphicsManagement.hex_to_rgba(c)
            vision = GraphicsManagement.generateCircle(10, selColor)  # Pour tous les rayons possibles par défaut
            GraphicsManager.addPhotoImage(ImageTk.PhotoImage(vision), 'unitVision')
            self.loadSomething()

        for res in self.resources:
            GraphicsManager.getPhotoImage(res)
            self.loadSomething()
        for sp in self.sprites:
            GraphicsManager.getSpriteSheet(sp)
            self.loadSomething()

    def loadSomething(self):
        self.nbLoadedRes += 1
        progression = int(self.nbLoadedRes * 100 / self.nbResTotal)
        self.progressBar.setProgression(progression)
        self.progressBar.update()


def main():
    t = LoadingScreen()

    resources = GraphicsManagement.detectGraphics()
    ResourceLoaderThread(resources, t.progressBar).start()

    t.show()


if __name__ == '__main__':
    main()