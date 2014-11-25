from View import *
import socket

        

class MenuInit:
    def __init__(self,vue):
        self.vue = vue
        # position du depart pour draw
        self.initX = 574
        self.initY = 50
        self.canevasInit = Canvas(self.vue.root, width=self.vue.width, height=self.vue.height)
        self.vue.changeCanevas(self.canevasInit)
        self.frameInit = GFrame(self.canevasInit, width=400, height=500)
        self.boutSolo = GButton(self.canevasInit, text="Solo",command=self.vue.creationSolo,color=0)
        self.boutMulti = GButton(self.canevasInit, text="Multijoueur",command=self.vue.menuMultijoueur,color=0)
        self.boutQuitter = GButton(self.canevasInit, text="Quitter",command=self.vue.destroy,color=0)
        self.draw(self.initX,self.initY)

    def draw(self,x,y):
        self.frameInit.draw(x+0, y+0)
        self.canevasInit.create_text(x+200, y+70, text="Âge de l'Empire",fill="#B45F04",font="Arial 26")
        self.canevasInit.create_text(x+100, y+130, text="Jouer",fill="#B45F04",font="Arial 14")
        self.boutSolo.draw(x+100,y+150)
        self.boutMulti.draw(x+100,y+210)
        self.boutQuitter.draw(x+100,y+350)

class MenuMultijoueur:
    def __init__(self,vue):
        self.vue = vue
        # position du depart pour draw
        self.initX = 674
        self.initY = 50
        self.canevasMulti = Canvas(self.vue.root, width=self.vue.width, height=self.vue.height)
        self.vue.changeCanevas(self.canevasMulti)
        self.frameMultiJ = GFrame(self.canevasMulti, width=300, height=400)
        self.boutCrServ = GButton(self.canevasMulti, text="Créer un serveur",command=self.vue.menuServeur,color=0)
        self.boutRejServ = GButton(self.canevasMulti, text="Rejoindre un serveur",command=self.vue.menuRejoindreServeur,color=0)
        self.boutRetour = GButton(self.canevasMulti, text="Retour",command=self.vue.afficheMenuInit,color=0)
        self.draw(self.initX,self.initY)

    def draw(self,x,y):
        self.frameMultiJ.draw(x+0,y+0)
        self.canevasMulti.create_text(x+150, y+50, text="Multijoueur",fill="#B45F04",font="Arial 20")
        self.boutCrServ.draw(x+50,y+100)
        self.boutRejServ.draw(x+50,y+170)
        self.boutRetour.draw(x+50,y+300)


class MenuServeur:
    def __init__(self,vue):
        self.vue = vue
        # position du depart pour draw
        self.initX = 374
        self.initY = 50
        self.canevasServeur = Canvas(self.vue.root, width=self.vue.width, height=self.vue.height)
        self.vue.changeCanevas(self.canevasServeur)
        self.frameServ = GFrame(self.canevasServeur, width=600, height=270)
        self.vue.siServeur = True
        #self.vue.eventListener.controller.startServeur()
        self.ip = socket.gethostbyname(socket.gethostname())
        self.inputNom = Entry(self.canevasServeur, bd=4, font="Courier 20")
        #label "taille de la carte"
        # à faire

        self.boutFinalServ = GButton(self.canevasServeur, text="Finaliser serveur",command=self.lireNom,color=0)
        self.boutRetour = GButton(self.canevasServeur, text="Retour",command=self.vue.menuMultijoueur,color=0)
        self.draw(self.initX,self.initY)

    def lireNom(self):
        # vérifie le nom du joueur
        self.nomJoueur = self.inputNom.get()
        if len(self.nomJoueur) == 0:
            self.nomJoueur = "Batman"
        print(self.nomJoueur)

        self.vue.eventListener.controller.startServeur(self.nomJoueur)
        self.vue.menuLobby()

    def draw(self,x,y):
        self.frameServ.draw(x+0, y+0)
        self.canevasServeur.create_text(x+300, y+20, anchor='n',text="Création du serveur",fill="#B45F04",font="Arial 26")
        self.canevasServeur.create_text(x+300, y+70, anchor='n',text="Votre adresse IP: " + self.ip,fill="#B45F04",font="Arial 20")
        self.canevasServeur.create_text(x+300, y+150, anchor='e',text="Entrez votre nom: ",fill="#B45F04",font="Arial 20")
        self.inputNom.place(x=x+300,y=y+130,width=200,height=40)
        self.boutFinalServ.draw(x+370,y+195)
        self.boutRetour.draw(x+30,y+195)


