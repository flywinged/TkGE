
# Tkinter imports
from tkinter import Canvas

# Python imports
from typing import Tuple
from typing import List

# Package imports
from .collider import Collider
from .event import TGEEvent
from .event import EVENT_HANDLER
from .gameState import GameState

class GameObject:
    '''
    A Gameobject is the building block for everything.

    Parameters
    ----------
    canvas: The tkinter canvas object. Used to keep track of the object so it can be redrawn without deleting every frame.

    collider = None: Collider object to handle mouse interaction
    '''

    currentID: int = 0

    def __init__(
        self,
        canvas: Canvas,
        dimensions: Tuple[int] = (0, 0),
        collider: Collider = None
        ):

        # Need to have a reference to the canvas
        self.canvas: Canvas = canvas
        
        # To remember the size of the screen
        self.screenWidth: int = dimensions[0]
        self.screenHeight: int = dimensions[1]

        # Set for use elsewhere
        self.initialScreenWidth: int = 0
        self.initialScreenHeight: int = 0

        # Set the collider if exists
        self.collider: Collider = collider

        # Whether or not the object has been setup
        self.setup: bool = False

        # GameObject ID
        self.ID: int = GameObject.getNextID()

        # Whether or not this game object should be redrawn on the next update
        self.redraw: bool = True

        # List of all child gameObjects
        self.children: List[GameObject] = []

    @classmethod
    def getNextID(cls):
        cls.currentID += 1
        return cls.currentID

    def __hash__(self):
        return self.ID
    

    # Add children gameObjects. If added, their functions will all be qutomatically called
    def addChild(self, gameObject: "GameObject"):
        '''
        A Child gameobject will be handled automatically whenever a function is called.
        '''

        self.children.append(gameObject)
    

    # TODO: Make this actually do something...
    def _delete(self):
        '''
        Virtual function to overwrite.
        '''
    
    def delete(self):
        '''
        Remove all tkinter objects from the canvas
        '''

        for child in self.children:
            child.delete()

        self._delete()


    ############
    # RESIZING #
    ############
    def _resize(self):
        '''
        Virtual function to overwrite
        '''

    def resize(self, newWidth: int, newHeight: int):
        '''
        Resize the object and it's collider
        '''

        for child in self.children:
            child.resize(newWidth, newHeight)
            child.redraw = True

        if self.setup:

            # Update the old width variables
            self.screenWidth = newWidth
            self.screenHeight = newHeight

            self._resize()
            self.redraw = True


    ###########
    # DRAWING #
    ###########
    def _draw(self):
        '''
        Virtual function to overwrite
        '''

    def _setup(self):
        '''
        Virtual function to overwrite
        '''

    def draw(self, canvas: Canvas, width: int, height: int, parentForce: bool = False):
        '''
        Draw the object and it's collider
        '''

        if not self.setup:

            # First, do initial setup
            self.screenWidth = width
            self.screenHeight = height

            # Set the initial screen width and height
            self.initialScreenWidth = width
            self.initialScreenHeight = height

            self._setup()
            self.setup = True

            # Call a resize
            self.resize(width, height)

        if self.redraw or parentForce:
            self._draw()

        for child in self.children:
            child.draw(canvas, width, height, self.redraw or parentForce)
        
        # Reset the redraw value
        if self.redraw:
            self.canvas.update_idletasks()
            self.redraw = False


    ##################
    # EVENT HANDLING #
    ##################
    def _handleEvent(self, event: TGEEvent, gameState: GameState): # pylint: disable=unused-argument
        '''
        Virtual function to overwrite
        '''

        return EVENT_HANDLER.NOT_CAPTURED

    def handleEvent(self, event: TGEEvent, gameState: GameState) -> int:
        '''
        Basic event handler filter
        '''

        # Handle child events first
        for child in self.children:
            if child.handleEvent(event, gameState) == EVENT_HANDLER.CAPTURED:
                return

        # If the child didn't capture the event, 
        if self.setup:
            return self._handleEvent(event, gameState)

        # Otherwise, assume the event was not captured
        return EVENT_HANDLER.NOT_CAPTURED

    ##########
    # UPDATE #
    ##########
    def _update(self, gameState: GameState):
        '''
        Virtual function to overwrite
        '''

    def update(self, gameState: GameState):
        '''
        Basic update handler.
        '''

        for child in self.children:
            child.update(gameState)

        if self.setup:
            self._update(gameState)

    def isPointInside(self, point: Tuple[int]):
        '''
        Does the point collide with the object. If no collider is attached to the gameObject, return False by default.
        '''

        if self.collider is not None:
            return self.collider.isPointInside(point)
        return False