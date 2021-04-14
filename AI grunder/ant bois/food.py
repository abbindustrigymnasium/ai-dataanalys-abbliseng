import pygame
from  utils import convertToPixelCoords, updateGameMap

class Food():
    def __init__(self, location, game_screen):
        self.pos = location
        self.object = pygame.Rect(convertToPixelCoords(self.pos)[0],convertToPixelCoords(self.pos)[1], 1, 1)
        self.game_screen = game_screen

        self.display()

    def display(self):
        pygame.draw.rect(self.game_screen.screen, (254, 196, 0), self.object)
        