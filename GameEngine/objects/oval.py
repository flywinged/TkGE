from tkinter import Canvas, CENTER, Event, EventType

from ..base.collider import OvalCollider
from ..base.gameObject import GameObject
from ..base import fonts

from typing import Tuple

class Oval(GameObject):
    '''

    '''

    def __init__(
            self,
            canvas: Canvas,
            position: Tuple[int],
            radius: Tuple[float, float],
            **kwargs
            ):

        collider = OvalCollider(position[0], position[1], radius)
        GameObject.__init__(self, canvas, collider = collider, **kwargs)

        self.hovered: bool = False

        self.ID: int = self.canvas.create_oval(
            (collider.x - collider.r[0]) * self.initialScreenWidth,
            (collider.y - collider.r[1]) * self.initialScreenHeight,
            (collider.x + collider.r[0]) * self.initialScreenWidth,
            (collider.y + collider.r[1]) * self.initialScreenHeight,
            fill = "grey")

    def move(self):
        
        self.canvas.move(self.ID, 1, 1)

        self.collider.x += 1
        self.collider.y += 1

    def _handleEvent(self, event: Event):
        if event.type == EventType.Motion:
            self.checkHover((event.x, event.y))
    
    def _resize(self, newWidth: int, newHeight: int):
        '''
        Resize the circle
        '''

        self.canvas.scale(self.ID, 0, 0, newWidth / self.lastScreenWidth, newHeight / self.lastScreenHeight)

    def checkHover(self, point: Tuple[int]):
        '''

        '''

        if self.isPointInside(point):
            if not self.hovered:

                self.canvas.itemconfig(self.ID, fill = "yellow")
                self.hovered = True

        else:

            if self.hovered:

                self.canvas.itemconfig(self.ID, fill = "grey")
                self.hovered = False
    