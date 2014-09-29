#!/usr/bin/python3

from tkinter import *
import random


class Model(object):
	def __init__(self,size):
		self.size = size
		self.carte = [[0 for x in range(0,size)] for x in range(0,size)]
		self.joueurs = []

		for x in range(0,4):
			self.joueurs.append(self.Joueur(self.size-10))


	def createRessources(self):
		for x in range(0,self.size):
			for y in range(0,self.size):
				self.carte[x][y] = random.randint(0,100)
				if x > 0 and y > 0 and self.carte[x][y] < 100:
					moyenne = (self.carte[x][y] + self.carte[x-1][y] + self.carte[x][y-1]) / 3
					self.carte[x][y] = moyenne

	def update(self):
		for joueur in self.joueurs:
			if joueur.x < self.size/2:
				joueur.x += 1
			elif joueur.x > self.size/2:
				joueur.x -= 1

			if joueur.y < self.size/2:
				joueur.y += 1
			elif joueur.y > self.size/2:
				joueur.y -= 1

	class Joueur(object):
		def __init__(self,size):
			self.x = random.randint(3,size)
			self.y = random.randint(3,size)

class View(object):
	def __init__(self,size):
		self.size = size*6
		self.root = Tk()
		self.canevas = Canvas(self.root,width=self.size/2+2,height=self.size/2+2,bg="white")
		self.radius = 20
		self.canevas.pack()

	def printMap(self,carte,size,joueurs):
		for x in range(0,size):
			for y in range(0,size):
				trouve = 0
				for joueur in joueurs:
					if (joueur.x-x)*(joueur.x-x) < self.radius and (joueur.y-y)*(joueur.y-y) < self.radius:
					#if 1:
						if carte[x][y] < 55:
							self.canevas.create_rectangle(x*3+3,y*3+3,x*3+3+5,y*3+3+5,fill="#0B610B")

						elif carte[x][y] >= 55 and carte[x][y] < 60:
							self.canevas.create_rectangle(x*3+3,y*3+3,x*3+3+5,y*3+3+5,fill="#D7DF01")

						elif carte[x][y] >= 60 and carte[x][y] < 72:
							self.canevas.create_rectangle(x*3+3,y*3+3,x*3+3+5,y*3+3+5,fill="#1C1C1C")

						elif carte[x][y] >= 72 and carte[x][y] <= 99:
							self.canevas.create_rectangle(x*3+3,y*3+3,x*3+3+5,y*3+3+5,fill="#BDBDBD")

						elif carte[x][y] == 100:
							self.canevas.create_rectangle(x*3+3,y*3+3,x*3+3+5,y*3+3+5,fill="#2E9AFE")
						trouve = 1
				if trouve == 0:
					self.canevas.create_rectangle(x*3+3,y*3+3,x*3+3+5,y*3+3+5,fill="gray")

		for joueur in joueurs:
			self.canevas.create_oval(joueur.x*3,joueur.y*3,joueur.x*3+5,joueur.y*3+5,fill="red")

	def updateMap(self,carte,size,joueurs):
		rad = 5
		for joueur in joueurs:
			for x in range(joueur.x-rad,joueur.x+rad):
				if x > 5 and x < size-5:
					for y in range(joueur.y-rad,joueur.y+rad):
						if y > 5 and y < size-5:
							if carte[x][y] < 55:
								self.canevas.create_rectangle(x*3+3,y*3+3,x*3+3+5,y*3+3+5,fill="#0B610B")

							elif carte[x][y] >= 55 and carte[x][y] < 60:
								self.canevas.create_rectangle(x*3+3,y*3+3,x*3+3+5,y*3+3+5,fill="#D7DF01")

							elif carte[x][y] >= 60 and carte[x][y] < 72:
								self.canevas.create_rectangle(x*3+3,y*3+3,x*3+3+5,y*3+3+5,fill="#1C1C1C")

							elif carte[x][y] >= 72 and carte[x][y] <= 99:
								self.canevas.create_rectangle(x*3+3,y*3+3,x*3+3+5,y*3+3+5,fill="#BDBDBD")

							elif carte[x][y] == 100:
								self.canevas.create_rectangle(x*3+3,y*3+3,x*3+3+5,y*3+3+5,fill="#2E9AFE")

		for joueur in joueurs:
			self.canevas.create_oval(joueur.x*3,joueur.y*3,joueur.x*3+5,joueur.y*3+5,fill="red")

class Controller(object):
	"""docstring for Controller"""
	def __init__(self):
		self.model = Model(100)
		self.vue = View(self.model.size)
		self.model.createRessources()
		self.vue.printMap(self.model.carte,self.model.size,self.model.joueurs)

		self.vue.root.after(10,self.Jouer) #refresh every 5 milli seconds

		self.vue.root.mainloop()
		

	def Jouer(self):
		self.model.update()
		self.vue.updateMap(self.model.carte,self.model.size,self.model.joueurs)
		self.vue.root.after(10,self.Jouer) #refresh every 5 milli seconds

def main():
	c = Controller()

if __name__ == '__main__':
	main()