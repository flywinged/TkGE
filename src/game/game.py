
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
from typing import Tuple

import time

# Package imports
from ..base import GameObject
from ..base import initializeFonts

from ..base import TGEEvent
from ..base import EVENT_TYPE
from ..base import BUTTONS
from ..base import EVENT_HANDLER
from ..base import GameState

from ..common import getTime

###################
# BASE GAME CLASS #
###################

class Game:
    '''
    A Game object contains all the logic necessary for the game loop.

    Parameters
    ----------
    gameState - GameState object or any object which inherits from gameState.

    TODO: Use variable aspect ratio. Figure this out later though.
    width - Initial pixel width of the game window. Determines the aspect ratio of the game which is locked.

    height - Initial pixel height of the game window. Determines the aspect ratio of the game which is locked.

    updateDelay - Time (in ms) between succesive update calls
    '''

    def __init__(self, gameState: GameState, width = 1280, height = 720, updateDelay: float = 1 / 60, drawDelay: float = 1 / 60):

        # Set the gameState
        self.gameState: GameState = gameState

        # Initial width and height, in pixels, of the game
        self.width: int = width
        self.height: int = height

        # Aspect ratio of the game window. If forceAspect Ratio is set, it 
        self.aspectRatio: float = self.width / self.height

        # How long (ms) between state updates.
        self.updateDelay: float = updateDelay
        self.drawDelay: float = drawDelay

        # Create the event thread object. Manage all user inputs
        self.eventThread: EventThread = EventThread(self)

        # Create the updateThread object. Manage time-based updates
        self.updateThread: UpdateThread = UpdateThread(self)

        # Create the drawing thread
        self.drawingThread: DrawingThread = DrawingThread(self)

        # Create the tk root and initialize the canvas and padFrame
        self.root = Tk()
        self.padFrame = Frame(borderwidth = 0, background = "#111", width = self.width, height = self.height)
        self.padFrame.grid(row = 0, column = 0, sticky="nsew")

        # Create the double buffered canvas
        self.DBCanvas: DoubleBufferedCanvas = DoubleBufferedCanvas(self)

        # Initialize the gameObjects dict
        self.gameObjects: Dict[int, GameObject] = {}

        # INITIALIZE #
        self.initialize()


    ############################
    # INITIALIZATION FUNCTIONS #
    ############################

    def initialize(self):
        '''
        Call everything necessary to get the game up and running.
        '''

        # Initialize all the font objects from the base.fonts file
        initializeFonts()

        # Lock the game's aspect ratio to whatever the current width and height are
        self.DBCanvas.setAspectRatio()

        # Bind all the event callbacks
        self.bindCallbacks()


    #############
    # CALLBACKS #
    #############

    def bindCallbacks(self):
        '''
        Bind all the callbacks to root.
        '''

        self.root.bind_all("<Motion>", self.motionCallback)

        self.root.bind_all("<MouseWheel>", self.mouseWheelCallback)

        self.root.bind_all("<ButtonPress>", self.mouseClickCallback)
        self.root.bind_all("<ButtonRelease>", self.mouseReleaseCallback)

        self.root.bind_all("<KeyPress>", self.keyPressCallback)
        self.root.bind_all("<KeyRelease>", self.keyReleaseEvent)

        self.root.protocol("WM_DELETE_WINDOW", self.programCloseEvent)

    def motionCallback(self, event: Event):
        '''
        Normalize mouse motion and create a TGE Event for the motion.
        '''

        # Create the event and assign all relevant variables
        motionEvent = TGEEvent()

        # If there are no buttons currently held down in the state, just create a normal mouse motion event
        if len(self.gameState.inputState.pressedButtons) == 0:
            motionEvent.type = EVENT_TYPE.MOUSE_MOTION
        
        # Otherwise, create a mouse drag event
        else:
            motionEvent.type = EVENT_TYPE.MOUSE_DRAG
        
        motionEvent.mouseX = event.x / int(self.width)
        motionEvent.mouseY = event.y / int(self.height)

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
        if clickEvent.button not in self.gameState.inputState.pressedButtons:
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
        if keyPressEvent.keysym not in self.gameState.inputState.pressedKeys:
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

    def programCloseEvent(self):
        '''
        Starts the program close process.
        '''

        # Tell both the active threads to start shutting down
        self.eventThread.isActive = False
        self.updateThread.isActive = False
        self.drawingThread.isActive = False
    
        # As long as the threads are still active, dont destroy the root
        if not (self.eventThread.complete and self.updateThread.complete and self.drawingThread.complete):
            self.root.after(10, self.programCloseEvent)
        else:
            self.root.destroy()


    ########################
    # GAME STATE FUNCTIONS #
    ########################

    def updateBefore(self):
        '''
        This gets called ever update call before any of the gameObjects are updated
        '''

        # Virtual function to overwrite by children
    
    def updateAfter(self):
        '''
        This gets called ever update call after all of the gameObjects are updated
        '''

        # Virtual function to overwrite by children


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
        Remove a gameObject from the gameObjects dictionary and from the canvas
        '''

        self.gameObjects[gameObject.ID].delete()
        del self.gameObjects[gameObject.ID]
    
    def getAllGameObjects(self) -> GameObject:
        '''
        Generator for returning all the gameObjects in the gameObjects dictionary
        '''

        for ID in list(self.gameObjects):
            yield self.gameObjects[ID]


    ###################
    # EVENT FUNCTIONS #
    ###################

    def _handleEvent(self, event: TGEEvent): # pylint: disable=unused-argument
        '''
        Virtual function to overwrite.
        '''

        return EVENT_HANDLER.NOT_CAPTURED

    ##################
    # START THE GAME #
    ##################

    def play(self):
        '''
        Start all the threads for the game before beginning the tkinter main loop.
        '''

        # Start all the game threads
        self.eventThread.start()
        self.updateThread.start()
        self.drawingThread.start()
        
        # Begin the tkinter loop
        self.root.mainloop()


################
# EVENT THREAD #
################

class EventThread(Thread):
    '''
    Thread to handle all of the events which will come through the game.

    Parameters
    ----------
    game: Game instance. The thread needs a reference in order to access the gameObjects
    '''

    def __init__(self, game: Game):
        Thread.__init__(self)

        # Assign the game reference
        self.game: Game = game

        # List of TGEEvents. First in, first out
        self.eventQueue: List[TGEEvent] = []

        # Control for killing the thread from outside
        self.isActive: bool = True

        # Whether or not the thread has succesfully finished
        self.complete: bool = False
    
    def run(self):

        # Define mousemotion events outside of the run loop so it's easier to read
        mouseMotionTypes = {EVENT_TYPE.MOUSE_MOTION, EVENT_TYPE.MOUSE_DRAG}

        while self.isActive:

            # As long as there are events in the queue, we want to process them.
            while len(self.eventQueue) > 0 and self.isActive:

                # Lower the amount of checks for mouse motion or mouse dragging

                # We only need to check for multiple mouse motion events if the event we are going to process on
                #   this iteration is a mouse motion event and there is more than one event in the queue
                if self.eventQueue[0].type in mouseMotionTypes and len(self.eventQueue) > 0:

                    # Define the current index which had motion
                    motionIndex = 0

                    # Determine what type of motion event is queued
                    motionType = self.eventQueue[motionIndex].type

                    # Find the last motion index which still has the event type MOUSE_MOTION
                    while motionIndex + 1 < len(self.eventQueue) and self.eventQueue[motionIndex + 1].type == motionType:
                        motionIndex += 1
                
                    # If there were multiple mouse motion events in the queue, remove all the duplicate ones
                    if motionIndex > 0:
                        self.eventQueue = self.eventQueue[motionIndex:]

                # Get the next event in the queue and pass it to all gameObjects
                event = self.eventQueue.pop(0)

                # Let the game try and handle the event first
                if self.game._handleEvent(event) == EVENT_HANDLER.NOT_CAPTURED:
                    for gameObject in self.game.getAllGameObjects():

                        # If any of the game objects capture the event, none of the other ones should capture them
                        if gameObject.handleEvent(event, self.game.gameState) == EVENT_HANDLER.CAPTURED:
                            break
                
                ######################
                # INPUT STATE UPDATE #
                ######################
                
                # Mouse Motion
                if event.type == EVENT_TYPE.MOUSE_MOTION or event.type == EVENT_TYPE.MOUSE_DRAG:

                    self.game.gameState.inputState.mouseX = event.mouseX
                    self.game.gameState.inputState.mouseY = event.mouseY                

                # Mouse Click
                elif event.type == EVENT_TYPE.MOUSE_CLICK:

                    self.game.gameState.inputState.pressedButtons.add(event.button)
                
                # Mouse Release
                elif event.type == EVENT_TYPE.MOUSE_RELEASE and event.button in self.game.gameState.inputState.pressedButtons:

                    self.game.gameState.inputState.pressedButtons.remove(event.button)

                # Key Press
                elif event.type == EVENT_TYPE.KEY_PRESS:

                    self.game.gameState.inputState.pressedKeys.add(event.keysym)
                
                # Key Release
                elif event.type == EVENT_TYPE.KEY_RELEASE and event.keysym in self.game.gameState.inputState.pressedKeys:

                    self.game.gameState.inputState.pressedKeys.remove(event.keysym)

            # Once all the events have been processed, wait a small amount of time to keep the thread from using too much processing power
            time.sleep(.001)

        self.complete = True
        print("Closed Event Thread")


#################
# UPDATE THREAD #
#################

class UpdateThread(Thread):
    '''
    Thread to handle all the time-based game updates.

    Parameters
    ----------
    game: Game instance. The thread needs a reference in order to access the gameObjects
    '''

    def __init__(self, game: Game):
        Thread.__init__(self)

        # Assign the game reference
        self.game: Game = game

        # Control for killing the thread from elsewhere
        self.isActive: bool = True

        # Whether or not the thread has succesfully finished
        self.complete: bool = False
    
    def run(self):
        '''

        '''

        # Not necessary, leaving it in for debugging purposes
        while self.isActive:
            
            # Update the time for the game state before doing anything else
            self.game.gameState.updateTime()

            # First call games before update call
            self.game.updateBefore()

            # Now update each of the gameObjects
            for gameObject in self.game.getAllGameObjects():
                gameObject.update(self.game.gameState)

            # Now call the update after
            self.game.updateAfter()
            
            # Now wait for the appropriate amount of time specified by self.game.updateDelay
            # We wait before doing anything to ensure this thread doesn't use excessive amounts of processing power
            timeLeft = self.game.updateDelay - (getTime() - self.game.gameState.now)
            if timeLeft < 0: timeLeft = 0
           
            # Sleep for the appropriate amount of time
            time.sleep(timeLeft)
        
        # Close the thread when the game is no longer active
        self.complete = True
        print("Closed Update Thread")

##################
# DRAWING THREAD #
##################

class DrawingThread(Thread):
    '''
    Thread to handle all the time-based game updates.

    Parameters
    ----------
    game: Game instance. The thread needs a reference in order to access the gameObjects
    '''

    def __init__(self, game: Game):
        Thread.__init__(self)

        # Assign the game reference
        self.game: Game = game

        # Control for killing the thread from elsewhere
        self.isActive: bool = True

        # Whether or not the thread has succesfully finished
        self.complete: bool = False

    def run(self):
        '''

        '''

        while self.isActive:

            # Record when this loop started
            startTime = getTime()
            
            # Now update each of the gameObjects
            for gameObject in self.game.getAllGameObjects():
                gameObject.draw(self.game.DBCanvas.bufferCanvas, self.game.width, self.game.height)
            
            # Once they are all drawn, flip the screens
            self.game.DBCanvas.flip()
            
            # Now wait for the appropriate amount of time specified by self.game.updateDelay
            # We wait before doing anything to ensure this thread doesn't use excessive amounts of processing power
            finishTime = getTime()
            timeLeft = self.game.drawDelay - (finishTime - startTime)
            if timeLeft < 0: timeLeft = 0
            
            # Wait the appropriate amount of time
            time.sleep(timeLeft)
        
        self.complete: bool = True
        print("Closed Drawing Thread")


##################################
# DOUBLE BUFFERED TKINTER CANVAS #
##################################
class DoubleBufferedCanvas:
    '''
    A Double buffered canvas contains two tkinter canvas objects and displays one while the other one is being drawn.
    Then it flips.
    '''

    def __init__(self, game: Game):

        self.game: Game = game

        # Create the necessary canvases
        canvas1 = Canvas(self.game.root, width = self.game.width, height = self.game.height, highlightthickness = 0, background = '#000')
        canvas2 = Canvas(self.game.root, width = self.game.width, height = self.game.height, highlightthickness = 0, background = '#000')
        self.canvases: List[Canvas] = [canvas1, canvas2]

        # Variables for management of the two canvases
        self.activeCanvasIndex: int = 0
        self.bufferCanvasIndex: int = 1
        self.activeCanvas: Canvas = self.canvases[self.activeCanvasIndex]
        self.bufferCanvas: Canvas = self.canvases[self.bufferCanvasIndex]

        # For placing in the center
        self.offset: Tuple[int] = (0, 0)
    
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
            desiredHeight = int(event.width / self.game.aspectRatio)

            # if the window is too tall to fit, use the height as
            # the controlling dimension
            if desiredHeight > event.height:
                desiredHeight = event.height
                desiredWidth = int(event.height * self.game.aspectRatio)

            # place the window, giving it an explicit size
            self.offset = ((event.width - desiredWidth)//2, (event.height - desiredHeight) // 2)
            self.canvases[self.activeCanvasIndex].place(in_=self.game.padFrame, x=self.offset[0], y = self.offset[1], 
                width=desiredWidth, height=desiredHeight)
            
            # Resize everything in the self.canvases[self.activeCanvasIndex]
            self.canvases[self.activeCanvasIndex].configure(width = desiredWidth, height = desiredHeight)
            self.canvases[self.bufferCanvasIndex].configure(width = desiredWidth, height = desiredHeight)

            # Call the resize function on each child gameObject
            for gameObject in self.game.getAllGameObjects():
                gameObject.resize(desiredWidth, desiredHeight)
            
            # Set the new width and height of the game
            self.game.width = desiredWidth
            self.game.height = desiredHeight

        self.game.padFrame.bind("<Configure>", enforceAspectRatio)

        # TODO: Figure out what all this row and column configure business does.
        self.game.root.rowconfigure(0, weight = 1)
        self.game.root.columnconfigure(0, weight = 1)
    
    def flip(self):
        '''
        Flip will change the active canvas and repack the correct canvas
        '''

        # Change which canvas is immediately placed
        self.activeCanvas.place_forget()
        self.bufferCanvas.place(in_=self.game.padFrame, x=self.offset[0], y = self.offset[1], 
                width=self.game.width, height=self.game.height)       

        # Then update the indexes
        self.activeCanvasIndex = (self.activeCanvasIndex + 1) % 2
        self.bufferCanvasIndex = (self.bufferCanvasIndex + 1) % 2
        self.activeCanvas = self.canvases[self.activeCanvasIndex]
        self.bufferCanvas = self.canvases[self.bufferCanvasIndex]

        # Then clear everything on the new inactive canvas
        self.bufferCanvas.delete(ALL)