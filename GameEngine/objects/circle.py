from tkinter import Canvas, CENTER, Event, EventType

from ..base.collider import CircleCollider
from ..base.gameObject import GameObject
from ..base import fonts

from typing import Tuple

class Circle(GameObject):
    '''

    '''

    def __init__(
            self,
            canvas: Canvas,
            position: Tuple[int],
            radius: float,
            **kwargs
            ):

        collider = CircleCollider(position[0], position[1], radius)
        GameObject.__init__(self, canvas, collider = collider, **kwargs)

        self.hovered: bool = False

        self.ID: int = self.canvas.create_oval(collider.x - collider.r, collider.y - collider.r, collider.x + collider.r, collider.y + collider.r, fill = "grey")

    def move(self):
        
        self.canvas.move(self.ID, 1, 1)

        self.collider.x += 1
        self.collider.y += 1

    def _handleEvent(self, event: Event):
        if event.type == EventType.Motion:
            self.checkHover((event.x, event.y))

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
    