import math
from Utils import pointsInCircle, fromArrayLocation, getArrayLocation, hsl2rgb, debugDraw, checkIfFood
import pygame
from MapPoint import MapPoint
# from main import _height, _width, _sSize, _ratio, relX, relY

_width = math.floor(1920/15)
_height = math.floor(1080/15)
_sSize = [_width, _height]
_ratio = _height/_width
relX = math.floor(_width/2)
relY = math.floor(_height/2)

class Nest:
    def __init__(self, envir):
        self.x = relX
        self.y = relY
        self.envir = envir
        self.tiles = [] 
        for tile in [[self.x, self.y],[self.x+1, self.y],[self.x, self.y+1],[self.x+1, self.y+1]]:
        # for tile in pointsInCircle([self.x, self.y], 3):
            self.tiles.append(pygame.Rect(tile[0], tile[1], 1, 1))
            self.envir.map[getArrayLocation([tile[0], tile[1]])].type = MapPoint.TYPE_NEST
    def display(self):
        for tile in self.tiles:
            pygame.draw.rect(self.envir.fake_screen, (255,0,0), tile)