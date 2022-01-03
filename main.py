import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
# from character import Character

class AlienInvasion:
    """Class for game initialization"""
    def __init__(self):
        """Game initialization"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        # self.character = Character(self)

    def run_game(self):
        """The main cycle of the game"""
        while True:
            self._check_events()
            self.ship.update_position()
            self._update_bullets()
            self._update_screen()

    def _check_events(self):
        # The events monitoring
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Reaction on pressing buttons"""
        if event.key == pygame.K_RIGHT:
            # Replace the spaceship on 1 pix right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Replace the spaceship on 1 pix left
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_F12:
            # Open the game in the fullscreen mode
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
            self.ship.rect.y += 100
            self.ship.screen_rect.right += 168
        elif event.key == pygame.K_ESCAPE:
            # Exit from the fullscreen mode
            self.screen = pygame.display.set_mode((1200, 670))
            if self.ship.x < 0:
                self.ship.x = 0
            elif self.ship.x > 1200:
                self.ship.x -= 168
            self.ship.rect.y -= 100
            self.ship.screen_rect.right -= 168

    def _check_keyup_events(self, event):
        """Reaction wnen a button is not pressed"""
        if event.key == pygame.K_RIGHT:
            # Do not move the spaceship
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        # Repainting the screen after each cycle iteration
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # self.character.blit_zombie()

        # Show the last painted screen
        pygame.display.flip()

    def _fire_bullet(self):
        # Adding new bullet to group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """The method for bullets updating"""
        # Bullets positions updating
        self.bullets.update()
        # Removing bullets that out of the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

if __name__ == "__main__":
    # Creating the game object and run the game
    ai = AlienInvasion()
    ai.run_game()