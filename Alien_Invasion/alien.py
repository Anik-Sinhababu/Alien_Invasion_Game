import pygame
from pygame.sprite import Sprite
from game_stats import GameStats


class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.image = pygame.transform.smoothscale(pygame.image.load("images/alien.png"), (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.settings = ai_game.settings

    def update(self, ai_game):
        if ai_game.stats.level%2 == 0:
            self.x += self.settings.alien_speed * self.settings.fleet_direction
            self.y += self.settings.alien_speed * self.settings.fleet_direction
            self.rect.x = self.x
            self.rect.y = self.y

        else:
            self.x += self.settings.alien_speed * self.settings.fleet_direction
            self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= screen_rect.left) or (self.rect.bottom >= screen_rect.height) or (self.rect.top <= 0)


