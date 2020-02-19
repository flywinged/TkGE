
# Tkinter imports
from tkinter import Canvas
from tkinter import CENTER

# Python imports
from typing import Tuple, List

# Package imports
from ..base.collider import PolygonCollider
from ..base.gameObject import GameObject

from ..common import convertRGBToHex

from ..base.event import TGEEvent, EVENT_TYPE
from ..base.gameState import GameState

class Polygon(GameObject):
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
            points: List[Tuple[float]],
            fillColor: Tuple[float] = (1.0, 1.0, 1.0),
            **kwargs
            ):
        
        polygonCollider = PolygonCollider(points)
        GameObject.__init__(self, canvas, collider=polygonCollider, **kwargs)

        self.fillColor: Tuple[float] = fillColor

        self.polygonID: int = self.canvas.create_polygon(
            *self.collider.getCoords(self.initialScreenWidth, self.initialScreenHeight),
            fill = convertRGBToHex(self.fillColor))
    
    def _resize(self, newWidth: int, newHeight: int):
        '''
        Resize the button
        '''

        self.canvas.scale(self.polygonID, 0, 0, newWidth / self.currentScreenWidth, newHeight / self.currentScreenHeight)

    def _delete(self):
        '''
        Delete the rect from the canvas
        '''

        self.canvas.delete(self.polygonID)