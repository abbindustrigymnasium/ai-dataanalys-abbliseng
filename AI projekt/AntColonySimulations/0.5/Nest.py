import math
from Utils import getRelX, getRelY, getArrayLocation;
import pygame
from MapPoint import MapPoint

class Nest:
    def __init__(self, envir):
        self.x = getRelX()
        self.y = getRelY()
        self.envir = envir
        self.tiles = []
    
        for tile in [[self.x, self.y],[self.x+1, self.y],[self.x, self.y+1],[self.x+1, self.y+1]]:
            self.tiles.append(pygame.Rect(tile[0], tile[1], 1, 1))
            self.envir.map[getArrayLocation([tile[0], tile[1]])].type = MapPoint.TYPE_NEST # Update MapPoint type
    
    def display(self):
        for tile in self.tiles:
            pygame.draw.rect(self.envir.fake_screen, (255,0,0), tile)