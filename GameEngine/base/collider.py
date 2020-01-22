from tkinter.constants import *

from typing import Tuple

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

class BoxCollider(Collider):
    '''
    Collider logic for a basic box object.
    '''

    def __init__(self, x: int, y: int, w: int, h: int, anchor: str = CENTER):
        Collider.__init__(self)

        # The logic for the box changes slightly depending on the supplied anchor.
        # Handle the x values first
        if anchor == E or anchor == NE or anchor == SE:
            x -= w
        elif anchor == N or anchor == CENTER or anchor == S:
            x -= w//2
        
        # Then handle the Y values
        if anchor == W or anchor == CENTER or anchor == E:
            y -= h//2
        elif anchor == SW or anchor == S or anchor == SE:
            y -= h

        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h
    
    def _isPointInside(self, point: Tuple[int]) -> bool:
        '''
        If the point is within (or on) the box described by self.x, y, w, and h, return true
        '''

        return (point[0] >= self.x and point[0] <= self.x + self.w and point[1] >= self.y and point[1] <= self.y + self.h)

class CircleCollider(Collider):
    '''
    Collider logic for a basic box object.
    '''

    def __init__(self, x: int, y: int, r: float):
        Collider.__init__(self)

        self.x: int = x
        self.y: int = y
        self.r: float = r
    
    def _isPointInside(self, point: Tuple[int]) -> bool:
        '''
        If the point is within (or on) the box described by self.x, y, w, and h, return true
        '''

        pointDistance = ((point[0] - self.x)**2 + (point[1] - self.y)**2) ** (1/2)
        return (pointDistance <= self.r)