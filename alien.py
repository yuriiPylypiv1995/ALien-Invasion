import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """The class for aliens fleets control"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen

        # Load the alien image and get its rect attribute
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Position settings for first alien
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's x position
        self.x = float(self.rect.x)