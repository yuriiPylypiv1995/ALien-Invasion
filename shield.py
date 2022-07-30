import pygame

class Shield:
    """This is a class for ship shield creation"""

    def __init__(self, ai_game):
        """The shield attibutes initialization"""
        self.ship = ai_game.ship
        self.ship_rect = self.ship.rect
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.show_shield = False

        self.power_shield_image = pygame.image.load("images/power_shield.bmp")
        self.power_shield_image = pygame.transform.scale(self.power_shield_image, (self.settings.power_shield_width,
                                                                                   self.settings.power_shield_height))
        self.rect = self.power_shield_image.get_rect()

    def move_power_shield(self):
        """This is the method for power ship shield moving with the ship"""
        self.rect.center = self.ship_rect.center
        self.rect.y = 450

    def blit_power_shield(self):
        """This method for ship shield blitting like an image"""
        self.screen.blit(self.power_shield_image, self.rect)