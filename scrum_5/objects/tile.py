import pygame
import os
from config import TILE_SIZE, SOLID_TILES, DANGER_TILES, SCALE_FACTOR, SCALED_TILE

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_id):
        super().__init__()
        self.tile_id = tile_id
        self.original_image = self.load_tile_image()
        self.image = pygame.transform.scale(self.original_image, 
                                           (SCALED_TILE, SCALED_TILE))
        self.rect = self.image.get_rect(topleft=(x * SCALE_FACTOR, y * SCALE_FACTOR))
        self.mask = pygame.mask.from_surface(self.image)
        self.name = "danger" if tile_id in DANGER_TILES else "solid" if tile_id in SOLID_TILES else "background"

    def load_tile_image(self):
        path = os.path.join("assets", "tiles", f"{self.tile_id}.png")
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

    def draw(self, surface, offset_x, offset_y):
        surface.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))