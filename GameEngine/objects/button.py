from tkinter import Canvas, CENTER, Event, EventType

from ..base.collider import BoxCollider
from ..base.gameObject import GameObject
from ..base import fonts

from typing import Tuple

class Button(GameObject):
    '''

    '''

    def __init__(
            self,
            canvas: Canvas,
            position: Tuple[int],
            text: str,
            anchor: str = CENTER,
            **kwargs
            ):

        # A Button uses the basic box collider. Build the appropriate box collider.
        w = fonts.courier.measure(text)
        h = fonts.courier.metrics()["linespace"]
        collider = BoxCollider(position[0], position[1], w, h, anchor = anchor)

        GameObject.__init__(self, canvas, collider = collider, **kwargs)

        self.text: str = text

        self.hovered: bool = False

        self.rectID: int = self.canvas.create_rectangle(collider.x, collider.y, collider.x + w, collider.y + h, fill = "grey")
        self.textID: int = self.canvas.create_text(position, text = self.text, fill = "black", anchor = anchor, font = fonts.courier)

    def move(self):
        
        self.canvas.move(self.rectID, 1, 1)
        self.canvas.move(self.textID, 1, 1)

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

                self.canvas.itemconfig(self.rectID, fill = "yellow")
                self.hovered = True

        else:

            if self.hovered:

                self.canvas.itemconfig(self.rectID, fill = "grey")
                self.hovered = False
    