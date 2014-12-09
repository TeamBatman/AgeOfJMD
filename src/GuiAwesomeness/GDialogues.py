#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'fireraccon A.K.A Jean-William Perreault'
from GuiAwesomeness.GButtons import *
from GuiAwesomeness.GPanels import *


try:
    # Python2
    from Tkinter import NW
except ImportError:
    # Python3
    from tkinter import NW


# TODO FIX THIS SHIT
class GConfirmDialogue(GFrame):

    def __init__(self, parent, message, command=None, color=0):
        self.message = message
        self.command = command
        #self.buttonYes = GCheckButton(parent, command=self.onYes)
        #self.buttonNo = GCrossButton(parent, command=self.onNo)

        self.button = GButton(parent, text="OK", command=self.onOK, color=color)
        GFrame.__init__(self, parent, width=300, height=150, color=color)
        # CHANGE INSET HEIGHT AND REBUILD
        self.panelInset.height = self.button.height + self.margin
        self.panelInset._buildFullImage()

       #self.button = GCheckButton(parent, command=self.onOK, color=self.btnColor)


    def onOK(self):
        self.destroy()

    def draw(self, x, y):
        PANEL_WIDTH = 300
        PANEL_HEIGHT = 250
        MARGIN = 15

        INSET_WIDTH = PANEL_WIDTH - MARGIN
        INSET_HEIGHT = PANEL_HEIGHT - 80

        self.panel.draw(x, y, PANEL_WIDTH, PANEL_HEIGHT)

        inset_x = x + PANEL_WIDTH / 2 - INSET_WIDTH / 2 + 2
        inset_y = y + MARGIN
        self.panelInset.draw(inset_x, inset_y, INSET_WIDTH, INSET_HEIGHT)

        self.parent.create_text(inset_x + 10, inset_y + 12, text=self.message, anchor=NW, font="Helvetica",
                                fill="#575246", tags=self.id)

        btn_x = x + PANEL_WIDTH / 2 - self.button.width / 2
        btn_y = y + PANEL_HEIGHT - self.button.height - MARGIN
        self.button.draw(btn_x, btn_y)

    def destroy(self):
        self.panel.destroy()
        self.panelInset.destroy()
        self.button.destroy()


class GChoiceDialogue(GFrame):
    """ YES/NO Dialogue """
    # CHOICES
    YES = 0
    NO = 1

    def __init__(self, parent, message, command=None, color=0):
        self.message = message
        self.command = command
        self.buttonYes = GCheckButton(parent, command=self.onYes)
        self.buttonNo = GCrossButton(parent, command=self.onNo)

        GFrame.__init__(self, parent, width=300, height=150, color=color)
        # CHANGE INSET HEIGHT AND REBUILD
        self.panelInset.height = self.buttonYes.height + self.margin
        self.panelInset._buildFullImage()





    def draw(self, x, y):
        GFrame.draw(self, x, y)
        # DRAW TEXT
        textX = self.panelInset.x + 10
        textY = self.panelInset.y + 12
        self.parent.create_text(textX, textY, text=self.message, anchor=NW,
                                font='Helvetica', fill='#575246', tags=self.id)

        # DRAW BUTTONS IN THE CENTER OF THE FRAME
        total = self.buttonYes.width * 2 + self.margin
        total_x = x + self.width / 2 - total / 2

        btn_y = y + self.height - self.buttonYes.height - self.margin
        self.buttonYes.draw(total_x, btn_y)

        no_x = total_x + self.margin + self.buttonNo.width / 2
        self.buttonNo.draw(no_x + self.margin, btn_y)

    def destroy(self):
        GFrame.destroy(self)
        self.buttonYes.destroy()
        self.buttonNo.destroy()

    def onYes(self):
        self.command(GChoiceDialogue.YES)

    def onNo(self):
        self.command(GChoiceDialogue.NO)

