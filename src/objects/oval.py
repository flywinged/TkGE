
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

    radius - (x(float), y(float)) normalized radii of the oval along the x and y axis.

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
        collider = OvalCollider(position[0], position[1], radius, anchor=anchor)
        GameObject.__init__(self, canvas, collider = collider, **kwargs)

        # Base fill color for the oval
        self.fillColor: Tuple[float, float, float] - fillColor

        self.ID: int = self.canvas.create_oval(
            (collider.x - collider.r[0]) * self.initialScreenWidth,
            (collider.y - collider.r[1]) * self.initialScreenHeight,
            (collider.x + collider.r[0]) * self.initialScreenWidth,
            (collider.y + collider.r[1]) * self.initialScreenHeight,
            fill = convertRGBToHex(self.fillColor))

    def _resize(self, newWidth: int, newHeight: int):
        '''
        Resize the circle
        '''

        self.canvas.scale(self.ID, 0, 0, newWidth / self.lastScreenWidth, newHeight / self.lastScreenHeight)
