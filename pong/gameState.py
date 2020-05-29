from src import GameState

from typing import Tuple

class PongState(GameState):
    '''

    '''

    def __init__(self):
        GameState.__init__(self)

        self.playerPaddleLocation: float = .5
        self.enemyPaddleLocation: float = .5
        self.ballLocation: Tuple[float, float] = (.5, .5)
        # self.ballVelocity: Tuple[float, float] = (.5, 0.1)
        self.ballVelocity: Tuple[float, float] = (0.5, 0)