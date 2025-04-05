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
        target_center = target.rect.center
        camera_center = self.offset + pygame.Vector2(Config.WIDTH//2, Config.HEIGHT//2)
        
        if not self.deadzone.collidepoint(target_center):
            offset = pygame.Vector2(target_center) - camera_center
            self.offset += offset * 0.05
        
        self.offset.x = max(min(0, self.offset.x), Config.WIDTH - self.level_width)
        self.offset.y = max(min(0, self.offset.y), Config.HEIGHT - self.level_height)