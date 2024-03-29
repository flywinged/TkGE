
# Tkinter imports
from tkinter import Canvas
from tkinter import CENTER
from tkinter import NW
from tkinter.font import Font

# Python imports
from typing import Tuple, Dict

# Package imports
from ..base import BoxCollider
from ..base import GameObject
from ..base import fonts

from ..common import convertRGBToHex

class Text(GameObject):
    '''
    Base class for text gameObjects. 

    Parameters
    ----------
    canvas - tkinter canvas object.

    position - where to place the text object on the screen (0-1)

    text - text string of what to display

    font - Name of a font. "Courier" "Times New Roman" etc.

    fontSize - int for font size. See fonts.py file to see the minimum and maximum sizes.

    textColor - (r, g, b) float values from (0, 1). Color of the text.

    anchor - tkinter anchor value (NW, S, CENTER, etc.)
    '''

    def __init__(
                self,
                canvas: Canvas,
                position: Tuple[float],
                text: str,
                font: str = "Courier",
                fontSize: int = 12,
                textColor: Tuple[float, float, float] = (1.0, 1.0, 1.0),
                anchor: str = CENTER,
                **kwargs
            ):
        
        # Initialize the gameobject
        GameObject.__init__(self, canvas, **kwargs)

        # The text object needs to remeber its initial font size so it can be rezied appropriately
        self.initialFontSize: int = fontSize
        self.currentFontSize: int = fontSize

        # Set the values for text
        self.text: str = text
        self.font: Dict[int, Font] = fonts.FONTS[font]
        self.textColor: str = convertRGBToHex(textColor)

        # Set up the collider for the text.
        self.collider: BoxCollider = BoxCollider(position[0], position[1], 0, 0, anchor = anchor)

        # Remember the original position
        self.originalPosition: Tuple[float] = position
    
        # Create textID
        self.textID: int = 0

    def updateText(self):
        '''

        '''

        self.collider.x = self.originalPosition[0]
        self.collider.y = self.originalPosition[1]

        self.collider.w = self.font[self.currentFontSize].measure(self.text) / self.screenWidth
        self.collider.h = self.font[self.currentFontSize].metrics()["linespace"] / self.screenHeight
        self.collider.adjustPoints()

    def _setup(self):
        self.updateText()

    def _draw(self):

        if self.textID != 0:
            self.canvas.delete(self.textID)
        
        self.textID = self.canvas.create_text(
            self.collider.x * self.screenWidth,
            self.collider.y * self.screenHeight,
            text = self.text,
            fill = self.textColor,
            anchor = NW, # Anchor is always NW because the collider normalizes all points to be this way
            font = self.font[self.currentFontSize]
        )


    def _resize(self):
        '''
        Resize the text according to the new screen width and height.
        '''

        # May need to create different sized text as the size is adjusted. Do this here.
        textSize = int(self.initialFontSize * self.screenWidth / self.initialScreenWidth)

        # Don't let the text be resized larger or smaller than the available text sizes.
        if textSize < fonts.SMALLEST_FONT_SIZE:
            textSize = fonts.SMALLEST_FONT_SIZE
        if textSize > fonts.LARGEST_FONT_SIZE:
            textSize = fonts.LARGEST_FONT_SIZE

        self.currentFontSize = textSize

        # Now call all the canvas methods necessary
        self.updateText()
    
    def _delete(self):
        '''
        Remove all the IDs from the canvas
        '''

        self.canvas.delete(self.textID)