import random
import sys
import pygame
from time import sleep
import pygame.font

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from shield import Shield

class AlienInvasion:
    """Class for game initialization"""

    def __init__(self):
        """Game initialization"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.shield = Shield(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.font = pygame.font.SysFont(None, self.settings.font_size)
        self.font_message = None
        self.message_image = self.font.render(self.font_message, True, self.settings.font_color, self.settings.bg_color)
        self.message_image_rect = self.message_image.get_rect()
        self.ok_button_show = None
        self.new_level_up = None
        self._create_fleet()

        # The buttons creating
        self.play_button = Button(self, "Play", 200, 50, (205, 92, 92), (255, 255, 255), 48, 530, 420)
        self.easy_level_button = Button(self, "Easy", 100, 40, (0, 255, 0), (255, 255, 255), 24, 430, 490)
        self.normal_level_button = Button(self, "Normal", 100, 40, (255, 215, 0), (255, 255, 255), 24, 580, 490)
        self.hard_level_button = Button(self, "Hard", 100, 40, (255, 0, 0), (255, 255, 255), 24, 730, 490)
        self.reset_high_score_button = Button(self, "Reset", 70, 20, (96, 96, 96), (255, 255, 255), 20,
                                              (self.sb.high_score_rect.right + 10), 25)
        self.ok_button = None

    def run_game(self):
        """The main cycle of the game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update_position()
                self.shield.move_power_shield()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        # The events monitoring
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)
                self.check_level_choice_button(mouse_pos)
                self.check_reset_button(mouse_pos)
                self._check_ok_button(mouse_pos)
                self._check_start_new_level_button(mouse_pos)

    def check_play_button(self, mouse_pos):
        """Start the new game when user press the'Play' button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        self._start_game_with_play_button(button_clicked)

    def check_reset_button(self, mouse_pos):
        """Reset the high score to zero if user clicked the 'reset' button"""
        button_clicked = self.reset_high_score_button.rect.collidepoint(mouse_pos)
        if button_clicked and int(self.sb.read_high_score()) > 0:
            with open('high_score.txt', 'w') as file_object:
                file_object.write(str(self.stats.high_score))
            self.sb.prep_high_score()
            self.reset_high_score_button.rect.x = self.sb.high_score_rect.right + 10
            self.reset_high_score_button.prep_msg("Done")

    def _check_ok_button(self, mouse_pos):
        """Hide the level buttons messages"""
        try:
            button_ok_clicked = self.ok_button.rect.collidepoint(mouse_pos)
            if button_ok_clicked and self.stats.game_active is not True:
                self.message_image.fill(self.settings.bg_color)
                self.ok_button = Button(self, "", 0, 0, (96, 96, 96), (96, 96, 96), 0, 600, 475)
        except AttributeError:
            pass

    def _check_start_new_level_button(self, mouse_pos):
        """Start next level with button clicked"""
        try:
            button_clicked = self.start_new_level_button.rect.collidepoint(mouse_pos)
            if button_clicked:
                # Icrease the game level
                self._start_new_level()
                self.start_new_level_button = Button(self, "", 0, 0, (96, 96, 96), (96, 96, 96), 0, 0, 0)
        except AttributeError:
            pass

    def _check_keydown_events(self, event):
        """Reaction on pressing buttons"""
        if event.key == pygame.K_RIGHT:
            # Replace the spaceship on 1 pix right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Replace the spaceship on 1 pix left
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_F12:
            # Open the game in the fullscreen mode
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
            self.ship.rect.y += 100
            self.ship.screen_rect.right += 168
            self._create_fleet()
        elif event.key == pygame.K_ESCAPE:
            # Exit from the fullscreen mode
            self.screen = pygame.display.set_mode((1200, 670))
            if self.ship.x < 0:
                self.ship.x = 0
            elif self.ship.x > 1200:
                self.ship.x -= 168
            self.ship.rect.y -= 100
            self.ship.screen_rect.right -= 168
            self._create_fleet()
        elif event.key == pygame.K_p:
            self._start_game_with_p_button()
        elif event.key == pygame.K_n:
            self._start_next_level_with_n_button()
        elif event.key == pygame.K_s:
            self.shield.show_shield = True
        elif event.key == pygame.K_a:
            self.shield.show_shield = False

    def _check_keyup_events(self, event):
        """Reaction wnen a button is not pressed"""
        if event.key == pygame.K_RIGHT:
            # Do not move the spaceship
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _start_game_with_play_button(self, button_clicked):
        if button_clicked and not self.stats.game_active:
            # Set up the dynamic settings
            self.settings.ititialize_dynamic_settings()

            # Update the game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_images()

            # Clear the aliens fleet and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and put the ship to the screen center
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _start_game_with_p_button(self):
        if not self.stats.game_active:
            # Set up the dynamic settings
            self.settings.ititialize_dynamic_settings()

            # Update the game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_images()

            # Clear the aliens fleet and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and put the ship to the screen center
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _start_next_level_with_n_button(self):
        """This method respons for starting a next game level"""
        self._start_new_level()
        self.start_new_level_button = Button(self, "", 0, 0, (96, 96, 96), (96, 96, 96), 0, 0, 0)

    def check_level_choice_button(self, mouse_pos):
        """This is the method for choosing the game level by a user"""
        button_easy_clicked = self.easy_level_button.rect.collidepoint(mouse_pos)
        button_normal_clicked = self.normal_level_button.rect.collidepoint(mouse_pos)
        button_hard_clicked = self.hard_level_button.rect.collidepoint(mouse_pos)
        if button_easy_clicked:
            self.settings.speed_up_scale += 0
            self.prep_level_buttons_messages("You have chosen an easy game level")
            self.ok_button_show = True
            self.ok_button = Button(self, "Ok", 70, 20, (119, 136, 153), (255, 255, 255), 20, 600, 575)
        elif button_normal_clicked:
            self.settings.speed_up_scale += 0.01
            self.prep_level_buttons_messages("You have chosen a normal game level")
            self.ok_button_show = True
            self.ok_button = Button(self, "Ok", 70, 20, (119, 136, 153), (255, 255, 255), 20, 600, 575)
        elif button_hard_clicked:
            self.settings.speed_up_scale += 0.02
            self.prep_level_buttons_messages("You have chosen a hard game level. Be careful!")
            self.ok_button_show = True
            self.ok_button = Button(self, "Ok", 70, 20, (119, 136, 153), (255, 255, 255), 20, 600, 575)

    def prep_level_buttons_messages(self, message: str):
        """This method prepares the messages images for level buttons clicked"""
        self.message_image = self.font.render(message, True, self.settings.font_color, self.settings.bg_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.play_button.rect.center
        self.message_image_rect.y = 550
        self.blit_level_buttons_messages(self.message_image, self.message_image_rect)

    def blit_level_buttons_messages(self, message_image, message_image_rect):
        """This method blits the messages images for level buttons clicked"""
        self.screen.blit(message_image, message_image_rect)

    def _create_fleet(self):
        """Create a fleet of aliens"""
        # Available space of screen on x equil screen width - two alien widthes
        # Available aliens number equil available space of screen on x / two alien widthes
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # Available space of screen on y equil screen height - three alien heights - spaceship height
        # Available range aliens number equil available space of screen on y / two alien heights
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # Create an alien and add it to range
        # Create ranges
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        randon_number = random.randint(-35, 10)
        alien_width, alien_height = alien.rect.size
        if self.stats.game_active and self.stats.level >= 4:
            alien_x = (alien_width + 2 * alien_width * alien_number) + randon_number
            alien.rect.x = alien_x
            alien.rect.y = ((alien_height + 2 * alien_height * row_number) + 50) + randon_number
            self.aliens.add(alien)
        else:
            alien_x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien_x
            alien.rect.y = (alien_height + 2 * alien_height * row_number) + 50
            self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Check if any of aliens reached the edge of screen"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Move the fleet down and change its direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        # Repainting the screen after each cycle iteration
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score image in the screen
        self.sb.show_score()

        # Drawing the play and other button if the game is not active
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_level_button.draw_button()
            self.normal_level_button.draw_button()
            self.hard_level_button.draw_button()
            self.reset_high_score_button.draw_button()
            self.sb.read_high_score()

            # Painting the level buttons clicked massages images
            self.blit_level_buttons_messages(self.message_image, self.message_image_rect)
            if self.ok_button_show:
                self.ok_button.draw_button()
        if self.new_level_up:
            self.start_new_level_button.draw_button()
        if self.shield.show_shield and self.stats.game_active:
            self.shield.blit_power_shield()

        # Show the last painted screen
        pygame.display.flip()

    def _fire_bullet(self):
        # Adding new bullet to group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """The method for bullets updating"""
        # Bullets positions updating
        self.bullets.update()
        # Removing bullets that out of the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Removing shot aliens
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points * len(alien)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.aliens.empty()
            self.bullets.empty()
            self.new_level_up = True
            self.shield.show_shield = False
            self.start_new_level_button = Button(self, 'Next level', 170, 50, (255, 153, 51), (255, 255, 255), 48, 530,
                                                 335)
            pygame.mouse.set_visible(True)
            self.ship.center_ship()

    def _start_new_level(self):
        """Increase the level when bullet alien collisions"""
        # Delete remaining bullets and create a new fleet
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()
        self.stats.level += 1
        self.sb.prep_level()
        pygame.mouse.set_visible(False)

    def _update_aliens(self):
        """Check the fleet is on the screen edge and update fleet position"""
        self._check_fleet_edges()
        self.aliens.update()

        # Check if any allien touched the ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check if the aliens from the group reached the bottom of the screen
        self._check_aliens_bottom()

    def _ship_hit(self):
        """This method regulates what we do when aliens hit the ship"""
        if self.stats.ships_left > 0:
            # Refuse ship_left from statistic and update the scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Delete the remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new one fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.sb.prep_high_score()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()

    def _check_aliens_bottom(self):
        """Check if at least one alien from the group reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Have the same behavior if the aliens hit the ship
                self._ship_hit()
                break

if __name__ == "__main__":
    # Creating the game object and run the game
    ai = AlienInvasion()
    ai.run_game()
