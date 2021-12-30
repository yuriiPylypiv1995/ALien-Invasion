import pygame

class Ship:
    """The spaceship params and working"""
    def __init__(self, ai_game):
        """The spaceship initialization and start position"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Getting an image of the spaceship
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Setting of the spaceship start position (on the botton centre of the screen)
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Paiting of the spaceship on its start position"""
        self.screen.blit(self.image, self.rect)