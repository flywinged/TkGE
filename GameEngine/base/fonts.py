from typing import Dict

from tkinter.font import Font

courier: Dict[int, Font] = {}

def initializeFonts():
    '''

    '''

    # Initialize all courier fonts    
    global courier
    for size in range(8, 72 + 1):
        courier[size] = Font(family = "Courier", size = size)
