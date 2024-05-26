import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game, position=None, direction='up', color = None):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = color if color else self.settings.bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        if position:
            self.rect.midtop = position
        else:
            self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)
        self.direction = direction

    def update(self):
        if self.direction == 'up':
            self.y -= self.settings.bullet_speed

        elif self.direction == 'down':
            self.y += self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
