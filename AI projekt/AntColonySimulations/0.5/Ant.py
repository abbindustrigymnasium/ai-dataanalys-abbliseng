from Utils import pointsInCircle, fromArrayLocation, getArrayLocation, hsl2rgb, debugDraw, checkIfFood
from random import random, randint, randrange, choice
from MapPoint import MapPoint
import pygame

class Ant:

    TYPE_SEEKER = 0
    TYPE_FOLLOWER = 1
    TYPE_RETURNER = 2
    TYPE_RETURNER2 = 3

    MAX_TRIP = 450 # self.envir._width*2+self.envir._height

    PH_FOOD_MULTIPLIER = 5
    PH_FOOD_MULTIPLIER_LENGTH = 10

    # MAX_PH_DROP = 20.0
    MAX_PH_DROP = 5.0
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
            possible_target_points = [[self.x+1, self.y+1],[self.x-1, self.y+1],[self.x, self.y+1]]
        elif (self.dir == 1): # RIGHT
            possible_target_points = [[self.x+1, self.y],[self.x+1, self.y-1],[self.x+1, self.y+1]]
        elif (self.dir == 2): # DOWN
            possible_target_points = [[self.x+1, self.y-1],[self.x-1, self.y-1],[self.x, self.y-1]]
        elif (self.dir == 3): # LEFT
            possible_target_points = [[self.x-1, self.y],[self.x-1, self.y-1],[self.x-1, self.y+1]]
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
        
        if self.envir.map[getArrayLocation([self.x, self.y])].type == MapPoint.TYPE_NEST:
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

        if (self.type == Ant.TYPE_SEEKER or self.type == Ant.TYPE_FOLLOWER):
            if (self.x == 0 or self.x == self.envir._width or self.y == 0 or self.y == self.envir._height):
                self.type = Ant.TYPE_RETURNER2

        self.object.x = self.x
        self.object.y = self.y