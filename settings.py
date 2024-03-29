class Settings:
    """This is a class for saving all game's settings"""

    def __init__(self):
        """Game settings initialization"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 670
        self.bg_color = (230, 230, 230)
        self.font_color = (96, 96, 96)
        self.font_size = 27

        # Ship settings
        self.ship_speed = None
        self.ship_limit = 5

        # Bullets settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        self.bullet_speed = None
        self.alien_bullet_speed = None
        self.alien_bullet_color = (188, 143, 143)
        self.alien_bullet_width = 3
        self.alien_bullet_height = 100

        # Shield settings
        self.shield_limit = 1
        self.shield_life_poitns = 300
        self.power_shield_width = 450
        self.power_shield_height = 295

        # Aliens settings
        self.fleet_direction = None
        self.alien_speed = None
        self.fleet_drop_speed = 10
        self.alien_points = None
        self.red_alien_points = None

        # The game speed up
        self.speed_up_scale = 1.1
        self.ititialize_dynamic_settings()

        # Increase the alien points
        self.score_scale = 1.5

    def ititialize_dynamic_settings(self):
        """This method cotrols the game dynamic settings only"""
        self.ship_speed = 1.5
        self.bullet_speed = 1.0
        self.alien_bullet_speed = 0.3
        self.alien_speed = 1.0

        # 1 - to right, -1 - to left
        self.fleet_direction = 1

        # Points for any one alien
        self.alien_points = 50
        self.red_alien_points = 70

    def increase_speed(self):
        """"Incresing speed settings"""
        self.ship_speed *= self.speed_up_scale
        self.bullet_speed *= self.speed_up_scale
        self.alien_bullet_speed *= self.speed_up_scale
        self.alien_speed *= self.speed_up_scale

        # Increasing the amount of points by killing each one red or green alien
        self.alien_points = int(self.alien_points * self.score_scale)
        self.red_alien_points = int(self.red_alien_points * self.score_scale)


