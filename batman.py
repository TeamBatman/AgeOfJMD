# -*- coding: iso-8859-1 -*-

#Oleksandr Yuvzhenko

from tkinter import *
from carte import *

class Vue():
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.canevasActif = None
        # valeurs entrées pour l'affichage
        self.miniX = 0
        self.miniY = 0

    def changeCanevas(self, canev):
        if self.canevasActif:
            self.canevasActif.pack_forget()
        self.canevasActif = canev
        self.canevasActif.pack()
    
    def afficheMenuInit(self, event):
        self.canevasInit = Canvas(self.root, width=400, height=500,
                            bg="#FFDA81")
        #self.canevasInit.pack()
        self.changeCanevas(self.canevasInit)
        
        #label titre
        self.labelTitre = Label(self.canevasInit,
                                text="Âge de l'Empire",
                                font="Arial 26",
                                bg="#FFDA81")
        self.labelTitre.place(x=80, y=20)
        
        #label "jouer"
        self.labelJouer = Label(self.canevasInit,
                                text="Jouer",
                                font="Arial 14",
                                bg="#FFDA81")
        self.labelJouer.place(x=70, y=110)
       
        #bouton "jouer solo"
        self.boutSolo = Button(self.canevasInit,
                               text="Solo",
                               font="Arial 14",
                               bg="#C88C3C",
                               fg="#FFF000")
        self.boutSolo.bind("<Button-1>", self.creationSolo)
        self.boutSolo.place(x=100, y=150, width=200, height=50)
        
        #bouton "jouer multijoueur"
        self.boutMulti = Button(self.canevasInit,
                                text="Multijoueur",
                                font="Arial 14",
                                bg="#C88C3C",
                                fg="#FFF000")
        self.boutMulti.bind("<Button-1>", self.menuMultijoueur)
        self.boutMulti.place(x=100, y=210, width=200, height=50)
    
        #bouton "quitter"
        self.boutQuitter = Button(self.canevasInit,
                                  text="Quitter",
                                  font="Arial 14",
                                  bg="#C88C3C",
                                  fg="#FFF000")
        self.boutQuitter.bind("<Button-1>", self.fermer)
        self.boutQuitter.place(x=100, y=350, width=200, height=50)
        
    def menuMultijoueur(self, event):
        self.canevasMulti = Canvas(self.root, width=300, height=400,
                            bg="#006300")
        self.changeCanevas(self.canevasMulti)
        
        #bouton "créer un serveur"
        self.boutCrServ = Button(self.canevasMulti,
                                text="Créer un serveur",
                                font="Arial 14",
                                bg="#C88C3C",
                                fg="#FFF000")
        self.boutCrServ.place(x=50, y=50, width=200, height=80)
        
        #bouton "rejoindre un serveur"
        self.boutRejServ = Button(self.canevasMulti,
                                text="Rejoindre un serveur",
                                font="Arial 14",
                                bg="#C88C3C",
                                fg="#FFF000")
        self.boutRejServ.place(x=50, y=150, width=200, height=80)
        
        #bouton "retour"
        self.boutRetour = Button(self.canevasMulti,
                                text="Retour",
                                font="Arial 14",
                                bg="#C88C3C",
                                fg="#FFF000")
        self.boutRetour.bind("<Button-1>", self.afficheMenuInit)
        self.boutRetour.place(x=100, y=300, width=100, height=50)
        
    def creationSolo(self, event):
        self.canevasSolo = Canvas(self.root, width=540, height=400,
                            bg="#C0C0C0")
        self.changeCanevas(self.canevasSolo)
        
        #label "couleur"
        self.labelCouleur = Label(self.canevasSolo,
                                text="Couleur",
                                font="Arial 14",
                                bg="#C0C0C0")
        self.labelCouleur.place(x=20, y=20)
        
        #radiobutton "couleur"
        self.varCoul = IntVar()
        self.rBoutCoul1 = Radiobutton(self.canevasSolo, text='Rouge', variable=self.varCoul, value=1, bg="#C0C0C0", selectcolor="#FF0000")
        self.rBoutCoul2 = Radiobutton(self.canevasSolo, text='Jaune', variable=self.varCoul, value=2, bg="#C0C0C0", selectcolor="#FFFF00")
        self.rBoutCoul3 = Radiobutton(self.canevasSolo, text='Lime', variable=self.varCoul, value=3, bg="#C0C0C0", selectcolor="#00FF00")
        self.rBoutCoul4 = Radiobutton(self.canevasSolo, text='Syan', variable=self.varCoul, value=4, bg="#C0C0C0", selectcolor="#00FFFF")
        self.rBoutCoul5 = Radiobutton(self.canevasSolo, text='Bleu', variable=self.varCoul, value=5, bg="#C0C0C0", selectcolor="#0000FF")
        self.rBoutCoul6 = Radiobutton(self.canevasSolo, text='Magenta', variable=self.varCoul, value=6, bg="#C0C0C0", selectcolor="#FF00FF")
        self.rBoutCoul7 = Radiobutton(self.canevasSolo, text='Orange', variable=self.varCoul, value=7, bg="#C0C0C0", selectcolor="#FFA500")
        self.rBoutCoul8 = Radiobutton(self.canevasSolo, text='Vert', variable=self.varCoul, value=8, bg="#C0C0C0", selectcolor="#008000")
        self.rBoutCoul9 = Radiobutton(self.canevasSolo, text='Rose', variable=self.varCoul, value=9, bg="#C0C0C0", selectcolor="#FFC0CB")
        self.rBoutCoul1.place(x=20, y=60)
        self.rBoutCoul2.place(x=20, y=90)
        self.rBoutCoul3.place(x=20, y=120)
        self.rBoutCoul4.place(x=20, y=150)
        self.rBoutCoul5.place(x=20, y=180)
        self.rBoutCoul6.place(x=150, y=60)
        self.rBoutCoul7.place(x=150, y=90)
        self.rBoutCoul8.place(x=150, y=120)
        self.rBoutCoul9.place(x=150, y=150)
        self.rBoutCoul1.select()
        
        #label "civilisation"
        self.labelCivil = Label(self.canevasSolo,
                                text="Civilisation",
                                font="Arial 14",
                                bg="#C0C0C0")
        self.labelCivil.place(x=20, y=220)
        
        #radiobutton "civilisation"
        self.varCivil = IntVar()
        self.rBoutCivil1 = Radiobutton(self.canevasSolo, text='civilisation 1', variable=self.varCivil, value=1, bg="#C0C0C0")
        self.rBoutCivil2 = Radiobutton(self.canevasSolo, text='civilisation 2', variable=self.varCivil, value=2, bg="#C0C0C0")
        self.rBoutCivil3 = Radiobutton(self.canevasSolo, text='civilisation 3', variable=self.varCivil, value=3, bg="#C0C0C0")
        self.rBoutCivil1.place(x=20, y=260)
        self.rBoutCivil2.place(x=20, y=300)
        self.rBoutCivil3.place(x=20, y=340)
        self.rBoutCivil1.select()
        
        #label "difficulté"
        self.labelDiffic = Label(self.canevasSolo,
                                text="Difficulté",
                                font="Arial 14",
                                bg="#C0C0C0")
        self.labelDiffic.place(x=150, y=220)
        
        #radiobutton "difficulté"
        self.varDif = IntVar()
        self.rBoutDiff1 = Radiobutton(self.canevasSolo, text='facile', variable=self.varDif, value=1, bg="#C0C0C0")
        self.rBoutDiff2 = Radiobutton(self.canevasSolo, text='moyenne', variable=self.varDif, value=2, bg="#C0C0C0")
        self.rBoutDiff3 = Radiobutton(self.canevasSolo, text='difficile', variable=self.varDif, value=3, bg="#C0C0C0")
        self.rBoutDiff1.place(x=150, y=260)
        self.rBoutDiff2.place(x=150, y=300)
        self.rBoutDiff3.place(x=150, y=340)
        self.rBoutDiff2.select()
        
        #label "vitesse"
        self.labelVitesse = Label(self.canevasSolo,
                                text="Vitesse du jeu",
                                font="Arial 14",
                                bg="#C0C0C0")
        self.labelVitesse.place(x=320, y=20)
        
        #scale "vitesse"
        self.scaleVitesse = Scale(self.canevasSolo,
                          orient=HORIZONTAL,
                          length=200,
                          from_=1, to=10,
                          tickinterval=1, resolution=1,
                          bg="#FFF")
        self.scaleVitesse.place(x=320, y=50)
        
        #label "nbAI"
        self.labelNbAI = Label(self.canevasSolo,
                                text="Nombre d'ennemis",
                                font="Arial 14",
                                bg="#C0C0C0")
        self.labelNbAI.place(x=320, y=120)
        
        #scale "nbAI"
        self.scaleNbAI = Scale(self.canevasSolo,
                          orient=HORIZONTAL,
                          length=200,
                          from_=1, to=8,
                          tickinterval=1, resolution=1,
                          bg="#FFF")
        self.scaleNbAI.place(x=320, y=150)
        
        #bouton "accepter"
        self.boutAccept = Button(self.canevasSolo,
                                text="Accepter",
                                font="Arial 14",
                                bg="#C0C0C0", cursor="hand2")
        self.boutAccept.bind("<Button-1>", self.debutJeu)
        self.boutAccept.place(x=420, y=250, width=100, height=50)
        
        #bouton "retour"
        self.boutRetour = Button(self.canevasSolo,
                                text="Retour",
                                font="Arial 14",
                                bg="#C0C0C0")
        self.boutRetour.bind("<Button-1>", self.afficheMenuInit)
        self.boutRetour.place(x=420, y=310, width=100, height=50)
        
    def debutJeu(self, event):
        #800 600
        self.largeur = 1000
        self.hauteur = 800
        self.nbCasesHoriz = 50
        self.nbCasesVert = 50
        self.canevasJeu = Canvas(self.root, width=self.largeur, height=self.hauteur,
                            bg="#C0C0C0", cursor="hand2")
        self.changeCanevas(self.canevasJeu)
        self.canevasJeu.bind("<Button-1>", self.getXY)
        #taille des caisses sur la mini-carte
        self.mCaisse = 4
               
        """
        for i in carte:
            if i==0:
                self.canevasJeu.create_rectangle(x,y,x+30,y+30,fill="white",outline="blue")
                self.canevasJeu.create_rectangle(x1,y1,x1+3,y1+3,fill="yellow")
            elif i==1:
                self.canevasJeu.create_rectangle(x,y,x+30,y+30,fill="black",outline="blue")
                self.canevasJeu.create_rectangle(x1,y1,x1+3,y1+3,fill="green")
            else:
                self.canevasJeu.create_rectangle(x,y,x+30,y+30,fill="red",outline="blue")
                self.canevasJeu.create_rectangle(x1,y1,x1+3,y1+3,fill="pink")
            
            if x==1470:
                x=0
                y=y+30
                x1=650
                y1=y1+3
            else:
                x=x+30
                x1=x1+3
        """
        # affiche carte
        carte = self.parent.getCarte()
        x = 0
        y = 0
        #self.xEntre=0 # valeurs entrées pour affichage
        #yEntre=0
        mX = self.miniX
        mY = self.miniY
        while mY < self.nbCasesVert:
            if carte[mY][mX] == 0:
                self.canevasJeu.create_rectangle(x, y, x + 30, y + 30, fill="white", outline="blue")
            elif  carte[mY][mX] == 1:
                self.canevasJeu.create_rectangle(x, y, x + 30, y + 30, fill="black", outline="blue")
            elif  carte[mY][mX] == 2:
                self.canevasJeu.create_rectangle(x, y, x + 30, y + 30, fill="tan", outline="blue")
            elif  carte[mY][mX] == 3:
                self.canevasJeu.create_rectangle(x, y, x + 30, y + 30, fill="yellow", outline="blue")
            else:
                self.canevasJeu.create_rectangle(x, y, x + 30, y + 30, fill="red", outline="blue")
            if mX == self.nbCasesHoriz - 1:
                x = 0
                mX = self.miniX
                y = y + 30
                mY = mY + 1
            else:
                mX = mX + 1
                x = x + 30
                
        
        
        # affiche mini-carte
        x1 = self.largeur - 200
        y1 = 0
        mX = 0
        mY = 0
        
        while mY < self.nbCasesVert:
            if carte[mY][mX] == 0:
                self.canevasJeu.create_rectangle(x1, y1, x1 + self.mCaisse, y1 + self.mCaisse, fill="white")
            elif  carte[mY][mX] == 1:
                self.canevasJeu.create_rectangle(x1, y1, x1 + self.mCaisse, y1 + self.mCaisse, fill="black")
            elif  carte[mY][mX] == 2:
                self.canevasJeu.create_rectangle(x1, y1, x1 + self.mCaisse, y1 + self.mCaisse, fill="tan")
            elif  carte[mY][mX] == 3:
                self.canevasJeu.create_rectangle(x1, y1, x1 + self.mCaisse, y1 + self.mCaisse, fill="yellow")
            else:
                self.canevasJeu.create_rectangle(x1, y1, x1 + self.mCaisse, y1 + self.mCaisse, fill="red")
            if mX == self.nbCasesHoriz - 1:
                x1 = self.largeur - 200
                mX = 0
                y1 = y1 + self.mCaisse
                mY = mY + 1
            else:
                mX = mX + 1
                x1 = x1 + self.mCaisse
                
       # affiche menu de jeu
        self.canMenuBas = Canvas(self.canevasJeu, width=800, height=150,
                            bg="#DEB887")
        self.canMenuBas.place(x=0, y=650)
        self.canMenuDroit = Canvas(self.canevasJeu, width=200, height=600,
                            bg="#DEB887")
        self.canMenuDroit.place(x=800, y=200)
        
        # label age
        self.labelAge = Label(self.canMenuBas,
                                text="Âge: Préhistoire",
                                font="Arial 14",
                                bg="#DEB887")
        self.labelAge.place(x=20, y=20)
        
        # label population
        self.labelPopul = Label(self.canMenuBas,
                                text="Population: 5",
                                font="Arial 14",
                                bg="#DEB887")
        self.labelPopul.place(x=220, y=20)
        
        # label morale
        self.labelMoral = Label(self.canMenuBas,
                                text="Morale: 100/100",
                                font="Arial 14",
                                bg="#DEB887")
        self.labelMoral.place(x=20, y=70)
        
        # label nourriture
        self.labelNourrit = Label(self.canMenuBas,
                                text="Nourriture: 100",
                                font="Arial 14",
                                bg="#DEB887")
        self.labelNourrit.place(x=220, y=70)
        
        # label bois
        self.labelBois = Label(self.canMenuBas,
                                text="Bois: 10",
                                font="Arial 14",
                                bg="#DEB887")
        self.labelBois.place(x=370, y=20)
        
        
    
    def afficheMinicarte(self):
        pass
    
    #lire les coord. sur la mini carte
    def getXY(self, event):
        if (event.x >self.largeur-200 and event.x < self.largeur):
            if (event.y >= 0 and event.y < 200):
                print(event.x, event.y)
                #chaques 4 px == une caisse
                miniX = int((event.x - (self.largeur-200)) / self.mCaisse)
                miniY = int(event.y / self.mCaisse)
                #placer camera au centre choisi
                if miniX < 13:
                    miniX = 0
                elif (miniX >= 13 and miniX < 24):
                    miniX = miniX - 13
                else:
                    miniX = 24
                if miniY < 11:
                    miniY = 0
                elif(miniY >= 11 and miniY < 28):
                    miniY = miniY - 11
                else:
                    miniY = 28
                #miniX et miniY - 0.0 de mini carte
                self.miniX = miniX
                self.miniY = miniY
                print(self.miniX, self.miniY)
                self.debutJeu(event)
            
                #entourer la zone choisie
                self.canevasJeu.create_line(event.x-13*self.mCaisse,event.y-10*self.mCaisse, event.x+13*self.mCaisse,event.y-10*self.mCaisse,width=2,fill="white")
                self.canevasJeu.create_line(event.x+13*self.mCaisse,event.y-10*self.mCaisse, event.x+13*self.mCaisse,event.y+10*self.mCaisse,width=2,fill="white")
                self.canevasJeu.create_line(event.x+13*self.mCaisse,event.y+10*self.mCaisse, event.x-13*self.mCaisse,event.y+10*self.mCaisse,width=2,fill="white")
                self.canevasJeu.create_line(event.x-13*self.mCaisse,event.y+10*self.mCaisse, event.x-13*self.mCaisse,event.y-10*self.mCaisse,width=2,fill="white")
            
        #else:
            #self.menuJeu()
                
    def menuUhit(self):
        self.canevUnit = Canvas(self.canevasJeu, width=800, height=150,
                            bg="#FF7F50")
        self.canevUnit.place(x=0, y=650)
        
                
        
    def fermer(self, event):
        self.root.destroy() 
     
        
class Modele():
    def __init__(self, parent):
        self.parent = parent
        
        
class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.vue = Vue(self)
        
        self.carte = Carte()
        self.vue.afficheMenuInit(self)
        
        
        self.vue.root.mainloop()
        
    def getCarte(self):
        #return self.modele.carte
        return self.carte.carteTest
        
if __name__ == '__main__':
    c = Controleur()
