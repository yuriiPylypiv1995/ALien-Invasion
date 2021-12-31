import sys
import pygame
from settings import Settings
from ship import Ship
# from character import Character

class AlienInvasion:
    """Class for game initialization"""
    def __init__(self):
        """Game initialization"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        # self.character = Character(self)

    def run_game(self):
        """The main cycle of the game"""
        while True:
            self._check_events()
            self.ship.update_position()
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
        # self.character.blit_zombie()

        # Show the last painted screen
        pygame.display.flip()

if __name__ == "__main__":
    # Creating the game object and run the game
    ai = AlienInvasion()
    ai.run_game()