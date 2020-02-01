
# Tkinter imports
from tkinter import Canvas
from tkinter import CENTER

# Python imports
from typing import Tuple

# Package imports
from ..base.collider import OvalCollider
from ..base.gameObject import GameObject

from ..common import convertRGBToHex

class Oval(GameObject):
    '''
    Oval object class definition.

    Parameters
    ----------
    canvas - tkinter canvas object. This should be the main game canvas.

    position - (x(float), y(float)) normalized position of the oval on the screen. (.5, .5) puts the oval in the center of the screen

    radius - (x(float), y(float)) normalized radii of the oval along the x and y axis. If only a single float is provided, it is assumed to be the radius with respect to height.

    fillColor - (r, g, b) float values from (0, 1). Color to fill in the rectangle.

    anchor - tkinter anchor value (NW, S, CENTER, etc.)
    '''

    def __init__(
            self,
            canvas: Canvas,
            position: Tuple[int],
            radius: Tuple[float, float],
            fillColor: Tuple[float, float, float] = (1.0, 1.0, 1.0),
            anchor: str = CENTER,
            **kwargs
            ):

        # Create the oval collider for the object. This collider is then passed in to the parent initializer
        GameObject.__init__(self, canvas, **kwargs)

        # Account for if only a single parameter was passed to oval. In this case, a circle is created.
        if type(radius) == float:
            radius = (self.initialScreenHeight / self.initialScreenWidth * radius, radius)
        self.collider = OvalCollider(position[0], position[1], radius, anchor=anchor)

        # Base fill color for the oval
        self.fillColor: Tuple[float, float, float] = fillColor

        self.ovalID: int = self.canvas.create_oval(
            *self.collider.getCoords(self.initialScreenWidth, self.initialScreenHeight),
            fill = convertRGBToHex(self.fillColor))

    def _resize(self, newWidth: int, newHeight: int):
        '''
        Resize the circle
        '''

        self.canvas.scale(self.ovalID, 0, 0, newWidth / self.currentScreenWidth, newHeight / self.currentScreenHeight)
