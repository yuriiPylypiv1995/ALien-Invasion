class Settings:
    """This is a class for saving all of game's settings"""
    def __init__(self):
        """Game settings initialization"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 670
        self.bg_color = (230, 230, 230)

        # The ship settings
        self.ship_speed = None
        self.ship_limit = 2

        # Bullets settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        self.bullet_speed = None

        # Aliens settings
        self.fleet_direction = None
        self.alien_speed = None
        self.fleet_drop_speed = 10

        # The game speed up
        self.speed_up_scale = 1.1
        self.ititialize_dynamic_settings()

    def ititialize_dynamic_settings(self):
        """This method cotrols the game dinamic settings only"""
        self.ship_speed = 1.5
        self.bullet_speed = 1.0
        self.alien_speed = 1.0

        # 1 - to right, -1 - to left
        self.fleet_direction = 1

    def increase_speed(self):
        """"Incresing speed settings"""
        self.ship_speed *= self.speed_up_scale
        self.bullet_speed *= self.speed_up_scale
        self.alien_speed *= self.speed_up_scale

