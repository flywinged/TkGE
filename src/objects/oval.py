
# Tkinter imports
from tkinter import Canvas
from tkinter import CENTER

# Python imports
from typing import Tuple

# Package imports
from ..base.collider import OvalCollider
from ..base.gameObject import GameObject

from ..base import EVENT_TYPE
from ..base import TGEEvent
from ..base import INPUT_STATE


class Oval(GameObject):
    '''
    Oval object class definition.

    Parameters
    ----------
    @param canvas - tkinter canvas object. This should be the main game canvas.

    @param position - (x(float), y(float)) normalized position of the oval on the screen. (.5, .5) puts the oval in the center of the screen

    @param radius - (x(float), y(float)) normalized radii of the oval along the x and y axis.
    '''

    def __init__(
            self,
            canvas: Canvas,
            position: Tuple[int],
            radius: Tuple[float, float],
            desiredAnchor: str = CENTER,
            givenAnchor: str = CENTER,
            **kwargs
            ):

        # Create the oval collider for the object. This collider is then passed in to the parent initializer
        collider = OvalCollider(position[0], position[1], radius, desiredAnchor=desiredAnchor, givenAnchor=givenAnchor)
        GameObject.__init__(self, canvas, collider = collider, **kwargs)

        # 
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

    def _handleEvent(self, event: TGEEvent):
        if event.type == EVENT_TYPE.MOUSE_MOTION:
            self.checkHover((event.mouseX, event.mouseY))
    
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
    