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
        
        states = {
            "stand": "alienGreen_stand",
            "walk1": "alienGreen_walk1",
            "walk2": "alienGreen_walk2",
            "jump": "alienGreen_Jump"  # Match your actual filename case
        }

        for state, filename in states.items():
            path = os.path.join("assets", "player", f"{filename}.png")
            original_image = pygame.image.load(path).convert_alpha()
            scaled_image = pygame.transform.scale(original_image,
                                                (SCALED_TILE, SCALED_TILE))
            assets[state] = scaled_image
        return assets

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        # Print position only when actually moving
        if dx != 0 or dy != 0:
            print(f"Player Position: X={self.rect.x}, Y={self.rect.y}")

    def jump(self):
        if self.jump_count < 2:
            self.y_vel = -self.GRAVITY * 8
            self.jump_count += 1
            # Play jump sound
            if hasattr(self, 'game'):  # Reference to game instance
                self.game.sounds["jump"].play()

    def update_animation(self):
        if self.y_vel < 0:
            self.state = "jump"
        elif self.x_vel != 0:
            self.state = "walk1" if pygame.time.get_ticks() % 200 < 100 else "walk2"
        else:
            self.state = "stand"

        self.image = pygame.transform.flip(self.assets[self.state], 
                                         self.direction == "left", False)