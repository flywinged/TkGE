
# Python imports
from colorsys import hls_to_rgb
from typing import Tuple


def convertRGBToHex(rgb: Tuple[float, float, float]) -> str:
    '''

    '''

    # Extract the int values of each color
    r = int(round(rgb[0] * 255))
    g = int(round(rgb[1] * 255))
    b = int(round(rgb[2] * 255))

    # Construct the hex code color
    hexCode = "#"

    # Get the hex for each color
    rHex = str(hex(r))[2:]
    gHex = str(hex(g))[2:]
    bHex = str(hex(b))[2:]

    # Add zeros if necessary
    if len(rHex) == 1: rHex = "0" + rHex
    if len(gHex) == 1: gHex = "0" + gHex
    if len(bHex) == 1: bHex = "0" + bHex

    # Remove the /x in front of each color
    hexCode += rHex + gHex + bHex
    
    return hexCode

def convertHLSToHex(hls: Tuple[float, float, float]) -> str:
    '''

    '''

    return convertRGBToHex(hls_to_rgb(hls[0], hls[1], hls[2]))