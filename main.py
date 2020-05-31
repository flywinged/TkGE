from src import Game
from src import GameState

from src import Rect, Text, Oval, Polygon, Button, Hexagon

gs = GameState()
g = Game(gs)

# g.play()

from src.math import HexGrid

h = HexGrid(13)