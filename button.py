import pygame.font

class Button:
    """This is a class for game's buttons initialization"""

    def __init__(self, ai_game, msg):
        """The attributes of buttons initialization"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # The size and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Rect object of the button and it's centering
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # This method shows text on the button "Play" one tine only
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Reform the text to image and position him to center of the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """This is method for drawing the button with text on the game screen"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)