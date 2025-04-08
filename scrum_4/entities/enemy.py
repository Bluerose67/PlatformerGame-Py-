import pygame
import os
from config import ENEMY_SPEED, TILE_SIZE, SCALE_FACTOR, SCALED_TILE

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type="slime"):
        super().__init__()
        self.enemy_type = enemy_type
        self.assets = self.load_assets()
        self.image = self.assets["walk"]
        self.rect = self.image.get_rect(midbottom=(x + SCALED_TILE//2, y + SCALED_TILE))
        self.start_x = x  # Patrol start position
        self.x_vel = ENEMY_SPEED
        self.direction = 1  # 1=right, -1=left
        self.patrol_distance = SCALED_TILE * 3  # Patrol 3 tiles width

    def load_assets(self):
        assets = {}
        base_path = os.path.join("assets", "enemy")
        
        if self.enemy_type == "slime":
            assets["walk"] = self.load_scaled_image(f"{base_path}/Slimewalk_2.png")
        else:  # worm
            assets["walk"] = self.load_scaled_image(f"{base_path}/wormGreen_walk.png")
        return assets

    def load_scaled_image(self, path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, 
            (int(TILE_SIZE * SCALE_FACTOR), 
             int(TILE_SIZE * SCALE_FACTOR)))

    def patrol(self):
        """Reverse direction when reaching patrol boundaries"""
        if abs(self.rect.x - self.start_x) > self.patrol_distance:
            self.x_vel *= -1
            self.direction *= -1

    def update(self):
        # Horizontal movement
        self.rect.x += self.x_vel
        
        # Reverse direction at patrol boundaries
        if abs(self.rect.x - self.start_x) > self.patrol_distance:
            self.x_vel *= -1
            self.direction *= -1
        
        # Update sprite facing direction
        if self.direction < 0:
            self.image = pygame.transform.flip(self.assets["walk"], True, False)
        else:
            self.image = self.assets["walk"]

    def update_animation(self):
        self.animation_timer += 1
        self.state = "walk" if abs(self.x_vel) > 0 else "idle"
        if self.animation_timer >= 10:  # Animation speed
            self.animation_timer = 0

    def handle_sprite_flip(self):
        # Only flip if direction changed
        new_direction = 1 if self.x_vel > 0 else -1 if self.x_vel < 0 else self.direction
        if new_direction != self.direction:
            self.direction = new_direction
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, surface, offset_x, offset_y):
        surface.blit(self.image, 
            (self.rect.x - offset_x, 
             self.rect.y - offset_y))