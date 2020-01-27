
# Tkinter imports
from tkinter import Canvas
from tkinter import Event
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

from ..base import TGEEvent
from ..base import EVENT_TYPE
from ..base import INPUT_STATE
from ..base import BUTTONS

from ..objects import Oval
from ..objects import Text
from ..objects import Rect


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


        ##########
        # EVENTS #
        ##########
        self.root.bind_all("<Motion>", self.motionCallback)

        self.root.bind_all("<MouseWheel>", self.mouseWheelCallback)

        self.root.bind_all("<ButtonPress>", self.mouseClickCallback)
        self.root.bind_all("<ButtonRelease>", self.mouseReleaseCallback)

        self.root.bind_all("<KeyPress>", self.keyPressCallback)
        self.root.bind_all("<KeyRelease>", self.keyReleaseEvent)


        # Initialize everything which gameObject could ever use. For now, that is just the fonts
        initializeFonts()

        # Initialize the gameObjects dict
        self.gameObjects: Dict[int, GameObject] = {}

        self.addGameObject(
            Rect(
                self.canvas,
                (.5, .5),
                .2,
                .3,
                fillColor=(.3, .3, .8),
                anchor=CENTER
            )
        )

        self.addGameObject(
            Text(
                self.canvas,
                (.5, .5),
                "HELLO WORLD",
                anchor=CENTER
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
        Normalize mouse motion and create a TGE Event for the motion.
        '''

        # Create the event and assign all relevant variables
        motionEvent = TGEEvent()

        # If there are no buttons currently held down in the state, just create a normal mouse motion event
        if len(INPUT_STATE.pressedButtons) == 0:
            motionEvent.type = EVENT_TYPE.MOUSE_MOTION
        
        # Otherwise, create a mouse drag event
        else:
            motionEvent.type = EVENT_TYPE.MOUSE_DRAG
        
        motionEvent.mouseX = event.x / int(self.canvas.cget("width"))
        motionEvent.mouseY = event.y / int(self.canvas.cget("height"))

        print(motionEvent)

        self.eventThread.eventQueue.append(motionEvent)

    def mouseWheelCallback(self, event: Event):
        '''
        Create a mouse wheel event
        '''

        # Create the event and assign all relevant variables
        wheelEvent = TGEEvent()

        wheelEvent.type = EVENT_TYPE.MOUSE_WHEEL
        wheelEvent.wheelOffset = event.delta

        self.eventThread.eventQueue.append(wheelEvent)

    def mouseClickCallback(self, event: Event):
        '''
        Create a mouse button press callback
        '''

        # Create the event and assign all relevant variabels
        clickEvent = TGEEvent()

        clickEvent.type = EVENT_TYPE.MOUSE_CLICK

        # Determine which button constant was pressed
        mouseButton = 0
        if event.num == 1:
            mouseButton = BUTTONS.LEFT_CLICK
        elif event.num == 2:
            mouseButton = BUTTONS.MIDDLE_CLICK
        elif event.num == 3:
            mouseButton = BUTTONS.RIGHT_CLICK
        clickEvent.button = mouseButton

        # Make sure the button is not already pressed
        if clickEvent.button not in INPUT_STATE.pressedButtons:
            self.eventThread.eventQueue.append(clickEvent)

    def mouseReleaseCallback(self, event: Event):
        '''
        Create a mouse release event
        '''

        # Create the event and assign all relevant variables
        mouseReleaseEvent = TGEEvent()

        mouseReleaseEvent.type = EVENT_TYPE.MOUSE_RELEASE

        # Determine which button constant was pressed
        mouseButton = 0
        if event.num == 1:
            mouseButton = BUTTONS.LEFT_CLICK
        elif event.num == 2:
            mouseButton = BUTTONS.MIDDLE_CLICK
        elif event.num == 3:
            mouseButton = BUTTONS.RIGHT_CLICK
        mouseReleaseEvent.button = mouseButton

        # Add the event to the queue
        self.eventThread.eventQueue.append(mouseReleaseEvent)

    def keyPressCallback(self, event: Event):
        '''
        Create a keyPress Event
        '''

        # Create an event and assign all the relevant variables
        keyPressEvent = TGEEvent()

        keyPressEvent.type = EVENT_TYPE.KEY_PRESS
        keyPressEvent.keysym = event.keysym.lower()

        # Make sure that the keysym is not already pressed
        if keyPressEvent.keysym not in INPUT_STATE.pressedKeys:
            self.eventThread.eventQueue.append(keyPressEvent)

    def keyReleaseEvent(self, event: Event):
        '''
        Create a keyRelease event
        '''

        # Create an event and assign all the relevant variables
        keyReleaseEvent = TGEEvent()

        keyReleaseEvent.type = EVENT_TYPE.KEY_RELEASE
        keyReleaseEvent.keysym = event.keysym.lower()

        # Add the event to the thread
        self.eventThread.eventQueue.append(keyReleaseEvent)

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

        self.eventQueue: List[TGEEvent] = []
        self.isActive: bool = True
    
    def run(self):

        while self.isActive:

            while len(self.eventQueue) > 0:

                # Lower the amount of checks for mouse motion
                motionIndex = 0
                while motionIndex + 1 < len(self.eventQueue) and self.eventQueue[motionIndex + 1].type == EVENT_TYPE.MOUSE_MOTION:
                    motionIndex += 1
                if motionIndex > 0:
                    self.eventQueue = self.eventQueue[motionIndex:]

                # Get the next event in the queue and pass it to all gameObjects
                event = self.eventQueue.pop(0)
                for gameObject in self.game.getAllGameObjects():
                    gameObject.handleEvent(event)
                

                ######################
                # INPUT_STATE UPDATE #
                ######################
                
                # Mouse Motion
                if event.type == EVENT_TYPE.MOUSE_MOTION or event.type == EVENT_TYPE.MOUSE_DRAG:

                    INPUT_STATE.mouseX = event.mouseX
                    INPUT_STATE.mouseY = event.mouseY                

                # Mouse Click
                elif event.type == EVENT_TYPE.MOUSE_CLICK:

                    INPUT_STATE.pressedButtons.add(event.button)
                
                # Mouse Release
                elif event.type == EVENT_TYPE.MOUSE_RELEASE and event.button in INPUT_STATE.pressedButtons:

                    INPUT_STATE.pressedButtons.remove(event.button)

                # Key Press
                elif event.type == EVENT_TYPE.KEY_PRESS:

                    INPUT_STATE.pressedKeys.add(event.keysym)
                
                # Key Release
                elif event.type == EVENT_TYPE.KEY_RELEASE and event.keysym in INPUT_STATE.pressedKeys:

                    INPUT_STATE.pressedKeys.remove(event.keysym)

            time.sleep(.001)