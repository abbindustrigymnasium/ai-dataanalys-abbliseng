import pygame
from pygame.locals import *
import math
from  random import choice, randrange, randint, random
import threading

from Nest import Nest
from Ant import Ant
from Food import Food
from MapPoint import MapPoint
from Utils import *

pygame.init()

class Environment:
    def __init__(self, width, height, number_of_ants):
        self._width = width
        self._height = height
        self._running = True
        self.screen = pygame.display.set_mode((width, height), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.fake_screen = self.screen.copy()
        # Initialize game map
        self.map = []
        for i in range(self._width*self._height):
            self.map.append(MapPoint(fromArrayLocation(i),MapPoint.TYPE_EMPTY, self))
        ##
        self.nest = Nest(self)
        self.food = {}
        self.ants = []
        ##
        for i in range(number_of_ants): # Spawns some ants
            self.ants.append(Ant(self, self.nest, Ant.TYPE_SEEKER))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONUP and pygame.key.get_mods()&pygame.KMOD_ALT: # alt + click spawns food within a radius
            p = [0,0]
            pos = pygame.mouse.get_pos()
            p[0] = math.floor((pos[0]/self.screen.get_width())*self._width)
            p[1] = math.floor((pos[1]/self.screen.get_height())*self._height)
            foodPoints = pointsInCircle(p, 6)
            for point in foodPoints:
                try: # Just make sure its within the array bounds
                    overlord.food[getArrayLocation(point)] = Food(self, point)
                except:
                    pass
        elif event.type == VIDEORESIZE: # Resize with same ratio
            newWindowSize = (event.size[0], math.floor(event.size[0]*getRatio()))
            self.screen = pygame.display.set_mode(newWindowSize, HWSURFACE|DOUBLEBUF|RESIZABLE)
        elif event.type  == pygame.KEYDOWN:
            if event.key ==  ord('q'): # Quit game if q is pressed
                self._running = False
    
    def resetWindow(self):
        self.screen.fill((0, 0, 0))
        self.fake_screen.fill((0, 0, 0))
        pass

    def display(self):
        for tile in self.map:
            tile.display()
        for ant in self.ants:
            ant.display()
    
    def handle_ants(self):
        for ant in self.ants:
            ant.move()
    
    def hiveDist(self, x, y):
        if (x == self.nest.x and y == self.nest.y):
            pass
        else:
            # Calculate distance from the nest
            return math.sqrt(abs(pow(x-self.nest.x, 2))+abs(pow(y-self.nest.y, 2)))
        return 0.0


overlord = Environment(getWidth(), getHeight(), 100) # width, height, number of ants
overlord.ants.append(Ant(overlord, overlord.nest, Ant.TYPE_SEEKER, "My")) # Myran My

# Uncomment the code bellow to enable starter patches of food in each corner of the screen
'''
START FOOD (IN CORNERS)
for x in range(10,25):
    for y in range(10,20):
        overlord.food[getArrayLocation((x,y))] = Food(overlord, (x,y))
        # overlord.food[getArrayLocation((_width-x,y))] = Food(overlord, (_width-x,y))
        # overlord.food[getArrayLocation((x,_height-y))] = Food(overlord, (x,_height-y))
        overlord.food[getArrayLocation((getWidth()-x,getHeight()-y))] = Food(overlord, (getWidth()-x,getHeight()-y))
'''
while overlord._running:
    overlord.resetWindow()

    for event in pygame.event.get():
        overlord.handle_event(event)

    overlord.handle_ants()
    overlord.display() # This function also calls the functions that handle pheromones and such.

    # Zoom
    overlord.screen.blit(pygame.transform.scale(overlord.fake_screen, overlord.screen.get_rect().size), (0,0))
    
    #Update screen
    pygame.display.flip()

pygame.quit()