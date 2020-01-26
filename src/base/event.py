
# Python imports
from enum import auto
from enum import Enum

from dataclasses import dataclass
from dataclasses import field

from typing import Set


# Event types
class EVENT_TYPE(Enum):
    NO_EVENT: int = auto()

    MOUSE_MOTION: int = auto()
    MOUSE_CLICK: int = auto()
    MOUSE_RELEASE: int = auto()
    MOUSE_DRAG: int = auto()
    MOUSE_WHEEL: int = auto()

    KEY_PRESS: int = auto()
    KEY_RELEASE: int = auto()

# Mouse Buttons enum
class BUTTONS(Enum):

    LEFT_CLICK: int = auto()
    MIDDLE_CLICK: int = auto()
    RIGHT_CLICK: int = auto()


@dataclass
class InputState:
    '''
    Keeps track of the current input state of the application.
    '''

    mouseX: float = 0.0
    mouseY: float = 0.0

    pressedKeys: Set[str] = None
    pressedButtons: Set[int] = None

# Create the input set
INPUT_STATE = InputState()

# Assign all the mutable variables
INPUT_STATE.pressedKeys = set()
INPUT_STATE.pressedButtons = set()

@dataclass
class TGEEvent:
    '''

    '''

    # General event type
    type: int = 0

    # Cursor location
    mouseX: float = None
    mouseY: float = None

    # Mouse wheel offset
    wheelOffset: float = None

    # Mouse button
    button: int = None

    # Key sym value (from tkinter)
    keysym: str = None