import pickle

class GameState:
    '''
    General gameState class. A custom gameState should be created for each application to enable nice type-hints.

    A Game state should be initialized with NO parameters. This enables easy saving and loading.
    '''

    def __init__(self):
        pass

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