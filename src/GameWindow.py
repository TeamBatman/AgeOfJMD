from GuiAwesomeness import GWindow
from tkinter import *

class GameWindow(GWindow):
    def __init__(self):
        GWindow.__init__(self)
        self.width = 1024
        self.height = 768
        self.root.geometry('%sx%s' % (self.width, self.height))
        self.root.configure(background='#2B2B2B')

        # ZONE DE DESSIN
        self.canvas = Canvas(self.root, width=self.width, height=self.height, background='#91BB62', bd=0,
                             highlightthickness=0)  # higlightthickness retire la bordure par défaut blanche des canvas
        self.canvas.pack()


    def clearWindow(self):
        self.canvas.delete(ALL)

    def destroy(self):
        self.root.destroy()