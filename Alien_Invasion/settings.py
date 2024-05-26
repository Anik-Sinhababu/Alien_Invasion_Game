from random import randint

class Settings:
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = "black"
        self.bullet_width = 3
        self.bullet_height = 20
        self.bullet_color = ("orange")
        self.bullets_allowed = 4
        self.fleet_drop_speed = 9
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.ship_limit = 3
        self.speedup_scale = 0.3
        self.score_scale = 1.2

    def initialize_dynamic_settings(self):
        self.alien_speed = 4
        self.ship_speed = 7
        self.bullet_speed = 9.0
        self.alien_bullet_speed = 5
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed += self.speedup_scale
        self.bullet_speed += self.speedup_scale
        self.alien_bullet_speed += self.speedup_scale
        self.ship_speed += self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

