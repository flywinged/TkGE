
# Tkinter imports
from tkinter import Canvas

# Python imports
from typing import Tuple

# Package imports
from .collider import Collider
from .event import TGEEvent

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
        self.initialScreenHeight: int = int(self.canvas.cget("width"))

        self.lastScreenWidth: int = int(self.canvas.cget("width"))
        self.lastScreenHeight: int = int(self.canvas.cget("width"))

        # GameObject ID
        self.ID: int = self.currentID
        GameObject.currentID += 1

    def __hash__(self):
        return self.ID
    
    def _handleEvent(self, event: TGEEvent):
        '''
        Virtual function to overwrite
        '''

    def _resize(self, newWidth: int, newHeight: int):
        '''
        Cirtual function to overwrite
        '''

    def resize(self, newWidth: int, newHeight: int):
        '''
        Resize the object and it's collider
        '''

        self.collider.resize(newWidth, newHeight)
        self._resize(newWidth, newHeight)

        # Update the old width variables
        self.lastScreenWidth = newWidth
        self.lastScreenHeight = newHeight

    def handleEvent(self, event: TGEEvent):
        '''
        Basic event handler filter
        '''

        self._handleEvent(event)

    def isPointInside(self, point: Tuple[int]):
        '''
        Does the point collide with the object. If no collider is attached to the gameObject, return False by default.
        '''

        if self.collider is not None:
            return self.collider.isPointInside(point)
        else:
            return False