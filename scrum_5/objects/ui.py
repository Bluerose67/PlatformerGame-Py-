import pygame
import os

class UI:
    def __init__(self):
        self.hearts = 3  # Starting with 3 lives
        self.heart_img = pygame.image.load(os.path.join("assets", "ui", "heart.png"))  # Load heart image
        self.heart_img = pygame.transform.scale(self.heart_img, (30, 30))  # Resize if needed

    def take_damage(self):
        if self.hearts > 0:
            self.hearts -= 1
            return True
        return False

    def draw(self, screen):
        # Draw hearts in top-left corner
        for i in range(self.hearts):
            screen.blit(self.heart_img, (10 + i * 35, 10))
    
    def reset(self):
        self.hearts = 3