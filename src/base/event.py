
# Tkinter imports
from tkinter import Event
from tkinter import EventType


# Event types
NO_EVENT: int = 0

MOUSE_MOTION: int = 1
MOUSE_CLICK: int = 2
MOUSE_RELEASE: int = 3
MOUSE_DRAG: int = 4
MOUSE_WHEEL: int = 5

KEY_PRESS: int = 6
KEY_RELEASE: int = 7

class INPUT_STATE:
    '''
    Keeps track of 
    '''



class TGEEvent:
    '''

    '''

    def __init__(self):

        # General event type
        self.eventType: int = 0

        # Cursor location
        self.mouseX: float = None
        self.mouseY: float = None

        #