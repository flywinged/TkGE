
# Tkinter imports
from tkinter import Canvas
from tkinter import CENTER
from tkinter import NW
from tkinter.font import Font

# Python imports
from typing import Tuple, Dict

# Library imports
from ..base import BoxCollider
from ..base import GameObject
from ..base import fonts

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

    textColor - HexColor "#fff" is white "#ff00ff" is purple.

    anchor - tkinter anchor value (NW, S, CENTER, etc.)
    '''

    def __init__(
                self,
                canvas: Canvas,
                position: Tuple[int],
                text: str,
                font: str = "Courier",
                fontSize: int = 12,
                textColor: str = "#fff",
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

        # Set up the collider for the text.
        w = self.font[self.currentFontSize].measure(text) / self.initialScreenWidth
        h = self.font[self.currentFontSize].metrics()["linespace"] / self.initialScreenHeight
        self.collider = BoxCollider(position[0], position[1], w, h, anchor = anchor)

        # Create the text on the canvas and retain the handle on the textID
        self.textID: int = self.canvas.create_text(
            self.collider.x * self.initialScreenWidth,
            self.collider.y * self.initialScreenHeight,
            text = self.text,
            fill = textColor,
            anchor = NW, # Anchor is always NW because the collider normalizes all points to be this way
            font = self.font[self.currentFontSize]
        )
    
    def _resize(self, newWidth: int, newHeight: int):
        '''
        Resize the text
        '''

        self.canvas.scale(self.textID, 0, 0, newWidth / self.lastScreenWidth, newHeight / self.lastScreenHeight)

        # May need to create different sized text as the size is adjusted. Do this here.
        textSize = int(self.initialFontSize * newWidth / self.initialScreenWidth)
        if textSize < fonts.SMALLEST_FONT_SIZE:
            textSize = fonts.SMALLEST_FONT_SIZE
        if textSize > fonts.LARGEST_FONT_SIZE:
            textSize = fonts.LARGEST_FONT_SIZE
        
        # To resize the text, we have to actually change the font.
        self.canvas.itemconfig(self.textID, font = self.font[textSize])
