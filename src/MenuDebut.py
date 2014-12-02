from View import *

from Commands import Command



class TitleEvent:
    """ Action pouvant être performée par l'utilisateur lors des menu d'avant partie
    """

    LANCER_PARTIE_MULTIJOUEUR = 'lpm'
    VOIR_MENU_PRINCIPAL = 'vmp'
    VOIR_MENU_MULTIJOUEUR = 'vmm'
    VOIR_MENU_SOLO = 'vms'
    VOIR_MENU_CREER_SERVEUR = 'vmcs'
    VOIR_MENU_REJOINDRE_SERVEUR = 'vmrs'

    CREER_SERVEUR = 'cs'
    REJOINDRE_SERVEUR = 'rs'
    QUITTER_JEU = 'qj'
    LANCER_PARTIE_SOLO = 'lps'

    SIGNALER_PRET = 'sp'    # Permet à un client de signaler qu'il est prêt dans le lobby à entamer la partie
    ARRETER_SERVEUR = 'as'




class MenuPrincipal:
    """ Menu Permettant de quitter, d'accéder au menu Solo ou au menu Multijoueur
    """
    def __init__(self, window, controller):
        self.window = window
        self.controller = controller
        self.x = 500
        self.y = 270


        self.frame = GFrame(self.window.canvas, 300, 250)
        self.btnSolo = GButton(self.window.canvas, text="Jouer Solo", command=lambda: self.controller.catchMenuEvent(TitleEvent.VOIR_MENU_SOLO))
        self.btnMultijoueur = GButton(self.window.canvas, text="Jouer Multijoueur", command=lambda: self.controller.catchMenuEvent(TitleEvent.VOIR_MENU_MULTIJOUEUR))
        self.btnQuitter = GButton(self.window.canvas, text="Quitter", command=lambda: self.controller.catchMenuEvent(TitleEvent.QUITTER_JEU))


    def draw(self):
        self.frame.draw(500, 270)
        self.btnSolo.draw(550, 320)
        self.btnMultijoueur.draw(550, 380)
        self.btnQuitter.draw(550, 440)

    def destroy(self):
        self.frame.destroy()
        self.btnSolo.destroy()
        self.btnMultijoueur.destroy()
        self.btnQuitter.destroy()



class MenuMultijoueur:
    """ Menu permettant de se connecter à un serveur
    ou d'en crééer un
    """
    def __init__(self, window, controller):
        self.window = window
        self.controller = controller
        # position du depart pour draw
        self.x = 674
        self.y = 50
        self.frameMultiJ = GFrame(self.window.canvas, width=300, height=400)
        self.boutCrServ = GButton(self.window.canvas, text="Créer un serveur",
                                  command=lambda: self.controller.catchMenuEvent(TitleEvent.VOIR_MENU_CREER_SERVEUR))

        self.boutRejServ = GButton(self.window.canvas, text="Rejoindre un serveur",
                                   command=lambda: self.controller.catchMenuEvent(TitleEvent.VOIR_MENU_REJOINDRE_SERVEUR))

        self.boutRetour = GButton(self.window.canvas, text="Retour",
                                  command=lambda: self.controller.catchMenuEvent(TitleEvent.VOIR_MENU_PRINCIPAL))
    # TODO Se fier à X et Y
    def draw(self):
        self.frameMultiJ.draw(self.x + 0, self.y + 0)
        self.window.canvas.create_text(self.x + 150, self.y + 50, text="Multijoueur", fill="#B45F04", font="Arial 20",
                                       tags='menuMultijoueur')
        self.boutCrServ.draw(self.x + 50, self.y + 100)
        self.boutRejServ.draw(self.x + 50, self.y + 170)
        self.boutRetour.draw(self.x + 50, self.y + 300)


    def destroy(self):
        self.window.canvas.delete('menuMultijoueur')
        self.frameMultiJ.destroy()
        self.boutCrServ.destroy()
        self.boutRejServ.destroy()
        self.boutRetour.destroy()


