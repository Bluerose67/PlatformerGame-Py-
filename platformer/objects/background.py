import pygame
import os
from config import WIDTH, HEIGHT, BG_SCALE_FACTOR

class Background:
    def __init__(self):
        self.layers = []
        path = os.path.join("assets", "background", "blue_grass.png")
        image = pygame.image.load(path).convert_alpha()
        
        # Scale to match game's visual比例
        scaled_width = int(image.get_width() * BG_SCALE_FACTOR)
        scaled_height = int(image.get_height() * BG_SCALE_FACTOR)
        scaled_image = pygame.transform.smoothscale(image, (scaled_width, scaled_height))
        
        self.layers.append({
            "image": scaled_image,
            "speed": 0.2,  # Parallax scroll speed
            "size": (scaled_width, scaled_height)
        })

    def draw(self, surface, camera_offset):
        screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        
        for layer in self.layers:
            img = layer["image"]
            img_w, img_h = layer["size"]
            speed = layer["speed"]
            
            # Calculate parallax offset
            offset_x = -camera_offset[0] * speed
            offset_y = -camera_offset[1] * speed
            
            # Calculate tiling needs
            tiles_x = (WIDTH // img_w) + 2
            tiles_y = (HEIGHT // img_h) + 2
            
            # Draw repeating background
            for x in range(tiles_x):
                for y in range(tiles_y):
                    pos = (
                        offset_x + (x * img_w),
                        offset_y + (y * img_h)
                    )
                    if screen_rect.colliderect(pygame.Rect(pos, (img_w, img_h))):
                        surface.blit(img, pos)