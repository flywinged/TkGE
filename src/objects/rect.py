
# Tkinter imports
from tkinter import Canvas
from tkinter import CENTER

# Python imports
from typing import Tuple
from typing import List

# Package imports
from ..base import BoxCollider
from ..base import GameObject

from ..common import convertRGBToHex

class Rect(GameObject):
    '''
    Basic rectangle. Forced to be parallel to x and y axis.

    Parameters
    ----------
    canvas - tkinter canvas object.

    position - where to place the text object on the screen (0, 1)

    width, height - width and height of the rectangle in normalized screen coordinates.

    fillColor - (r, g, b) float values from (0, 1). Color to fill in the rectangle.

    anchor - tkinter anchor value (NW, S, CENTER, etc.)
    '''

    def __init__(
            self,
            canvas: Canvas,
            position: Tuple[float],
            width: float,
            height: float,
            fillColor: Tuple[float] = (1.0, 1.0, 1.0),
            anchor: str = CENTER,
            **kwargs
            ):

        GameObject.__init__(self, canvas, **kwargs)

         # A Button uses the basic box collider. Build the appropriate box collider.
        self.collider = BoxCollider(position[0], position[1], width, height, anchor=anchor)

        # Coords for drawing
        self.coords: List[float] = []

        # Color
        self.fillColor: str = convertRGBToHex(fillColor)

        # Create the rectID for use later
        self.rectID: int = 0


    def _setup(self):
        self.coords = self.collider.getCoords(self.screenWidth, self.screenHeight)

    def _draw(self):

        if self.rectID != 0:
            self.canvas.delete(self.rectID)

        self.rectID = self.canvas.create_rectangle(
            *self.coords,
            fill = self.fillColor
        )
    
    def _resize(self):
        '''
        Resize the rectangle
        '''

        self.coords = self.collider.getCoords(self.screenWidth, self.screenHeight)
        self.canvas.coords(self.rectID, self.coords)
    
    def _delete(self):
        '''
        Remove all the IDs from the canvas
        '''

        self.canvas.delete(self.rectID)