class MenuServeur:
    """ Menu permettant la création d'un serveur
    """
    def __init__(self, window, controller, adresseIP):
        self.window = window
        self.controller = controller
        # position du depart pour draw
        self.x = 374
        self.y = 50
        self.frameServ = GFrame(self.window.canvas, width=600, height=270)

        self.ip = adresseIP
        self.nomJoueur = ''

        self.inputNom = Entry(self.window.canvas, bd=4, font="Courier 20")
        # TODO label "taille de la carte"
        # à faire

        self.boutFinalServ = GButton(self.window.canvas, text="Finaliser serveur", command=self.lireNom)
        self.boutRetour = GButton(self.window.canvas, text="Retour",
                                  command=lambda: self.controller.catchMenuEvent(TitleEvent.VOIR_MENU_MULTIJOUEUR))

    def lireNom(self):
        # vérifie le nom du joueur
        self.nomJoueur = self.inputNom.get()
        if len(self.nomJoueur) == 0:
            self.nomJoueur = "Batman"
        print(self.nomJoueur)

        self.controller.catchMenuEvent(TitleEvent.CREER_SERVEUR)




    def draw(self):
        self.frameServ.draw(self.x + 0, self.y + 0)
        self.window.canvas.create_text(self.x + 300, self.y + 20, anchor='n', text="Création du serveur",
                                       fill="#B45F04", font="Arial 26", tags='menuServeur')
        self.window.canvas.create_text(self.x + 300, self.y + 70, anchor='n', text="Votre adresse IP: " + self.ip,
                                       fill="#B45F04", font="Arial 20", tags='menuServeur')
        self.window.canvas.create_text(self.x + 300, self.y + 150, anchor='e', text="Entrez votre nom: ",
                                       fill="#B45F04", font="Arial 20", tags='menuServeur')
        #self.inputNom.place(x=self.x + 300, y=self.y + 130, width=200, height=40)
        self.window.canvas.create_window(self.x + 300, self.y + 130,  anchor=NW, width=200, height=40,
                                         window=self.inputNom, tags='menuServeur')


        self.boutFinalServ.draw(self.x + 370, self.y + 195)
        self.boutRetour.draw(self.x + 30, self.y + 195)


    def destroy(self):
        self.window.canvas.delete('menuServeur')
        self.frameServ.destroy()
        self.boutFinalServ.destroy()
        self.boutRetour.destroy()


class MenuRejoindreServeur:
    """ Menu permettant de rejoindre un serveur en entrant son adresse IP
    """
    def __init__(self, window, controller):
        self.window = window
        self.controller = controller
        # position du depart pour draw
        self.x = 474
        self.y = 50

        self.frameRejServ = GFrame(self.window.canvas, width=500, height=370)

        # self.vue.siServeur = False # TODO See this


        self.inputIp = Entry(self.window.canvas, bd=4, font="Courier 30")
        # self.inputIp.bind("<Return>",self.testIP)
        self.inputNom = Entry(self.window.canvas, bd=4, font="Courier 20")
        self.boutRejoindre = GButton(self.window.canvas, text="Rejoindre serveur", command=self.lireNom, color=0)
        self.boutRetour = GButton(self.window.canvas, text="Retour", command=lambda: self.controller.catchMenuEvent(TitleEvent.VOIR_MENU_MULTIJOUEUR), color=0)

    def lireNom(self):
        # vérifie le nom du joueur
        self.nomJoueur = self.inputNom.get()
        if len(self.nomJoueur) == 0:
            self.nomJoueur = "Batgirl"
        print(self.nomJoueur)
        self.IPJoueur = self.inputIp.get()
        self.controller.catchMenuEvent(TitleEvent.REJOINDRE_SERVEUR)

    def draw(self):
        self.frameRejServ.draw(self.x + 0, self.y + 0)
        self.window.canvas.create_text(self.x + 250, self.y + 40, anchor='n', text="Entrez l’adresse IP du serveur",
                                       fill="#B45F04", font="Arial 20", tags='menuRejoindreServeur')

        self.window.canvas.create_window(self.x + 60, self.y + 100, width=380, height=70, window=self.inputIp,
                                         anchor=NW, tags='menuRejoindreServeur')

        self.window.canvas.create_text(self.x + 250, self.y + 220, anchor='e', text="Entrez votre nom: ", fill="#B45F04",
                                       font="Arial 20", tags='menuRejoindreServeur')


        self.window.canvas.create_window(self.x + 250, self.y + 200, width=200, height=40, window=self.inputNom,
                                         anchor=NW, tags='menuRejoindreServeur')

        self.boutRejoindre.draw(self.x + 270, self.y + 295)
        self.boutRetour.draw(self.x + 30, self.y + 295)


    def destroy(self):
        self.frameRejServ.destroy()
        self.boutRejoindre.destroy()
        self.boutRetour.destroy()
        self.window.canvas.delete('menuRejoindreServeur')


