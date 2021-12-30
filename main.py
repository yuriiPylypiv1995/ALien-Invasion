import sys
import pygame
from settings import Settings

class AlienInvasion:
    """Class for game initialization"""
    def __init__(self):
        """Game initialization"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alian Invasion")

    def run_game(self):
        """The main cycle of the game"""
        while True:
            # The events monitoring
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Repainting the screen after each cycle iteration
            self.screen.fill(self.settings.bg_color)

            # Show the last painted screen
            pygame.display.flip()

if __name__ == "__main__":
    # Creating the game object and run the game
    ai = AlienInvasion()
    ai.run_game()