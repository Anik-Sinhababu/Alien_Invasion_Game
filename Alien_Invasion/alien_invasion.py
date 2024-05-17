import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from random import randint
from star import Stars
from draw_obj import DrawableObject


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
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
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
        self.saturn = DrawableObject(self, "images/sun1.png", (500, 500), (1100, -200))
        self.black_hole = DrawableObject(self, "images/black_hole.png", (1000, 1000), (300, 0))
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self._create_fleet()
        self._create_star_fleet()
        # A sprite is a graphical object that can be drawn onto the screen. In the context of game development,
        # a sprite often represents a game entity such as a player character, enemy, projectile, item,
        # or environmental element.
        # Grouping and Management: Sprites can be organized into groups for efficient
        # management and manipulation. Pygame provides the pygame.sprite.Group class, which allows you to group
        # sprites together and perform operations on the entire group, such as updating, drawing, or collision
        # detection.
        pygame.mixer.music.load("bg_music.mp3")
        pygame.mixer.music.play(loops=-1)
        self.explosion_sound = pygame.mixer.Sound("explosion.mp3")
        self.fire_sound = pygame.mixer.Sound("fire.mp3")
        self.game_over_sound = pygame.mixer.Sound("game_over.mp3")
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

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _alien_fire_bullet(self, alien):
        new_bullet = Bullet(self, alien.rect.midbottom, direction='down', color="green")
        self.alien_bullets.add(new_bullet)

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_star(self, x_position, y_position):
        size = randint(8, 20)
        new_star = Stars(self, size)
        new_star.x = x_position
        new_star.rect.x = x_position
        new_star.rect.y = y_position
        self.stars.add(new_star)


    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        h = self.settings.screen_height - 200
        w = self.settings.screen_width - 300
        while current_y < (h - (3*alien_height)):
            while current_x < (w - (2*alien_width)):
                self._create_alien(current_x, current_y)
                i = randint(3, 4)
                current_x += (i * alien_width)
            current_x = alien_width
            current_y += (i * alien_height)

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

    def _update_aliens(self):
        now = pygame.time.get_ticks()
        print(now)
        if now - self.last_alien_shot_time > randint(2000, 6000):  # Check if 1 second has passed
            for alien in self.aliens.sprites():
                self._alien_fire_bullet(alien)
            self.last_alien_shot_time = now
        self._check_fleet_edges()
        self.aliens.update()

    def _update_alien_bullets(self):
        self.alien_bullets.update()
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.ship_group, self.alien_bullets, True, True)
        if collisions:
            self.game_over_sound.play()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_event(event)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.explosion_sound.play()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.saturn.draw()
        self.black_hole.draw()
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
