import threading
from GameWindow import GameWindow
from GraphicsManagement import GraphicsManager
import GraphicsManagement
from GuiAwesomeness import *

from View import Color


class LoadingScreen():
    def __init__(self, window, controller):
        self.window = window
        self.canvas = self.window.canvas

        self.initBackground()
        self.initMenu()

    def initMenu(self):
        self.frame = GFrame(self.canvas, 600, 100)
        self.frame.draw(self.window.width / 2 - self.frame.width / 2, self.window.height - 150)
        self.progressBar = GProgressBar(self.canvas, self.frame.width - 60, text="Chargement...")
        self.progressBar.setProgression(0)
        self.progressBar.draw(self.frame.x + 30, self.frame.y + 30)

    def initBackground(self):
        self.title = GraphicsManager.getPhotoImage('Graphics/Screens/LoadingScreen.jpg')
        self.canvas.create_image(0, 0, anchor=NW, image=self.title)
        self.canvas.create_image(0, 0, anchor=NW, image=self.title, tags='background')

    def startLoading(self):
        self.loader.start()

    def update(self, progression):
        print("UPDATE")
        self.progressBar.setProgression(progression)
        self.progressBar.update()
        self.window.root.update()


class ResourceLoader():
    def __init__(self, resources, view):
        self.view = view
        self.progression = 0
        self.resources = resources
        self.sprites = [r for r in self.resources if 'Units' in r]
        self.couleursHEX = [Color.BLANC, Color.BLEU, Color.JAUNE, Color.MAUVE,
                            Color.NOIR, Color.ORANGE, Color.ROSE, Color.ROUGE,
                            Color.VERT]

        self.nbResTotal = len(self.resources) + len(self.sprites) + len(self.couleursHEX) * 2  # *2 =>units + tours guet
        self.nbLoadedRes = 0
        self.isDone = False


    def run(self):
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

        self.isDone = True


    def loadSomething(self):
        self.nbLoadedRes += 1
        self.progression = int(self.nbLoadedRes * 100 / self.nbResTotal)
        self.view.update(self.progression)


def main():
    w = GameWindow()
    l = LoadingScreen(w, None)
    w.show()


if __name__ == '__main__':
    main()



