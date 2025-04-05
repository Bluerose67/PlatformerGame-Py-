import pygame
from config import Config

class Camera:
    def __init__(self, level_width, level_height):
        self.offset = pygame.Vector2(0, 0)
        self.level_width = level_width
        self.level_height = level_height
        self.deadzone = pygame.Rect(
            Config.WIDTH//2 - 300,
            Config.HEIGHT//2 - 200,
            600,
            400
        )

    def update(self, target):

        if target is None:  
            return
        
        # Smooth camera follow logic
        target_x = -target.rect.centerx + Config.WIDTH/2
        target_y = -target.rect.centery + Config.HEIGHT/2
        
        # Apply smoothing
        self.offset.x += (target_x - self.offset.x) * 0.1
        self.offset.y += (target_y - self.offset.y) * 0.1