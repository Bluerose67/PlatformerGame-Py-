import pygame
import os
from config import TILE_SIZE, GRAVITY, ANIMATION_DELAY, SCALED_TILE, SCALE_FACTOR

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game=None):
        super().__init__()
        self.assets = self.load_assets()
        self.rect = pygame.Rect(x, y, SCALED_TILE, SCALED_TILE)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "right"
        self.animation_count = 0
        self.jump_count = 0
        self.state = "stand"
        self.game = game
        self.image = self.assets[self.state]  # Initialize with stand image

    def load_assets(self):
        assets = {}
        states = ["stand", "walk1", "walk2", "jump"]
        
        # Create fall state by reusing jump assets if needed
        for state in states:
            path = os.path.join("assets", "player", f"alienGreen_{state}.png")
            original_image = pygame.image.load(path).convert_alpha()
            scaled_image = pygame.transform.scale(original_image,
                                                (SCALED_TILE, SCALED_TILE))
            assets[state] = scaled_image
        
        # Use jump sprite for fall if no dedicated fall sprite
        assets["fall"] = assets["jump"]
        return assets


    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def jump(self):
        if self.jump_count < 2:
            self.y_vel = -GRAVITY * 15
            self.jump_count += 1
            if self.game:
                self.game.sounds["jump"].play()

    def update_animation(self):
        # State transitions
        if self.y_vel < 0:
            self.state = "jump"
        elif self.y_vel > GRAVITY * 1.5:
            self.state = "fall"
        elif self.x_vel != 0:
            # Alternate between walk animations
            self.state = "walk1" if (self.animation_count // ANIMATION_DELAY) % 2 == 0 else "walk2"
        else:
            self.state = "stand"

        # Get the correct sprite
        try:
            sprite = self.assets[self.state]
        except KeyError:
            # Fallback to stand sprite if state doesn't exist
            sprite = self.assets["stand"]
            
        # Apply direction flip
        self.image = pygame.transform.flip(sprite, self.direction == "left", False)
        self.animation_count += 1