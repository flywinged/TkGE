
# Tkinter imports
from tkinter import Canvas
from tkinter import CENTER

# Python imports
from typing import Tuple
from typing import List

# Package imports
from ..base import BoxCollider
from ..base import GameObject
from ..base import GameState

from ..base import TGEEvent
from ..base import EVENT_TYPE

class Button(GameObject):
    '''

    '''

    def __init__(
            self,
            position: Tuple[int],
            width: int,
            height: int,
            anchor: str = CENTER,
            **kwargs
            ):

        GameObject.__init__(self, **kwargs)

         # A Button uses the basic box collider. Build the appropriate box collider.
        self.collider = BoxCollider(position[0], position[1], width, height, anchor=anchor)

        self.coords: List[float] = []

        self.hovered: bool = False

    def _setup(self):
        self.coords = self.collider.getCoords(self.screenWidth, self.screenHeight)
    
    def _resize(self):
        self.coords = self.collider.getCoords(self.screenWidth, self.screenHeight)

    def _draw(self, canvas: Canvas):

        canvas.create_rectangle(
            *self.coords,
            fill = "yellow" if self.hovered else "grey")

    def _handleEvent(self, event: TGEEvent, gameState: GameState):
        if event.type == EVENT_TYPE.MOUSE_MOTION:
            self.checkHover((event.mouseX, event.mouseY))

    def checkHover(self, point: Tuple[int]):
        '''

        '''

        if self.isPointInside(point):
            if not self.hovered:
                self.hovered = True

        else:

            if self.hovered:
                self.hovered = False
    