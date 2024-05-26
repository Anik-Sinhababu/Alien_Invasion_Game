import pygame

class DrawableObject:
    def __init__(self, ai_game, image_path, initial_size, initial_position):
        self.screen = ai_game.screen
        self.image = pygame.image.load(image_path)
        self.size = initial_size
        self.position = initial_position
        self.update_image()

    def update_image(self):
        self.image = pygame.transform.smoothscale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

    def draw(self):
        self.screen.blit(self.image, self.rect)