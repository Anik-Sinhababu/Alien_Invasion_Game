import pygame
from pygame.sprite import Sprite
from PIL import Image


class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        super().__init__()
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect.
        self.original_image = pygame.transform.smoothscale(pygame.image.load('images/ship.png'), (100, 100))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.explosion_frames = self._load_explosion_frames('images/explosion.gif')

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

    def center_ship(self):
            self.rect.midbottom = self.screen_rect.midbottom
            self.x = float(self.rect.x)
            self.y = float(self.rect.y)

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def _load_explosion_frames(self, gif_path):
        """Draw the explosion image at the given position."""
        explosion_frames = []
        gif = Image.open(gif_path)
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = pygame.image.fromstring(gif.tobytes(), gif.size, gif.mode)
            frame_image = pygame.transform.scale(frame_image, (130, 130))
            explosion_frames.append(frame_image)
        return explosion_frames

    def blit_explosion(self, position, frame_index):
        """Draw the explosion image at the given position."""
        explosion_rect = self.explosion_frames[frame_index].get_rect(center=position)
        self.screen.blit(self.explosion_frames[frame_index], explosion_rect)

    def resize(self, width, height):
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()

