import pygame
from config import WIDTH, HEIGHT

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 48)
        self.selected = 0
        self.options = ["Play", "Quit"]
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill((30, 30, 60))  # Dark blue background
        
    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw title
        title = self.font_large.render("Platform Adventure", True, (255, 255, 255))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        # Draw options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font_small.render(option, True, color)
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, 250 + i * 60))
            
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_DOWN] and not self.key_down:
            self.selected = (self.selected + 1) % len(self.options)
            self.key_down = True
        elif keys[pygame.K_UP] and not self.key_down:
            self.selected = (self.selected - 1) % len(self.options)
            self.key_down = True
        elif not (keys[pygame.K_DOWN] or keys[pygame.K_UP]):
            self.key_down = False
            
        if keys[pygame.K_RETURN]:
            return self.options[self.selected]
        return None