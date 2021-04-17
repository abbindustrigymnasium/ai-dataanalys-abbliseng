import pygame
from pygame.locals import *
import math
from  random import choice, randrange, randint, random
import threading

pygame.init()
width = math.floor(1280/3)
height = math.floor(960/3)
zoom = 4.0
_sSize = [width, height]
relX = math.floor(width/2)
relY = math.floor(height/2)

## USEFUL FUNCTIONS (gonna be its own file eventually)
def forEveryPointInCircle(location, radius, func):
    # Calculate bounding rectangle
    upperX = location[0]-radius
    upperY = location[1]-radius
    w = radius+radius
    # Get circle points
    for x in range(w):
        x += upperX
        for y in range(w):
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
    w = radius+radius
    # Get circle points
    for x in range(w):
        x += upperX
        for y in range(w):
            y += upperY
            dx = x - location[0]
            dy = y - location[1]
            distanceSquared = dx*dx+dy*dy
            if (distanceSquared <= radius*radius):
                points.append([x,y])
    return points

def getArrayLocation(location, w=width):
    return location[1]*w+location[0]

def fromArrayLocation(location, w=width):
    return [location[1]%w, math.floor(location[0]/w)]

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
    def __init__(self, envir):
        self.x = math.floor(width/2)
        self.y = math.floor(height/2)
        self.object = pygame.Rect((relX-5, relY-5), (5, 5))
        self.tiles = []
        self.envir = envir
        for tile in pointsInCircle([self.x, self.y], 10):
            print(tile)
            envir.board[getArrayLocation(tile)]["nest"] = True
            self.tiles.append(pygame.Rect(fromArrayLocation(tile)[0], fromArrayLocation(tile)[1], 1, 1))

    def display(self):
        for tile in self.tiles:
            pygame.draw.rect(self.envir.fake_screen, (255, 0, 0), tile)

# class Ant():
#     def __init__(self, nest):
#         self.x = nest.x
#         self.y = nest.y
#         self.speed = randint(1,10)
#         self.freedom = random()
#         self.dir = randint(0,4)
#         self.viewdist = randint(5,10)
#         self.object = pygame.Rect(self.x, self.y, 1, 1)
#         self.scout = not True
#         # Other things like freedom, speed and stuff
#     def checkIfYummy(self):
#         if (gameArray[getArrayLocation([self.x, self.y], width)]["food"])
    
#     def getTarget(self):
#         possible_options = pointsInCircle([self.x, self.y], self.viewdist)
#         possiblier_options = {}
#         for might_be_possiblier in possible_options:
#             if (getArrayLocation(might_be_possiblier, width) > 0 and getArrayLocation(might_be_possiblier, width) < width*height-1):
#                 possiblier_options[might_be_possiblier] = gameArray[might_be_possiblier]["pheromone"]
#         target = max(possiblier_options, key=lambda x: possiblier_options[x])
#         if (random()<=self.freedom):
#             target = choice(possiblier_options)
#         return target
    
#     def Move(self):
#         target = fromArrayLocation(self.getTarget(), width)

#         # a = self.getMovement()
#         # target = fromArrayLocation(a, width)
#         # if (gameArray[a]["food"] != None):
#         #     print("Yum yummy!")
#         # # debugDraw(target)

#         if (self.x < target[0]):
#             self.x += 1
#         elif (self.x > target[0]):
#             self.x -= 1
#         if (self.y < target[1]):
#             self.y += 1
#         elif (self.y > target[1]):
#             self.y -= 1

#         self.object.x = self.x
#         self.object.y = self.y

#         self.checkIfYummy()

# class Pheromone():
#     def __init__(self, ant, scout, strength=0.7):
#         self.x = ant.x
#         self.y = ant.y
#         self.strength = strength
#         self.age = 0
#         self.id = getArrayLocation([self.x, self.y], width)
#         self.object = pygame.Rect(self.x, self.y, 1, 1)
#         self.red = scout
#         # if (self.red):
#         #     gameArray[getArrayLocation([self.x, self.y], width)]["pheromone"]["blue"] = self.strength
#         # else:
#         #     gameArray[getArrayLocation([self.x, self.y], width)]["pheromone"]["blue"] = -self.strength
    
