
# Tkinter imports
from tkinter import Canvas
from tkinter import CENTER

# Python imports
from typing import Tuple

# Library imports
from ..base import BoxCollider
from ..base import GameObject
from ..base import fonts

class Text(GameObject):
    '''
    Base class for text gameObjects. 
    '''

    def __init__(
                self,
                canvas: Canvas,
                position: Tuple[int],
                text: str,
                font: str,
                fontSize: int,
                anchor: str = CENTER,
                **kwargs
            ):
        
        GameObject.__init__(self, canvas)
