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