"""14-6. Expanding Alien Invasion: Think of a way to expand Alien Invasion. For
example, you could program the aliens to shoot bullets down at the ship or
add shields for your ship to hide behind, which can be destroyed by bullets
from either side. Or use something like the pygame.mixer module to add sound
effects like explosions and shooting sounds.
actual sounds volume values:
respawn =  1.0
play_button =  1.0
background =  0.9921875
bullet =  1.0
explosion =  1.0
ship_hit =  1.0
"""

import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from pygame.mixer import music
import game_functions as gf

def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    music.load("sounds/background.wav")
    background_playing = False

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
            if not background_playing:
                music.set_volume(0.5)
                music.play(-1)
                
                background_playing = True

            # Display the game objects.
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()