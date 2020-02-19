
# Tkinter imports
from tkinter import Canvas
from tkinter import CENTER

# Python imports
from typing import Tuple

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

        # Fill color variable
        self.fillColor: Tuple[float, float, float] = fillColor

        self.rectID: int = self.canvas.create_rectangle(
            *self.collider.getCoords(self.initialScreenWidth, self.initialScreenHeight),
            fill = convertRGBToHex(fillColor))
    
    def _resize(self, newWidth: int, newHeight: int):
        '''
        Resize the button
        '''

        self.canvas.scale(self.rectID, 0, 0, newWidth / self.currentScreenWidth, newHeight / self.currentScreenHeight)

    def _delete(self):
        '''
        Delete the rect from the canvas
        '''

        self.canvas.delete(self.rectID)