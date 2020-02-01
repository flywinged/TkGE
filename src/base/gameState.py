from ..common import getTime

import pickle

class GameState:
    '''
    General gameState class. A custom gameState should be created for each application to enable nice type-hints.

    A Game state should be initialized with NO parameters. This enables easy saving and loading.
    '''

    def __init__(self):
        self.__dict__ = {}

        # The current gameState time (in seconds)
        self.now: float = getTime()

        # The last gameState time (in seconds)
        self.last: float = getTime()

    ######################
    # SAVING AND LOADING #
    ######################

    def save(self, savePath: str):
        '''
        Saves the whole GameState into a pickle.
        '''

        with open(savePath, "wb") as f:
            pickle.dump(
                self.__dict__,
                f,
                protocol=pickle.HIGHEST_PROTOCOL
            )
    
    @staticmethod
    def load(loadPath: str):
        '''
        Loads the whole GameState from a pickle.
        '''

        gameState = GameState()

        with open(loadPath, "rb") as f:
            gameState.__dict__ = pickle.load(f)

        return gameState
    

    ##########
    # TIMING #
    ##########

    def updateTime(self):
        '''
        Updates self.now and self.last. This function will be called before every game update.
        '''

        self.last = self.now
        self.now = getTime()
    
    def getFrameTime(self):
        '''
        Returns how long the last call of update was ago (in seconds)
        '''

        return self.now - self.last