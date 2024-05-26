import pygame
from pygame.sprite import Sprite
from random import randint

class Galaxy(Sprite):
    def __init__(self, ai_game, size):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.transform.smoothscale(pygame.image.load("images/galaxy.png"), (size, size))
        self.rect = self.image.get_rect()

        # Initial position: spread stars across the screen
        self.rect.x = randint(0, self.screen_rect.width - self.rect.width)
        self.rect.y = randint(0, self.screen_rect.height - self.rect.height)

        self.y = float(self.rect.y)
        self.speed = 3  # Adjust as needed

    def update(self):
        # Move the star downwards
        self.y += self.speed
        self.rect.y = self.y

        # If star reaches the bottom of the screen, reset its position to the top
        if self.rect.top >= self.screen_rect.bottom:
            self.rect.bottom = 0
            self.rect.x = randint(0, self.screen_rect.width - self.rect.width)
            self.y = float(self.rect.y)