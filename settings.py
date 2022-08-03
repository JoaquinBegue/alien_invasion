class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 500
        self.bullet_height = 15
        self.bullet_color = 200, 200, 0
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed_factor = 50
        self.fleet_drop_speed = 100
        # fleet_direction of 1 represent right; -1 represent left.
        self.fleet_direction = 1