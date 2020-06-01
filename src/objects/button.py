
# Tkinter imports
from tkinter import CENTER

# Python imports
from typing import Tuple

# Package imports
from ..base import GameState

from ..base import TGEEvent
from ..base import EVENT_TYPE

from ..common import convertRGBToHex

from .text import Text
from .rect import Rect

class Button(Rect):
    '''

    '''

    def __init__(
            self,
            position: Tuple[int],
            width: int,
            height: int,
            anchor: str = CENTER,
            fillColor: Tuple[float] = (.5, .5, .5),
            highlightColor: Tuple[float] = (.8, .8, .2),

            # Text variables
            text: str = "",
            textSize: int = 12,
            font: str = "Courier",
            textColor: Tuple[float] = (1, 1, 1),
            textHighlight: Tuple[float] = (1, 1, 1),

            **kwargs
            ):

        Rect.__init__(
            self,
            position,
            width, height,
            fillColor=fillColor,
            anchor=anchor
        )

        # Convert the colors appropriately
        self.defaultColor: str = convertRGBToHex(fillColor)
        self.highlightColor: str = convertRGBToHex(highlightColor)

        # Store the text Colors
        self.textColor = convertRGBToHex(textColor)
        self.textHighlight = convertRGBToHex(textHighlight)

        self.text: Text = Text(
            (self.collider.x + self.collider.w / 2, self.collider.y + self.collider.h / 2),
            text = text,
            fontSize=textSize,
            textColor=textColor,
            font=font
        )
        self.addChild(self.text)

        self.hovered: bool = False

    def _setup(self):
        self.coords = self.collider.getCoords(self.screenWidth, self.screenHeight)
    
    def _resize(self):
        self.coords = self.collider.getCoords(self.screenWidth, self.screenHeight)

    def _handleEvent(self, event: TGEEvent, gameState: GameState):
        if event.type == EVENT_TYPE.MOUSE_MOTION:
            self.checkHover((event.mouseX, event.mouseY))

    def checkHover(self, point: Tuple[int]):
        '''

        '''

        if self.isPointInside(point):
            if not self.hovered:
                self.hovered = True
                self.text.textColor = self.textHighlight
                self.fillColor = self.highlightColor

        else:

            if self.hovered:
                self.hovered = False
                self.text.textColor = self.textColor
                self.fillColor = self.defaultColor
    