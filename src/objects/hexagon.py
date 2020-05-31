
# Tkinter imports
from tkinter import Canvas

# Python imports
from typing import Tuple
import math

# Package imports
from .polygon import Polygon

class Hexagon(Polygon):
    '''
    Oval object class definition.

    Parameters
    ----------
    canvas - tkinter canvas object. This should be the main game canvas.

    position - The center of the hexagon

    radius - Distance from the center of the polygon to a corner of the hexagon in terms of the y-axis

    rotation - Angle (in radians) the polygon is rotated. 0 puts a corner of the hexagon directly on the x axis.

    fillColor - (r, g, b) float values from (0, 1). Color to fill in the rectangle.

    anchor - tkinter anchor value (NW, S, CENTER, etc.)
    '''

    def __init__(
            self,
            position: Tuple[float],
            radius: float,
            rotation: float = 0.0,
            **kwargs
            ):
        
        initialScreenWidth: int = int(canvas.cget("width"))
        initialScreenHeight: int = int(canvas.cget("height"))
        ratio = initialScreenHeight / initialScreenWidth

        # Create the point list
        points = []
        for i in range(6):
            angle = (i / 6) * math.tau + rotation
            points.append((
                position[0] + radius * math.cos(angle) * ratio,
                position[1] + radius * math.sin(angle)
            ))

        Polygon.__init__(self, points, **kwargs)