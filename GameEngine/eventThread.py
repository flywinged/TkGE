from threading import Thread

from tkinter import Event, EventType

from .base.gameObject import GameObject

from typing import List

from .gameState import GameState

import time

class EventThread(Thread):
    '''
    Thread to handle all of the events which will come through the game.
    '''

    def __init__(self):
        Thread.__init__(self)

        self.eventQueue: List[Event] = []
        self.isActive: bool = True
    
    def run(self):

        while self.isActive:

            while len(self.eventQueue) > 0:

                # Lower the amount of checks for mouse motion
                motionIndex = 0
                while motionIndex + 1 < len(self.eventQueue) and self.eventQueue[motionIndex + 1].type == EventType.Motion:
                    motionIndex += 1
                if motionIndex > 0:
                    self.eventQueue = self.eventQueue[motionIndex:]

                # Get the next event in the queue and pass it to all gameObjects
                event = self.eventQueue.pop(0)
                for gameObject in GameState.all():
                    gameObject.handleEvent(event)

            time.sleep(.001)