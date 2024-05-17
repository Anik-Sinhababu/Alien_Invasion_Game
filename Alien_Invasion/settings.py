from random import randint

class Settings:
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = "black"
        self.ship_speed = 7
        self.bullet_speed = 7.0
        self.alien_bullet_speed = 5
        self.bullet_width = 3
        self.bullet_height = 12
        self.bullet_color = ("orange")
        self.bullets_allowed = 4
        self.alien_speed = 2
        self.fleet_drop_speed = 5
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
