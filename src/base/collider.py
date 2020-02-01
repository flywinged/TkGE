
# Tkinter imports
from tkinter.constants import *

# Python imports
from typing import Tuple

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
    
    def _isPointInside(self, point: Tuple[int]) -> bool:
        '''
        If the point is within (or on) the box described by self.x, y, w, and h, return true
        '''

        return (point[0] >= self.x and point[0] <= self.x + self.w and point[1] >= self.y and point[1] <= self.y + self.h)
    
    def getCoords(self, screenWidth: int, screenHeight: int):

        return (
            screenWidth * (self.x),
            screenHeight* (self.y),
            screenWidth * (self.x + self.w),
            screenHeight* (self.y + self.h)
        )


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
    
    def _isPointInside(self, point: Tuple[int]) -> bool:
        '''
        If the point is within (or on) the box described by self.x, y, w, and h, return true
        '''

        normalizedDistance = (((point[0] - self.x) * self.r[1])**2 + ((point[1] - self.y) * self.r[0])**2)
        return (normalizedDistance <= self.r[0]**2 * self.r[1]**2)
    
    def getCoords(self, screenWidth: int, screenHeight: int):
        '''
        Return x1, y1, x2, y2
        '''

        return (
            (self.x - self.r[0]) * screenWidth,
            (self.y - self.r[1]) * screenHeight,
            (self.x + self.r[0]) * screenWidth,
            (self.y + self.r[1]) * screenHeight,
        )