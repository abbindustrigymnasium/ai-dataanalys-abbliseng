def everyPointInCircle(p, location, radius, func):
    # Calculate bounding rectangle
    upperX = location[0]-radius
    upperY = location[1]-radius
    width = radius+radius
    # Get circle points
    for x in range(width):
        x += upperX
        for y in range(width):
            y += upperY
            dx = x - location[0]
            dy = y - location[1]
            distanceSquared = dx*dx+dy*dy
            if (distanceSquared <= radius*radius):
                func([x,y])
    return None