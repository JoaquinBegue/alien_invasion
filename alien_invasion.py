"""14-5. Refactoring: Look for functions and methods that are doing more
than one task, and refactor them to keep your code organized and efficient.
For example, move some of the code in check_bullet_alien_collisions(),
which starts a new level when the fleet of aliens has been destroyed,
to a function called start_new_level(). Also, move the four separate
method calls in the __init__() method in Scoreboard to a method called
prep_images() to shorten __init__(). The prep_images() method could also
help check_play_button() or start_game() if you’ve already refactored
check_play_button()."""

import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf

def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    start_button = Button(screen, "images/button.bmp","START", 80, 1)
    restart_button = Button(screen, "images/wide_button.bmp","RESTART", 80, 1)
    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship, a group of bullets and a group of aliens.
    ship = Ship(ai_settings, screen, "images/ship.bmp")
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, sb, ship, aliens)

    # Start the main loop for the game.
    while True:
        if stats.first_game:
            play_button = start_button
        else:
            play_button = restart_button

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
            
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()