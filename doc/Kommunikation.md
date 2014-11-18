# KOMMUNICATION

## COMBAT
- Unité ne se place pas au même endroit par rapport à leur ennemi dans les différents clients

## DÉPLACEMENT
- Le leader ne pourrait-il pas être le plus près de la position de destination? Parce que parfois une unité peu être à une case de différence de la destination mais va s'en aller dans la direction opposée pour aller rejoindre le Leader pour finalement retourner à la destination.
- Grand Dépalcement Fait des trucs étranges avec certains client parfois (seulement lors de multiple clients). Il se mette à faire les fantômes.


## FICHIER
est-ce que le fichier **dev/minimapTest/main.py** est toujours nécessaires?

## TODO 
SPEED CONTROL (Ping, Server)


# OPTIMISATION DE LA VUE POINT INTÉRESSANT:
http://stackoverflow.com/questions/9855314/python-gui-tkinter-ttk-application-slow
"""My understanding of the canvas is that the more element ids that have been allocated, the slower it gets. It can handle tens of thousands without much problem (and maybe even 100's of thousands), but if you're creating and deleting 6000 items every 100ms, that is likely your problem. Even though you are deleting the items, it still affects performance especially when you are creating 60,000 per second.

Instead of deleting all items every 100ms, simply move the items off screen and remember them, then reuse them by using the coords method to change their coordinates for the new graph."""



### ENCORE:
http://stackoverflow.com/questions/10515720/tkinter-canvas-updating-speed-reduces-during-the-course-of-a-program
"""You create new items at each updates. The canvas display all the rectangles you have previously added and thus go slower and slower (each update create 900 rectangles, after 30 you have 27,000 objects in your scene...)

To avoid this, you may create your rectangles once, and then only update their colors.

You could have at toplevel:

rectangles = [ [ canvas.create_rectangle (CELL_SIZE*x, CELL_SIZE*y,
                    CELL_SIZE*x+CELL_SIZE, CELL_SIZE*y+CELL_SIZE,
                    fill="#000000",outline="#000000", width=1) 
                 for x in range(nCols)] for y in range(nRows)]
and in drawbox:

canvas.itemconfig(rectangles[y][x], fill=color)"""


### ENCORE
http://stackoverflow.com/questions/15839491/tkinter-shapes-clearing-screen
Note that items added to the canvas are kept until you remove them. If you want to change the drawing, you can either use methods like  coords, itemconfig, and move to modify the items, or use delete to remove them.


### ET ENCORE!!!!
http://www.tkdocs.com/tutorial/canvas.html

Il est possible d'afficher un canvas d'une taille de (500px, 500px) mais dont la taille réelle est de (1000px,1000px). Ainsi on peu utiliser des scrollbar ou pas et modifier la partie du canvas afficher avec les méthodes canvasx et canvasy