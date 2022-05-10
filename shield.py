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

    def move_shield(self):
        """This is the method for ship shield moving by the ship"""
        self.rect.center = self.ship_rect.center
        self.rect.y = self.ship_rect.top - 12
        if self.rect.right >= self.screen_rect.right:
            self.rect.x = self.screen_rect.right - 160
        elif self.rect.x <= 0:
            self.rect.x = self.screen_rect.left

    def draw_shield(self):
        """This is the method for ship shield creating"""
        pygame.draw.rect(self.screen, self.color, self.rect)