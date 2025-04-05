import pygame
import os
from config import WIDTH, HEIGHT, BG_LAYERS, SCALE_FACTOR

class Background:
    def __init__(self):
        self.layers = []
        self.bg_width = 0
        self.bg_height = 0
        
        for layer in BG_LAYERS:
            path = os.path.join("assets", "background", layer["path"])
            image = pygame.image.load(path).convert_alpha()
            scaled_image = pygame.transform.scale(image, 
                (int(image.get_width() * SCALE_FACTOR), 
                 int(image.get_height() * SCALE_FACTOR)))
            self.layers.append({
                "image": scaled_image,
                "speed": layer["speed"],
                "pos": [0, 0]
            })
            
        # Calculate repeating needs
        self.bg_width = self.layers[0]["image"].get_width()
        self.bg_height = self.layers[0]["image"].get_height()
        self.tiles_x = WIDTH // self.bg_width + 2
        self.tiles_y = HEIGHT // self.bg_height + 2

    def draw(self, surface, offset):
        for layer in self.layers:
            # Calculate parallax offset
            parallax_offset_x = offset[0] * layer["speed"]
            parallax_offset_y = offset[1] * layer["speed"]
            
            # Calculate starting positions
            start_x = -(parallax_offset_x % self.bg_width)
            start_y = -(parallax_offset_y % self.bg_height)
            
            # Draw tiled background
            for x in range(self.tiles_x):
                for y in range(self.tiles_y):
                    pos = (start_x + x * self.bg_width,
                           start_y + y * self.bg_height)
                    surface.blit(layer["image"], pos)