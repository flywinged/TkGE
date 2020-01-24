from typing import Dict

from tkinter.font import Font

FONTS: Dict[str, Dict[int, Font]] = {
    "Courier" : {}
}

SMALLEST_FONT_SIZE = 4
LARGEST_FONT_SIZE = 72

def initializeFonts():
    '''

    '''

    for fontName in FONTS:
        for size in range(SMALLEST_FONT_SIZE, LARGEST_FONT_SIZE + 1):
            FONTS[fontName][size] = Font(family = "Courier", size = size)

