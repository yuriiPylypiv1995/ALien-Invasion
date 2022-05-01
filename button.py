import pygame.font

class Button:
    """This is a class for game's buttons initialization"""

    def __init__(self, ai_game, msg: str, width: int, height: int, button_color: tuple, text_color: tuple,
                 font_size: int, x: int, y: int):
        """The attributes of buttons initialization"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # The size and properties of the button
        self.width, self.height = width, height
        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, font_size)

        # Rect object of the button and it's position
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = x
        self.rect.y = y

        # This method shows text on the buttons
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
