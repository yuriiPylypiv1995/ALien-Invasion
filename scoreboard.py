import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """"This class regulates the game score"""

    def __init__(self, ai_game):
        """The score's attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # These are a font's settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 30)

        self.score_image = None
        self.high_score_image = None
        self.level_image = None
        self.score_rect = None
        self.high_score_rect = None
        self.level_rect = None
        self.ships = None
        self.shield_life_remain_image = None
        self.shield_life_remain_image_rect = None
        self.shields_remain_image = None
        self.shields_remain_image_rect = None

        # Making an image for start showing
        self.prep_images()

    def prep_score(self):
        """Reform the digital score to an image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Show the score image n the top right corner of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Reform the digital score to an image"""
        high_score = int(self.read_high_score())
        high_score_str = "Highest score: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Horizontal center the high score
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Reform the level to an image"""
        level_str = str("Level: " + str(self.stats.level))
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        # Locate the level under the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_shield_life_remain(self):
        """Reform the shield life remain points to an image"""
        shield_life_remain_str = str("Shield's life points: " + str(round(self.stats.shield_life_remain)))
        self.shield_life_remain_image = self.font.render(shield_life_remain_str, True, self.text_color,
                                                         self.settings.bg_color)

        # Horizontal center the shield life points
        self.shield_life_remain_image_rect = self.shield_life_remain_image.get_rect()
        self.shield_life_remain_image_rect.centerx = self.screen_rect.centerx
        self.shield_life_remain_image_rect.y = self.high_score_rect.y + 25

    def prep_shields(self):
        """Reform the remaining shields amount to an image"""
        shields_remain_str = str("Shields: " + str(self.stats.shield_left))
        self.shields_remain_image = self.font.render(shields_remain_str, True, self.text_color,
                                                         self.settings.bg_color)

        # Locate the remaining shields amount to right corner of the game screen
        self.shields_remain_image_rect = self.shields_remain_image.get_rect()
        self.shields_remain_image_rect.right = self.level_rect.right
        self.shields_remain_image_rect.y = self.level_rect.bottom + 10

    def prep_ships(self):
        """This method shows how many ships left in use by user"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """This method draws the score, level, ships and shield images on the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.shield_life_remain_image, self.shield_life_remain_image_rect)
        self.screen.blit(self.shields_remain_image, self.shields_remain_image_rect)
        self.ships.draw(self.screen)

    def save_high_score(self):
        """Saving the highest score to a file in order to show it when game will be reopened"""
        high_score_filename = "high_score.txt"
        high_score = str(self.stats.high_score)
        with open(high_score_filename, 'w') as file_object:
            file_object.write(high_score)

    @staticmethod
    def read_high_score():
        """Reading the high score from the file"""
        with open('high_score.txt', 'r') as file_object:
            high_score_saved = file_object.read()

        return high_score_saved

    def check_high_score(self):
        """Check if the new high score is reached"""
        if self.stats.score > int(self.read_high_score()):
            self.stats.high_score = self.stats.score
            self.save_high_score()
            self.prep_high_score()

    def prep_images(self):
        """This method shows all of score's images on the game screen"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_shield_life_remain()
        self.prep_shields()
