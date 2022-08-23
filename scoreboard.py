import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """A class to report scoring information."""

    def __init__(self, ai_settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        # Font settings for scoring information.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("fonts/back-to-1982.regular.ttf", 30)
        self.large_font = pygame.font.Font("fonts/back-to-1982.regular.ttf", 60)

        # Prepare the scoreboard's images.
        self.prep_images()

    def prep_images(self):
        """Calls to each prepare method."""
        self.prep_background_rect()
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    
    def prep_background_rect(self):
        """Create the background rect."""
        self.bgr_width, self.bgr_height = self.screen_rect.width, 100
        self.bgr_rect = pygame.Rect(0, 0, self.bgr_width, self.bgr_height)
        self.bgr_color = (50, 50, 50)

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
        self.bgr_color)
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 15

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.large_font.render(high_score_str, True,
            self.text_color, self.bgr_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render(str(self.stats.level), True,
            self.text_color, self.bgr_color)
        
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        distance = 20
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen, "images/ship_small.bmp")
            ship.rect.x = distance + ship_number * ship.rect.width
            ship.rect.y = 20
            self.ships.add(ship)
            distance += 10

    def show_score(self):
        """Draw scores and ships to the screen."""
        self.screen.fill(self.bgr_color, self.bgr_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # Draw ships.
        self.ships.draw(self.screen)