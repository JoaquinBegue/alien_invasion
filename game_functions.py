from logging import exception
import sys, pygame
from io import open
from bullet import Bullet
from alien import Alien
from time import sleep
from pygame.mixer import Sound

# Display functions.

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    if stats.game_active:
        # Redraw all bullets behind ship and aliens.
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        aliens.draw(screen)

        # Draw the score information.
        sb.show_score()
    else:
        # Draw the play button if the game is inactive.
        play_button.blitme()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of the old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of the bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if the fleet is at an edge, and the update the positions of
    all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


# Player interactive functions.

def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        save_high_score(stats)
        sys.exit()
    elif event.key == pygame.K_p:
        if not stats.game_active:
            start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score(stats)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        bullet_sound = Sound("sounds/bullet.wav")
        bullet_sound.set_volume(0.5)
        bullet_sound.play()


# Object interaction functions.

def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            explosion_sound = Sound("sounds/explosion.wav")
            explosion_sound.set_volume(0.35)
            explosion_sound.play()
        check_high_scores(stats, sb)

    # If the entire fleet is destroyed start a new level.
    if len(aliens) == 0:
        start_new_level(ai_settings, stats, sb, bullets)
        create_fleet(ai_settings, screen, sb, ship, aliens)

def start_new_level(ai_settings, stats, sb, bullets):
    """Remove existing bullets and increase game speed."""
    bullets.empty()
    ai_settings.increase_speed()

    # Increase level.
    stats.level += 1
    sb.prep_level()

    new_level_sound = Sound("sounds/new_level.wav")
    new_level_sound.play()
    sleep(0.75)

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        ship_hit_sound = Sound("sounds/ship_hit.wav")
        ship_hit_sound.set_volume(0.75)
        ship_hit_sound.play()
        # Decrement ships_left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Pause.
        sleep(0.5)

        # Reset game objects.
        reset_objects(ai_settings, screen, sb, ship, aliens, bullets)
    else:
        stats.game_active = False
        stats.first_game = False
        pygame.mouse.set_visible(True)


# Misc functions.

def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Reset the game settings.
    ai_settings.initialize_dynamic_settings()

    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)

    # Reset the game statistics.
    stats.reset_stats()
    stats.game_active = True

    # Reset the scoreboard images.
    sb.prep_images()

    # Reset game objects.
    reset_objects(ai_settings, screen, sb, ship, aliens, bullets)

def reset_objects(ai_settings, screen, sb, ship, aliens, bullets):
    """Reset the game objects at it's initial states."""
    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship.
    create_fleet(ai_settings, screen, sb, ship, aliens)
    ship.center_ship()

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
        play_button_sound = Sound("sounds/play_button.wav")
        play_button_sound.set_volume(0.5)
        play_button_sound.play()

def check_high_scores(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def save_high_score(stats):
    with open("high_scores.txt", "w") as file:
        file.write(str(stats.high_score))
    

# Alien fleet's functions.

def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, sb, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (5 * alien_height) - 
                            ship_height - sb.bgr_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, sb, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = sb.bgr_height + alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, sb, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)    
    number_rows = get_number_rows(ai_settings, sb, ship.rect.height,
        alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, sb, aliens, alien_number,
                row_number)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same way as if the ship got hit.
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break