class MenuRejoindreServeur:
    def __init__(self,vue):
        self.vue = vue
        # position du depart pour draw
        self.initX = 474
        self.initY = 50
        self.canevasRejServ = Canvas(self.vue.root, width=self.vue.width, height=self.vue.height)
        self.vue.changeCanevas(self.canevasRejServ)
        self.frameRejServ = GFrame(self.canevasRejServ, width=500, height=370)
        self.vue.siServeur = False
        self.inputIp = Entry(self.canevasRejServ, bd=4, font="Courier 30")
        #self.inputIp.bind("<Return>",self.testIP)
        self.inputNom = Entry(self.canevasRejServ, bd=4, font="Courier 20")
        self.boutRejoindre = GButton(self.canevasRejServ, text="Rejoindre serveur",command=self.lireNom,color=0)
        self.boutRetour = GButton(self.canevasRejServ, text="Retour",command=self.vue.menuMultijoueur,color=0)
        self.draw(self.initX,self.initY)

    def lireNom(self):
        # vérifie le nom du joueur
        self.nomJoueur = self.inputNom.get()
        if len(self.nomJoueur) == 0:
            self.nomJoueur = "Batgirl"
        print(self.nomJoueur)

        self.vue.eventListener.controller.startServeur(self.nomJoueur)
        self.vue.menuLobby()

    def draw(self,x,y):
        self.frameRejServ.draw(x+0, y+0)
        self.canevasRejServ.create_text(x+250, y+40, anchor='n',text="Entrez l’adresse IP du serveur",fill="#B45F04",font="Arial 20")
        self.inputIp.place(x=x+60,y=y+100,width=380,height=70)
        self.canevasRejServ.create_text(x+250, y+220, anchor='e',text="Entrez votre nom: ",fill="#B45F04",font="Arial 20")
        self.inputNom.place(x=x+250,y=y+200,width=200,height=40)
        self.boutRejoindre.draw(x+270,y+295)
        self.boutRetour.draw(x+30,y+295)

