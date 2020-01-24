
# Tkinter imports
from tkinter import Canvas
from tkinter import CENTER
from tkinter import Event
from tkinter import EventType

# Python imports
from typing import Tuple

# Package imports
from ..base.collider import BoxCollider
from ..base.gameObject import GameObject
from ..base import fonts

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
        w = ((fonts.FONTS["Courier"][self.currentFontSize].measure(text) + 8) / self.initialScreenWidth) * 1.05
        h = ((fonts.FONTS["Courier"][self.currentFontSize].metrics()["linespace"] + 8) / self.initialScreenHeight) * 1.05
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
            font = fonts.FONTS["Courier"][12])

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
        if textSize < fonts.SMALLEST_FONT_SIZE:
            textSize = fonts.SMALLEST_FONT_SIZE
        if textSize > fonts.LARGEST_FONT_SIZE:
            textSize = fonts.LARGEST_FONT_SIZE
        self.canvas.itemconfig(self.textID, font = fonts.FONTS["Courier"][textSize])

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
    