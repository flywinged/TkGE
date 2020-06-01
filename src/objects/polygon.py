
# Tkinter imports
from tkinter import Canvas

# Python imports
from typing import Tuple, List

# Package imports
from ..base.collider import PolygonCollider
from ..base.gameObject import GameObject

from ..common import convertRGBToHex

class Polygon(GameObject):
    '''
    Oval object class definition.

    Parameters
    ----------
    canvas - tkinter canvas object. This should be the main game canvas.

    points - List of points describing the edges of the polygon

    fillColor - (r, g, b) float values from (0, 1). Color to fill in the rectangle.

    anchor - tkinter anchor value (NW, S, CENTER, etc.)
    '''

    def __init__(
            self,
            points: List[Tuple[float]],
            fillColor: Tuple[float] = (1.0, 1.0, 1.0),
            **kwargs
            ):
        
        polygonCollider = PolygonCollider(points)
        GameObject.__init__(self, collider=polygonCollider, **kwargs)

        self.coords: List[float] = []

        self.fillColor: Tuple[float] = convertRGBToHex(fillColor)
    
    def _setup(self):
        self.coords = self.collider.getCoords(self.screenWidth, self.screenHeight) 

    def _draw(self, canvas: Canvas):

        canvas.create_polygon(
            *self.collider.getCoords(self.screenWidth, self.screenHeight),
            fill = self.fillColor)

    def _resize(self):
        self.coords = self.collider.getCoords(self.screenWidth, self.screenHeight) 