class MenuLobby:
    def __init__(self,vue):
        self.vue = vue
        # position du depart pour draw
        self.initX = 174
        self.initY = 50
        self.canevasLobby = Canvas(self.vue.root, width=self.vue.width, height=self.vue.height)
        self.vue.changeCanevas(self.canevasLobby)
        self.frameLobby = GFrame(self.canevasLobby, width=800, height=550)
        """
        # vérifie le nom du joueur
        self.nomJoueur = self.inputNom.get()
        if len(self.nomJoueur) == 0:
            self.nomJoueur = "Batman"
        """
        #self.clientId = self.vue.eventListener.controller.network.client.id
        #self.clientId = self.vue.eventListener.controller.network.getClientId()
        
        self.clients = self.vue.eventListener.controller.network.client.host.getClients()
        print(self.clients)

        self.boutPret = GButton(self.canevasLobby, text="Prêt",command=self.vue.pret,color=0)
        self.boutQuitServ = GButton(self.canevasLobby, text="Quitter le serveur",command=self.vue.menuMultijoueur,color=0)
        #bouton "Lancer la partie" - si serveur
        if self.vue.siServeur == True:
            self.boutLancerPartie = GButton(self.canevasLobby, text="Lancer la partie",command=self.vue.debutJeu,color=0)
            #label "vitesse"
            #scale "vitesse"
            self.scaleVitesse = Scale(self.canevasLobby,orient=HORIZONTAL,length=250,
                              from_=1, to=10,tickinterval=1, resolution=1,
                              sliderlength=10,troughcolor="#B45F04",fg="#B45F04",
                              width=10,bd=0,showvalue=0,bg="#D3BF8F")
        self.draw(self.initX,self.initY,self.clients)

    def draw(self,x,y,clients):
        nb = len(clients)
        print(nb)
        self.frameLobby.draw(x+0, y+0)
        self.canevasLobby.create_text(x+200, y+30, anchor='n',text="Joueurs",fill="#B45F04",font="Arial 22")
        #couleur = Color()
        # TODO - chercher dans View - Color
        #              ROUGE     BLEU        VERT       MAUVE    ORANGE      ROSE        NOIR      BLANC      JAUNE
        couleurs = ["#D34343", "#3D99BB", "#26BE2E", "#5637DD", "#F39621", "#CF4592", "#0F0F0F", "#FFFFFF", "#F5F520"]
        # fond pour les joueurs
        self.canevasLobby.create_rectangle(x+30,y+75,x+400,y+350, fill="#E1F5A9")
        # afficher l'information des joueurs
        ligne = 1
        for i in range(nb):
            # ID de client
            self.canevasLobby.create_text(x+35, y+50+30*ligne, anchor='nw',text=clients[i]["name"],fill="#B45F04",font="Arial 14")
            # couleur de client
            self.canevasLobby.create_rectangle(x+345,y+55+30*ligne,x+395,y+75+30*ligne, fill=couleurs[clients[i]["civId"]-1])
            ligne+=1

        self.boutPret.draw(x+30,y+370)
        self.boutQuitServ.draw(x+30,y+475)
        if self.vue.siServeur == True:
            self.boutLancerPartie.draw(x+570,y+475)
            self.canevasLobby.create_text(x+600, y+50, anchor='n',text="Vitesse du jeu",fill="#B45F04",font="Arial 20")
            self.scaleVitesse.place(x=x+470, y=y+80)

