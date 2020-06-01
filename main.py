from src import Game
from src import GameState

from src import Button

gs = GameState()
g = Game(gs)

def f():
    print("Clicked!")

button = Button(
    (.5, .5),
    .2, .05,

    callback=f,

    text="TEST"
)
g.addGameObject(button)

g.play()

# from src.math import HexGrid

# h = HexGrid(13)