class MenuLobby:
    """ Lobby des joueurs lorsqu'ils entrent dans un serveur
    """
    def __init__(self, window, controller, isClientHost):
        self.controller = controller
        self.window = window
        # position du depart pour draw
        self.x = 174
        self.y = 50
        self.frameLobby = GFrame(self.window.canvas, width=800, height=550)
        self.siServeur = isClientHost
        """
        # vérifie le nom du joueur
        self.nomJoueur = self.inputNom.get()
        if len(self.nomJoueur) == 0:
            self.nomJoueur = "Batman"
        """
        # self.clientId = self.vue.eventListener.controller.network.client.id
        # self.clientId = self.vue.eventListener.controller.network.getClientId()
        # TODO - chercher dans View - Color
        #                  ROUGE     BLEU        VERT       MAUVE    ORANGE      ROSE        NOIR      BLANC      JAUNE
        self.couleurs = ["#D34343", "#3D99BB", "#26BE2E", "#5637DD", "#F39621", "#CF4592", "#0F0F0F", "#FFFFFF",
                         "#F5F520"]

        self.boutPret = GButton(self.window.canvas, text="Prêt",
                                command=self.controller.catchMenuEvent(TitleEvent.SIGNALER_PRET))

        self.boutQuitServ = GButton(self.window.canvas, text="Quitter le serveur",
                                    command=lambda: self.controller.catchMenuEvent(TitleEvent.ARRETER_SERVEUR))
        #bouton "Lancer la partie" - si serveur

        # TODO Completer
        if self.siServeur:
            #self.boutLancerPartie = GButton(self.canevasLobby, text="Lancer la partie",command=self.vue.debutJeu,color=0)
            self.boutLancerPartie = GButton(self.window.canvas, text="Lancer la partie",
                                            command=lambda: self.controller.catchMenuEvent(TitleEvent.LANCER_PARTIE_MULTIJOUEUR))
            #scale "vitesse"
            self.scaleVitesse = Scale(self.window.canvas, orient=HORIZONTAL, length=250,
                                      from_=1, to=10, tickinterval=1, resolution=1,
                                      sliderlength=10, troughcolor="#B45F04", fg="#B45F04",
                                      width=10, bd=0, showvalue=0, bg="#D3BF8F")

    def envoiCommandeLancer(self):
        print("envoie")
        cmd = Command(self.vue.eventListener.controller.network.client.id, Command.START_LOADING)
        # cmd.addData('ID', 'MOI')
        self.vue.eventListener.controller.sendCommand(cmd)

    def draw(self):
        x = self.x
        y = self.y

        self.frameLobby.draw(x + 0, y + 0)
        self.window.canvas.create_text(x + 200, y + 30, anchor='n', text="Joueurs", fill="#B45F04", font="Arial 22",
                                       tags='lobby')
        # couleur = Color()

        # fond pour les joueurs
        self.window.canvas.create_rectangle(x + 30, y + 75, x + 400, y + 350, fill="#E1F5A9", tags='lobby')

        self.boutPret.draw(x + 30, y + 370)
        self.boutQuitServ.draw(x + 30, y + 475)
        if self.siServeur:
            self.boutLancerPartie.draw(x + 570, y + 475)
            # self.canevasLobby.create_text(x+600, y+50, anchor='n',text="Vitesse du jeu",fill="#B45F04",font="Arial 20")
            #self.scaleVitesse.place(x=x+470, y=y+80)

    def update(self, dictClients):
        x = self.x
        y = self.y
        self.window.canvas.delete("lobby")
        self.clients = dictClients
        nb = len(self.clients)
        # afficher l'information des joueurs
        ligne = 1
        for i in range(nb):
            # ID de client
            self.window.canvas.create_text(x + 35, y + 50 + 30 * ligne, anchor='nw', text=self.clients[i]["name"],
                                          fill="#B45F04", font="Arial 14", tag="lobby")
            # couleur de client
            self.window.canvas.create_rectangle(x + 345, y + 55 + 30 * ligne, x + 395, y + 75 + 30 * ligne,
                                               fill=self.couleurs[self.clients[i]["civId"] - 1], tag="lobby")
            ligne += 1


    def destroy(self):
        self.frameLobby.destroy()
        self.boutLancerPartie.destroy()
        self.boutPret.destroy()
        self.boutQuitServ.destroy()
        self.window.canvas.delete('lobby')




