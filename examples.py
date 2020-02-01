# File for showing example games

import sys

# Game imports
from pong import play as playPong

if __name__ == "__main__":

    if len(sys.argv) != 2:
        raise Exception("Specify the game you want to play.")
    
    # Play pong
    if sys.argv[1] == "pong":
        playPong()
    
    else:
        raise Exception(f"{sys.argv[1]} is not a recognized game. Try again.")