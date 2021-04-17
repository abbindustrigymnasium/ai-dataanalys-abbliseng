class MapPoint:
    TYPE_FOOD = 0
    TYPE_NEST = 1
    TYPE_EMPTY = 2
    TYPE_BORDER = 3
    TYPE_BORDER2 = 4

    MAX_CONCENTRATION = 100.0
    MAX_FOOD_CONCENTRATION = 30
    finite_food = True

    def __init__(self, type, position):
        self.type = type
        self.pheromone_concentration = 0
        self.position = position
        self.food_concentrarion = 0
        self.being_collected = False
        self.decay_constant = 0.006

    def setBeingCollected(self, val):
        self.being_collected = val
    def beingCollected(self):
        return self.being_collected

    @staticmethod
    def setFinite(finite):
        MapPoint.finite_food = finite
    @staticmethod
    def getFinite():
        return MapPoint.finite_food

    def setDecayConstant(self, decay_constant):
        self.decay_constant = decay_constant
    def pheromoneDecay(self):
        self.pheromone_concentration = (1-self.decay_constant)*self.pheromone_concentration
    def pheromoneIncrease(self, delta_pheromone):
        if (self.type != MapPoint.TYPE_BORDER or self.type != MapPoint.TYPE_BORDER2):
            self.pheromone_concentration = self.pheromone_concentration + delta_pheromone

    def setType(self, t):
        self.type = t
        if (self.type == MapPoint.TYPE_BORDER or self.type == MapPoint.TYPE_BORDER2):
            self.pheromone_concentration = 0.0
            self.food_concentrarion = 0
        elif (self.type == MapPoint.TYPE_FOOD):
            self.setFoodConcentration(MapPoint.MAX_FOOD_CONCENTRATION)
    def returnType(self):
        return self.type
    
    def getFoodConcentration(self):
        return self.food_concentrarion
    def setFoodConcentration(self, val):
        self.food_concentrarion = val
    def foodDecrease(self):
        if (MapPoint.finite_food):
            self.food_concentrarion -= 1
            if (self.food_concentrarion == 0):
                self.setType(MapPoint.TYPE_EMPTY)

    def getPosition(self):
        return self.position
    
    def isBorderPoint(self, nX, nY):
        if (self.position[0]==0 or self.position[1]==0 or self.position[0] == nX-1 or self.position[1]==nY-1):
            return True
        else:
            return False