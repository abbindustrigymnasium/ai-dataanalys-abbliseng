import pygame

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

class MapPoint:

    TYPE_EMPTY = 0
    TYPE_FOOD = 1
    TYPE_NEST = 2
    TYPE_OBSTACLE = 3

    MAX_CONCENTRATION = 100.0
    # DECAY_CONSTANT = 0.006
    DECAY_CONSTANT = 0.016

    SEEKER_SWAY = MAX_CONCENTRATION*0.75

    def __init__(self, position, t, envir):
        self.type = t
        self.pos = position
        self.pheromone_concentration = 0
        self.object = pygame.Rect(self.pos[0], self.pos[1], 1, 1)
        self.envir = envir
        self.DECAY_CONSTANT = MapPoint.DECAY_CONSTANT

    def pheromoneDecay(self, envir=None, pos=None):
        self.pheromone_concentration = (1-self.DECAY_CONSTANT)*self.pheromone_concentration
        if (self.pheromone_concentration <= 0.0000001):
            self.pheromone_concentration = 0
            self.DECAY_CONSTANT = MapPoint.DECAY_CONSTANT
            
    def pheromoneIncrease(self, val):
        if (self.type != MapPoint.TYPE_OBSTACLE):
            self.DECAY_CONSTANT = MapPoint.DECAY_CONSTANT
            self.pheromone_concentration += val
            if (self.pheromone_concentration > MapPoint.MAX_CONCENTRATION):
                self.pheromone_concentration = MapPoint.MAX_CONCENTRATION
    
    def display(self):
        self.pheromoneDecay()

        if (self.type == MapPoint.TYPE_NEST):
            pygame.draw.rect(self.envir.fake_screen, (255,0,0), self.object)
        elif (self.type == MapPoint.TYPE_FOOD):
            pygame.draw.rect(self.envir.fake_screen, (0, 255, 0), self.object)
        else:
            pygame.draw.rect(self.envir.fake_screen, hsl2rgb(264, 100, 100*(self.pheromone_concentration/MapPoint.MAX_CONCENTRATION)), self.object)