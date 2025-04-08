import pygame
import os

class UI:
    def __init__(self):
        self.hearts = 3
        self.heart_img = pygame.image.load(
            os.path.join("assets", "ui", "heart.png")).convert_alpha()
        self.heart_img = pygame.transform.scale(self.heart_img, (32, 32))

    def draw(self, surface):
        for i in range(self.hearts):
            surface.blit(self.heart_img, (10 + i * 35, 10))