import math
import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from random import randint
from star import Stars
from galaxy import Galaxy
from draw_obj import DrawableObject
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        pygame.init()  # The pygame.init() function is a crucial part of any Pygame application. When called,
        # it initializes all the Pygame modules needed for your game or application to run properly.
        self.settings = Settings()
        """Settings() calls the constructor (__init__ method) of the Settings class, creating a new 
        instance of the class."""
        # By creating a separate Settings class and instantiating it within another class (e.g., the main game class)
        # , you're following principles of encapsulation and modularity.
        # This separation of concerns allows you to manage game settings independently and easily modify them
        # without affecting other parts of the code.
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height),
                                              pygame.FULLSCREEN)
        self.stats = GameStats(self)
        self.play_button = Button(self, "Play")
        # pygame.display.set_mode(): This function creates a window for displaying graphics. It takes a tuple as an
        # argument, specifying the dimensions (width and height) of the window. self.settings.screen_width and
        # self.settings.screen_height: These attributes hold the width and height of the game window, respectively.
        # They are accessed from the settings object, which is an instance of the Settings class that stores various
        # game settings.
        self.clock = pygame.time.Clock()
        # Overall, self.clock = pygame.time.Clock() is used to create a Clock object that helps regulate the timing
        # and frame rate of your game, ensuring a consistent and smooth player experience.
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.ship_group = pygame.sprite.GroupSingle(self.ship)
        self.saturn = DrawableObject(self, "images/sun1.png", (500, 500), (1100, -300))
        self.black_hole = DrawableObject(self, "images/black_hole.png", (1000, 1000), (300, 0))
        self.logo = DrawableObject(self, "images/logo.png", (300, 300), (self.settings.screen_width/2 - 350, (self.settings.screen_height/2) - 500))
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.galaxies = pygame.sprite.Group()
        self._create_fleet()
        self._create_star_fleet()
        self._create_galaxy_fleet()
        # A sprite is a graphical object that can be drawn onto the screen. In the context of game development,
        # a sprite often represents a game entity such as a player character, enemy, projectile, item,
        # or environmental element.
        # Grouping and Management: Sprites can be organized into groups for efficient
        # management and manipulation. Pygame provides the pygame.sprite.Group class, which allows you to group
        # sprites together and perform operations on the entire group, such as updating, drawing, or collision
        # detection.
        pygame.mixer.music.load("music/music.mp3")
        pygame.mixer.music.play(loops=-1)
        self.explosion_sound = pygame.mixer.Sound("music/explosion.mp3")
        self.fire_sound = pygame.mixer.Sound("music/fire.mp3")
        self.game_over_sound = pygame.mixer.Sound("music/game_over.mp3")
        self.wave_complete = pygame.mixer.Sound("music/wave.mp3")
        self.settings.screen_width = self.screen.get_rect().width
        # The line self.settings.screen_width = self.screen.get_rect().width retrieves the width of the game window
        # and assigns it to the screen_width attribute in the Settings object. Here's what it does:
        #
        # self.screen.get_rect().width:
        #
        # self.screen refers to the game window surface created using Pygame's pygame.display.set_mode() function.
        # The get_rect() method returns a Rect object that represents the dimensions and position of the surface.
        # width retrieves the width of the Rect object, which corresponds to the width of the game window.
        self.settings.screen_height = self.screen.get_rect().height
        # same as above but for the height
        self.last_alien_shot_time = pygame.time.get_ticks()
        self.game_active = False
        self.sb = Scoreboard(self)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()
            self.alien_bullets.empty()
            if self.stats.level % 2 == 0:
                self._create_fleet()
            else:
                self._create_circular_fleet()
            self.ship.center_ship()
            self.sb.prep_level()
            self.sb.prep_ships()
            pygame.mouse.set_visible(False)



    def _check_keydown_event(self, event):
        if event.key == pygame.K_d:
            if self.ship.rect.right < self.settings.screen_width:
                self.ship.move_right = True
        elif event.key == pygame.K_a:
            if self.ship.rect.left > 0:
                self.ship.move_left = True
        elif event.key == pygame.K_w:
            if self.ship.rect.top < self.settings.screen_height:
                self.ship.move_up = True
        elif event.key == pygame.K_s:
            if self.ship.rect.bottom > 0:
                self.ship.move_down = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if len(self.bullets) <= self.settings.bullets_allowed:
                self._fire_bullet()
                self.fire_sound.play()

    def check_keyup_event(self, event):
        if event.key == pygame.K_d:
            self.ship.move_right = False
        elif event.key == pygame.K_a:
            self.ship.move_left = False
        elif event.key == pygame.K_w:
            self.ship.move_up = False
        elif event.key == pygame.K_s:
            self.ship.move_down = False

    def _create_star(self, x_position, y_position):
        size = randint(6, 15)
        new_star = Stars(self, size)
        new_star.x = x_position
        new_star.rect.x = x_position
        new_star.rect.y = y_position
        self.stars.add(new_star)

    def _create_galaxy(self, x_position, y_position):
        size = randint(300, 600)
        new_galaxy = Galaxy(self, size)
        new_galaxy.x = x_position
        new_galaxy.rect.x = x_position
        new_galaxy.rect.y = y_position
        self.stars.add(new_galaxy)

    def _create_galaxy_fleet(self):
        galaxy = Galaxy(self, 100)
        galaxy_width, galaxy_height = galaxy.rect.size
        current_x, current_y = galaxy_width, galaxy_height
        while current_y <= self.settings.screen_height:
            while current_x <= self.settings.screen_width:
                self._create_galaxy(current_x, current_y)
                i = randint(2, 4)
                current_x += i * i * galaxy_width
            current_x = galaxy_width
            current_y += i * i * galaxy_height

    def _create_star_fleet(self):
        star = Stars(self, 15)
        star_width, star_height = star.rect.size
        current_x, current_y = star_width, star_height
        while current_y <= self.settings.screen_height:
            while current_x <= self.settings.screen_width:
                self._create_star(current_x, current_y)
                i = randint(2, 4)
                current_x += i * i * star_width
            current_x = star_width
            current_y += i * i * star_height

    def _update_stars(self):
        self.stars.update()

    def _update_galaxies(self):
        self.galaxies.update()

    def _update_aliens(self):
        now = pygame.time.get_ticks()
        if now - self.last_alien_shot_time > randint(2000, 6000):  # Check if 1 second has passed
            for alien in self.aliens.sprites():
                self._alien_fire_bullet(alien)
            self.last_alien_shot_time = now
        self._check_fleet_edges()
        self.aliens.update(self)
        collision = pygame.sprite.spritecollideany(self.ship, self.aliens)
        if collision:
            self.game_over_sound.play()
            collision_point = collision.rect.center
            self._ship_hit(collision_point)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _alien_fire_bullet(self, alien):
        new_bullet = Bullet(self, alien.rect.midbottom, direction='down', color= "cyan")
        self.alien_bullets.add(new_bullet)

    def _update_alien_bullets(self):
        self.alien_bullets.update()
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)
        collision = pygame.sprite.spritecollideany(self.ship, self.alien_bullets)
        if collision:
            self.game_over_sound.play()
            collision_point = collision.rect.center
            self._ship_hit(collision_point)

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        h = self.settings.screen_height - 200
        w = self.settings.screen_width - 300
        while current_y < (h - (3 * alien_height)):
            while current_x < (w - (2 * alien_width)):
                self._create_alien(current_x, current_y)
                i = randint(2, 4)
                current_x += (i * alien_width)
            current_x = alien_width
            current_y += (i * alien_height)

    def _create_circular_fleet(self):
        num_aliens = randint(8, 16)
        radius = 200
        center_x = self.settings.screen_width/3
        center_y = self.settings.screen_height/3
        for i in range(num_aliens):
            angle = 2 * math.pi * i/num_aliens
            x_pos = center_x + radius * math.cos(angle)
            y_pos = center_y + radius * math.sin(angle)
            self._create_alien(x_pos, y_pos)

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_highest_score()
            self.explosion_sound.play()
        if not self.aliens:
            self.wave_complete.play()
            self.bullets.empty()
            self.alien_bullets.empty()
            if self.stats.level % 2 == 0:
                self._create_circular_fleet()
            else:
                self._create_fleet()

            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _ship_hit(self, collision_point = None):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            explosion_position = collision_point or self.ship.rect.center
            self.bullets.empty()
            self.alien_bullets.empty()
            self.aliens.empty()
            if self.stats.level%2 == 0:
                self._create_fleet()
            else:
                self._create_circular_fleet()
            self.ship.center_ship()
            self._show_explosion(explosion_position)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _show_explosion(self, position):
        """Display the explosion image at the given position."""
        frame_count = len(self.ship.explosion_frames)
        for frame_index in range(frame_count):
            self.screen.fill(self.settings.bg_color)
            self.ship.blit_explosion(position, frame_index)
            pygame.display.flip()
            pygame.time.delay(16)  # Adjust the delay for animation speed


    def _update_screen(self):
        if not self.game_active:
            self.logo.draw()
            self.play_button.draw_button()
            font = pygame.font.Font("pdark.ttf", 66)
            text = font.render("Alien Invasion", True, "red", (50, 50, 50))
            textRect = text.get_rect()
            textRect.center = (self.settings.screen_width / 2, self.settings.screen_height / 2 + 140)
            self.screen.blit(text, textRect)
            pygame.display.flip()
        else:
            self.screen.fill(self.settings.bg_color)
            self.sb.show_score()
            self.stars.draw(self.screen)
            self.galaxies.draw(self.screen)
            #self.saturn.draw()
            self.aliens.draw(self.screen)
            if self.ship in self.ship_group:
                self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            for bullet in self.alien_bullets.sprites():
                bullet.draw_bullet()
            pygame.display.flip()

    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self._update_stars()
                self._update_galaxies()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_alien_bullets()
            self._update_screen()
            self.clock.tick(60)


if __name__ == "__main__":
    """The if __name__ == "__main__": statement is a common Python idiom used to check whether the current script is 
    being run as the main program or if it's being imported as a module into another script.
    When a Python script is executed, the special variable __name__ is set to "__main__" if the script is being run 
    directly. However, if the script is being imported as a module into another script, then __name__ is set to the name 
    of the module."""
    ai = AlienInvasion()
    ai.run_game()
