import pygame
from pygame.locals import *
import math
from  random import choice, randrange, randint, random
import threading

pygame.init()

# _width = math.floor(1280/3)
# _height = math.floor(960/3)
_width = math.floor(1920/15)
_height = math.floor(1080/15)
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

def checkIfFood(self, possible_target_point):
    if (getArrayLocation(possible_target_point) < 0 or getArrayLocation(possible_target_point) > (self.envir._height*self.envir._width)-1):
        return False
    else:
        if (self.envir.map[getArrayLocation(possible_target_point)].type == MapPoint.TYPE_FOOD):
            target = possible_target_point
            return True
    return False

class Nest:
    def __init__(self, envir):
        self.x = relX
        self.y = relY
        self.envir = envir
        self.tiles = [] 
        for tile in pointsInCircle([self.x, self.y], 1):
            self.tiles.append(pygame.Rect(tile[0], tile[1], 1, 1))
            self.envir.map[getArrayLocation([tile[0], tile[1]])].type = MapPoint.TYPE_NEST
    def display(self):
        for tile in self.tiles:
            pygame.draw.rect(self.envir.fake_screen, (255,0,0), tile)

class Food:
    def __init__(self, envir, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.envir = envir
        self.object = pygame.Rect(self.x, self.y, 1, 1)
        self.envir.map[getArrayLocation([self.x, self.y])].type = MapPoint.TYPE_FOOD
    def display(self):
        pygame.draw.rect(self.envir.fake_screen, (0, 255, 0), self.object)

class Ant:

    TYPE_SEEKER = 0
    TYPE_FOLLOWER = 1
    TYPE_RETURNER = 2
    TYPE_RETURNER2 = 3

    MAX_TRIP = 450 # self.envir._width*2+self.envir._height

    PH_FOOD_MULTIPLIER = 5
    PH_FOOD_MULTIPLIER_LENGTH = 10

    MAX_PH_DROP = 20.0
    MIN_PH_DROP = 0.0

    SIDE_DROP = 2

    def __init__(self, envir, nest, t):
        self.x = nest.x
        self.y = nest.y
        self.type = t
        self.move_hist = []
        self.dir = randint(0,3) # 0-3
        self.envir = envir
        self.object = pygame.Rect(self.x, self.y, 1, 1)
        self.viewdist = 5
        self.freedom = randint(0,6)/10
        self.scout = True
        self.ph_increase = Ant.MAX_PH_DROP
        self.follower_to_seeker = self.ph_increase/10
        self.seeker_prob = round(MapPoint.MAX_CONCENTRATION+MapPoint.MAX_CONCENTRATION*0.05)
    def display(self):
        pygame.draw.rect(self.envir.fake_screen, (0, 0, 0), self.object)
    def pheromoneDrop(self, mapPoint, dirX, dirY):
        if (Ant.MAX_TRIP-len(self.move_hist) < Ant.PH_FOOD_MULTIPLIER_LENGTH):
            ph_inc = self.ph_increase * Ant.PH_FOOD_MULTIPLIER
            ph_inc_side = self.ph_increase * Ant.PH_FOOD_MULTIPLIER / Ant.SIDE_DROP
        else:
            ph_inc = self.ph_increase
            ph_inc_side = self.ph_increase/Ant.SIDE_DROP
        mapPoint.pheromoneIncrease(ph_inc)
        self.envir.pheromones.append((self.x, self.y))
        if (abs(dirX) <= 1 and abs(dirY) <= 1):
            for i in range(-1,2):
                for j in range(-1,2):
                    if (i==0 and j==0):
                        continue
                    if (getArrayLocation([self.x+i,self.y+j]) < 0 or getArrayLocation([self.x+i,self.y+j]) > self.envir._width*self.envir._height-1):
                        continue
                    self.envir.map[getArrayLocation([self.x+i,self.y+j])].pheromoneIncrease(ph_inc_side)
                    self.envir.pheromones.append((self.x+i, self.y+j))
    def findSeekerTarger(self):
        if self.dir >= 4:
            self.dir = 0
        elif self.dir <= -1:
            self.dir = 3
        possible_target_points = []
        if (self.dir == 0): # UP
            possible_target_points = [[self.x+1, self.y],[self.x-1, self.y],[self.x, self.y+1]]
        elif (self.dir == 1): # RIGHT
            possible_target_points = [[self.x+1, self.y],[self.x, self.y-1],[self.x, self.y+1]]
        elif (self.dir == 2): # DOWN
            possible_target_points = [[self.x+1, self.y],[self.x-1, self.y],[self.x, self.y-1]]
        elif (self.dir == 3): # LEFT
            possible_target_points = [[self.x-1, self.y],[self.x, self.y-1],[self.x, self.y+1]]
        if (randint(0,100) == randint(0,100)):
            self.dir += randint(-1,1)
        self.move_hist.append([self.x, self.y])
        target = choice(possible_target_points)
        for possible_target_point in possible_target_points:
            if (checkIfFood(self, possible_target_point)):
                break
        while (getArrayLocation(target) <= 0 or getArrayLocation(target) > (self.envir._height*self.envir._width)-1):
            self.dir += 2
            target = self.findSeekerTarger()
        return target
    def findReturnerTarget(self):
        if (len(self.move_hist) > 0):
            target = self.move_hist[-1]
            self.move_hist.pop(-1)
        else:
            target = [self.x,self.y]
        return target
    def findFollowerTarget(self):
        n = 0
        phSum = 0
        norm = 0
        possible_target_points = []
        intervall = []
        Random = randint(0,101)
        target = [0,0]
        for dx in range(-1,2):
            for dy in range(-1,2):
                if (dx == 0 and dy == 0):
                    continue
                if (checkIfFood(self, [self.x+dx, self.y+dy])):
                    return [self.x+dx, self.y+dy]
        for dx in range(-1,2):
            for dy in range(-1,2):
                if (dx == 0 and dy == 0):
                    continue
                if (self.envir.hiveDist(self.x, self.y)<=self.envir.hiveDist(self.x+dx, self.y+dy) and self.envir.map[getArrayLocation([self.x+dx, self.y+dy])].pheromone_concentration > 0 and getArrayLocation([self.x+dx, self.y+dy])>0 and getArrayLocation([self.x+dx, self.y+dy])<self.envir._width*self.envir._height-1):
                    possible_target_points.append([self.x+dx, self.y+dy])
                    phSum += self.envir.map[getArrayLocation([self.x+dx, self.y+dy])].pheromone_concentration**2
                    norm += (self.envir.map[getArrayLocation([self.x+dx, self.y+dy])].pheromone_concentration*self.envir.hiveDist(self.x+dx, self.y+dy))**2
                    n += 1
        if (phSum<self.follower_to_seeker or n==0):
            self.type = Ant.TYPE_SEEKER
        else:
            # print(possible_target_points[0][0])
            intervall.append((self.envir.map[getArrayLocation(possible_target_points[0])].pheromone_concentration*(100/norm)*self.envir.hiveDist(possible_target_points[0][0],possible_target_points[0][1]))**2)
            for i in range(1, n):
                intervall.append(intervall[i-1]+(self.envir.map[getArrayLocation(possible_target_points[i])].pheromone_concentration*(100/norm)*self.envir.hiveDist(possible_target_points[i][0],possible_target_points[i][1]))**2)
            for i in range(n):
                if (Random<=intervall[i]):
                    target = self.envir.map[getArrayLocation(possible_target_points[i])].pos
        self.move_hist.append([self.x, self.y])
        return target


    def move(self):
        if (self.type == Ant.TYPE_SEEKER):
            target = self.findSeekerTarger()
            if (len(self.move_hist) >= Ant.MAX_TRIP):
                self.type = Ant.TYPE_RETURNER2
        elif (self.type == Ant.TYPE_RETURNER or self.type == Ant.TYPE_RETURNER2):
            target = self.findReturnerTarget()
            if (self.type == Ant.TYPE_RETURNER):
                dirX = target[0]-self.x
                dirY = target[1]-self.y
                self.pheromoneDrop(self.envir.map[getArrayLocation([self.x, self.y])], dirX, dirY)
        elif (self.type == Ant.TYPE_FOLLOWER):
            target = self.findFollowerTarget()
            if (len(self.move_hist) >= Ant.MAX_TRIP):
                self.type = Ant.TYPE_RETURNER2
            # target = [self.x, self.y]

        if (self.x < target[0]):
            self.x += 1
        elif (self.x > target[0]):
            self.x -= 1
        if (self.y < target[1]):
            self.y += 1
        elif (self.y > target[1]):
            self.y -= 1
        
        # if(self.type == Ant.TYPE_RETURNER or self.type == Ant.TYPE_RETURNER2):
        if self.envir.map[getArrayLocation([self.x, self.y])].type == MapPoint.TYPE_NEST:
            # self.type = Ant.TYPE_SEEKER
            rnd = randint(0, self.seeker_prob)
            for dx in range(-1,2):
                for dy in range(-1,2):
                    if (dx == 0 and dy == 0):
                        continue
                    if (round(self.envir.map[getArrayLocation([self.x, self.y])].pheromone_concentration > rnd)):
                        self.type = Ant.TYPE_FOLLOWER
                        break
            if (self.type != Ant.TYPE_FOLLOWER):
                self.type = Ant.TYPE_SEEKER
        elif self.envir.map[getArrayLocation([self.x, self.y])].type == MapPoint.TYPE_FOOD:
            self.envir.map[getArrayLocation([self.x, self.y])].type = MapPoint.TYPE_EMPTY
            del self.envir.food[getArrayLocation([self.x, self.y])]
            self.type = Ant.TYPE_RETURNER

        self.object.x = self.x
        self.object.y = self.y

class MapPoint:

    TYPE_EMPTY = 0
    TYPE_FOOD = 1
    TYPE_NEST = 2
    TYPE_OBSTACLE = 3

    MAX_CONCENTRATION = 100.0

    def __init__(self, position, t):
        self.type = t
        self.pos = position
        self.decay_constant = 0.006
        self.pheromone_concentration = 0

    def pheromoneDecay(self, envir, pos):
        self.pheromone_concentration = (1-self.decay_constant)*self.pheromone_concentration
        if (self.pheromone_concentration <= 0.01):
            i = envir.pheromones.index(pos)
            envir.pheromones.pop(i)
            
    def pheromoneIncrease(self, val):
        if (self.type != MapPoint.TYPE_OBSTACLE):
            self.pheromone_concentration += val
            if (self.pheromone_concentration > MapPoint.MAX_CONCENTRATION):
                self.pheromone_concentration = MapPoint.MAX_CONCENTRATION

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