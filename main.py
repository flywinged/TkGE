from src import Game
from src import GameState

from src import Rect, Text, Oval, Polygon, Button

gs = GameState()
g = Game(gs)

go = Rect(
    (.5, .5), 
    .2, .2,
    (1.0, .5, .5)
)

text = Text(
    (.5, .5),
    "Test Text"
)

oval = Oval(
    (.2, .2),
    (.3, .1),
    fillColor=(0.5, 1.0, 0)
)

polygon = Polygon(
    [(.8, .8), (.8, .9), (.85, .85), (.82, .68)],
    fillColor=(0.0, 1.0, 1.0)
)

button = Button(
    (.8, .2),
    .3, .1
)


g.addGameObject(go)
g.addGameObject(text)
g.addGameObject(oval)
g.addGameObject(polygon)
g.addGameObject(button)

g.play()

# from src.math import HexGrid

# h = HexGrid(13)