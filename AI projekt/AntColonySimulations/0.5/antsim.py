import pygame
from pygame.locals import *
import math
from  random import choice, randrange, randint, random
import threading

from Nest import Nest
from Ant import Ant
from Food import Food
from MapPoint import MapPoint
from Utils import pointsInCircle, fromArrayLocation, getArrayLocation, hsl2rgb, debugDraw, checkIfFood

pygame.init()

# _width = math.floor(1280/3)
# _height = math.floor(960/3)
_width = math.floor(1920/15)
_height = math.floor(1080/15)
_sSize = [_width, _height]
_ratio = _height/_width
relX = math.floor(_width/2)
relY = math.floor(_height/2)

class Environment:
    def __init__(self, width, height, number_of_ants):
        self._width = width
        self._height = height

        self._running = True
        self.screen = pygame.display.set_mode((width, height), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.fake_screen = self.screen.copy()

        self.map = []
        for i in range(self._width*self._height):
            self.map.append(MapPoint(fromArrayLocation(i),MapPoint.TYPE_EMPTY))
        ##
        self.nest = Nest(self)
        self.food = {}
        self.pheromones = []
        self.pheromones_to_clear = []
        self.ants = []
        ##

        for i in range(number_of_ants):
            self.ants.append(Ant(self, self.nest, Ant.TYPE_SEEKER))
        self.ants.append(Ant(self, self.nest, Ant.TYPE_FOLLOWER))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        # elif event.type == pygame.MOUSEBUTTONUP and pygame.key.get_mods()&pygame.KMOD_CTRL:
        #     p = [0,0]
        #     pos = pygame.mouse.get_pos()
        #     p[0] = math.floor((pos[0]/self.screen.get_width())*self._width)
        #     p[1] = math.floor((pos[1]/self.screen.get_height())*self._height)
        #     points = pointsInCircle(p, 5)
        #     if (pygame.key.get_mods()&pygame.KMOD_ALT):
        #         for p in points:
        #             Pheromone(self, 0.7, pos=p)
        #     else:
        #         for p in points:
        #             Pheromone(self, -0.7, pos=p)
        elif event.type == pygame.MOUSEBUTTONUP and pygame.key.get_mods()&pygame.KMOD_ALT:
            p = [0,0]
            pos = pygame.mouse.get_pos()
            p[0] = math.floor((pos[0]/self.screen.get_width())*self._width)
            p[1] = math.floor((pos[1]/self.screen.get_height())*self._height)
            foodPoints = pointsInCircle(p, 10)
            for point in foodPoints:
                overlord.food[getArrayLocation(point)] = Food(self, point)
        elif event.type == VIDEORESIZE:
            newWindowSize = (event.size[0], math.floor(event.size[0]*_ratio))
            self.screen = pygame.display.set_mode(newWindowSize, HWSURFACE|DOUBLEBUF|RESIZABLE)
    
    def resetWindow(self):
        # self.screen.fill((78, 42, 42))
        self.screen.fill((255, 255, 255))
        self.fake_screen.fill((255, 255, 255))
        pass

    def display(self):
        for pheromone in self.pheromones:
            value = 1-self.map[getArrayLocation(pheromone)].pheromone_concentration/MapPoint.MAX_CONCENTRATION
            # print(value)
            pygame.draw.circle(self.fake_screen,hsl2rgb(264, 100, 100*value), pheromone, 1)
        for food in self.food:
            self.food[food].display()
        self.nest.display()
        for ant in self.ants:
            ant.display()
    
    def handle_pheromones(self):
        for pheromone in self.pheromones:
            self.map[getArrayLocation(pheromone)].pheromoneDecay(self, pheromone)
    def handle_ants(self):
        for ant in self.ants:
            ant.move()
    
    def hiveDist(self, x, y):
        if (x == self.nest.x and y == self.nest.y):
            pass
        else:
            return math.sqrt(abs(pow(x-self.nest.x, 2))+abs(pow(y-self.nest.y, 2)))
        return 0.0


overlord = Environment(_width, _height, 100)

while overlord._running:
    overlord.resetWindow()

    for event in pygame.event.get():
        overlord.handle_event(event)

    overlord.handle_pheromones()
    overlord.handle_ants()
    overlord.display()
    overlord.screen.blit(pygame.transform.scale(overlord.fake_screen, overlord.screen.get_rect().size), (0,0))
    
    pygame.display.flip()

pygame.quit()