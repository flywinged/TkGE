from src import Oval

from tkinter import Canvas, CENTER

from .gameState import PongState

class Ball(Oval):
    '''

    '''

    def __init__(self, canvas: Canvas):

        Oval.__init__(self, canvas, (.5, .5), .01, (.6, .6, .3), anchor=CENTER)
    
    def update(self, gameState: PongState):
        '''

        '''

        gameState.ballLocation = (
            gameState.ballLocation[0] + gameState.ballVelocity[0] * gameState.getFrameTime(),
            gameState.ballLocation[1] + gameState.ballVelocity[1] * gameState.getFrameTime()
        )

        if gameState.ballLocation[1] - self.collider.r[1] < 0:
            gameState.ballLocation = (
                gameState.ballLocation[0],
                -(gameState.ballLocation[1] - self.collider.r[1]) + self.collider.r[1]
            )

            gameState.ballVelocity = (
                gameState.ballVelocity[0],
                -gameState.ballVelocity[1]
            )
        
        if gameState.ballLocation[1] + self.collider.r[1] > 1.0:
            gameState.ballLocation = (
                gameState.ballLocation[0],
                2.0 - (gameState.ballLocation[1] + self.collider.r[1]) + self.collider.r[1]
            )

            gameState.ballVelocity = (
                gameState.ballVelocity[0],
                -gameState.ballVelocity[1]
            )

        self.collider.x = gameState.ballLocation[0]
        self.collider.y = gameState.ballLocation[1]
        
        self.canvas.coords(self.ovalID, self.collider.getCoords(self.currentScreenWidth, self.currentScreenHeight))