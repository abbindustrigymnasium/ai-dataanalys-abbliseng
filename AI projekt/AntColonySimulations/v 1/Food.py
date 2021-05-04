from Utils import *
import pygame
from MapPoint import MapPoint

class Food:
    def __init__(self, envir, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.envir = envir
        self.object = pygame.Rect(self.x, self.y, 1, 1)
        self.envir.map[getArrayLocation([self.x, self.y])].type = MapPoint.TYPE_FOOD
    def display(self):
        pygame.draw.rect(self.envir.fake_screen, (0, 255, 0), self.object)