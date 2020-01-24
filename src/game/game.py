
# Tkinter imports
from tkinter import Canvas
from tkinter import Event
from tkinter import EventType
from tkinter import Frame
from tkinter import Tk
from tkinter.constants import *

# Python Built-in imports
from threading import Thread
from typing import Dict
from typing import List

import time

# Package imports
from ..base import GameObject
from ..base import initializeFonts

from ..objects import Oval
from ..objects import Button


###################
# BASE GAME CLASS #
###################

class Game:
    '''
    A Game object contains all the logic necessary for the game loop.
    '''

    def __init__(self, width = 1280, height = 720, frameDelay: int = 17):

        # Initial width and height, in pixels, of the game
        self.width: int = width
        self.height: int = height

        # Aspect ratio of the game window. If forceAspect Ratio is set, it 
        self.aspectRatio: float = self.width / self.height

        # How long (ms) between screen updates.
        self.frameDelay: int = frameDelay

        # Create the event thread object. Manage all user inputs
        self.eventThread: EventThread = EventThread(self)

        # Create the tk root and initialize the canvas and padFrame
        self.root = Tk()
        self.padFrame = Frame(borderwidth = 0, background = "#111", width = self.width, height = self.height)
        self.padFrame.grid(row = 0, column = 0, sticky="nsew")
        self.canvas: Canvas = Canvas(self.root, width = self.width, height = self.height, highlightthickness = 0, background = '#000')

        # Bind the tkinter configure action in order to force the aspect ratio of the canvas to always be consistent
        self.setAspectRatio()

        # TODO: Figure out what all this row and column configure business does.
        self.root.rowconfigure(0, weight = 1)
        self.root.columnconfigure(0, weight = 1)

        # Initialize all the event callbacks
        self.root.bind_all("<Motion>", self.motionCallback)
        self.root.bind_all("<Key>", self.eventCallback)
        self.root.bind_all("<KeyRelease>", self.eventCallback)

        # Initialize everything which gameObject could ever use. For now, that is just the fonts
        initializeFonts()

        # Initialize the gameObjects dict
        self.gameObjects: Dict[int, GameObject] = {}

        cols = 4
        rows = 6
        

        width = self.width // cols
        height = self.height // rows

        for x in range(cols):
            for y in range(rows):
                button = Oval(
                    self.canvas,
                    (x / cols, y / rows),
                    (30 / self.width, 30 / self.height)
                )

                self.addGameObject(button)
        
        self.addGameObject(
            Button(
                self.canvas,
                (.6, .51),
                "test",
                24
            )
        )


    ############################
    # INITIALIZATION FUNCTIONS #
    ############################

    def setAspectRatio(self):
        '''
        Function which forces the content frame to maintain a specified aspect ratio.
        It does this by placing the content frame inside of a padded frame, and resizes the content frame accordingly.
        '''
        
        def enforceAspectRatio(event: Event):
            '''
            Enforce function to be bound to tkinter.bind
            '''

            # start by using the width as the controlling dimension
            desiredWidth = event.width
            desiredHeight = int(event.width / self.aspectRatio)

            # if the window is too tall to fit, use the height as
            # the controlling dimension
            if desiredHeight > event.height:
                desiredHeight = event.height
                desiredWidth = int(event.height * self.aspectRatio)

            # place the window, giving it an explicit size
            self.canvas.place(in_=self.padFrame, x=(event.width - desiredWidth)//2, y=(event.height - desiredHeight) // 2, 
                width=desiredWidth, height=desiredHeight)
            
            # Resize everything in the self.canvas
            self.canvas.configure(width = desiredWidth, height = desiredHeight)

            # Call the resize function on each child gameObject
            for gameObject in self.getAllGameObjects():
                gameObject.resize(desiredWidth, desiredHeight)

        self.padFrame.bind("<Configure>", enforceAspectRatio)


    #############
    # CALLBACKS #
    #############

    def motionCallback(self, event: Event):
        '''
        Noprmalize mouse motion
        '''

        event.x = event.x / int(self.canvas.cget("width"))
        event.y = event.y / int(self.canvas.cget("height"))

        self.eventThread.eventQueue.append(event)

    def eventCallback(self, event: Event):
        '''
        Generic Event callback function. All events should send callbacks here.
        '''

        self.eventThread.eventQueue.append(event)


    ########################
    # GAMEOBJECT FUNCTIONS #
    ########################

    def addGameObject(self, gameObject: GameObject):
        '''
        Just adds a gameobject to the gameObjects dictionary
        '''

        self.gameObjects[gameObject.ID] = gameObject
    
    def removeGameObject(self, gameObject: GameObject):
        '''
        Remove a gameObject from the gameObjects dictionary
        '''

        del self.gameObjects[gameObject.ID]
    
    def getAllGameObjects(self) -> GameObject:
        '''
        Generator for returning all the gameObjects in the gameObjects dictionary
        '''

        for ID in self.gameObjects:
            yield self.gameObjects[ID]


    def start(self):
        initializeFonts()

        self.eventThread.start()

        self.root.mainloop()

        self.eventThread.isActive = False


################
# EVENT THREAD #
################

class EventThread(Thread):
    '''
    Thread to handle all of the events which will come through the game.
    '''

    def __init__(self, game: Game):
        Thread.__init__(self)

        self.game: Game = game

        self.eventQueue: List[Event] = []
        self.isActive: bool = True
    
    def run(self):

        while self.isActive:

            while len(self.eventQueue) > 0:

                # Lower the amount of checks for mouse motion
                motionIndex = 0
                while motionIndex + 1 < len(self.eventQueue) and self.eventQueue[motionIndex + 1].type == EventType.Motion:
                    motionIndex += 1
                if motionIndex > 0:
                    self.eventQueue = self.eventQueue[motionIndex:]

                # Get the next event in the queue and pass it to all gameObjects
                event = self.eventQueue.pop(0)
                for gameObject in self.game.getAllGameObjects():
                    gameObject.handleEvent(event)

            time.sleep(.001)