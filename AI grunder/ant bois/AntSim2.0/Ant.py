from MapPoint import MapPoint

class Ant:
    ANT_SEEKER = 0
    ANT_FOLLOWER = 1
    ANT_RETURNER = 2
    ANT_RETURNER2 = 3

    def __init__(self, spawn_point, ):
        self.SEEKER_ANGLE = 70.00
        self.FOLLOWER_ANGLE = 360.00
        self.SEEKER_PROB = round(MapPoint.MAX_CONCENTRATION+MapPoint.MAX_CONCENTRATION*0.05)
        self.ASSES_FOOD_RADIUS = 1
        self.PHEROMONE_FOOD_MULTIPLIER = 5 # Utsöndra mer pheromoner stax efter mat
        self.PHEROMONE_MULTIPLIER_LENGTH = 10 # Hur länge gäller boosten
        self.SIDE_DROP = 2

    # SEEKER_ANGLE = 70.00
    # FOLLOWER_ANGLE = 360.00