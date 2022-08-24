import pygame
from pygame.sprite import Sprite
from time import sleep
from pygame.mixer import Sound

class Ship(Sprite):
    def __init__(self, ai_settings, screen, image_path):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current position."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
        respawn_sound = Sound("sounds/ship_respawn.wav")
        respawn_sound.set_volume(0.5)
        respawn_sound.play()

    def blink(self): # Work in progress
        for n in range(3):
            self.rect.y = self.ai_settings.screen_height
            self.y = self.rect.y
            sleep(0.25)
            self.rect.bottom = self.screen_rect.bottom
            self.y = self.rect.bottom + self.rect.height