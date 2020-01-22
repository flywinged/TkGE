from .base.gameObject import GameObject

from typing import Dict

class GameState:
    '''
    Controls all the gameObject present in the game
    '''

    gameObjects: Dict[int, GameObject] = {}

    @classmethod
    def addGameObject(cls, gameObject: GameObject):
        cls.gameObjects[gameObject.ID] = gameObject
    
    @classmethod
    def removeGameObject(cls, gameObject: GameObject):
        del cls.gameObjects[gameObject.ID]
    
    @classmethod
    def all(cls) -> GameObject:
        for ID in cls.gameObjects:
            yield cls.gameObjects[ID]