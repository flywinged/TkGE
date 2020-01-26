
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

def adjustTopLeftCorner(position: Tuple[float, float], desiredAnchor: str, givenAnchor: str, width: float, height: float) -> Tuple[float, float]:
    '''
    Takes a given position with a width and height, and returns a new position
        describing wehere the top left corner of the bounding box has to go in
        order to have the appropriate desiredAnchor.

    Parameters
    ----------
    @param position - (x, y) position on the screen. This position is what is desired to be at the given desiredAnchor

    @param desiredAnchor - tkinter desiredAnchor value

    @param givenAnchor - tkinter givenAnchor value

    @param width/height - Width and height of the desired bounding box
    '''

    # Extract the x and y vaules of the position
    x, y = position

    # Modify the x, y values to be the top left corner according to the given anchor values
    # Handle the x values first
    if givenAnchor in [E, NE, SE]:
        x -= width / 2
    elif givenAnchor in [W, NW, SW]:
        x += width / 2

    # Then handle the Y values
    if givenAnchor in [NW, N , NE]:
        y += height / 2
    elif givenAnchor in [SW, S, SE]:
        y -= height / 2


    # The logic for the box changes slightly depending on the supplied desiredAnchor.
    # Handle the x values first
    if desiredAnchor in [E, NE, SE]:
        x -= width
    elif desiredAnchor in [N, CENTER, S]:
        x -= width / 2
    
    # Then handle the Y values
    if desiredAnchor in [W, CENTER, E]:
        y -= height /2
    elif desiredAnchor in [SW, S, SE]:
        y -= height

    return x, y