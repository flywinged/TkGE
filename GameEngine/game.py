from tkinter import Tk, Canvas, Event, Frame
from tkinter.constants import *

from typing import List, Tuple

from .eventThread import EventThread

from .base.gameObject import GameObject

from .base.fonts import initializeFonts
from .base.fonts import courier

from .objects.circle import Circle

from .gameState import GameState

def setAspectRatio(contentFrame: Canvas, padFrame: Frame, aspectRatio: float):
    '''
    Function which forces the content frame to maintain a specified aspect ratio.
    It does this by placing the content frame inside of a padded frame, and resizes the content frame accordingly.

    Parameters
    ----------
    @param contentFrame - The canvas object where everything is placed

    @param padFrame - Frame containing the content frame

    @param aspectRatio - Desired fixed aspect ratio
    '''
    
    def enforceAspectRatio(event: Event):
        '''
        Enforce function to be bound to tkinter.bind
        '''

        # start by using the width as the controlling dimension
        desiredWidth = event.width
        desiredHeight = int(event.width / aspectRatio)

        # if the window is too tall to fit, use the height as
        # the controlling dimension
        if desiredHeight > event.height:
            desiredHeight = event.height
            desiredWidth = int(event.height * aspectRatio)

        # Determine the change in size of the content frame
        widthScale = desiredWidth / int(contentFrame.cget("width"))
        heightScale = desiredHeight / int(contentFrame.cget("height"))

        # place the window, giving it an explicit size
        contentFrame.place(in_=padFrame, x=(event.width - desiredWidth)//2, y=(event.height - desiredHeight) // 2, 
            width=desiredWidth, height=desiredHeight)
        
        # Resize everything in the contentFrame
        contentFrame.configure(width = desiredWidth, height = desiredHeight)
        contentFrame.scale("all", 0, 0, widthScale, heightScale)

    padFrame.bind("<Configure>", enforceAspectRatio)

class Game:
    '''
    A Game object contains all the logic necessary for the game loop.
    '''

    def __init__(self, width = 1280, height = 720, frameDelay: int = 17, forceAspectRatio: bool = True):

        self.width: int = width
        self.height: int = height
        self.aspectRatio: float = self.width / self.height
        self.forceAspectRatio: bool = forceAspectRatio
        self.frameDelay: int = frameDelay

        self.eventThread: EventThread = EventThread()

        # Create the tk root and initialize the canvas
        self.root = Tk()
        self.padFrame = Frame(borderwidth = 0, background = "green", width = self.width, height = self.height)
        self.padFrame.grid(row = 0, column = 0, sticky="nsew")
        self.canvas: Canvas = Canvas(self.root, width = self.width, height = self.height, highlightthickness = 0, background = '#000')

        # Force the aspect ratio
        if self.forceAspectRatio:
            setAspectRatio(self.canvas, self.padFrame, self.aspectRatio)
            self.root.rowconfigure(0, weight = 1)
            self.root.columnconfigure(0, weight = 1)

        # Pack the canvas so it can be used
        # self.canvas.pack(expand = True, fill = "both")

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
        
        self.canvas.create_text(60, 60, fill = "white", text = "TEST", font = "Courier 20")

    def eventCallback(self, event: Event):
        '''
        Generic Event callback function. All events should send callbacks here.
        '''

        self.eventThread.eventQueue.append(event)

    def enforceAspectRatio(self, event: Event):
        '''
        If the forceAspectRatio flag is set, make sure any configure calls don't change the aspect ratio
        '''

        # don't do anything if the flag isn't set
        if not self.forceAspectRatio:
            return

        # Keep the height fixed, but adjust the width accordingly
        self.height = event.height
        self.width = int(round(event.height * self.aspectRatio))

        self.canvas.place(in_=self.padFrame, x=0, y=0, width = self.width, height = self.height)


    def start(self):
        initializeFonts()

        self.eventThread.start()

        self.root.mainloop()

        self.eventThread.isActive = False
