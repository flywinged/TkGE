from tkinter import Canvas, Event

from typing import Tuple

from .collider import Collider

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

        # GameObject ID
        self.ID: int = self.currentID
        GameObject.currentID += 1

    def __hash__(self):
        return self.ID
    
    def _handleEvent(self, event: Event):
        '''
        Virtual function to overwrite
        '''

    def handleEvent(self, event: Event):
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