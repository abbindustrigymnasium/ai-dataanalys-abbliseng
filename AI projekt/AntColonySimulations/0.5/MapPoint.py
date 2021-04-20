import pygame
class MapPoint:

    TYPE_EMPTY = 0
    TYPE_FOOD = 1
    TYPE_NEST = 2
    TYPE_OBSTACLE = 3

    MAX_CONCENTRATION = 100.0
    DECAY_CONSTANT = 0.006

    def __init__(self, position, t):
        self.type = t
        self.pos = position
        # self.decay_constant = 0.006
        self.pheromone_concentration = 0
        self.object = pygame.Rect(self.pos[0], self.pos[1], 1, 1)

    def pheromoneDecay(self, envir=None, pos=None):
        self.pheromone_concentration = (1-MapPoint.DECAY_CONSTANT)*self.pheromone_concentration
        if (self.pheromone_concentration <= 0.0000001):
            self.pheromone_concentration = 0
            
    def pheromoneIncrease(self, val):
        if (self.type != MapPoint.TYPE_OBSTACLE):
            self.pheromone_concentration += val
            if (self.pheromone_concentration > MapPoint.MAX_CONCENTRATION):
                self.pheromone_concentration = MapPoint.MAX_CONCENTRATION