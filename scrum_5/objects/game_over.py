import pygame
from config import WIDTH, HEIGHT

class GameOver:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 36)
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill((60, 30, 30))  # Dark red background
        
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        title = self.font_large.render("Game Over", True, (255, 255, 255))
        prompt = self.font_small.render("Press ENTER to return to menu", True, (200, 200, 200))
        
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 50))
        self.screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 + 50))
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        return keys[pygame.K_RETURN]