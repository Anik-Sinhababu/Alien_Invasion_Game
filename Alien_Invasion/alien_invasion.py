import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
    """Overall class to manage game assets and behavior"""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            pygame.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    """The if __name__ == "__main__": statement is a common Python idiom used to check whether the current script is 
    being run as the main program or if it's being imported as a module into another script.
    When a Python script is executed, the special variable __name__ is set to "__main__" if the script is being run 
    directly. However, if the script is being imported as a module into another script, then __name__ is set to the name 
    of the module."""
    ai = AlienInvasion()
    ai.run_game()
