import math
from MapPoint import MapPoint

# _width = math.floor(1920/15)
# _height = math.floor(1080/15)

_width = math.floor(200)
_height = math.floor(200)

_sSize = [_width, _height]
_ratio = _height/_width
relX = math.floor(_width/2)
_ratio = _height/_width
relY = math.floor(_height/2)

def getWidth():
    return _width
def getHeight():
    return _height
def getsSize():
    return _sSize
def getRelX():
    return relX
def getRelY():
    return relY
def getRatio():
    return _ratio

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

def checkIfFood(self, possible_target_point):
    if (getArrayLocation(possible_target_point) < 0 or getArrayLocation(possible_target_point) > (self.envir._height*self.envir._width)-1):
        return False
    else:
        if (self.envir.map[getArrayLocation(possible_target_point)].type == MapPoint.TYPE_FOOD):
            target = possible_target_point
            return True
    return False