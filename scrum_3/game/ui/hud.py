import pygame
import os
from config import Config

class HUD:
    def __init__(self, player):
        self.player = player
        # Initialize with safe defaults
        self.font = pygame.font.Font(None, 36)
        self.heart_img = Config.load_image("ui/heart.png") if self.player else None

    def draw(self, screen):
        if not self.player:
            return
        self._draw_health(screen)
        self._draw_score(screen)

    def _draw_health(self, screen):
        if not hasattr(self.player, 'health'):
            return
            
        try:
            for i in range(self.player.health):
                pos = (10 + i * 40, 10)
                screen.blit(self.heart_img, pos)
        except Exception as e:
            print(f"Error drawing health: {e}")