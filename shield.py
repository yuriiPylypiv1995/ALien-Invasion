import pygame

class Shield:
    """This is a clas for ship shield creation"""

    def __init__(self, ai_game):
        """The shield attibutes initialization"""
        self.ship = ai_game.ship
        self.ship_rect = self.ship.rect
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.color = self.settings.shield_color
        self.show_shield = False

        self.rect = pygame.Rect(0, 0, self.settings.shield_width, self.settings.shield_height)
        self.power_shield_image = pygame.image.load("images/power_shield.bmp")
        self.power_shield_image = pygame.transform.scale(self.power_shield_image, (self.settings.power_shield_width,
                                                                                   self.settings.power_shield_height))
        self.power_shield_rect = self.power_shield_image.get_rect()

    def move_shield(self):
        """This is the method for ship shield moving with the ship"""
        self.rect.center = self.ship_rect.center
        self.rect.y = self.ship_rect.top - 12
        if self.rect.right >= self.screen_rect.right:
            self.rect.x = self.screen_rect.right - 160
        elif self.rect.x <= 0:
            self.rect.x = self.screen_rect.left

    def move_power_shield(self):
        """This is the method for power ship shield moving with the ship"""
        self.power_shield_rect.center = self.ship_rect.center
        self.power_shield_rect.y = 450

    def draw_shield(self):
        """This is the method for ship shield creating"""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def blit_power_shield(self):
        """This method for ship shield blitting like an image"""
        self.screen.blit(self.power_shield_image, self.power_shield_rect)