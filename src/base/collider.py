
# Tkinter imports
from tkinter.constants import *

# Python imports
from typing import Tuple, List

# Package imports
from ..common import adjustTopLeftCorner

class Collider:
    '''
    A Collider keeps track of when the mouse is inside of it or not.
    '''

    def __init__(self):
        pass

    def _isPointInside(self, point: Tuple[int]) -> bool:
        '''
        Virtual function to overwrite by children.
        '''

    def isPointInside(self, point: Tuple[int]) -> bool:
        '''
        Virtual function to overwrite by children.
        '''

        return self._isPointInside(point)
    
    def _resize(self, newWidth: int, newHeight: int):
        '''
        Virtual function to overwrite
        '''
    
    def resize(self, newWidth: int, newHeight: int):
        '''
        Virtual function to overwrite
        '''

        self._resize(newWidth, newHeight)
    
    def _getCoords(self, screenWidth: int, screenHeight: int):
        '''
        Virtual functino to overwrite
        '''
    
    def getCoords(self, screenWidth: int, screenHeight: int):
        '''
        Return all the coords for the collider. This describes the bounds of the collider
        '''

        return self._getCoords(screenWidth, screenHeight)

class BoxCollider(Collider):
    '''
    Collider logic for a basic box object.
    '''

    def __init__(self, x: float, y: float, w: float, h: float, anchor: str = CENTER):
        Collider.__init__(self)

        # Adjust the x, y positions using common function
        x, y = adjustTopLeftCorner((x, y), anchor, w, h)

        self.x: float = x
        self.y: float = y
        self.w: float = w
        self.h: float = h
    
    def _isPointInside(self, point: Tuple[float]) -> bool:
        '''
        If the point is within (or on) the box described by self.x, y, w, and h, return true
        '''

        return (point[0] >= self.x and point[0] <= self.x + self.w and point[1] >= self.y and point[1] <= self.y + self.h)
    
    def _getCoords(self, screenWidth: int, screenHeight: int):

        return [
            screenWidth * (self.x),
            screenHeight* (self.y),
            screenWidth * (self.x + self.w),
            screenHeight* (self.y + self.h)
        ]


class OvalCollider(Collider):
    '''
    Collider logic for a basic box object.
    '''

    def __init__(self, x: float, y: float, r: Tuple[float, float], anchor: str = CENTER):
        Collider.__init__(self)

        x, y = adjustTopLeftCorner((x, y), anchor,2 * r[0], 2 * r[1])

        self.x: float = x + r[0]
        self.y: float = y + r[1]
        self.r: Tuple[float, float] = r
    
    def _isPointInside(self, point: Tuple[float]) -> bool:
        '''
        If the point is within (or on) the box described by self.x, y, w, and h, return true
        '''

        normalizedDistance = (((point[0] - self.x) * self.r[1])**2 + ((point[1] - self.y) * self.r[0])**2)
        return (normalizedDistance <= self.r[0]**2 * self.r[1]**2)
    
    def _getCoords(self, screenWidth: int, screenHeight: int):
        '''
        Return x1, y1, x2, y2
        '''

        return [
            (self.x - self.r[0]) * screenWidth,
            (self.y - self.r[1]) * screenHeight,
            (self.x + self.r[0]) * screenWidth,
            (self.y + self.r[1]) * screenHeight,
        ]

class PolygonCollider(Collider):
    '''
    Collider logic for a polygon
    '''

    def __init__(self, points: List[Tuple[float, float]]):
        Collider.__init__(self)

        self.points: List[Tuple[float]] = points
    
    def _isPointInside(self, point: Tuple[float]) -> bool:
        '''
        Determine if a given point is inside of the polygon. Do this using the winding number algorithm.
        '''

        # Keep track of the current winding number
        windingNumberCounter = 0

        # Loop through each edge of the polygon
        for i in range(len(self.points)):

            # Extract the lower and upper edge of the polygon
            lowerPoint = self.points[i]
            upperPoint = self.points[(i + 1) % len(self.points)]

            # Which side of the line this point is on
            d = (point[0] - lowerPoint[0]) * (upperPoint[1] - lowerPoint[1]) - (point[1] - lowerPoint[1]) * (upperPoint[0] - lowerPoint[0])

            # Edge goes past this point and point is strictly to the left of the line
            if upperPoint[1] > point[1] and lowerPoint[1] < point[1] and d < 0:
                windingNumberCounter += 1
            elif upperPoint[1] < point[1] and lowerPoint[1] > point[1] and d > 0:
                windingNumberCounter -= 1
        
        # If winding number is non-zero, the point is in the polygon
        if windingNumberCounter == 0:
            return False
        return True
    
    def _getCoords(self, screenWidth: int, screenHeight: int):
        '''
        Return x1, y1, x2, y2
        '''

        pixelCoords = []
        for point in self.points:
            pixelCoords.append(point[0] * screenWidth)
            pixelCoords.append(point[1] * screenHeight)

        return pixelCoords