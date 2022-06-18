import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """The class for alien bullet control"""

    def __init__(self, ai_game):
        """Bullet settings"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.aliens = ai_game.aliens
        self.red_aliens = self.get_red_alien_from_the_group(self.aliens)
        self.alien_bullet_color = self.settings.alien_bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.alien_bullet_width, self.settings.alien_bullet_height)

        self.y = float(self.rect.y)

    def update(self):
        """This method update alien bullet vertical position"""
        self.y += self.settings.alien_bullet_speed
        self.rect.y = self.y

    def draw_alien_bullet(self):
        """This method draw alien bullets with their parameters and color"""
        for red_alien in self.red_aliens.sprites():
            self.rect.midtop = red_alien.rect.midbottom
            self.rect.y -= 5
            pygame.draw.rect(self.screen, self.alien_bullet_color, self.rect)

    @staticmethod
    def get_red_alien_from_the_group(aliens):
        """This method returns the red aliens only"""
        red_aliens = pygame.sprite.Group()
        for alien in aliens.sprites():
            if alien.fire_bullet:
                red_aliens.add(alien)

        return red_aliens
