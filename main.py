import random
import sys
import pygame
from time import sleep
import pygame.font
import pygame.mixer

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien_bullet import AlienBullet
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
        pygame.mixer.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Sounds of the game
        self.play_click = pygame.mixer.Sound("sounds/play_button.wav")
        self.level_choice_button_click = pygame.mixer.Sound("sounds/easy_normal_hard_level_buttons.wav")
        self.reset_and_ok_click = pygame.mixer.Sound("sounds/reset_and_ok_buttons.wav")
        self.power_shield_sound = pygame.mixer.Sound("sounds/power_shield.wav")
        self.alien_bullets_sound = pygame.mixer.Sound("sounds/alien_bullets.wav")
        self.alien_explosion = pygame.mixer.Sound("sounds/alien_explosion.wav")
        self.bullets_sound = pygame.mixer.Sound("sounds/bullet_fire.wav")

        # The main objects of the game
        self.ship = Ship(self)
        self.shield = Shield(self)
        self.aliens = pygame.sprite.Group()
        self.red_aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()

        # The font attributes
        self.font = pygame.font.SysFont(None, self.settings.font_size)
        self.font_message = None
        self.message_image = self.font.render(self.font_message, True, self.settings.font_color, self.settings.bg_color)
        self.message_image_rect = self.message_image.get_rect()
        self.ok_button_show = None
        self.new_level_up = None

        # The buttons creating
        self.play_button = Button(self, "Play", 200, 50, (205, 92, 92), (255, 255, 255), 48, 530, 420)
        self.easy_level_button = Button(self, "Easy", 100, 40, (0, 255, 0), (255, 255, 255), 24, 430, 490)
        self.normal_level_button = Button(self, "Normal", 100, 40, (255, 215, 0), (255, 255, 255), 24, 580, 490)
        self.hard_level_button = Button(self, "Hard", 100, 40, (255, 0, 0), (255, 255, 255), 24, 730, 490)
        self.reset_high_score_button = Button(self, "Reset", 70, 20, (96, 96, 96), (255, 255, 255), 20,
                                              (self.sb.high_score_rect.right + 10), self.sb.high_score_rect.y - 1)
        self.ok_button = None
        self.start_new_level_button = None
        self.work_next_level_button_with_n = False

        # Create a fleet when starting game
        self._create_fleet()

    def run_game(self):
        """The main cycle of the game"""

        # The main game music settings
        pygame.mixer.music.load("sounds/background.wav")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.7)

        while True:
            if self.stats.game_active:
                self.ship.update_position()
                self.shield.move_power_shield()
                self._update_bullets()
                self.show_alien_bullets()
                self._update_aliens()

            self._check_events()
            self._update_screen()

    def _check_events(self):
        # The game events monitoring
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
        """Start a new game when a user press the 'Play' button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        self._start_game_with_play_button(button_clicked)

    def check_reset_button(self, mouse_pos):
        """Reset the high score to zero if user clicked the 'reset' button"""
        button_clicked = self.reset_high_score_button.rect.collidepoint(mouse_pos)
        if button_clicked and int(self.sb.read_high_score()) > 0:
            self.reset_and_ok_click.play()
            with open('high_score.txt', 'w') as file_object:
                file_object.write(str(self.stats.high_score))
            self.sb.prep_high_score()
            self.reset_high_score_button.rect.x = self.sb.high_score_rect.right + 10
            self.reset_high_score_button.prep_msg("Done")

    def _check_ok_button(self, mouse_pos):
        """Hide the level buttons messages"""
        try:
            button_ok_clicked = self.ok_button.rect.collidepoint(mouse_pos)
            if button_ok_clicked and not self.stats.game_active:
                self.reset_and_ok_click.play()
                self.message_image.fill(self.settings.bg_color)
                self.ok_button = Button(self, "", 0, 0, (96, 96, 96), (96, 96, 96), 0, 600, 475)
        except AttributeError:
            pass

    def _check_start_new_level_button(self, mouse_pos):
        """Start next level with this button clicked"""
        try:
            button_clicked = self.start_new_level_button.rect.collidepoint(mouse_pos)
            if button_clicked:
                self.play_click.play()

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
        elif event.key == pygame.K_p:
            self._start_game_with_p_button()
        elif event.key == pygame.K_n:
            self._start_next_level_with_n_button()
        elif event.key == pygame.K_s:
            self.shield.show_shield = True
        elif event.key == pygame.K_a:
            self.power_shield_sound.stop()
            self.shield.show_shield = False

    def _check_keyup_events(self, event):
        """Reaction wnen a buttons are not pressed"""
        if event.key == pygame.K_RIGHT:
            # Do not move the spaceship
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _start_game_with_play_button(self, button_clicked):
        if button_clicked and not self.stats.game_active:
            # Click sound
            self.play_click.play()

            # Set up the dynamic game settings
            self.settings.ititialize_dynamic_settings()

            # Update the game stats
            self.stats.reset_stats()

            # Start the game and images preparing
            self.stats.game_active = True
            self.sb.prep_images()

            # Clear the aliens fleet and bullets
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            # Create a new fleet and put the ship to the screen center
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor when game is active
            pygame.mouse.set_visible(False)

    def _start_game_with_p_button(self):
        if not self.stats.game_active:
            # Click sound
            self.play_click.play()

            # Set up the dynamic game settings
            self.settings.ititialize_dynamic_settings()

            # Update the game stats
            self.stats.reset_stats()

            # Start the game and images preparing
            self.stats.game_active = True
            self.sb.prep_images()

            # Clear the aliens fleet and bullets
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            # Create a new fleet and put the ship to the screen center
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _start_next_level_with_n_button(self):
        """This method respons for starting a next game level with 'n' button"""
        if self.work_next_level_button_with_n:
            self._start_new_level()
            self.start_new_level_button = Button(self, "", 0, 0, (96, 96, 96), (96, 96, 96), 0, 0, 0)

    def check_level_choice_button(self, mouse_pos):
        """This is the method for choosing the game level by the user"""
        button_easy_clicked = self.easy_level_button.rect.collidepoint(mouse_pos)
        button_normal_clicked = self.normal_level_button.rect.collidepoint(mouse_pos)
        button_hard_clicked = self.hard_level_button.rect.collidepoint(mouse_pos)

        if button_easy_clicked:
            self.level_choice_button_click.play()
            self.settings.speed_up_scale += 0
            self.prep_level_buttons_messages("You have chosen an easy game level")
            self.ok_button_show = True
            self.ok_button = Button(self, "Ok", 70, 20, (119, 136, 153), (255, 255, 255), 20, 600, 575)
        elif button_normal_clicked:
            self.level_choice_button_click.play()
            self.settings.speed_up_scale += 0.01
            self.prep_level_buttons_messages("You have chosen a normal game level")
            self.ok_button_show = True
            self.ok_button = Button(self, "Ok", 70, 20, (119, 136, 153), (255, 255, 255), 20, 600, 575)
        elif button_hard_clicked:
            self.level_choice_button_click.play()
            self.settings.speed_up_scale += 0.02
            self.prep_level_buttons_messages("You have chosen a hard game level. Be careful!")
            self.ok_button_show = True
            self.ok_button = Button(self, "Ok", 70, 20, (119, 136, 153), (255, 255, 255), 20, 600, 575)

    def prep_level_buttons_messages(self, message: str):
        """This method prepares the messages images if level buttons are clicked"""
        self.message_image = self.font.render(message, True, self.settings.font_color, self.settings.bg_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.play_button.rect.center
        self.message_image_rect.y = 550
        self.blit_level_buttons_messages(self.message_image, self.message_image_rect)

    def blit_level_buttons_messages(self, message_image, message_image_rect):
        """This method blits the messages images if level buttons are clicked"""
        self.screen.blit(message_image, message_image_rect)

    def _create_fleet(self):
        """Create a fleet of aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # Available space of screen on x equil screen width - two alien widthes
        # Available aliens number equil available space of screen on x / two aliens widthes
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # Available space of screen on y equil screen height - three alien heights - spaceship height
        # Available range aliens number equil available space of screen on y / two alien heights
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # Create ranges
        for row_number in range(number_rows):
            # Create an alien and add it to a range
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

        # Add red aliens to the fleet
        self._add_red_aliens_to_the_fleet()

    def _add_red_aliens_to_the_fleet(self):
        """Add red aliens when the game is active"""
        if self.stats.game_active:
            self._add_red_aliens()
            self.get_red_aliens_from_the_group()

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        random_number = random.randint(-35, 10)
        alien_width, alien_height = alien.rect.size
        if self.stats.game_active and self.stats.level > 14:
            alien_x = (alien_width + 2 * alien_width * alien_number) + random_number
            alien.rect.x = alien_x
            alien.rect.y = ((alien_height + 2 * alien_height * row_number) + 50) + random_number
            self.aliens.add(alien)
        else:
            alien_x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien_x
            alien.rect.y = (alien_height + 2 * alien_height * row_number) + 50
            self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Check if any aliens reached the edge of the screen"""
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
        # Repainting the game screen and all its elements after each cycle iteration

        self.fill_screen()
        self.show_aliens_ship_score_on_the_screen()
        self.draw_bullets()
        self.show_power_shield_on_the_screen()
        self.show_buttons_on_the_screen()
        self.show_reset_button_on_the_screen()
        self.blit_level_buttons_messages_on_the_screen()

        # Show the last painted screen
        pygame.display.flip()

    def draw_bullets(self):
        """Draw the alien's and ship's bullets on the screen"""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for alien_bullet in self.alien_bullets.sprites():
            alien_bullet.draw_alien_bullet()

    def fill_screen(self):
        self.screen.fill(self.settings.bg_color)

    def show_power_shield_on_the_screen(self):
        if self.shield.show_shield and self.stats.game_active and self.stats.shield_left >= 0 and \
                self.stats.shield_life_remain > 0:
            self.power_shield_sound.play()
            self.shield.blit_power_shield()

    def blit_level_buttons_messages_on_the_screen(self):
        """Painting the level buttons messages images"""
        if not self.stats.game_active:
            self.blit_level_buttons_messages(self.message_image, self.message_image_rect)

    def show_aliens_ship_score_on_the_screen(self):
        """Draw the score, ship and aliens on the screen"""
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()

    def show_reset_button_on_the_screen(self):
        if not self.stats.game_active:
            if int(self.sb.read_high_score()) != 0:
                self.reset_high_score_button.draw_button()
            self.sb.read_high_score()

    def show_buttons_on_the_screen(self):
        """Drawing the play and other buttons on the screen if the game is not active"""
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_level_button.draw_button()
            self.normal_level_button.draw_button()
            self.hard_level_button.draw_button()

            if self.ok_button_show:
                self.ok_button.draw_button()

        if self.new_level_up:
            self.start_new_level_button.draw_button()

    def _fire_bullet(self):
        # Adding a new bullet to the group
        if len(self.bullets) < self.settings.bullets_allowed and self.stats.game_active:
            self.bullets_sound.play()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def show_alien_bullets(self):
        """This method shows the alien bullets on the screen if red aliens appeared"""
        if len(self.alien_bullets) <= 0 and self.red_aliens:
            self._fire_alien_bullet()

    def _fire_alien_bullet(self):
        # Adding a new alien bullet to the group
        if self.red_aliens and self.stats.game_active:
            self.alien_bullets_sound.play()
            new_bullet = AlienBullet(self)
            self.alien_bullets.add(new_bullet)

    def _update_bullets(self):
        """The method for bullets condittions updating"""
        # Bullets positions updating
        self.bullets.update()
        self.alien_bullets.update()

        self.remove_bullets_from_the_screen()

        # Check if any aliens bullet touched the ship
        self._check_alien_bullets_ship_collision()

        # Check if any bullet from the ship touched aliens
        self._check_bullet_alien_collisions()

        # Removing alien's bullets and ship's bullets if they touched the ship's shield
        self._check_power_shield_alian_bullets_collisions()
        self._check_power_shield_bullets_collisions()

    def remove_bullets_from_the_screen(self):
        """Removing bullets that are out of the screen"""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        for alien_bullet in self.alien_bullets.copy():
            if alien_bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(alien_bullet)

    def _check_alien_bullets_ship_collision(self):
        """Check if any alien bullet touched the ship"""
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            for alien_bullet in self.alien_bullets.sprites():
                alien_bullet.kill()
            self._ship_hit()

    def _check_bullet_alien_collisions(self):
        # Adding points to the score for the shot aliens
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            self.alien_explosion.play()

            for alien in collisions.values():
                if self.stats.level > 14:
                    self.stats.score += self.settings.red_alien_points * len(alien)
                else:
                    if alien[0].redness:
                        self.stats.score += self.settings.red_alien_points * len(alien)
                    else:
                        self.stats.score += self.settings.alien_points * len(alien)

            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.prepare_new_game_level()

    def prepare_new_game_level(self):
        """The new game level settings if there are no aliens"""
        if self.stats.level > 29:
            self.power_shield_sound.stop()
            self.bullets_sound.stop()
            self.stats.game_active = False
            self.sb.prep_high_score()
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()
            self._create_fleet()
            pygame.mouse.set_visible(True)
        else:
            self.power_shield_sound.stop()
            self.bullets_sound.stop()
            self.aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()
            self.new_level_up = True
            self.shield.show_shield = False
            self.start_new_level_button = Button(self, 'Next level', 170, 50, (255, 153, 51), (255, 255, 255), 48,
                                                 530, 335)
            self.work_next_level_button_with_n = True
            self.ship.center_ship()
            pygame.mouse.set_visible(True)

    def _check_power_shield_alians_collisions(self):
        """Removing those aliens that touched the ship power shield and minusing shields life points"""
        for alien in self.aliens.sprites():
            if pygame.sprite.spritecollideany(self.shield, self.aliens) and self.shield.show_shield and alien.rect.y \
                    >= self.shield.rect.y and alien.rect.x >= self.shield.rect.x and self.stats.shield_left >= 0 and \
                    self.stats.shield_life_remain > 0:
                self.alien_explosion.play()

                if self.stats.level > 14:
                    alien.kill()
                    self.stats.shield_life_remain -= 1
                    self.sb.prep_shield_life_remain()
                    self.stats.score += self.settings.red_alien_points
                    self.sb.prep_score()
                    self.sb.check_high_score()
                else:
                    if alien.redness:
                        alien.kill()
                        self.stats.shield_life_remain -= 1
                        self.sb.prep_shield_life_remain()
                        self.stats.score += self.settings.red_alien_points
                        self.sb.prep_score()
                        self.sb.check_high_score()
                    else:
                        alien.kill()
                        self.stats.shield_life_remain -= 1
                        self.sb.prep_shield_life_remain()
                        self.stats.score += self.settings.alien_points
                        self.sb.prep_score()
                        self.sb.check_high_score()

        self.minus_power_shield_points()

    def minus_power_shield_points(self):
        """Minus the shields remaining score if it's life points = 0"""
        if self.stats.shield_life_remain < 1:
            self.stats.shield_life_remain = self.settings.shield_life_poitns // 2
            self.sb.prep_shield_life_remain()
            self.stats.shield_left -= 1
            self.sb.prep_shields()

        # Set all power shield indicators to zero if there are no shields left
        if self.stats.shield_left <= -1:
            self.stats.shield_life_remain = 0
            self.sb.prep_shield_life_remain()
            self.stats.shield_left = 0
            self.sb.prep_shields()

    def _check_power_shield_alian_bullets_collisions(self):
        """Removing those alien's bullets that touched the ship power shield and minusing shield life points"""
        for alien_bullet in self.alien_bullets:
            if pygame.sprite.spritecollideany(self.shield, self.alien_bullets) and self.shield.show_shield \
                    and self.stats.shield_left >= 0 and self.stats.shield_life_remain > 0:
                self.stats.shield_life_remain -= 0.01
                self.sb.prep_shield_life_remain()
                alien_bullet.kill()

    def _check_power_shield_bullets_collisions(self):
        """Removing those bullets that touched the ship power shield and minusing shield life points because of that"""
        for bullet in self.bullets:
            if pygame.sprite.spritecollideany(self.shield, self.bullets) and self.shield.show_shield \
                    and self.stats.shield_left >= 0 and self.stats.shield_life_remain > 0:
                self.stats.shield_life_remain -= 0.1
                self.sb.prep_shield_life_remain()
                bullet.kill()

    def _start_new_level(self):
        """Increase the game level and other levels settings"""
        self.play_click.play()

        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()

        self._create_fleet()

        self.settings.increase_speed()

        self.stats.level += 1
        self.sb.prep_level()

        self.work_next_level_button_with_n = False
        pygame.mouse.set_visible(False)

    def _update_aliens(self):
        """This method is for aliens contition updating"""
        self._check_fleet_edges()
        self.aliens.update()

        self._check_aliens_ship_collision()

        # Check if aliens from the group reached the bottom of the screen
        self._check_aliens_bottom()

        # Removing an alien if it touched the ship's power shield
        self._check_power_shield_alians_collisions()

    def _check_aliens_ship_collision(self):
        """Check if any alien touched the ship"""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _check_aliens_bottom(self):
        """Check if at least one alien from the group reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Set the same behavior if the aliens hit the ship
                self._ship_hit()
                break

    def _ship_hit(self):
        """This method regulates what we do when aliens hit the ship"""
        if self.stats.ships_left > 0:
            self.power_shield_sound.stop()

            # Refuse ship_left param from game statistic and update the scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Delete the remaining aliens and bullets
            self.aliens.empty()
            self.red_aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            # Create a new aliens fleet, center the ship and don't change the game level
            self.stats.level -= 1
            self._create_fleet()
            self.ship.center_ship()
            self.stats.level += 1

            # Pause
            sleep(0.5)
        else:
            self.power_shield_sound.stop()

            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self.sb.prep_high_score()

            self.aliens.empty()
            self.red_aliens.empty()
            self.bullets.empty()
            self.alien_bullets.empty()

            self._create_fleet()

    def _add_red_aliens(self):
        """This method (when it called) adds red aliens to the fleet because of the game level"""
        if self.stats.level == 1:  # no red aliens on 1 and 2 levels
            pass
        elif self.stats.level == 2:  # red alien appears on level 3
            self._create_red_alien(4)
            # 1 red alien appeared
        elif self.stats.level == 3:  # red aliens appear on level 4
            self._create_red_alien(26)
            self._create_red_alien(0)
            # 2 red aliens appeared
        elif self.stats.level == 4:  # red aliens appear on level 5
            self._create_red_alien(7)
            self._create_red_alien(4)
            self._create_red_alien(11)
            # 3 red aliens appeared
        elif self.stats.level == 5:  # red aliens appear on level 6
            self._create_red_alien(9)
            self._create_red_alien(20)
            self._create_red_alien(17)
            self._create_red_alien(3)
            # 4 red aliens appeared
        elif self.stats.level == 6:  # red aliens appear on level 7
            self._create_red_alien(21)
            self._create_red_alien(5)
            self._create_red_alien(6)
            self._create_red_alien(14)
            self._create_red_alien(19)
            self._create_red_alien(20)
            # 6 red aliens appeared
        elif self.stats.level == 7:  # red aliens appear on level 8
            self._create_red_alien(22)
            self._create_red_alien(26)
            self._create_red_alien(5)
            self._create_red_alien(14)
            self._create_red_alien(11)
            self._create_red_alien(18)
            self._create_red_alien(3)
            self._create_red_alien(8)
            self._create_red_alien(10)
            # 9 red aliens appeared
        elif self.stats.level == 8:  # red aliens appear on level 9
            self._create_red_alien(9)
            self._create_red_alien(0)
            self._create_red_alien(23)
            self._create_red_alien(21)
            self._create_red_alien(5)
            self._create_red_alien(14)
            self._create_red_alien(19)
            self._create_red_alien(17)
            self._create_red_alien(18)
            self._create_red_alien(11)
            self._create_red_alien(10)
            self._create_red_alien(8)
            self._create_red_alien(2)
            # 13 red aliens appeared
        elif self.stats.level == 9:  # red aliens appear on level 10
            self._create_red_alien(9)
            self._create_red_alien(11)
            self._create_red_alien(13)
            self._create_red_alien(0)
            self._create_red_alien(18)
            self._create_red_alien(26)
            self._create_red_alien(12)
            self._create_red_alien(15)
            self._create_red_alien(2)
            self._create_red_alien(10)
            self._create_red_alien(3)
            self._create_red_alien(19)
            self._create_red_alien(21)
            self._create_red_alien(25)
            self._create_red_alien(1)
            # 15 red aliens appeared
        elif self.stats.level == 10:  # red aliens appear on level 11
            self._create_red_alien(26)
            self._create_red_alien(1)
            self._create_red_alien(11)
            self._create_red_alien(22)
            self._create_red_alien(14)
            self._create_red_alien(16)
            self._create_red_alien(25)
            self._create_red_alien(0)
            self._create_red_alien(12)
            self._create_red_alien(20)
            self._create_red_alien(23)
            self._create_red_alien(19)
            self._create_red_alien(9)
            self._create_red_alien(17)
            self._create_red_alien(5)
            self._create_red_alien(24)
            self._create_red_alien(18)
            self._create_red_alien(7)
            # 18 red aliens appeared
        elif self.stats.level == 11:  # red aliens appear on level 12
            self._create_red_alien(8)
            self._create_red_alien(21)
            self._create_red_alien(9)
            self._create_red_alien(20)
            self._create_red_alien(23)
            self._create_red_alien(3)
            self._create_red_alien(10)
            self._create_red_alien(24)
            self._create_red_alien(11)
            self._create_red_alien(18)
            self._create_red_alien(1)
            self._create_red_alien(25)
            self._create_red_alien(4)
            self._create_red_alien(12)
            self._create_red_alien(17)
            self._create_red_alien(6)
            self._create_red_alien(16)
            self._create_red_alien(13)
            self._create_red_alien(7)
            self._create_red_alien(5)
            # 20 red aliens appeared
        elif self.stats.level == 12:  # red aliens appear on level 13
            self._create_red_alien(9)
            self._create_red_alien(21)
            self._create_red_alien(8)
            self._create_red_alien(22)
            self._create_red_alien(6)
            self._create_red_alien(19)
            self._create_red_alien(20)
            self._create_red_alien(11)
            self._create_red_alien(5)
            self._create_red_alien(18)
            self._create_red_alien(24)
            self._create_red_alien(17)
            self._create_red_alien(4)
            self._create_red_alien(12)
            self._create_red_alien(3)
            self._create_red_alien(16)
            self._create_red_alien(23)
            self._create_red_alien(13)
            self._create_red_alien(14)
            self._create_red_alien(1)
            self._create_red_alien(25)
            self._create_red_alien(26)
            # 22 red aliens appeared
        elif self.stats.level == 13:  # red aliens appear on level 14
            self._create_red_alien(20)
            self._create_red_alien(13)
            self._create_red_alien(5)
            self._create_red_alien(11)
            self._create_red_alien(24)
            self._create_red_alien(21)
            self._create_red_alien(4)
            self._create_red_alien(18)
            self._create_red_alien(19)
            self._create_red_alien(3)
            self._create_red_alien(14)
            self._create_red_alien(26)
            self._create_red_alien(6)
            self._create_red_alien(7)
            self._create_red_alien(2)
            self._create_red_alien(23)
            self._create_red_alien(16)
            self._create_red_alien(8)
            self._create_red_alien(22)
            self._create_red_alien(1)
            self._create_red_alien(9)
            self._create_red_alien(17)
            self._create_red_alien(0)
            self._create_red_alien(10)
            # 24 red aliens appeared
        elif self.stats.level == 14:  # red aliens appear on level 15
            self._create_red_alien(14)
            self._create_red_alien(24)
            self._create_red_alien(7)
            self._create_red_alien(13)
            self._create_red_alien(1)
            self._create_red_alien(20)
            self._create_red_alien(5)
            self._create_red_alien(19)
            self._create_red_alien(0)
            self._create_red_alien(12)
            self._create_red_alien(21)
            self._create_red_alien(18)
            self._create_red_alien(2)
            self._create_red_alien(8)
            self._create_red_alien(23)
            self._create_red_alien(26)
            self._create_red_alien(15)
            self._create_red_alien(3)
            self._create_red_alien(11)
            self._create_red_alien(17)
            self._create_red_alien(4)
            self._create_red_alien(22)
            self._create_red_alien(6)
            self._create_red_alien(9)
            self._create_red_alien(16)
            self._create_red_alien(10)
            # 26 red aliens appeared

    def _create_red_alien(self, alien_position_number):
        """
        Use this method if you want to create a new one red alien in your fleet.
        Repeat this method so much times as you want.
        """
        red_alien = self.aliens.sprites()[alien_position_number]
        red_alien.image = pygame.image.load("images/red_alien.bmp")
        red_alien.redness = True

    def get_red_aliens_from_the_group(self):
        """This method adds the red aliens to the aliens group"""
        for alien in self.aliens.sprites():
            if alien.redness:
                self.red_aliens.add(alien)

if __name__ == "__main__":
    # Creating the game object and run the game
    ai = AlienInvasion()
    ai.run_game()
