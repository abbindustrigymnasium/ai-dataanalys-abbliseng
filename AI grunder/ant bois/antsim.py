import pygame
from pygame.locals import *
import math
from  random import choice, randrange, randint, random
import threading

pygame.init()

height = math.floor(960/3)
width = math.floor(1280/3)
_sSize = [width, height]
relX = math.floor(width/2)
relY = math.floor(height/2)

class Environment:
    def __init__(self, width, height):
        self._running = True
        self.screen = pygame.display.set_mode((width, height), HWSURFACE|DOUBLEBUF|RESIZABLE)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

overlord = Environment(height, width)

while overlord._running:
    for event in pygame.event.get():
        overlord.handle_event(event)
    pygame.display.flip()

pygame.quit()

# game = Environment(_sSize[0], _sSize[1], 500)
