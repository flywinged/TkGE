
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

    # Remove the /x in front of each color
    hexCode += str(hex(r))[2:]
    hexCode += str(hex(g))[2:]
    hexCode += str(hex(b))[2:]

    return hexCode

def convertHLSToHex(hls: Tuple[float, float, float]) -> str:
    '''

    '''

    return convertRGBToHex(hls_to_rgb(hls[0], hls[1], hls[2]))