
# Tkinter imports
from tkinter import Canvas
from tkinter import CENTER

# Python imports
from typing import Tuple

# Package imports
from ..base import BoxCollider
from ..base import GameObject

from ..base import TGEEvent
from ..base import EVENT_TYPE

class Button(GameObject):
    '''

    '''

    def __init__(
            self,
            canvas: Canvas,
            position: Tuple[int],
            width: int,
            height: int,
            anchor: str = CENTER,
            **kwargs
            ):

        GameObject.__init__(self, canvas, **kwargs)

         # A Button uses the basic box collider. Build the appropriate box collider.
        self.collider = BoxCollider(position[0], position[1], width, height, anchor=anchor)

        self.hovered: bool = False

        self.rectID: int = self.canvas.create_rectangle(
            (self.collider.x) * self.initialScreenWidth,
            (self.collider.y) * self.initialScreenHeight,
            (self.collider.x + width) * self.initialScreenWidth,
            (self.collider.y + height) * self.initialScreenHeight,
            fill = "grey")

    def move(self):
        
        self.canvas.move(self.rectID, 1, 1)

        self.collider.x += 1
        self.collider.y += 1

    def _handleEvent(self, event: TGEEvent):
        if event.type == EVENT_TYPE.MOUSE_MOTION:
            self.checkHover((event.mouseX, event.mouseY))
    
    def _resize(self, newWidth: int, newHeight: int):
        '''
        Resize the button
        '''

        self.canvas.scale(self.rectID, 0, 0, newWidth / self.currentScreenWidth, newHeight / self.currentScreenHeight)

    def checkHover(self, point: Tuple[int]):
        '''

        '''

        if self.isPointInside(point):
            if not self.hovered:

                self.canvas.itemconfig(self.rectID, fill = "yellow")
                self.hovered = True

        else:

            if self.hovered:

                self.canvas.itemconfig(self.rectID, fill = "grey")
                self.hovered = False
    