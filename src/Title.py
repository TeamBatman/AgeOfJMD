from GraphicsManagement import GraphicsManager
from GuiAwesomeness import *

class TitleScreen(GWindow):
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

        self.title = GraphicsManager.getImage('Graphics/Screens/title.jpg')
        self.title = ImageTk.PhotoImage(self.title)
        self.canvas.create_image(0, 0, anchor=NW, image=self.title)



        self.frame = GFrame(self.canvas, 300, 300)
        self.frame.draw(500, 220)

        self.btnCommencer = GButton(self.canvas, text="Jouer Solo")
        self.btnCommencer.draw(550, 320)

        self.btnCommencer = GButton(self.canvas, text="Jouer Multijoueur")
        self.btnCommencer.draw(550, 380)

        self.btnCommencer = GButton(self.canvas, text="Quitter")
        self.btnCommencer.draw(550, 440)


t = TitleScreen()
t.show()
