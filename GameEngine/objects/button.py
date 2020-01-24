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
            fontSize: int,
            anchor: str = CENTER,
            **kwargs
            ):

        GameObject.__init__(self, canvas, **kwargs)

        self.initialFontSize: int = fontSize
        self.currentFontSize: int = fontSize

         # A Button uses the basic box collider. Build the appropriate box collider.
        w = ((fonts.courier[self.currentFontSize].measure(text) + 8) / self.initialScreenWidth) * 1.05
        h = ((fonts.courier[self.currentFontSize].metrics()["linespace"] + 8) / self.initialScreenHeight) * 1.05
        self.collider = BoxCollider(position[0], position[1], w, h, anchor = anchor)

        self.text: str = text

        self.hovered: bool = False

        self.rectID: int = self.canvas.create_rectangle(
            (self.collider.x) * self.initialScreenWidth,
            (self.collider.y) * self.initialScreenHeight,
            (self.collider.x + w) * self.initialScreenWidth,
            (self.collider.y + h) * self.initialScreenHeight,
            fill = "grey")

        self.textID: int = self.canvas.create_text(
            (position[0] * self.initialScreenWidth, position[1] * self.initialScreenHeight),
            text = self.text,
            fill = "black",
            anchor = anchor,
            font = fonts.courier[12])

    def move(self):
        
        self.canvas.move(self.rectID, 1, 1)
        self.canvas.move(self.textID, 1, 1)

        self.collider.x += 1
        self.collider.y += 1

    def _handleEvent(self, event: Event):
        if event.type == EventType.Motion:
            self.checkHover((event.x, event.y))
    
    def _resize(self, newWidth: int, newHeight: int):
        '''
        Resize the button
        '''

        self.canvas.scale(self.rectID, 0, 0, newWidth / self.lastScreenWidth, newHeight / self.lastScreenHeight)
        self.canvas.scale(self.textID, 0, 0, newWidth / self.lastScreenWidth, newHeight / self.lastScreenHeight)

        # May need to create different sized text as the size is adjusted. Do this here.
        textSize = int(self.initialFontSize * newWidth / self.initialScreenWidth)
        if textSize < 4:
            textSize = 4
        self.canvas.itemconfig(self.textID, font = fonts.courier[textSize])

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
    