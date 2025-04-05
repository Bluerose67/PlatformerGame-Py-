import pygame
import os
from config import TILE_SIZE, GRAVITY, ANIMATION_DELAY, SCALED_TILE, SCALE_FACTOR

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.assets = self.load_assets()
        self.rect = pygame.Rect(x * SCALE_FACTOR, y * SCALE_FACTOR, SCALED_TILE, SCALED_TILE)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "right"
        self.animation_count = 0
        self.jump_count = 0
        self.state = "idle"

    def load_assets(self):
        assets = {}
        states = ["stand", "walk1", "walk2", "jump"]
        for state in states:
            path = os.path.join("assets", "player", f"alienGreen_{state}.png")
            original_image = pygame.image.load(path).convert_alpha()
            scaled_image = pygame.transform.scale(original_image,
                                                (SCALED_TILE, SCALED_TILE))
            assets[state] = scaled_image
        return assets

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        if self.y_vel < 0:
            self.state = "jump"
        elif self.x_vel != 0:
            self.state = "walk1" if pygame.time.get_ticks() % 200 < 100 else "walk2"
        else:
            self.state = "stand"

        self.image = pygame.transform.flip(self.assets[self.state], 
        self.direction == "left", False)