from tkinter import CENTER

from src import Rect

from src import TGEEvent, EVENT_TYPE

from .gameState import PongState

class PlayerPaddle(Rect):
    '''

    '''

    def __init__(self, canvas):

        Rect.__init__(self, canvas, (.005, .5), .01, .2, (0.2, 0.8, 0.2), anchor=CENTER)
    
    def _handleEvent(self, event: TGEEvent, gameState: PongState):
        '''

        '''

        if event.type == EVENT_TYPE.MOUSE_MOTION or event.type == EVENT_TYPE.MOUSE_DRAG:
            self.collider.y = event.mouseY - self.collider.h / 2

            if self.collider.y < 0:
                self.collider.y = 0
            if self.collider.y + self.collider.h > 1.0:
                self.collider.y = 1.0 - self.collider.h

            self.coords = self.collider.getCoords(self.screenWidth, self.screenHeight)
            self.redraw = True
        
            gameState.playerPaddleLocation = self.collider.y + self.collider.h / 2

class EnemyPaddle(Rect):
    '''

    '''

    def __init__(self, canvas):

        Rect.__init__(self, canvas, (.995, .5), .01, .2, (0.8, 0.2, 0.2), anchor=CENTER)
    
    def update(self, gameState: PongState):
        '''

        '''

        ballCenterY = gameState.ballLocation[1] - self.collider.h / 2

        if ballCenterY < 0:
            ballCenterY = 0
        if ballCenterY > 1.0 - self.collider.h:
            ballCenterY = 1.0 - self.collider.h
        
        self.collider.y = ballCenterY
        gameState.enemyPaddleLocation = ballCenterY + self.collider.h / 2

        self.coords = self.collider.getCoords(self.screenWidth, self.screenHeight)
        self.redraw = True
