import random
import pygame
from utils import convertToPixelCoords
import math

# Unit that has a speed, freedom (how likely to not pick the best tile to go to)
# pheromone strength, pheromone deterioation?, view angle, current position,
# red pheromone strength, red pheromone deterioration

class Ant():
    def __init__(self, id, game_screen):
        self.id = id
        self.game_screen = game_screen
        self.speed = random.randint(0,10) # 0 -> 9?
        self.freedom = random.random() # 0.0 -> 1.0
        self.bluePheromone = {"strength": random.random(), "deterioration": random.random()} # Automatically left behind
        self.redPheromone = {"strength": random.random(), "deterioration": random.random()} # Left if carrying food
        self.viewAngle = random.randint(0,181) # 0 -> 180
        self.viewRange = random.randint(0,31) # 0 -> 30
        self.pos = [0, 0]
        self.object = pygame.Rect(convertToPixelCoords(self.pos)[0],convertToPixelCoords(self.pos)[1],1,1)

    def printStats(self):
        print(("--- "+str(self.id)+" ---").center(16))
        print("Speed".ljust(16),":",self.speed)
        print("Freedom".ljust(16),":",self.freedom)
        print("Blue Pheromone".ljust(16),":",self.bluePheromone)
        print("Red Pheromone".ljust(16),":",self.redPheromone)
        print("View Angle".ljust(16),":",self.viewAngle)
        print("Current Position".ljust(16),":",self.pos)

    # def move(self):
    #     visibleTiles = getVisibleTiles(self.pos, self.viewRange, self.viewAngle)
        
    def displayAnt(self):
        pos = convertToPixelCoords(self.pos)
        # pygame.draw.circle(self.game_screen.screen, (0, 0, 0), (math.floor(pos[0]), math.floor(pos[1])), 1)
        pygame.draw.rect(self.game_screen.screen, (0,0,0), self.object)


# Ant(0).printStats()