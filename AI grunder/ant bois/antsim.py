import pygame
from pygame.locals import *
import math
from  random import choice, randrange, randint, random
import threading

pygame.init()

_width = math.floor(1280/3)
_height = math.floor(960/3)
_sSize = [_width, _height]
_ratio = _height/_width
relX = math.floor(_width/2)
relY = math.floor(_height/2)

def pointsInCircle(location, radius):
    points = []
    # Calculate bounding rectangle
    upperX = location[0]-radius
    upperY = location[1]-radius
    width = 2*radius
    # Get circle points
    for x in range(width):
        x += upperX
        for y in range(width):
            y += upperY
            dx = x - location[0]
            dy = y - location[1]
            distanceSquared = dx*dx+dy*dy
            if (distanceSquared <= radius*radius):
                points.append([x,y])
    return points

def getArrayLocation(location, width=_width):
    return location[1]*width+location[0]

def fromArrayLocation(location, width=_width):
    return [location%width, math.floor(location/width)]

def hsl2rgb(h, s, l):
    s /= 100
    l /= 100
    c = (1 - abs(2*l-1))*s
    x = c*(1-abs((h/60)%2-1))
    m = l-c/2
    r = 0
    g = 0
    b = 0
    if (0 <= h and h < 60):
        r, g, b = c, x, 0
    elif (60 <= h and h < 120):
        r, g, b = x, c, 0
    elif (120 <= h and h < 180):
        r, g, b = 0, c, x
    elif (180 <= h and h < 240):
        r, g, b = 0, x, c
    elif (240 <= h and h < 300):
        r, g, b = x, 0, c
    elif (300 <= h and h < 360):
        r, g, b = c, 0, x
    r = round((r+m)*255)
    g = round((g+m)*255)
    b = round((b+m)*255)
    return((r,g,b))

def debugDraw(pos):
    pygame.draw.circle(overlord.fake_screen, (0, 255, 0), (pos[0], pos[1]), 1)

class Nest:
    def __init__(self, envir):
        self.x = relX
        self.y = relY
        self.envir = envir
        self.tiles = [] 
        for tile in pointsInCircle([self.x, self.y], 3):
            self.tiles.append(pygame.Rect(tile[0], tile[1], 1, 1))
            self.envir.board[getArrayLocation([tile[0], tile[1]])]["nest"] = True
    def display(self):
        for tile in self.tiles:
            pygame.draw.rect(self.envir.fake_screen, (255,0,0), tile)

