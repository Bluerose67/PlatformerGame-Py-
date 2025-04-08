import pygame
from config import WIDTH, HEIGHT, WHITE, BLACK, GRAY, HIGHLIGHT

class Menu:
    def __init__(self):
        self.font_large = pygame.font.SysFont("Arial", 72)
        self.font_medium = pygame.font.SysFont("Arial", 48)
        self.selected = 0  # 0 = Play, 1 = Quit
        self.options = ["Play", "Quit"]
        
    def draw(self, surface):
        # Draw background
        surface.fill(BLACK)
        
        # Draw title
        title = self.font_large.render("PLATFORMER", True, WHITE)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        
        # Draw menu options
        for i, option in enumerate(self.options):
            color = HIGHLIGHT if i == self.selected else WHITE
            text = self.font_medium.render(option, True, color)
            surface.blit(text, (WIDTH//2 - text.get_width()//2, 300 + i*80))
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_DOWN] and self.selected < len(self.options)-1:
            self.selected += 1
        elif keys[pygame.K_UP] and self.selected > 0:
            self.selected -= 1
            
        if keys[pygame.K_RETURN]:
            return self.options[self.selected]
        return None