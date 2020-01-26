
# Python imports
from typing import Tuple

# Tkinter imports
from tkinter.constants import NW
from tkinter.constants import N
from tkinter.constants import NE
from tkinter.constants import W
from tkinter.constants import CENTER
from tkinter.constants import E
from tkinter.constants import SW
from tkinter.constants import S
from tkinter.constants import SE

def adjustTopLeftCorner(position: Tuple[float, float], anchor: str, width: float, height: float) -> Tuple[float, float]:
    '''
    Takes a given position with a width and height, and returns a new position
        describing wehere the top left corner of the bounding box has to go in
        order to have the appropriate anchor.

    Parameters
    ----------
    @param position - (x, y) position on the screen. This position is what is desired to be at the given anchor

    @param anchor - tkinter anchor value

    @param width/height - Width and height of the desired bounding box
    '''

    # Extract the x and y vaules of the position
    x, y = position

    # The logic for the box changes slightly depending on the supplied anchor.
    # Handle the x values first
    if anchor in [E, NE, SE]:
        x -= width
    elif anchor in [N, CENTER, S]:
        x -= width / 2
    
    # Then handle the Y values
    if anchor in [W, CENTER, E]:
        y -= height /2
    elif anchor in [SW, S, SE]:
        y -= height

    return x, y