class Food:
    def __init__(self, envir, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.envir = envir
        self.object = pygame.Rect(self.x, self.y, 1, 1)
        self.envir.board[getArrayLocation([self.x, self.y])]["food"] = True
        self.envir.board[getArrayLocation([self.x, self.y])]["value"] = 1.0
        # self.envir.food.append(self)
    def display(self):
        pygame.draw.rect(self.envir.fake_screen, (0, 255, 0), self.object)

class Pheromone:
    def __init__(self, envir, value, pos=None, ant=None):
        self.x = 0
        self.y = 0
        if (ant):
            self.x = ant.x
            self.y = ant.y
        elif (pos):
            self.x = pos[0]
            self.y = pos[1]
        self.envir = envir
        self.value = value
        self.object = pygame.Rect(self.x, self.y, 1, 1)
        self.envir.board[getArrayLocation([self.x, self.y])]["value"] = self.value
        self.envir.pheromones.append(self)
    def blur(self):
        if self.value < 0:
            self.value += 0.02
            if (self.value >= 0):
                self.value = 0
        elif (self.value > 0):
            self.value += 0.002
            if (self.value >= 1):
                self.value = 0
        else:
            self.envir.board[getArrayLocation([self.x, self.y])]["value"] = 0
            return True # Destroy the instance
        self.envir.board[getArrayLocation([self.x, self.y])]["value"] = self.value
        return False
    def display(self):
        if (self.value < 0):
            pygame.draw.rect(self.envir.fake_screen, hsl2rgb(222, 63, 100*(1-abs(self.value))), self.object)
        else:
            pygame.draw.rect(self.envir.fake_screen, hsl2rgb(13, 100, 100*(1-self.value)), self.object)

class Ant:
    def __init__(self, envir, nest):
        self.x = nest.x
        self.y = nest.y
        self.envir = envir
        self.object = pygame.Rect(self.x, self.y, 1, 1)
        self.viewdist = 5
        self.freedom = randint(0,6)/10
        self.scout = True
    def display(self):
        pygame.draw.rect(self.envir.fake_screen, (0, 0, 0), self.object)
    def findTarget(self):
        possible_targets = {}
        possible_target_points = pointsInCircle([self.x, self.y], self.viewdist)
        # random chance to just pick a random target instead of following the rule bellow
        if (random() <= self.freedom):
            target = getArrayLocation(choice(possible_target_points))
            return target
        #
        for possible_target_point in possible_target_points:
            if (getArrayLocation(possible_target_point) > 0 and getArrayLocation(possible_target_point) < _width*_height-1):
                possible_targets[getArrayLocation(possible_target_point)] = self.envir.board[getArrayLocation(possible_target_point)]["value"]
        if len(possible_targets) <= 0:
            return getArrayLocation(self.x, self.y)
        target = max(possible_targets, key=lambda x: possible_targets[x])
        # if the target value is zero pick a random tile with the same value
        if (self.envir.board[target]["value"] == 0):
            zero_points = []
            for possible_target_point in possible_target_points:
                if (getArrayLocation(possible_target_point) > 0 and getArrayLocation(possible_target_point) < _width*_height-1 and self.envir.board[getArrayLocation(possible_target_point)]["value"] == 0):
                    zero_points.append(possible_target_point)
            target = getArrayLocation(choice(zero_points))
        return target
    def goHome(self):
        return [relX,relY]
    def move(self):
        # leave pheromone behind
        if (self.scout):
            if (self.envir.board[getArrayLocation([self.x, self.y])]["value"] <= 0):
                # Pheromone(self.envir, -0.8, ant=self)
                pass
            target = fromArrayLocation(self.findTarget())
        else:
            Pheromone(self.envir, 0.001, ant=self)
            target = self.goHome()

        if (self.x < target[0]):
            self.x += 1
        elif (self.x > target[0]):
            self.x -= 1
        if (self.y < target[1]):
            self.y += 1
        elif (self.y > target[1]):
            self.y -= 1
        # Check if food is found
        if (self.scout):
            if (self.envir.board[getArrayLocation([self.x, self.y])]["food"]):
                self.envir.board[getArrayLocation([self.x, self.y])]["food"] = False
                del self.envir.food[getArrayLocation([self.x, self.y])]
                self.scout = False
        else:
            if (self.envir.board[getArrayLocation([self.x, self.y])]["nest"]):
                self.scout = True
        self.object.x = self.x
        self.object.y = self.y

class Environment:
    def __init__(self, width, height, number_of_ants):
        self._width = width
        self._height = height

        self._running = True
        self.screen = pygame.display.set_mode((width, height), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.fake_screen = self.screen.copy()

        self.board = []
        for i in range(self._width*self._height):
            self.board.append({
                "id": i,
                "walkable": True,
                "nest": False,
                "food": False,
                "value": 0
            })

        ##
        self.nest = Nest(self)
        self.food = {}
        self.pheromones = []
        self.pheromones_to_clear = []
        self.ants = []
        ##

        for i in range(number_of_ants):
            self.ants.append(Ant(self, self.nest))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONUP and pygame.key.get_mods()&pygame.KMOD_CTRL:
            p = [0,0]
            pos = pygame.mouse.get_pos()
            p[0] = math.floor((pos[0]/self.screen.get_width())*self._width)
            p[1] = math.floor((pos[1]/self.screen.get_height())*self._height)
            points = pointsInCircle(p, 5)
            if (pygame.key.get_mods()&pygame.KMOD_ALT):
                for p in points:
                    Pheromone(self, 0.7, pos=p)
            else:
                for p in points:
                    Pheromone(self, -0.7, pos=p)
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
            pheromone.display()
        for food in self.food:
            self.food[food].display()
        self.nest.display()
        for ant in self.ants:
            ant.display()
    
    def handle_pheromones(self):
        self.pheromones_to_clear = []
        for pheromone in self.pheromones:
            if (pheromone.blur()):
                self.pheromones_to_clear.append(pheromone)
        for i in self.pheromones_to_clear:
            self.pheromones.remove(i)
    
    def handle_ants(self):
        for ant in self.ants:
            ant.move()


overlord = Environment(_width, _height, 350)

while overlord._running:
    overlord.resetWindow()

    debugDraw([50,50])

    for event in pygame.event.get():
        overlord.handle_event(event)

    overlord.handle_pheromones()
    overlord.handle_ants()
    overlord.display()
    overlord.screen.blit(pygame.transform.scale(overlord.fake_screen, overlord.screen.get_rect().size), (0,0))
    
    pygame.display.flip()

pygame.quit()

# game = Environment(_sSize[0], _sSize[1], 500)
