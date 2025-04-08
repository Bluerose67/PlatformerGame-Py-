import pygame
import os
from config import ENEMY_SPEED, GRAVITY, TILE_SIZE, ANIMATION_DELAY

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type="slime"):
        super().__init__()
        self.enemy_type = enemy_type
        self.assets = self.load_assets()
        self.rect = pygame.Rect(x, y, TILE_SIZE//2, TILE_SIZE//2)  # Smaller hitbox
        self.x_vel = 0
        self.y_vel = 0
        self.direction = 1  # 1=right, -1=left
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

    def patrol(self, tiles):
        if self.grounded:
            self.stable_frames += 1
            # Only move after being stable for a few frames
            if self.stable_frames > 5:
                self.x_vel = ENEMY_SPEED * self.direction
                
                # Edge detection
                edge_check = pygame.Rect(
                    self.rect.x + (self.direction * 20),
                    self.rect.bottom + 1,
                    10, 2
                )
                
                has_ground = False
                for tile in tiles:
                    if edge_check.colliderect(tile.rect):
                        has_ground = True
                        break
                
                if not has_ground:
                    self.direction *= -1
                    self.x_vel = ENEMY_SPEED * self.direction
        else:
            self.x_vel = 0  # Stop horizontal movement in air

    def apply_gravity(self):
        if not self.grounded:
            self.y_vel += self.gravity
        else:
            self.y_vel = 0  # Reset gravity when grounded

    def apply_gravity(self):
        if not self.grounded:
            self.y_vel += self.gravity
        else:
            self.y_vel = 0  # Reset when grounded
            # Ensure we stay snapped to ground
            self.rect.y = int(self.rect.y)

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
        self.patrol(tiles)
        
        # Apply gravity only if not grounded
        if not self.grounded:
            self.y_vel += self.gravity
        else:
            self.y_vel = 0
            # Snap to ground position
            self.rect.bottom = self.last_grounded_y
        
        # Apply movement
        self.handle_collisions(tiles, self.x_vel, self.y_vel)
        
        self.update_sprite()

    def handle_collisions(self, tiles, dx, dy):
        self.grounded = False
        
        # Check horizontal collisions first if moving
        if dx != 0:
            self.rect.x += dx
            for tile in tiles:
                if pygame.sprite.collide_rect(self, tile):
                    if dx > 0:
                        self.rect.right = tile.rect.left
                    else:
                        self.rect.left = tile.rect.right
                    self.direction *= -1  # Reverse direction on collision
                    self.x_vel = ENEMY_SPEED * self.direction
            self.rect.x = int(self.rect.x)  # Snap to integer position

        # Then check vertical collisions
        if dy != 0:
            self.rect.y += dy
            for tile in tiles:
                if pygame.sprite.collide_rect(self, tile):
                    if dy > 0:  # Landing
                        self.rect.bottom = tile.rect.top
                        self.last_grounded_y = self.rect.bottom
                        self.grounded = True
                        self.stable_frames = 0
                    elif dy < 0:  # Hitting ceiling
                        self.rect.top = tile.rect.bottom
                    self.y_vel = 0
            self.rect.y = int(self.rect.y)  # Snap to integer position

    def draw(self, surface, offset_x, offset_y):
        surface.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
         # Draw hitbox border (RED)
        hitbox_rect = pygame.Rect(
            self.rect.x - offset_x,
            self.rect.y - offset_y,
            self.rect.width,
            self.rect.height
        )
        pygame.draw.rect(surface, (255, 0, 0), hitbox_rect, 1)  # 1px red border