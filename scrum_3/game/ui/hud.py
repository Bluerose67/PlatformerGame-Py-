import pygame
import os
from config import Config

class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(
            os.path.join(Config.ASSETS_PATH, "fonts", "pixel_font.ttf"), 24
        )
        self.heart_img = Config.load_image("ui/heart.png")
        
    def draw(self, screen):
        self._draw_health(screen)
        self._draw_score(screen)
        
    def _draw_health(self, screen):
        heart_spacing = 40
        for i in range(self.player.health):
            pos = (10 + i * heart_spacing, 10)
            screen.blit(self.heart_img, pos)
            
    def _draw_score(self, screen):
        score_text = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        screen.blit(score_text, (Config.WIDTH - 200, 10))