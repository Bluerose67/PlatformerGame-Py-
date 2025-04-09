import pygame
import os
from config import TILE_SIZE, GRAVITY, ANIMATION_DELAY, SCALED_TILE, SCALE_FACTOR

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game=None):
        super().__init__()
        self.assets = self.load_assets()
        self.image = self.assets["stand"]  # Initialize with standing image
        self.rect = pygame.Rect(x * SCALE_FACTOR, y * SCALE_FACTOR, SCALED_TILE, SCALED_TILE)
        self.mask = pygame.mask.from_surface(self.image)  # Initialize mask
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "right"
        self.animation_count = 0
        self.jump_count = 0
        self.state = "idle"
        self.GRAVITY = GRAVITY
        self.game = game
        self.invincible = False
        self.invincible_duration = 3000  # 3 seconds in milliseconds
        self.invincible_start = 0
        self.blink_interval = 100  # milliseconds between blinks
        self.visible = True  # For blinking effect
        


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
        
        # Update image and mask
        self.image = pygame.transform.flip(self.assets[self.state], 
                                         self.direction == "left", False)
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self):
        # Handle invincibility and blinking
        if self.invincible:
            current_time = pygame.time.get_ticks()
            # Calculate time since damage was taken
            time_since_damage = current_time - self.invincible_start
            
            # Toggle visibility every blink_interval milliseconds
            self.visible = (time_since_damage // self.blink_interval) % 2 == 0
            
            # End invincibility after duration
            if time_since_damage >= self.invincible_duration:
                self.invincible = False
                self.visible = True

    def take_damage(self):
        if not self.invincible:
            self.invincible = True
            self.invincible_start = pygame.time.get_ticks()
            self.visible = True  # Start visible then begin blinking
            return True
        return False

    def draw(self, surface, offset_x, offset_y):
        if self.visible:
            surface.blit(self.image, 
                        (self.rect.x - offset_x, 
                         self.rect.y - offset_y))