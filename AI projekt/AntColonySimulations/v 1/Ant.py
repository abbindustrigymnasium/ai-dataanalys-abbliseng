from Utils import *
from random import random, randint, randrange, choice
from MapPoint import MapPoint
import pygame
import  math

class Ant:

    # Four ant types/roles
    TYPE_SEEKER = 0
    TYPE_FOLLOWER = 1
    TYPE_RETURNER = 2
    TYPE_RETURNER2 = 3

    MAX_TRIP = 450 # self.envir._width*2+self.envir._height

    PH_FOOD_MULTIPLIER = 5 # PH drop boost after finding food
    PH_FOOD_MULTIPLIER_LENGTH = 10 # How long boost lasts

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
        self.dir = randint(0,7) # 0-7 # Get start direction
        self.envir = envir
        self.object = pygame.Rect(self.x, self.y, 1, 1)
        self.is_carrying = False # limit to one food pickup
        self.freedom = random() # likeliness to deviate
        self.ph_increase = Ant.STD_PH_DROP
        self.follower_to_seeker = self.ph_increase/10
        self.seeker_prob = round(MapPoint.MAX_CONCENTRATION+MapPoint.MAX_CONCENTRATION*0.05)

    def display(self):
        if (self.id != None):
            pygame.draw.rect(self.envir.fake_screen, (76, 230, 230), self.object)
        elif (self.type == Ant.TYPE_RETURNER):
            pygame.draw.rect(self.envir.fake_screen, (47, 168, 47), self.object)
        elif (self.type == Ant.TYPE_FOLLOWER):
            pygame.draw.rect(self.envir.fake_screen, (235, 147, 52), self.object)
        else:
            pygame.draw.rect(self.envir.fake_screen, (255, 255, 255), self.object)

    def pheromoneDrop(self, mapPoint, dirX, dirY):
        if (Ant.MAX_TRIP-len(self.move_hist) < Ant.PH_FOOD_MULTIPLIER_LENGTH): # Check if boost applies
            ph_inc = self.ph_increase * Ant.PH_FOOD_MULTIPLIER
            ph_inc_side = self.ph_increase * Ant.PH_FOOD_MULTIPLIER / Ant.SIDE_DROP
        else:
            ph_inc = self.ph_increase
            ph_inc_side = self.ph_increase/Ant.SIDE_DROP
        mapPoint.pheromoneIncrease(ph_inc) # Increase with calculated value
        if (abs(dirX) <= 1 and abs(dirY) <= 1):
            for i in range(-1,2):
                for j in range(-1,2):
                    if (i==0 and j==0):
                        continue
                    if (getArrayLocation([self.x+i,self.y+j]) < 0 or getArrayLocation([self.x+i,self.y+j]) > self.envir._width*self.envir._height-1): # Make sure it is within bounds
                        continue
                    self.envir.map[getArrayLocation([self.x+i,self.y+j])].pheromoneIncrease(ph_inc_side) # Drop pheromones to surrounding spots
                    # self.envir.pheromones.append((self.x+i, self.y+j))

    def checkForSurrondingFood(self, tier=0): # Look through surrounding and check if any tile has food, if so make that the target
        food_options = []
        for dx in range(-1-tier,2+tier):
            for dy in range(-1-tier,2+tier):
                p = [self.x+dx, self.y+dy]
                if ((dx == 0 and dy == 0)):
                    continue
                elif ((getArrayLocation(p) < 0 or getArrayLocation(p) > getWidth()*getHeight()-1)):
                    return "EDGE"
                if (checkIfFood(self, p)):
                    food_options.append(p)
        if (food_options != []):
            return choice(food_options) # If multiple options pick random within these
        return False

    def findSeekerTarget(self):
        # Check for surrounding food
        target = self.checkForSurrondingFood()
        if (target == "EDGE"):
            self.type = Ant.TYPE_RETURNER2
            return [self.x, self.y]
        elif (target):
            self.move_hist.append([self.x, self.y])
            return target
        # Check for surrounding trails
        for dx in range(-1,2):
            for dy in range(-1,2):
                p = [self.x+dx, self.y+dy]
                if ((dx == 0 and dy == 0) or (getArrayLocation(p) < 0 or getArrayLocation(p) > getWidth()*getHeight()-1)):
                    continue
                if (self.envir.map[getArrayLocation(p)].pheromone_concentration > MapPoint.SEEKER_SWAY*self.freedom):
                    self.type = Ant.TYPE_FOLLOWER
                    return [self.x+dx, self.y+dy]
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
        # Randomly select a target from possible points
        target = choice(possible_target_points)
        # Turn
        if (target == possible_target_points[0]):
            self.dir -= 1
        elif (target == possible_target_points[2]):
            self.dir += 1
        # Append current pos to move history
        self.move_hist.append([self.x, self.y])
        # return the target
        return target

    def findReturnerTarget(self):
        '''
        The returner ants move directly towards the nest with some random turns thrown in.
        They are actually just limited to decreasing their distance to the nest.
        In nature ants actually use light and landmarks to find their way back and this was the closes I could
        replicate that behavior within the timeframe.
        '''
        possiblie_return_points = []
        for dx in range(-1,2):
            for dy in range(-1,2):
                if ((dx == 0 and dy == 0) or getArrayLocation([self.x+dx, self.y+dy]) < 0 or getArrayLocation([self.x+dx, self.y+dy]) > getWidth()*getHeight()-1):
                    continue
                if (self.envir.hiveDist(self.x, self.y)>=self.envir.hiveDist(self.x+dx, self.y+dy)): # Increase the distance to hive
                    possiblie_return_points.append([self.x+dx, self.y+dy])
        return choice(possiblie_return_points)
                
    def findFollowerTarget(self):
        # Initialize variables
        n = 0
        phSum = 0
        norm = 0
        possible_target_points = []
        intervall = []
        Random = random()
        target = [0,0]

        # Check for food in surrounding (one extra view dist)
        possible_target = self.checkForSurrondingFood(1)
        if (possible_target and possible_target != "EDGE"):
            self.move_hist.append([self.x, self.y])
            return possible_target # If food is found, go there
        
        # Get possible targets with a pheromone concentration over 1 and further from nest (always increase distance)
        for dx in range(-1,2):
            for dy in range(-1,2):
                if ((dx == 0 and dy == 0) or getArrayLocation([self.x+dx, self.y+dy]) < 0 or getArrayLocation([self.x+dx, self.y+dy]) > getWidth()*getHeight()-1): # Make sure its within bounds
                    continue
                if (self.envir.hiveDist(self.x, self.y)<=self.envir.hiveDist(self.x+dx, self.y+dy) and self.envir.map[getArrayLocation([self.x+dx, self.y+dy])].pheromone_concentration > 0):
                    possible_target_points.append([self.x+dx, self.y+dy])
                    # Calculate possible target point weights
                    phSum += self.envir.map[getArrayLocation([self.x+dx, self.y+dy])].pheromone_concentration**2
                    norm += (self.envir.map[getArrayLocation([self.x+dx, self.y+dy])].pheromone_concentration*self.envir.hiveDist(self.x+dx, self.y+dy))**2
                    n += 1
        # If no possible targets or no good enough targets switch to seeker type
        if (phSum<self.follower_to_seeker or n==0):
            self.type = Ant.TYPE_SEEKER
        else:
            # Calculate the actual map tile weights depending on dist and ph concentration
            intervall.append((self.envir.map[getArrayLocation(possible_target_points[0])].pheromone_concentration*(100/norm)*self.envir.hiveDist(possible_target_points[0][0],possible_target_points[0][1]))**2)
            for i in range(1, n):
                intervall.append(intervall[i-1]+(self.envir.map[getArrayLocation(possible_target_points[i])].pheromone_concentration*(100/norm)*self.envir.hiveDist(possible_target_points[i][0],possible_target_points[i][1]))**2)
            for i in range(n):
                if (Random<=intervall[i]):
                    target = self.envir.map[getArrayLocation(possible_target_points[i])].pos
                    self.move_hist.append([self.x, self.y])
                    return target
            if (target == [0,0]):
                # If none is found (random fails) just pick a random one
                target = choice(possible_target_points)

        self.move_hist.append([self.x, self.y])
        return target


    def move(self):
        # Depending on type find accurate target
        if (self.type == Ant.TYPE_SEEKER):
            target = self.findSeekerTarget()
            if (len(self.move_hist) >= Ant.MAX_TRIP): # Return if max trip is reached
                self.type = Ant.TYPE_RETURNER2
        elif (self.type == Ant.TYPE_RETURNER or self.type == Ant.TYPE_RETURNER2):
            target = self.findReturnerTarget()
            if (self.type == Ant.TYPE_RETURNER): # Leave pheromones
                dirX = target[0]-self.x
                dirY = target[1]-self.y
                self.pheromoneDrop(self.envir.map[getArrayLocation([self.x, self.y])], dirX, dirY)
        elif (self.type == Ant.TYPE_FOLLOWER):
            target = self.findFollowerTarget()
            if (len(self.move_hist) >= Ant.MAX_TRIP): # Dont walk to far now :)
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
            self.move_hist = [[self.x, self.y]] # Reset the move hist
            if (self.type == Ant.TYPE_RETURNER and self.is_carrying): # Drop food
                self.is_carrying = False
            if (self.type != Ant.TYPE_FOLLOWER):
                self.type = Ant.TYPE_SEEKER
        # If food is found and you arent already returning return home with it and leave trail
        elif self.envir.map[getArrayLocation([self.x, self.y])].type == MapPoint.TYPE_FOOD and self.type != Ant.TYPE_RETURNER:
            self.is_carrying = True
            self.envir.map[getArrayLocation([self.x, self.y])].type = MapPoint.TYPE_EMPTY # reset the maptype
            try:
                del self.envir.food[getArrayLocation([self.x, self.y])]
            except KeyError:
                pass
            self.type = Ant.TYPE_RETURNER

        if (self.type == Ant.TYPE_SEEKER or self.type == Ant.TYPE_FOLLOWER):
            if (self.x == 0 or self.x == self.envir._width or self.y == 0 or self.y == self.envir._height): # If and edge is hit just return home
                self.type = Ant.TYPE_RETURNER2
        
        # Actually move the object
        self.object.x = self.x
        self.object.y = self.y