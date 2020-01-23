from tkinter import Tk, Canvas, Event
from tkinter.constants import *

from typing import List

from .eventThread import EventThread

from .base.gameObject import GameObject

from .base.fonts import initializeFonts

from .objects.circle import Circle

from .gameState import GameState

# a subclass of Canvas for dealing with resizing of windows
class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

class Game:
    '''
    A Game object contains all the logic necessary for the game loop.
    '''

    def __init__(self, width = 1280, height = 720, frameDelay: int = 17):

        self.width: int = width
        self.height: int = height
        self.frameDelay: int = frameDelay

        self.eventThread: EventThread = EventThread()

        # Create the tk root and initialize the canvas
        self.root = Tk()
        self.canvas: Canvas = ResizingCanvas(self.root, width = self.width, height = self.height, highlightthickness = 0)

        # Set the background of canvas to black, just so it looks sleeker
        self.canvas.configure(background = '#000')

        # Pack the canvas so it can be used
        self.canvas.pack(expand = True, fill = "both")

        # Initialize all the event callbacks
        self.root.bind_all("<Motion>", self.eventCallback)
        self.root.bind_all("<Key>", self.eventCallback)

        # Initialize everything which gameObject will use
        initializeFonts()

        cols = 4
        rows = 6
        

        width = self.width // cols
        height = self.height // rows

        for x in range(cols):
            for y in range(rows):
                button = Circle(
                    self.canvas,
                    (x * width, y * height),
                    15.4
                )

                GameState.addGameObject(button)

    def eventCallback(self, event: Event):
        '''
        Generic Event callback function. All events should send callbacks here.
        '''

        self.eventThread.eventQueue.append(event)


    def start(self):
        initializeFonts()

        self.eventThread.start()

        self.root.mainloop()

        self.eventThread.isActive = False
