import pygame
from config import Config

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, tile_type="ground"):
        super().__init__()
        self._load_assets(tile_type)
        self.rect = self.image.get_rect(topleft=pos)
    
    def _load_assets(self, tile_type):
        """Load different tile types from assets"""
        try:
            self.image = Config.load_image(f"tiles/{tile_type}.png")
        except FileNotFoundError:
            # Fallback to colored blocks
            self.image = pygame.Surface((Config.TILE_SIZE, Config.TILE_SIZE))
            colors = {
                "ground": (34, 139, 34),   # Forest green
                "platform": (139, 69, 19), # Brown
                "danger": (255, 0, 0)      # Red
            }
            self.image.fill(colors.get(tile_type, (0, 255, 0)))