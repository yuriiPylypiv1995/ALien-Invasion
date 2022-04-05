import pygame

class Ship:
    """The spaceship params and working"""
    def __init__(self, ai_game):
        """The spaceship initialization and start position"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # Getting an image of the spaceship
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Setting of the spaceship start position (on the botton centre of the screen)
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        # The moving right indicator
        self.moving_right = False
        # The moving left indicator
        self.moving_left = False

    def update_position(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Updating rect x
        self.rect.x = self.x

    def blitme(self):
        """Paiting of the spaceship on its start position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on midbottom of the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)