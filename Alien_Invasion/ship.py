import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        super().__init__()
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect.
        self.image = pygame.transform.scale(pygame.image.load('images/redfighter0005.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.x = float(self.rect.x)

        # Start each new ship at the bottom center of the screen.

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

    def update(self):
        if self.move_right:
            if self.rect.right < self.settings.screen_width:
                self.rect.x += self.settings.ship_speed
        if self.move_left:
            if self.rect.left > 0:
                self.rect.x -= self.settings.ship_speed
        if self.move_up:
            if self.rect.top > 0:
                self.rect.y -= self.settings.ship_speed
        if self.move_down:
            if self.rect.bottom < self.settings.screen_height:
                self.rect.y += self.settings.ship_speed

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
