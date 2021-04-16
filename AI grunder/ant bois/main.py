import pygame
from pygame.locals import *
import math
from  random import choice, randrange, randint, random
import threading

## USEFUL FUNCTIONS (gonna be its own file eventually)
def forEveryPointInCircle(location, radius, func):
    # Calculate bounding rectangle
    upperX = location[0]-radius
    upperY = location[1]-radius
    width = radius+radius
    # Get circle points
    for x in range(width):
        x += upperX
        for y in range(width):
            y += upperY
            dx = x - location[0]
            dy = y - location[1]
            distanceSquared = dx*dx+dy*dy
            if (distanceSquared <= radius*radius):
                func([x,y])
    return None

def pointsInCircle(location, radius):
    points = []
    # Calculate bounding rectangle
    upperX = location[0]-radius
    upperY = location[1]-radius
    width = radius+radius
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

def getArrayLocation(location, width):
    return location[1]*width+location[0]

def fromArrayLocation(location, width):
    return [location%width, math.floor(location/width)]

def debugDraw(pos):
    pygame.draw.circle(game.screen, (0, 255, 0), (pos[0], pos[1]), 1)

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

## CLASSES

class Nest():
    def __init__(self):
        self.xpos = math.floor(width/2)
        self.ypos = math.floor(height/2)
        self.object = pygame.Rect((relX-5, relY-5), (5, 5))

class Ant():
    def __init__(self, nest):
        self.xpos = nest.xpos
        self.ypos = nest.ypos
        self.speed = randint(1,10)
        self.freedom = random()
        self.dir = randint(0,4)
        self.viewdist = randint(5,10)
        self.object = pygame.Rect(self.xpos, self.ypos, 1, 1)
        self.scout = True
        # Other things like freedom, speed and stuff
    
    def getMovement(self):
        pheromoneArray = {}
        optionsA = pointsInCircle([self.xpos, self.ypos], self.viewdist)
        options = []
        # forEveryPointInCircle([self.xpos, self.ypos], 40, debugDraw)
        for option in optionsA:
            p = getArrayLocation(option, width)
            if (p > 0 and p < width*height-1):
                options.append(getArrayLocation(option, width))
        # print(options)
        if (randint(0,10)<=self.freedom*10):
            return choice(options)
        for option in options:
            pheromoneValue = gameArray[option]["pheromone"]["blue"]
            pheromoneArray[option] = pheromoneValue
        bestOption = max(pheromoneArray, key = lambda k: pheromoneArray[k])
        if pheromoneArray[bestOption] == 0:
            bestOption = choice(options)
        # print(getArrayLocation([self.xpos, self.ypos], width))
        game.pheromones[getArrayLocation([self.xpos, self.ypos], width)] = Pheromone(self, self.scout)
        return bestOption
    
    def Move(self):
        a = self.getMovement()
        target = fromArrayLocation(a, width)
        # debugDraw(target)

        if (self.xpos < target[0]):
            self.xpos += 1
        elif (self.xpos > target[0]):
            self.xpos -= 1
        if (self.ypos < target[1]):
            self.ypos += 1
        elif (self.ypos > target[1]):
            self.ypos -= 1

        self.object.x = self.xpos
        self.object.y = self.ypos


class Pheromone():
    def __init__(self, ant, scout, strength=0.7):
        self.xpos = ant.xpos
        self.ypos = ant.ypos
        self.strength = strength
        self.age = 0
        self.id = getArrayLocation([self.xpos, self.ypos], width)
        self.object = pygame.Rect(self.xpos, self.ypos, 1, 1)
        self.red = scout
        if (self.red):
            gameArray[getArrayLocation([self.xpos, self.ypos], width)]["pheromone"]["blue"] = self.strength
        else:
            gameArray[getArrayLocation([self.xpos, self.ypos], width)]["pheromone"]["blue"] = -self.strength
    
    def blur(self):
        value = gameArray[getArrayLocation([self.xpos, self.ypos], width)]["pheromone"]["blue"]
        if (self.red):
            x = value - 0.05
        else:
            x = value + 0.05
        gameArray[getArrayLocation([self.xpos, self.ypos], width)]["pheromone"]["blue"] = x
    
    def delete(self):
        x = gameArray[getArrayLocation([self.xpos, self.ypos], width)]["pheromone"]["blue"]
        if (x > 0 and not self.red):
            gameArray[getArrayLocation([self.xpos, self.ypos], width)]["pheromone"]["blue"] = 0
            # game.pheromones.pop(self.id)
            return True
        elif (x < 0 and self.red):
            gameArray[getArrayLocation([self.xpos, self.ypos], width)]["pheromone"]["blue"] = 0
            return True
            # Delete the pheromone instance
        return False


class Environment():
    def __init__(self, width, height, number_of_ants):

        self._width = width
        self._height = height

        self._running = True

        self.screen = pygame.display.set_mode((width, height), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.fake_screen = self.screen.copy()

        pygame.display.set_caption("Ant Boi Sim")
        self.clock = pygame.time.Clock()

        self.resetWindow()

        self.nest = Nest()
        self.pheromones = {}
        self.number_of_ants = number_of_ants
        self.ants = []
        for i in range(number_of_ants):
            self.ants.append(Ant(self.nest))

    def resetWindow(self):
        # self.screen.fill((78, 42, 42))
        self.screen.fill((255, 255, 255))
        self.fake_screen.fill((255, 255, 255))
        pass
    
    def display(self):
        for pheromone in self.pheromones:
            if (not self.pheromones[pheromone].red):
                b = 1-gameArray[getArrayLocation([self.pheromones[pheromone].xpos, self.pheromones[pheromone].ypos], width)]["pheromone"]["blue"]*-1
                pygame.draw.rect(self.fake_screen, hsl2rgb(222, 63, 100*b), self.pheromones[pheromone].object)
            else:
                b = 1-gameArray[getArrayLocation([self.pheromones[pheromone].xpos, self.pheromones[pheromone].ypos], width)]["pheromone"]["blue"]
                pygame.draw.rect(self.fake_screen, hsl2rgb(13, 100, 100*b), self.pheromones[pheromone].object)
            self.pheromones[pheromone].blur()
        for ant in self.ants:
            pygame.draw.rect(self.fake_screen, (0,0,0), ant.object)
        pygame.draw.rect(self.fake_screen, (255,0,0), self.nest.object)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
        elif event.type == VIDEORESIZE:
            self.screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)

## VARS
pygame.init()
width = math.floor(1280/3)
height = math.floor(960/3)
zoom = 4.0
_sSize = [width, height]
relX = math.floor(width/2)
relY = math.floor(height/2)
# _sSize = [1280, 960]

gameArray = []
for i in range(_sSize[0]*_sSize[1]):
    gameArray.append({"ants":[], "pheromone": {"blue": 0, "red": 0}, "food": [], "walkable": True})

game = Environment(_sSize[0], _sSize[1], 500)

## MAIN
while game._running:
    game.resetWindow()
    for ant in game.ants:
        ant.Move()
        # pass¨
    to_clear = []
    for pheromone in game.pheromones:
        if game.pheromones[pheromone].delete():
            to_clear.append(pheromone)
    for val in to_clear:
        game.pheromones.pop(val)

    for event in pygame.event.get():
        game.handle_event(event)
    # "Flip the display" - (update the whole screen)

    game.display()
    game.screen.blit(pygame.transform.scale(game.fake_screen, game.screen.get_rect().size), (0,0))

    pygame.display.flip()

# Done! Time to quit.
pygame.quit()