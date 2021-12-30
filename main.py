import sys
import pygame
from settings import Settings

class AlianInvasion:
    """Клас, що ініціалізує гру"""
    def __init__(self):
        """Ініціалізація гри"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alian Invasion")

    def run_game(self):
        """Головний цикл гри"""
        while True:
            # Слідкувати за подіями миші і клавіатури
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Перемалювати екран на кожній ітерації циклу
            self.screen.fill(self.settings.bg_color)

            # Показати останній намальований екран
            pygame.display.flip()

if __name__ == "__main__":
    # Створити екземпляр класу гри і запустити гру
    ai = AlianInvasion()
    ai.run_game()