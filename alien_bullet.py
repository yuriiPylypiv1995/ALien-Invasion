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

        self.alien_bullet_rect = pygame.Rect(0, 0, self.settings.alien_bullet_width, self.settings.alien_bullet_height)

        self.alien_bullet_y = float(self.alien_bullet_rect.y)

    def update(self):
        """This method update bullet vertical position"""
        self.alien_bullet_y += self.settings.alien_bullet_speed
        self.alien_bullet_rect.x = self.alien_bullet_y

    def draw_alien_bullet(self):
        """This method draw alien bullets with their parameters and color"""
        for red_alien in self.red_aliens.sprites():
            self.alien_bullet_rect.midtop = red_alien.rect.midbottom
            self.alien_bullet_rect.y -= 5
            pygame.draw.rect(self.screen, self.alien_bullet_color, self.alien_bullet_rect)

    @staticmethod
    def get_red_alien_from_the_group(aliens):
        """This method returns the red aliens only"""
        red_aliens = pygame.sprite.Group()
        for alien in aliens.sprites():
            if alien.fire_bullet:
                red_aliens.add(alien)

        return red_aliens
