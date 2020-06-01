from src import Game
from src import GameState

from src import Button

gs = GameState()
g = Game(gs)

button = Button(
    (.5, .5),
    .2, .05,

    text="TEST"
)
g.addGameObject(button)

g.play()

# from src.math import HexGrid

# h = HexGrid(13)