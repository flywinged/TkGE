
# Tkinter imports
from tkinter import Canvas

# Python imports
from typing import Tuple

# Package imports
from .collider import Collider
from .event import TGEEvent
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
        collider: Collider = None
        ):
        
        # The only required argument to create a gameObject is the canvas it will be drawn on.
        self.canvas: Canvas = canvas

        # All the rest of the arguments are optional
        self.collider: Collider = collider

        # To remember the size of the screen
        self.initialScreenWidth: int = int(self.canvas.cget("width"))
        self.initialScreenHeight: int = int(self.canvas.cget("height"))

        self.currentScreenWidth: int = int(self.canvas.cget("width"))
        self.currentScreenHeight: int = int(self.canvas.cget("height"))

        # GameObject ID
        self.ID: int = GameObject.getNextID()

    @classmethod
    def getNextID(cls):
        cls.currentID += 1
        return cls.currentID

    def __hash__(self):
        return self.ID


    ############
    # RESIZING #
    ############
    def _resize(self, newWidth: int, newHeight: int):
        '''
        Virtual function to overwrite
        '''

    def resize(self, newWidth: int, newHeight: int):
        '''
        Resize the object and it's collider
        '''

        self.collider.resize(newWidth, newHeight)
        self._resize(newWidth, newHeight)

        # Update the old width variables
        self.currentScreenWidth = newWidth
        self.currentScreenHeight = newHeight


    ##################
    # EVENT HANDLING #
    ##################
    def _handleEvent(self, event: TGEEvent):
        '''
        Virtual function to overwrite
        '''

    def handleEvent(self, event: TGEEvent):
        '''
        Basic event handler filter
        '''

        self._handleEvent(event)


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

        self._update(gameState)

    def isPointInside(self, point: Tuple[int]):
        '''
        Does the point collide with the object. If no collider is attached to the gameObject, return False by default.
        '''

        if self.collider is not None:
            return self.collider.isPointInside(point)
        else:
            return False