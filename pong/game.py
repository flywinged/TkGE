from src import Game
from .gameState import PongState

from .paddle import PlayerPaddle, EnemyPaddle
from .ball import Ball
from .scoreBox import ScoreBox

class Pong(Game):
    '''

    '''

    def __init__(self):
        state = PongState()
        Game.__init__(self, state)

        self.addGameObject(PlayerPaddle(self.canvas))
        self.addGameObject(EnemyPaddle(self.canvas))
        self.addGameObject(Ball(self.canvas))
        self.addGameObject(ScoreBox(self.canvas))
    
    def updateBefore(self):
        '''

        '''