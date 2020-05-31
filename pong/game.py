from src import Game
from .gameState import PongState

from .paddle import PlayerPaddle, EnemyPaddle
from .ball import Ball

class Pong(Game):
    '''

    '''

    def __init__(self):
        state = PongState()
        Game.__init__(self, state)

        self.addGameObject(PlayerPaddle())
        self.addGameObject(EnemyPaddle())
        self.addGameObject(Ball())
    
    def updateBefore(self):
        '''

        '''