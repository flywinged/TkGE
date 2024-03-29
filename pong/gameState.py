from src import GameState

from typing import Tuple

class PongState(GameState):
    '''

    '''

    def __init__(self):
        GameState.__init__(self)

        # Initial paddle positions
        self.playerPaddleLocation: float = .5
        self.enemyPaddleLocation: float = .5

        # Initial ball location and velocity
        self.ballLocation: Tuple[float, float] = (.5, .5)
        self.ballVelocity: Tuple[float, float] = (0.5, 0)

        # Velocity increments
        self.ballVelocityValue: float = .5
        self.ballVelocityIncrement: float = 0.05

        # Score
        self.score: int = 0