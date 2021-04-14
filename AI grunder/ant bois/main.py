# Simple pygame program

# Import and initialize the pygame library
import pygame
import math
# from ant import Ant
# from food import Food
from utils import *
from  random import choice, randrange

pygame.init()
# _sSize = [1280, 960]
_sSize = [math.floor(1280/4), math.floor(960/4)]

gameArray = []
for i in range(_sSize[0]*_sSize[1]):
    gameArray.append({"ants":[], "pheromones": [], "food": []})

class AntWindow():
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._running = True
        self.screen = pygame.display.set_mode([width, height])
        # Fill the background
        self.screen.fill((78, 42, 42))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

game = AntWindow(_sSize[0], _sSize[1])

while game._running:

    for event in pygame.event.get():
        game.handle_event(event)

    # "Flip the display" - (update the whole screen)
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()