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

        # The logic for the box changes slightly depending on the supplied anchor.
        # Handle the x values first
        if anchor == E or anchor == NE or anchor == SE:
            x -= w
        elif anchor == N or anchor == CENTER or anchor == S:
            x -= w/2
        
        # Then handle the Y values
        if anchor == W or anchor == CENTER or anchor == E:
            y -= h/2
        elif anchor == SW or anchor == S or anchor == SE:
            y -= h

        self.x: float = x
        self.y: float = y
        self.w: float = w
        self.h: float = h
    
    def _isPointInside(self, point: Tuple[int]) -> bool:
        '''
        If the point is within (or on) the box described by self.x, y, w, and h, return true
        '''

        return (point[0] >= self.x and point[0] <= self.x + self.w and point[1] >= self.y and point[1] <= self.y + self.h)
    
    # def _resize(self, newWidth: int, newHeight: int):
    #     '''
    #     Resize the collider
    #     '''

    #     self.x *= newWidth
    #     self.w *= newWidth
    #     self.y *= newHeight
    #     self.h *= newHeight

class OvalCollider(Collider):
    '''
    Collider logic for a basic box object.
    '''

    def __init__(self, x: float, y: float, r: Tuple[float, float]):
        Collider.__init__(self)

        self.x: float = x
        self.y: float = y
        self.r: Tuple[float, float] = r
    
    def _isPointInside(self, point: Tuple[int]) -> bool:
        '''
        If the point is within (or on) the box described by self.x, y, w, and h, return true
        '''

        normalizedDistance = (((point[0] - self.x)/self.r[0])**2 + ((point[1] - self.y) / self.r[1])**2)
        return (normalizedDistance <= 1)
    
    # def _resize(self, newWidth: int, newHeight: int):
    #     '''
    #     Resize the circle collider
    #     '''

    #     self.x *= newWidth
    #     self.y *= newHeight
    #     self.r *= newWidth