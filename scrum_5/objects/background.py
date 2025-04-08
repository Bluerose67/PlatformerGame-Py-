import pygame
import os
from config import WIDTH, HEIGHT, BG_SCALE_FACTOR, BG_LAYERS

class Background:
    def __init__(self):
        self.layers = []
        self.bg_images = []
        
        # Load and scale background images
        for layer in BG_LAYERS:
            path = os.path.join("assets", "background", layer["path"])
            image = pygame.image.load(path).convert_alpha()
            
            # Calculate proportional scaling
            original_width, original_height = image.get_size()
            scaled_width = int(original_width * BG_SCALE_FACTOR)
            scaled_height = int(original_height * BG_SCALE_FACTOR)
            
            # Scale image while maintaining aspect ratio
            scaled_image = pygame.transform.smoothscale(image, (scaled_width, scaled_height))
            self.layers.append({
                "image": scaled_image,
                "speed": layer["speed"],
                "offset": [0, 0],
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
            
            # Calculate how many tiles we need
            tiles_x = (WIDTH // img_w) + 2
            tiles_y = (HEIGHT // img_h) + 2
            
            # Draw tiled background
            for x in range(tiles_x):
                for y in range(tiles_y):
                    pos = (
                        offset_x + (x * img_w),
                        offset_y + (y * img_h)
                    )
                    
                    # Only draw if visible in screen area
                    if screen_rect.colliderect(pygame.Rect(pos, (img_w, img_h))):
                        surface.blit(img, pos)