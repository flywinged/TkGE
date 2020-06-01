from tkinter import N

from src import Text

from .gameState import PongState

class ScoreBox(Text):
    '''

    '''

    def __init__(self):
        Text.__init__(
            self,
            (.5, 0),
            "0",
            fontSize=32,
            textColor=(.2, 1.0, .2),
            anchor=N
        )

    def _update(self, gameState: PongState):
        self.text = str(gameState.score)