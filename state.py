# Contains the state of everything in the game
from tkinter import Tk
from tkinter.constants import *

from GameEngine.objects.button import Button

from GameEngine.base import fonts

timerDelay = 40 # in milliseconds

button: Button = None

root: Tk = None

def initializeState(tkRoot: Tk, canvas):
    global root

    root = tkRoot

    fonts.initializeFonts()

    global button
    button =  Button(
        canvas,
        (640, 360),
        "Test Button. With hopefully multiple lines.",
        SE
    )
