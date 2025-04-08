import pygame
import os
from config import PLAYER_HEALTH

class UI:
    def __init__(self):
        self.heart_img = pygame.image.load(
            os.path.join("assets", "ui", "heart.png")).convert_alpha()
        self.heart_img = pygame.transform.scale(self.heart_img, (32, 32))
        self.hearts = PLAYER_HEALTH

    def draw(self, surface):
        for i in range(self.hearts):
            surface.blit(self.heart_img, (10 + i * 35, 10))

    def take_damage(self):
        if self.hearts > 0:
            self.hearts -= 1
        return self.hearts <= 0