class MenuSolo:
    def __init__(self,vue):
        self.vue = vue
        # position du depart pour draw
        self.initX = 524
        self.initY = 50
        self.canevasSolo = Canvas(self.vue.root, width=self.vue.width, height=self.vue.height)
        self.vue.changeCanevas(self.canevasSolo)
        self.frameSolo = GFrame(self.canevasSolo, width=450, height=500)
        # AI - 1
        self.varDif1 = IntVar()
        self.rBoutDiff1_0 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif1, value=0, bg="#D3BF8F")
        self.rBoutDiff1_1 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif1, value=1, bg="#D3BF8F")
        self.rBoutDiff1_2 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif1, value=2, bg="#D3BF8F")
        self.rBoutDiff1_3 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif1, value=3, bg="#D3BF8F")
        self.rBoutDiff1_1.select()
        # AI - 2
        self.varDif2 = IntVar()
        self.rBoutDiff2_0 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif2, value=0, bg="#D3BF8F")
        self.rBoutDiff2_1 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif2, value=1, bg="#D3BF8F")
        self.rBoutDiff2_2 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif2, value=2, bg="#D3BF8F")
        self.rBoutDiff2_3 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif2, value=3, bg="#D3BF8F")
        self.rBoutDiff2_0.select()
        # AI - 3
        self.varDif3 = IntVar()
        self.rBoutDiff3_0 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif3, value=0, bg="#D3BF8F")
        self.rBoutDiff3_1 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif3, value=1, bg="#D3BF8F")
        self.rBoutDiff3_2 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif3, value=2, bg="#D3BF8F")
        self.rBoutDiff3_3 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif3, value=3, bg="#D3BF8F")
        self.rBoutDiff3_0.select()
        # AI - 4
        self.varDif4 = IntVar()
        self.rBoutDiff4_0 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif4, value=0, bg="#D3BF8F")
        self.rBoutDiff4_1 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif4, value=1, bg="#D3BF8F")
        self.rBoutDiff4_2 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif4, value=2, bg="#D3BF8F")
        self.rBoutDiff4_3 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif4, value=3, bg="#D3BF8F")
        self.rBoutDiff4_0.select()
        # AI - 5
        self.varDif5 = IntVar()
        self.rBoutDiff5_0 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif5, value=0, bg="#D3BF8F")
        self.rBoutDiff5_1 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif5, value=1, bg="#D3BF8F")
        self.rBoutDiff5_2 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif5, value=2, bg="#D3BF8F")
        self.rBoutDiff5_3 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif5, value=3, bg="#D3BF8F")
        self.rBoutDiff5_0.select()
        # AI - 6
        self.varDif6 = IntVar()
        self.rBoutDiff6_0 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif6, value=0, bg="#D3BF8F")
        self.rBoutDiff6_1 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif6, value=1, bg="#D3BF8F")
        self.rBoutDiff6_2 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif6, value=2, bg="#D3BF8F")
        self.rBoutDiff6_3 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif6, value=3, bg="#D3BF8F")
        self.rBoutDiff6_0.select()
        # AI - 7
        self.varDif7 = IntVar()
        self.rBoutDiff7_0 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif7, value=0, bg="#D3BF8F")
        self.rBoutDiff7_1 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif7, value=1, bg="#D3BF8F")
        self.rBoutDiff7_2 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif7, value=2, bg="#D3BF8F")
        self.rBoutDiff7_3 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif7, value=3, bg="#D3BF8F")
        self.rBoutDiff7_0.select()
        # AI - 8
        self.varDif8 = IntVar()
        self.rBoutDiff8_0 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif8, value=0, bg="#D3BF8F")
        self.rBoutDiff8_1 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif8, value=1, bg="#D3BF8F")
        self.rBoutDiff8_2 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif8, value=2, bg="#D3BF8F")
        self.rBoutDiff8_3 = Radiobutton(self.canevasSolo, anchor='n', variable=self.varDif8, value=3, bg="#D3BF8F")
        self.rBoutDiff8_0.select()
        #scale "vitesse"
        self.scaleVitesse = Scale(self.canevasSolo,orient=HORIZONTAL,length=250,
                          from_=1, to=10,tickinterval=1, resolution=1,
                          sliderlength=10,troughcolor="#B45F04",fg="#B45F04",
                          width=10,bd=0,showvalue=0,bg="#D3BF8F")
        
        self.boutAccept = GButton(self.canevasSolo, text="Lancer la partie",command=self.vue.debutJeu,color=0)
        #bouton "retour"
        self.boutRetour = GButton(self.canevasSolo, text="Retour",command=self.vue.afficheMenuInit,color=0)
        self.draw(self.initX,self.initY)
        
        self.vue.eventListener.controller.startServeur()

    def draw(self,x,y):
        self.frameSolo.draw(x+0, y+0)
        self.canevasSolo.create_text(x+420, y+20, anchor='ne',text="Solo",fill="#B45F04",font="Arial 40")
        self.canevasSolo.create_text(x+100, y+30, anchor='nw',text="Ennemis",fill="#B45F04",font="Arial 20")
        self.canevasSolo.create_text(x+50, y+60, anchor='n',text="Non",fill="#B45F04",font="Arial 14")
        self.canevasSolo.create_text(x+110, y+60, anchor='n',text="Facile",fill="#B45F04",font="Arial 14")
        self.canevasSolo.create_text(x+180, y+60, anchor='n',text="Moyen",fill="#B45F04",font="Arial 14")
        self.canevasSolo.create_text(x+250, y+60, anchor='n',text="Difficile",fill="#B45F04",font="Arial 14")
        # AI - 1
        self.canevasSolo.create_text(x+30, y+85, anchor='n',text="1.",fill="#B45F04",font="Arial 14")
        self.rBoutDiff1_0.place(x=x+50, y=y+85)
        self.rBoutDiff1_1.place(x=x+110, y=y+85)
        self.rBoutDiff1_2.place(x=x+180, y=y+85)
        self.rBoutDiff1_3.place(x=x+250, y=y+85)
        # AI - 2
        self.canevasSolo.create_text(x+30, y+110, anchor='n',text="2.",fill="#B45F04",font="Arial 14")
        self.rBoutDiff2_0.place(x=x+50, y=y+110)
        self.rBoutDiff2_1.place(x=x+110, y=y+110)
        self.rBoutDiff2_2.place(x=x+180, y=y+110)
        self.rBoutDiff2_3.place(x=x+250, y=y+110)
        # AI - 3
        self.canevasSolo.create_text(x+30, y+135, anchor='n',text="3.",fill="#B45F04",font="Arial 14")
        self.rBoutDiff3_0.place(x=x+50, y=y+135)
        self.rBoutDiff3_1.place(x=x+110, y=y+135)
        self.rBoutDiff3_2.place(x=x+180, y=y+135)
        self.rBoutDiff3_3.place(x=x+250, y=y+135)
        # AI - 4
        self.canevasSolo.create_text(x+30, y+160, anchor='n',text="4.",fill="#B45F04",font="Arial 14")
        self.rBoutDiff4_0.place(x=x+50, y=y+160)
        self.rBoutDiff4_1.place(x=x+110, y=y+160)
        self.rBoutDiff4_2.place(x=x+180, y=y+160)
        self.rBoutDiff4_3.place(x=x+250, y=y+160)
        # AI - 5
        self.canevasSolo.create_text(x+30, y+185, anchor='n',text="5.",fill="#B45F04",font="Arial 14")
        self.rBoutDiff5_0.place(x=x+50, y=y+185)
        self.rBoutDiff5_1.place(x=x+110, y=y+185)
        self.rBoutDiff5_2.place(x=x+180, y=y+185)
        self.rBoutDiff5_3.place(x=x+250, y=y+185)
        # AI - 6
        self.canevasSolo.create_text(x+30, y+210, anchor='n',text="6.",fill="#B45F04",font="Arial 14")
        self.rBoutDiff6_0.place(x=x+50, y=y+210)
        self.rBoutDiff6_1.place(x=x+110, y=y+210)
        self.rBoutDiff6_2.place(x=x+180, y=y+210)
        self.rBoutDiff6_3.place(x=x+250, y=y+210)
        # AI - 7
        self.canevasSolo.create_text(x+30, y+235, anchor='n',text="7.",fill="#B45F04",font="Arial 14")
        self.rBoutDiff7_0.place(x=x+50, y=y+235)
        self.rBoutDiff7_1.place(x=x+110, y=y+235)
        self.rBoutDiff7_2.place(x=x+180, y=y+235)
        self.rBoutDiff7_3.place(x=x+250, y=y+235)
        # AI - 8
        self.canevasSolo.create_text(x+30, y+260, anchor='n',text="8.",fill="#B45F04",font="Arial 14")
        self.rBoutDiff8_0.place(x=x+50, y=y+260)
        self.rBoutDiff8_1.place(x=x+110, y=y+260)
        self.rBoutDiff8_2.place(x=x+180, y=y+260)
        self.rBoutDiff8_3.place(x=x+250, y=y+260)
        # couleurs - à changer pour avoir le choix
        self.canevasSolo.create_rectangle(x+300,y+85,x+350,y+105, fill="#DF0101")  # ROUGE
        self.canevasSolo.create_rectangle(x+300,y+110,x+350,y+130, fill="#2E2EFE") # BLEU
        self.canevasSolo.create_rectangle(x+300,y+135,x+350,y+155, fill="#01DF01") # VERT
        self.canevasSolo.create_rectangle(x+300,y+160,x+350,y+180, fill="#DF01D7") # MAUVE
        self.canevasSolo.create_rectangle(x+300,y+185,x+350,y+205, fill="#FF8000") # ORANGE
        self.canevasSolo.create_rectangle(x+300,y+210,x+350,y+230, fill="#FA58F4") # ROSE
        self.canevasSolo.create_rectangle(x+300,y+235,x+350,y+255, fill="#000000") # NOIR
        self.canevasSolo.create_rectangle(x+300,y+260,x+350,y+280, fill="#FFFFFF") # BLANC
        self.canevasSolo.create_text(x+150, y+300, anchor='n',text="Vitesse du jeu",fill="#B45F04",font="Arial 14")
        self.scaleVitesse.place(x=x+30, y=y+320)
        self.boutAccept.draw(x+230,y+425)
        self.boutRetour.draw(x+30,y+425)