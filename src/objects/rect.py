
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

    '''

    def __init__(
            self,
            canvas: Canvas,
            position: Tuple[int],
            width: int,
            height: int,
            fillColor: Tuple[float, float, float] = (1.0, 1.0, 1.0),
            anchor: str = CENTER,
            **kwargs
            ):

        GameObject.__init__(self, canvas, **kwargs)

         # A Button uses the basic box collider. Build the appropriate box collider.
        self.collider = BoxCollider(position[0], position[1], width, height, anchor=anchor)

        # Fill color variable
        self.fillColor: Tuple[float, float, float] = fillColor

        self.rectID: int = self.canvas.create_rectangle(
            (self.collider.x) * self.initialScreenWidth,
            (self.collider.y) * self.initialScreenHeight,
            (self.collider.x + width) * self.initialScreenWidth,
            (self.collider.y + height) * self.initialScreenHeight,
            fill = convertRGBToHex(fillColor))
    
    def _resize(self, newWidth: int, newHeight: int):
        '''
        Resize the button
        '''

        self.canvas.scale(self.rectID, 0, 0, newWidth / self.lastScreenWidth, newHeight / self.lastScreenHeight)

    