
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

    def __init__(self, x: float, y: float, w: float, h: float, desiredAnchor: str = CENTER, givenAnchor: str = NW):
        Collider.__init__(self)

        # Adjust the x, y positions using common function
        x, y = adjustTopLeftCorner((x, y), desiredAnchor, givenAnchor, w, h)

        self.x: float = x
        self.y: float = y
        self.w: float = w
        self.h: float = h
    
    def _isPointInside(self, point: Tuple[int]) -> bool:
        '''
        If the point is within (or on) the box described by self.x, y, w, and h, return true
        '''

        return (point[0] >= self.x and point[0] <= self.x + self.w and point[1] >= self.y and point[1] <= self.y + self.h)


class OvalCollider(Collider):
    '''
    Collider logic for a basic box object.
    '''

    def __init__(self, x: float, y: float, r: Tuple[float, float], desiredAnchor: str = CENTER, givenAnchor: str = CENTER):
        Collider.__init__(self)

        x, y = adjustTopLeftCorner((x, y), desiredAnchor, givenAnchor, r[0], r[1])

        self.x: float = x
        self.y: float = y
        self.r: Tuple[float, float] = r
    
    def _isPointInside(self, point: Tuple[int]) -> bool:
        '''
        If the point is within (or on) the box described by self.x, y, w, and h, return true
        '''

        normalizedDistance = (((point[0] - self.x) * self.r[1])**2 + ((point[1] - self.y) * self.r[0])**2)
        return (normalizedDistance <= self.r[0]**2 * self.r[1]**2)
    