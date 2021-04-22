from Utils import *
from random import random, randint, randrange, choice
from MapPoint import MapPoint
import pygame
import  math

class Ant:

    TYPE_SEEKER = 0
    TYPE_FOLLOWER = 1
    TYPE_RETURNER = 2
    TYPE_RETURNER2 = 3

    MAX_TRIP = 450 # self.envir._width*2+self.envir._height

    PH_FOOD_MULTIPLIER = 5
    PH_FOOD_MULTIPLIER_LENGTH = 10

    MAX_PH_DROP = 20.0
    STD_PH_DROP = 5.0
    MIN_PH_DROP = 0.0

    SIDE_DROP = 2

    def __init__(self, envir, nest, t, i = None):
        self.id = i
        self.x = nest.x
        self.y = nest.y
        self.type = t
        self.move_hist = []
        self.dir = randint(0,7) # 0-7
        self.envir = envir
        self.object = pygame.Rect(self.x, self.y, 1, 1)
        self.viewdist = 5
        self.is_carrying = False
        self.freedom = randint(0,10)/10
        self.scout = True
        self.ph_increase = Ant.STD_PH_DROP
        self.follower_to_seeker = self.ph_increase/10
        self.seeker_prob = round(MapPoint.MAX_CONCENTRATION+MapPoint.MAX_CONCENTRATION*0.05)

    def display(self):
        if (self.id != None):
            pygame.draw.rect(self.envir.fake_screen, (201, 42, 42), self.object)
        elif (self.type == Ant.TYPE_RETURNER):
            pygame.draw.rect(self.envir.fake_screen, (47, 168, 47), self.object)
        elif (self.type == Ant.TYPE_FOLLOWER):
            pygame.draw.rect(self.envir.fake_screen, (235, 147, 52), self.object)
        else:
            # pygame.draw.rect(self.envir.fake_screen, (0, 0, 0), self.object)
            pygame.draw.rect(self.envir.fake_screen, (255, 255, 255), self.object)

    def pheromoneDrop(self, mapPoint, dirX, dirY):
        if (Ant.MAX_TRIP-len(self.move_hist) < Ant.PH_FOOD_MULTIPLIER_LENGTH):
            ph_inc = self.ph_increase * Ant.PH_FOOD_MULTIPLIER
            ph_inc_side = self.ph_increase * Ant.PH_FOOD_MULTIPLIER / Ant.SIDE_DROP
        else:
            ph_inc = self.ph_increase
            ph_inc_side = self.ph_increase/Ant.SIDE_DROP
        mapPoint.pheromoneIncrease(ph_inc)
        # self.envir.pheromones.append((self.x, self.y))
        if (abs(dirX) <= 1 and abs(dirY) <= 1):
            for i in range(-1,2):
                for j in range(-1,2):
                    if (i==0 and j==0):
                        continue
                    if (getArrayLocation([self.x+i,self.y+j]) < 0 or getArrayLocation([self.x+i,self.y+j]) > self.envir._width*self.envir._height-1):
                        continue
                    self.envir.map[getArrayLocation([self.x+i,self.y+j])].pheromoneIncrease(ph_inc_side)
                    # self.envir.pheromones.append((self.x+i, self.y+j))

    def checkForSurrondingFood(self):
        # Might be better to append points to list and then randomize so if multiple choices it is random
        for dx in range(-1,2):
            for dy in range(-1,2):
                p = [self.x+dx, self.y+dy]
                if ((dx == 0 and dy == 0)):
                    continue
                elif ((getArrayLocation(p) < 0 or getArrayLocation(p) > getWidth()*getHeight()-1)):
                    return "EDGE"
                if (checkIfFood(self, p)):
                    return p
        return False

    def findSeekerTarger(self):
        target = self.checkForSurrondingFood()
        if (target == "EDGE"):
            self.type = Ant.TYPE_RETURNER2
            return [self.x, self.y]
        elif (target):
            self.move_hist.append([self.x, self.y])
            return target
        # Correct directions
        if self.dir >= 8:
            self.dir = 0
        elif self.dir <= -1:
            self.dir = 7
        # Get possible targets depending on direction
        possible_target_points = []
        surrounding_points = []
        for dx in range(-1,2):
            for dy in range(-1,2):
                p = [self.x+dx, self.y+dy]
                if ((dx == 0 and dy == 0) or (getArrayLocation(p) < 0 or getArrayLocation(p) > getWidth()*getHeight()-1)):
                    continue
                surrounding_points.append(p)
        if (self.dir == 0): # UP
            possible_target_points = [
                surrounding_points[0],
                surrounding_points[3],
                surrounding_points[5]
            ]
        elif (self.dir == 1): # UP-RIGHT
            possible_target_points = [
                surrounding_points[3],
                surrounding_points[5],
                surrounding_points[6]
            ]
        elif (self.dir == 2): # RIGHT
            possible_target_points = [
                surrounding_points[5],
                surrounding_points[6],
                surrounding_points[7]
            ]
        elif (self.dir == 3): # DOWN-RIGHT
            possible_target_points = [
                surrounding_points[6],
                surrounding_points[7],
                surrounding_points[4]
            ]
        elif (self.dir == 4): # DOWN
            possible_target_points = [
                surrounding_points[7],
                surrounding_points[4],
                surrounding_points[2]
            ]
        elif (self.dir == 5): # DOWN-LEFT
            possible_target_points = [
                surrounding_points[4],
                surrounding_points[2],
                surrounding_points[1]
            ]
        elif (self.dir == 6): # LEFT
            possible_target_points = [
                surrounding_points[2],
                surrounding_points[1],
                surrounding_points[0]
            ]
        elif (self.dir == 7): # UP-LEFT
            possible_target_points = [
                surrounding_points[1],
                surrounding_points[0],
                surrounding_points[3]
            ]

        if (randint(0,100) == randint(0,100)):
            self.dir += randint(-1,1)
        # Randomly select a target from possible points
        target = choice(possible_target_points)
        # Append current pos to move history
        self.move_hist.append([self.x, self.y])
        return target
    def findReturnerTarget(self):
        # Go to lastest position according to move hist and remove that element.
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
        Random = random()
        target = [0,0]
        # Check if any of surronding has food
        for dx in range(-1,2):
            for dy in range(-1,2):
                if (dx == 0 and dy == 0):
                    continue
                if (checkIfFood(self, [self.x+dx, self.y+dy])):
                    return [self.x+dx, self.y+dy]
        # Get possible targets with a pheromone concentration over 1
        for dx in range(-1,2):
            for dy in range(-1,2):
                if (dx == 0 and dy == 0):
                    continue
                # Check if invalid position
                if (getArrayLocation([self.x+dx, self.y+dy]) < 0 or getArrayLocation([self.x+dx, self.y+dy]) > getWidth()*getHeight()-1):
                    continue
                # Check if further from the nest and if has pheromone > 1
                if (self.envir.hiveDist(self.x, self.y)<=self.envir.hiveDist(self.x+dx, self.y+dy) and self.envir.map[getArrayLocation([self.x+dx, self.y+dy])].pheromone_concentration > 0):
                    possible_target_points.append([self.x+dx, self.y+dy])
                    phSum += self.envir.map[getArrayLocation([self.x+dx, self.y+dy])].pheromone_concentration**2
                    norm += (self.envir.map[getArrayLocation([self.x+dx, self.y+dy])].pheromone_concentration*self.envir.hiveDist(self.x+dx, self.y+dy))**2
                    n += 1
        # If no possible targets switch to seeker type
        if (phSum<self.follower_to_seeker or n==0):
            self.type = Ant.TYPE_SEEKER
        else:
            intervall.append((self.envir.map[getArrayLocation(possible_target_points[0])].pheromone_concentration*(100/norm)*self.envir.hiveDist(possible_target_points[0][0],possible_target_points[0][1]))**2)
            for i in range(1, n):
                intervall.append(intervall[i-1]+(self.envir.map[getArrayLocation(possible_target_points[i])].pheromone_concentration*(100/norm)*self.envir.hiveDist(possible_target_points[i][0],possible_target_points[i][1]))**2)
            for i in range(n):
                if (Random<=intervall[i]):
                    target = self.envir.map[getArrayLocation(possible_target_points[i])].pos
                    break
            # Check if the random function has failed and pick a random possible target instead
            if target == [0,0]:
                target = choice(possible_target_points)
        self.move_hist.append([self.x, self.y])
        return target


    def move(self):
        # Depending on type find accurate target
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
        # Calculate the new pos
        if (self.x < target[0]):
            self.x += 1
        elif (self.x > target[0]):
            self.x -= 1
        if (self.y < target[1]):
            self.y += 1
        elif (self.y > target[1]):
            self.y -= 1
        # Do other things that are specific to certain tiles
        if self.envir.map[getArrayLocation([self.x, self.y])].type == MapPoint.TYPE_NEST:
            if (self.type == Ant.TYPE_RETURNER and self.is_carrying):
                self.is_carrying = False
            # Random chance to become a follower
            rnd = randint(0, self.seeker_prob)
            for dx in range(-1,2):
                for dy in range(-1,2):
                    if (dx == 0 and dy == 0):
                        continue
                    # print(round(self.envir.map[getArrayLocation([self.x+dx, self.y+dy])].pheromone_concentration),":",rnd,":",round(self.envir.map[getArrayLocation([self.x+dx, self.y+dy])].pheromone_concentration) > rnd)
                    if (round(self.envir.map[getArrayLocation([self.x+dx, self.y+dy])].pheromone_concentration) > rnd):
                        self.type = Ant.TYPE_FOLLOWER
                        break
            # Otherwise become a seeker
            if (self.type != Ant.TYPE_FOLLOWER):
                self.type = Ant.TYPE_SEEKER
        # If food is found return home with it and leave trail
        elif self.envir.map[getArrayLocation([self.x, self.y])].type == MapPoint.TYPE_FOOD and self.type != Ant.TYPE_RETURNER:
            self.is_carrying = True
            self.envir.map[getArrayLocation([self.x, self.y])].type = MapPoint.TYPE_EMPTY
            try:
                del self.envir.food[getArrayLocation([self.x, self.y])]
            except KeyError:
                pass
            self.type = Ant.TYPE_RETURNER

        if (self.type == Ant.TYPE_SEEKER or self.type == Ant.TYPE_FOLLOWER):
            if (self.x == 0 or self.x == self.envir._width or self.y == 0 or self.y == self.envir._height):
                self.type = Ant.TYPE_RETURNER2
        
        # Actually move (display)
        self.object.x = self.x
        self.object.y = self.y