#     def blur(self):
#         # value = gameArray[getArrayLocation([self.x, self.y], width)]["pheromone"]["blue"]
#         # if (self.red):
#         #     x = value - 0.05
#         # else:
#         #     x = value + 0.05
#         # gameArray[getArrayLocation([self.x, self.y], width)]["pheromone"]["blue"] = x
#         pass
    
#     def delete(self):
#         # x = gameArray[getArrayLocation([self.x, self.y], width)]["pheromone"]["blue"]
#         # if (x > 0 and not self.red):
#         #     gameArray[getArrayLocation([self.x, self.y], width)]["pheromone"]["blue"] = 0
#         #     # game.pheromones.pop(self.id)
#         #     return True
#         # elif (x < 0 and self.red):
#         #     gameArray[getArrayLocation([self.x, self.y], width)]["pheromone"]["blue"] = 0
#         #     return True
#         #     # Delete the pheromone instance
#         # return False
#         pass

class Food:
    def __init__(self, pos):
        # self.x = pos[0]
        # self.y = pos[1]
        # self.object = pygame.Rect(self.x,self.y,1,1)
        # game.food.append(getArrayLocation(pos, width))
        # gameArray[getArrayLocation(pos, width)]["food"] = True
        pass

class Environment():
    def __init__(self, width, height, number_of_ants):

        self._width = width
        self._height = height

        self._running = True

        self.screen = pygame.display.set_mode((width, height), HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.fake_screen = self.screen.copy()
        
        self.board = []
        for i in range(self._width*self._height):
            # print(i)
            self.board.append({"ants": None, "value": 0, "food": None, "walkable": True, "nest": False})
        pygame.display.set_caption("Ant Boi Sim")
        self.clock = pygame.time.Clock()

        self.resetWindow()

        self.nest = Nest(self)
        # self.pheromones = {}
        # self.food = []

        # self.number_of_ants = number_of_ants
        # self.ants = []
        # for i in range(number_of_ants):
        #     self.ants.append(Ant(self.nest))

    def resetWindow(self):
        # self.screen.fill((78, 42, 42))
        self.screen.fill((255, 255, 255))
        self.fake_screen.fill((255, 255, 255))
        pass
    
    def display(self):
        pass
        # for pheromone in self.pheromones:
        #     if (not self.pheromones[pheromone].red):
        #         b = 1-gameArray[getArrayLocation([self.pheromones[pheromone].x, self.pheromones[pheromone].y], width)]["pheromone"]["blue"]*-1
        #         pygame.draw.rect(self.fake_screen, hsl2rgb(222, 63, 100*b), self.pheromones[pheromone].object)
        #     else:
        #         b = 1-gameArray[getArrayLocation([self.pheromones[pheromone].x, self.pheromones[pheromone].y], width)]["pheromone"]["blue"]
        #         pygame.draw.rect(self.fake_screen, hsl2rgb(13, 100, 100*b), self.pheromones[pheromone].object)
        #     self.pheromones[pheromone].blur()
        # for f in self.food:
        #     pygame.draw.rect(self.fake_screen, (0, 255, 0), gameArray[f]["food"].object)
        # for ant in self.ants:
        #     pygame.draw.rect(self.fake_screen, (0,0,0), ant.object)
        # pygame.draw.rect(self.fake_screen, (255,0,0), self.nest.object)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            # forEveryPointInCircle(pos, 10, Food)
        elif event.type == VIDEORESIZE:
            self.screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)

## VARS
# _sSize = [1280, 960]

# gameArray = []
# for i in range(_sSize[0]*_sSize[1]):
#     gameArray.append({"ants": None, "pheromone": 0, "food": None, "walkable": True, "nest": False})

game = Environment(_sSize[0], _sSize[1], 500)

## MAIN
while game._running:
    game.resetWindow()
    game.nest.display()
    # for ant in game.ants:
    #     ant.Move()
        # pass¨
    # to_clear = []
    # for pheromone in game.pheromones:
    #     if game.pheromones[pheromone].delete():
    #         to_clear.append(pheromone)
    # for val in to_clear:
    #     game.pheromones.pop(val)

    for event in pygame.event.get():
        game.handle_event(event)
    # "Flip the display" - (update the whole screen)

    game.display()
    game.screen.blit(pygame.transform.scale(game.fake_screen, game.screen.get_rect().size), (0,0))

    pygame.display.flip()

# Done! Time to quit.
pygame.quit()