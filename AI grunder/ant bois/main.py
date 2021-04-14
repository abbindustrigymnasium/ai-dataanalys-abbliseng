import pygame
import math
from  random import choice, randrange, randint, random

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

def pointsInCircle(location, radius, index=False):
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
                # if index:
                #     points.append(getArrayLocation([x,y], width))
                # else:
                points.append([x,y])
    return points

def getArrayLocation(location, width):
    return location[1]*width+location[0]

def fromArrayLocation(location, width):
    return [location%width, math.floor(location/width)]

def debugDraw(pos):
    pygame.draw.circle(game.screen, (0, 255, 0), (pos[0], pos[1]), 1)

## CLASSES

class Nest():
    def __init__(self):
        self.xpos = math.floor(width/2)
        self.ypos = math.floor(height/2)
        self.object = pygame.Rect((relX-5, relY-5), (10, 10))    

class Ant():
    def __init__(self, nest):
        self.xpos = nest.xpos
        self.ypos = nest.ypos
        self.speed = randint(1,10)
        self.freedom = random()
        self.object = pygame.Rect(self.xpos, self.ypos, 2, 2)
        # Other things like freedom, speed and stuff
    
    def getMovement(self):
        pheromoneArray = {}
        optionsA = pointsInCircle([self.xpos, self.ypos], 15, True)
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
            pheromoneValue += gameArray[option]["pheromone"]["red"]
            pheromoneArray[option] = pheromoneValue
        bestOption = max(pheromoneArray, key = lambda k: pheromoneArray[k])
        # print(bestOption, ":", pheromoneArray)
        if pheromoneArray[bestOption] == 0:
            bestOption = choice(options)
        game.pheromones.append(Pheromone(self))
        return bestOption
        # return 0
    
    def Move(self):
        a = self.getMovement()
        target = fromArrayLocation(a, width)
        # debugDraw(target)
        # pygame.draw.circle(game.screen, (0, 255, 0), (target[0], target[1]), 1)

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
    def __init__(self, ant, strength=0.05):
        self.xpos = ant.xpos
        self.ypos = ant.ypos
        self.strength = strength
        self.age = 0
        self.object = pygame.Rect(self.xpos, self.ypos, 1, 1)
        gameArray[getArrayLocation([self.xpos, self.ypos], width)]["pheromone"]["blue"] -= self.strength
        if (gameArray[getArrayLocation([self.xpos, self.ypos], width)]["pheromone"]["blue"] < -1):
            gameArray[getArrayLocation([self.xpos, self.ypos], width)]["pheromone"]["blue"] = -1
        # self.strength = 1.0

class Environment():
    def __init__(self, width, height, number_of_ants):

        self._width = width
        self._height = height

        self._running = True
        self.screen = pygame.display.set_mode([width, height])
        self.resetWindow()

        self.nest = Nest()
        self.pheromones = []
        self.number_of_ants = number_of_ants
        self.ants = []
        for i in range(number_of_ants):
            self.ants.append(Ant(self.nest))

    def resetWindow(self):
        # self.screen.fill((78, 42, 42))
        self.screen.fill((255, 255, 255))
    
    def display(self):
        pygame.draw.rect(self.screen, (255,0,0), self.nest.object)
        for ant in self.ants:
            pygame.draw.rect(self.screen, (0,0,0), ant.object)
        for pheromone in self.pheromones:
            s = gameArray[getArrayLocation([pheromone.xpos, pheromone.ypos], width)]["pheromone"]["blue"]*-1
            pygame.draw.rect(self.screen, (0,0,math.floor(255*s)), pheromone.object)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

## VARS
pygame.init()
width = math.floor(1280/4)
height = math.floor(960/4)
_sSize = [width, height]
relX = math.floor(width/2)
relY = math.floor(height/2)
# _sSize = [1280, 960]

gameArray = []
for i in range(_sSize[0]*_sSize[1]):
    gameArray.append({"ants":[], "pheromone": {"blue": 0, "red": 0}, "food": [], "walkable": True})

game = Environment(_sSize[0], _sSize[1], 10)
# for ant in game.ants:
#     ant.Move()
#     pass

# gameArray[math.floor(len(gameArray)/2)]["pheromone"] = 100

## MAIN
while game._running:
    game.resetWindow()
    for ant in game.ants:
        ant.Move()
        # pass

    game.display()

    for event in pygame.event.get():
        game.handle_event(event)
    # "Flip the display" - (update the whole screen)
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()