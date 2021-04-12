# Simple pygame program

# Import and initialize the pygame library
import pygame
import math
from ant import Ant
from utils import everyPointInCircle

pygame.init()

# Set up the drawing window

width = 1280
height = 960
gameboard = []

for i in range(height):
    gameboard.append([])
    for j in range(width):
        # [Walkable, Food, Home, Ant, Pheromones (negative red, positive blue)]
        gameboard[i].append([True, False, False, False, 0])

# Run until the user asks to quit
# running = True



def markSquare(location, number):
    gameboard[location[1]][location[0]]

class AntWindow():
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._running = True
        self.screen = pygame.display.set_mode([width, height])
        # Fill the background
        self.screen.fill((78, 42, 42))
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            test = Food(pos)

class AntHill():
    def __init__(self, location):
        self.location = location
        everyPointInCircle(self, location, 13, self.drawOne)
        everyPointInCircle(self, location, 9, self.drawTwo)
        everyPointInCircle(self, location, 5, self.drawThree)
        # self.draw(location)

    def drawOne(self, location):
        gameboard[math.floor(location[1])][math.floor(location[0])][2] = True # Home
        pygame.draw.circle(game.screen, (191, 123, 67), (math.floor(location[0]), math.floor(location[1])), 13)
    def drawTwo(self, location):
        pygame.draw.circle(game.screen, (245, 169, 76), (math.floor(location[0]), math.floor(location[1])), 9)
    def drawThree(self, location):
        pygame.draw.circle(game.screen, (255, 193, 112), (math.floor(location[0]), math.floor(location[1])), 5)


class Food():
    def __init__(self,location):
        everyPointInCircle(self, location, 12, self.draw)
    def draw(self, location):
        gameboard[math.floor(location[1])][math.floor(location[0])][1] = True # Food
        print(gameboard[math.floor(location[1])][math.floor(location[0])])
        pygame.draw.circle(game.screen, (254, 196, 0), (location[0], location[1]), 1)
        
game = AntWindow(1280, 960)

nAnts = 1
ants = Ant()
hill = AntHill([game._width/2, game._height/2])

while game._running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        game.handle_event(event)

    # Ant homebase

    # "Flip the display" - excuse me? wut
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()