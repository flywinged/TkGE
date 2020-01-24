# Tkinter imports
from tkinter.font import Font

# Python imports
from typing import Dict


# Font dictionary. To add more fonts, just add extra strings for those font names
#   and assign them an extra dictionary. The initialize fonts call will automatically create them.
FONTS: Dict[str, Dict[int, Font]] = {
    "Courier" : {}
}

# The smallest and largest font sizes to create
SMALLEST_FONT_SIZE = 4
LARGEST_FONT_SIZE = 72

def initializeFonts():
    '''

    '''

    for fontName in FONTS:
        for size in range(SMALLEST_FONT_SIZE, LARGEST_FONT_SIZE + 1):
            FONTS[fontName][size] = Font(family = "Courier", size = size)