class MenuSolo:
    """ Menu permettant de lancer une partie en Solo
    """
    def __init__(self, window, controller):
        self.window = window
        self.controller = controller
        # position du depart pour draw
        self.x = 524
        self.y = 50
        self.frameSolo = GFrame(self.window.canvas, width=450, height=500)
        # AI - 1
        self.varDif1 = IntVar()
        self.rBoutDiff1_0 = Radiobutton(self.window.canvas, anchor='n', variable=self.varDif1, value=0, bg="#D3BF8F")
        self.rBoutDiff1_1 = Radiobutton(self.window.canvas, anchor='n', variable=self.varDif1, value=1, bg="#D3BF8F")
        self.rBoutDiff1_2 = Radiobutton(self.window.canvas, anchor='n', variable=self.varDif1, value=2, bg="#D3BF8F")
        self.rBoutDiff1_3 = Radiobutton(self.window.canvas, anchor='n', variable=self.varDif1, value=3, bg="#D3BF8F")
        self.rBoutDiff1_1.select()


        # scale "vitesse"
        self.scaleVitesse = Scale(self.window.canvas, orient=HORIZONTAL, length=250,
                                  from_=1, to=10, tickinterval=1, resolution=1,
                                  sliderlength=10, troughcolor="#B45F04", fg="#B45F04",
                                  width=10, bd=0, showvalue=0, bg="#D3BF8F")

        self.boutAccept = GButton(self.window.canvas, text="Lancer la partie", command=lambda: self.controller.catchMenuEvent(TitleEvent.LANCER_PARTIE_SOLO), color=0)
        # bouton "retour"
        self.boutRetour = GButton(self.window.canvas, text="Retour", command=lambda: self.controller.catchMenuEvent(TitleEvent.VOIR_MENU_PRINCIPAL), color=0)


        #TODO Vérifier
        #self.vue.eventListener.controller.startServeur()

    def draw(self):
        self.frameSolo.draw(self.x + 0, self.y + 0)
        self.window.canvas.create_text(self.x + 420, self.y + 20, anchor='ne', text="Solo", fill="#B45F04", font="Arial 40", tags='menuSolo')
        self.window.canvas.create_text(self.x + 100, self.y + 30, anchor='nw', text="Ennemis", fill="#B45F04", font="Arial 20", tags='menuSolo')
        self.window.canvas.create_text(self.x + 50, self.y + 60, anchor='n', text="Non", fill="#B45F04", font="Arial 14", tags='menuSolo')
        self.window.canvas.create_text(self.x + 110, self.y + 60, anchor='n', text="Facile", fill="#B45F04", font="Arial 14", tags='menuSolo')
        self.window.canvas.create_text(self.x + 180, self.y + 60, anchor='n', text="Moyen", fill="#B45F04", font="Arial 14", tags='menuSolo')
        self.window.canvas.create_text(self.x + 250, self.y + 60, anchor='n', text="Difficile", fill="#B45F04", font="Arial 14", tags='menuSolo')


        # AI - 1
        self.window.canvas.create_text(self.x + 30, self.y + 85, anchor='n', text="1.", fill="#B45F04", font="Arial 14", tags='menuSolo')
        self.window.canvas.create_window(self.x + 50, self.y + 85, anchor=NW, window=self.rBoutDiff1_0, tags='menuSolo')
        self.window.canvas.create_window(self.x + 110, self.y + 85, anchor=NW, window=self.rBoutDiff1_1, tags='menuSolo')
        self.window.canvas.create_window(self.x + 180, self.y + 85, anchor=NW, window=self.rBoutDiff1_2, tags='menuSolo')
        self.window.canvas.create_window(self.x + 250, self.y + 85, anchor=NW, window=self.rBoutDiff1_3, tags='menuSolo')




        # couleurs - à changer pour avoir le choix
        self.window.canvas.create_rectangle(self.x + 300, self.y + 85, self.x + 350, self.y + 105, fill="#DF0101", tags='menuSolo')  # ROUGE
        self.window.canvas.create_rectangle(self.x + 300, self.y + 110, self.x + 350, self.y + 130, fill="#2E2EFE", tags='menuSolo')  # BLEU
        self.window.canvas.create_rectangle(self.x + 300, self.y + 135, self.x + 350, self.y + 155, fill="#01DF01", tags='menuSolo')  # VERT
        self.window.canvas.create_rectangle(self.x + 300, self.y + 160, self.x + 350, self.y + 180, fill="#DF01D7", tags='menuSolo')  # MAUVE
        self.window.canvas.create_rectangle(self.x + 300, self.y + 185, self.x + 350, self.y + 205, fill="#FF8000", tags='menuSolo')  # ORANGE
        self.window.canvas.create_rectangle(self.x + 300, self.y + 210, self.x + 350, self.y + 230, fill="#FA58F4", tags='menuSolo')  # ROSE
        self.window.canvas.create_rectangle(self.x + 300, self.y + 235, self.x + 350, self.y + 255, fill="#000000", tags='menuSolo')  # NOIR
        self.window.canvas.create_rectangle(self.x + 300, self.y + 260, self.x + 350, self.y + 280, fill="#FFFFFF", tags='menuSolo')  # BLANC
        self.window.canvas.create_text(self.x + 150, self.y + 300, anchor='n', text="Vitesse du jeu", fill="#B45F04",
                                       font="Arial 14", tags='menuSolo')
        self.window.canvas.create_window(self.x + 30, self.y + 320, anchor=NW, window=self.scaleVitesse, tags='menuSolo')



        self.boutAccept.draw(self.x + 230, self.y + 425)
        self.boutRetour.draw(self.x + 30, self.y + 425)


    def destroy(self):
        self.frameSolo.destroy()
        self.boutAccept.destroy()
        self.boutRetour.destroy()
        self.window.canvas.delete('menuSolo')