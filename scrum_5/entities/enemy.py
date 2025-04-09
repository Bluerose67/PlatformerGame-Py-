import pygame
import os
from config import ENEMY_SPEED, GRAVITY, TILE_SIZE, ANIMATION_DELAY

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type="slime"):
        super().__init__()
        self.enemy_type = enemy_type
        self.assets = self.load_assets()
        self.rect = self.assets["idle"].get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.assets["idle"])

        self.x_vel = 0
        self.y_vel = 0
        self.direction = 1  # 1=right, -1=left
        self.speed = 2
        self.animation_delay = 10  # Higher = slower animation (player uses 3)
        self.animation_count = 0
        self.current_frame = 0
        self.frames = ["idle", "walk"]  # Our two available frames
        self.state = "idle"
        self.patrol_distance = 200
        self.start_x = x
        self.fall_count = 0
        self.jump_count = 0
        self.grounded = False  # Add grounded state tracker
        # self.rect = pygame.Rect(x, y, 70, 23)
        self.last_grounded_y = y  # Track stable ground position
        self.stable_frames = 0  # Count stable frames
        
        # Match player's physics
        self.gravity = GRAVITY
        self.mask = None
        self.update_sprite()

    def load_assets(self):
        assets = {}
        scale = 0.6
        
        if self.enemy_type == "slime":
            # Use both frames we have
            idle_img = pygame.image.load(os.path.join("assets", "enemy", "Slimeidle_1.png"))
            walk_img = pygame.image.load(os.path.join("assets", "enemy", "Slimewalk_2.png"))
            
            assets["idle"] = pygame.transform.scale(idle_img, 
                (int(idle_img.get_width() * scale), 
                (int(idle_img.get_height() * scale))))
                
            assets["walk"] = pygame.transform.scale(walk_img,
                (int(walk_img.get_width() * scale),
                (int(walk_img.get_height() * scale))))
        
        else:  # worm
            # Same pattern for worm
            idle_img = pygame.image.load(os.path.join("assets", "enemy", "wormGreen_idle.png"))
            walk_img = pygame.image.load(os.path.join("assets", "enemy", "wormGreen_walk.png"))
            
            assets["idle"] = pygame.transform.scale(idle_img,
                (int(idle_img.get_width() * scale),
                (int(idle_img.get_height() * scale))))
                
            assets["walk"] = pygame.transform.scale(walk_img,
                (int(walk_img.get_width() * scale),
                (int(walk_img.get_height() * scale))))
        
        return assets

    def patrol(self):
        # Move in current direction
        self.x_vel = self.speed * self.direction
        
        # Reverse direction if reached patrol boundary
        if abs(self.rect.x - self.start_x) >= self.patrol_distance:
            self.direction *= -1
            self.start_x = self.rect.x

    def apply_gravity(self):
        """Apply gravity with proper ground detection"""
        if not self.grounded:
            self.y_vel += self.gravity
        else:
            # When grounded, snap to position and reset velocity
            self.y_vel = min(0, self.y_vel)  # Prevent sinking
            self.rect.y = int(self.rect.y)  # Ensure pixel-perfect alignment

    def update_sprite(self):
        # Slow animation by only updating every N frames
        if self.animation_count % self.animation_delay == 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        
        self.state = self.frames[self.current_frame]
        self.image = self.assets[self.state]
        
        if self.direction < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        
        self.animation_count += 1
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, tiles):
        self.patrol()
        
        self.apply_gravity()
        
        # Apply movement
        self.handle_collisions(tiles)
        
        self.update_sprite()

    def handle_collisions(self, tiles):
        # Horizontal collisions
        self.rect.x += self.x_vel
        for tile in tiles:
            if pygame.sprite.collide_mask(self, tile):
                if hasattr(tile, 'name') and tile.name == "solid":
                    if self.x_vel > 0:
                        self.rect.right = tile.rect.left
                        self.direction = -1
                    elif self.x_vel < 0:
                        self.rect.left = tile.rect.right
                        self.direction = 1
                    self.start_x = self.rect.x
                elif hasattr(tile, 'name') and tile.name == "danger":
                    print("Enemy damaged!")

        # Vertical collisions
        self.rect.y += self.y_vel
        for tile in tiles:
            if pygame.sprite.collide_mask(self, tile):
                if hasattr(tile, 'name') and tile.name == "solid":
                    if self.y_vel > 0:
                        self.rect.bottom = tile.rect.top
                        self.y_vel = 0
                    elif self.y_vel < 0:
                        self.rect.top = tile.rect.bottom
                        self.y_vel = 0

    def draw(self, surface, offset_x, offset_y):
        surface.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))