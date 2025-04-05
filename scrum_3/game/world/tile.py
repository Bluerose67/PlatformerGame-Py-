import os
import pygame
import csv
from config import Config

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, tile_id):
        super().__init__()
        self.tile_id = tile_id
        self.image = self._load_tile_image()
        self.rect = self.image.get_rect(topleft=pos) if self.image else None

    def _load_tile_image(self):
        if self.tile_id in Config.TILE_MAPPING and Config.TILE_MAPPING[self.tile_id]:
            try:
                return pygame.image.load(
                    os.path.join(Config.TILES_PATH, Config.TILE_MAPPING[self.tile_id])
                ).convert_alpha()
            except FileNotFoundError:
                print(f"Missing tile image: {Config.TILE_MAPPING[self.tile_id]}")
        return None