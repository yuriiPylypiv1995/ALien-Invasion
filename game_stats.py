class GameStats:
    """This is the class for game's statistic"""

    def __init__(self, ai_game):
        """The statistic initialization"""
        # Start the game with active status
        self.ships_left = None
        self.score = None
        self.level = None
        self.game_active = False
        self.high_score = 0
        self.shield_left = None
        self.shield_life_remain = 0

        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """The statistic initialization that may change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.shield_left = self.settings.shield_limit
        self.shield_life_remain = self.settings.shield_life_poitns