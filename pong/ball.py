from src import Oval

from tkinter import CENTER

from .gameState import PongState

import random

from math import sin
from math import cos
from math import pi

class Ball(Oval):
    '''

    '''

    def __init__(self, canvas):
        Oval.__init__(self, canvas, (.5, .5), .01, (.6, .6, .3), anchor=CENTER)

    def hitPaddle(self, gameState: PongState, multiplier: float):
        '''
        Multiplier is either 1.0 or -1.0. Just to flip the velocity either for hitting the player paddle or the enemy paddle
        '''

        # Pick a random angle for the ball to bounce at
        angle = 2.0 * (pi / 4.0) * (random.random() - .5)

        # Assign a new ball velocity according to the chosen angle
        gameState.ballVelocity = (
            multiplier * gameState.ballVelocityValue * cos(angle),
            gameState.ballVelocityValue * sin(angle)
        )

        # Make the ball start moving faster according to the variable set in the gameState
        gameState.ballVelocityValue += gameState.ballVelocityIncrement

    def _update(self, gameState: PongState):
        '''
        Move the ball and check to see if the ball has hit any walls or paddles.
        '''

        # Move the ball from its current location
        gameState.ballLocation = (
            gameState.ballLocation[0] + gameState.ballVelocity[0] * gameState.getFrameTime(),
            gameState.ballLocation[1] + gameState.ballVelocity[1] * gameState.getFrameTime()
        )

        # If the ball hits the bottom of the screen, flip its vertical velocity.
        if gameState.ballLocation[1] - self.collider.r[1] < 0:

            gameState.ballVelocity = (
                gameState.ballVelocity[0],
                -gameState.ballVelocity[1]
            )
        
        # Do the same if the ball hits the top of the screen.
        if gameState.ballLocation[1] + self.collider.r[1] > 1.0:

            gameState.ballVelocity = (
                gameState.ballVelocity[0],
                -gameState.ballVelocity[1]
            )
        

        # If the ball hits your paddle
        if (
            gameState.ballLocation[0] < self.collider.r[0] + 0.01 and
            abs(gameState.ballLocation[1] - gameState.playerPaddleLocation) < .1 and
            gameState.ballVelocity[0] < 0
        ):
            gameState.score += 1
            self.hitPaddle(gameState, 1.0)
        
        # If the ball hits the enemy paddle
        if (
            gameState.ballLocation[0] + self.collider.r[0] + 0.01 > 1.0 and
            abs(gameState.ballLocation[1] - gameState.enemyPaddleLocation) < .1 and
            gameState.ballVelocity[0] > 0
        ):
            self.hitPaddle(gameState, -1.0)
        
        # Check to see if the ball is off the screen and hasn't been captured by the paddle
        if (
            gameState.ballLocation[0] < 0 and
            gameState.ballVelocity[0] < 0
        ):
            gameState.ballLocation = (.5, .5)
            gameState.ballVelocityValue = .5
            gameState.ballVelocity = (.5, 0)
            gameState.score = 0
            
        if (
            gameState.ballLocation[0] > 1 and
            gameState.ballVelocity[0] > 0
        ):
            gameState.ballLocation = (.5, .5)
            gameState.ballVelocityValue = .5
            gameState.ballVelocity = (.5, 0)
            gameState.score = 0

        self.collider.x = gameState.ballLocation[0]
        self.collider.y = gameState.ballLocation[1]
        
        self.coords = self.collider.getCoords(self.screenWidth, self.screenHeight)
        self.redraw = True
