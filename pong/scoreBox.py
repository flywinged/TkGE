from tkinter import N

from src import Text

from .gameState import PongState

class ScoreBox(Text):
    '''

    '''

    def __init__(self, canvas):
        Text.__init__(
            self,
            canvas,
            (.5, 0),
            "0",
            fontSize=32,
            textColor=(.2, 1.0, .2),
            anchor=N
        )

    def _update(self, gameState: PongState):
        if self.text != str(gameState.score):
            self.text = str(gameState.score)
            self.redraw = True