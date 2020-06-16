
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
            canvas: Canvas,
            points: List[Tuple[float]],
            fillColor: Tuple[float] = (1.0, 1.0, 1.0),
            **kwargs
            ):
        
        polygonCollider = PolygonCollider(points)
        GameObject.__init__(self, canvas, collider=polygonCollider, **kwargs)

        self.coords: List[float] = []

        self.fillColor: Tuple[float] = convertRGBToHex(fillColor)

        self.polygonID: int = 0
    
    def _setup(self):
        self.coords = self.collider.getCoords(self.screenWidth, self.screenHeight) 

        self.polygonID = self.canvas.create_polygon(
            *self.collider.getCoords(self.screenWidth, self.screenHeight),
            fill = self.fillColor
        )

    def _draw(self):

        if self.polygonID != 0:
            self.canvas.delete(self.polygonID)

        self.polygonID = self.canvas.create_polygon(
            *self.collider.getCoords(self.screenWidth, self.screenHeight),
            fill = self.fillColor
        )

    def _resize(self):
        self.coords = self.collider.getCoords(self.screenWidth, self.screenHeight) 
