class Settings:
    """This is a class for saving all of game's settings"""
    def __init__(self):
        """Game settings initialization"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 670
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5