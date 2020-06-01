
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
        dimensions: Tuple[int] = (0, 0),
        collider: Collider = None
        ):
        
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

        if self.setup:

            # Update the old width variables
            self.screenWidth = newWidth
            self.screenHeight = newHeight

            self._resize()


    ###########
    # DRAWING #
    ###########
    def _draw(self, canvas: Canvas):
        '''
        Virtual function to overwrite
        '''

    def _setup(self):
        '''
        Virtual function to overwrite
        '''

    def draw(self, canvas: Canvas, width: int, height: int):
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

        self._draw(canvas)

        for child in self.children:
            child.draw(canvas, width, height)


    ##################
    # EVENT HANDLING #
    ##################
    def _handleEvent(self, event: TGEEvent, gameState: GameState): # pylint: disable=unused-argument
        '''
        Virtual function to overwrite
        '''

        return EVENT_HANDLER.NOT_CAPTURED

    def handleEvent(self, event: TGEEvent, gameState: GameState):
        '''
        Basic event handler filter
        '''

        for child in self.children:
            child.handleEvent(event, gameState)

        if self.setup:
            return self._handleEvent(event, gameState)


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
        else:
            return False