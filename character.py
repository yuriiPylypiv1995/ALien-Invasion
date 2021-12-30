import pygame

class Character:
    """Task 12.2 - homework"""
    """The zombie params and working"""

    def __init__(self, ai_game):
        """The zombie initialization and start position"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Getting an image of the zombie
        self.image = pygame.image.load('images/zombie.png')
        self.rect = self.image.get_rect()

        # Setting of the zombie start position (on the centre of the screen)
        self.rect.center = self.screen_rect.center

    def blit_zombie(self):
        """Paiting of the zombie on its start position"""
        self.screen.blit(self.image, self.rect)