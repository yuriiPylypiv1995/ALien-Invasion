import pygame.font

class Scoreboard:
    """"This class regulates the game score"""
    def __init__(self, ai_game):
        """The score's attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # There are a font's settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.score_image = None
        self.score_rect = None

        # Making an image for score's showing
        self.prep_score()

    def prep_score(self):
        """Reform the digital score to an image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Show the score image in the top right corner of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """This method draws the score image on the screen"""
        self.screen.blit(self.score_image, self.score_rect)
