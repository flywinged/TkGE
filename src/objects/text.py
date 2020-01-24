from tkinter import Canvas
from tkinter import CENTER
from ..base import BoxCollider
from ..base import GameObject
from ..base import fonts

from typing import Tuple

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
