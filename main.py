from src import Game
from src import GameState

from src import Oval

gs = GameState()
g = Game(gs)

def f():
    print("Clicked!")

# width = 14
# height = 24
# for x in range(0, width):
#     for y in range(0, height):
#         button = Button(

#             g.canvas,
#             (x / width, y / height),
#             1 / width, 1 / height,
#             anchor="NW",
#             text="(" + str(x) + "," + str(y) + ")",
#             textHighlight=(1, 0, 0)

#         )

#         g.addGameObject(button)

o = Oval(
    g.canvas,
    (.5, .5),
    .3
)
g.addGameObject(o)

g.play()

# from src.math import HexGrid

# h = HexGrid(13)