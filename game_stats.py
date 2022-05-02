class GameStats:
    """This is the class for game's statistic"""

    def __init__(self, ai_game):
        """The statistic initialization"""
        # Start the game with active status
        self.ships_left = None
        self.score = None
        self.game_active = False

        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """The statistic initialization that may change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0