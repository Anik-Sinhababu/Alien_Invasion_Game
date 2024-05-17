import pygame


class DrawableObject:
    def __init__(self, ai_game, image_path, size, initial_position):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.transform.scale(pygame.image.load(image_path), size)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position

    def draw(self):
        self.screen.blit(self.image, self.rect)
