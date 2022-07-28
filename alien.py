import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and get its rect.
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()
        #self.screen_rect = screen.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)

        # Movement flag
        #self.moving_right = False
        #self.moving_left = False

    #def update(self):
        """Update the alien's position based on the movement flag."""
        # Update the alien's center value, not the rect.
        #if self.moving_right and self.rect.right < self.screen_rect.right:
        #    self.center += self.ai_settings.alien_speed_factor
        #if self.moving_left and self.rect.left > 0:
        #    self.center -= self.ai_settings.alien_speed_factor

        # Update rect object from self.center.
        #self.rect.centerx = self.center

    def blitme(self):
        """Draw the alien at its current position."""
        self.screen.blit(self.image, self.rect)