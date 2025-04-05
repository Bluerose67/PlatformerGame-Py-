import os
import pygame
import csv
from config import Config
from game.entities.player import Player

class Tile(pygame.sprite.Sprite):
    COLLISION_MAP = {
        0: {"type": "solid", "damage": 0},
        1: {"type": "solid", "damage": 0},
        2: {"type": "solid", "damage": 0},
        3: {"type": "solid", "damage": 0},
        4: {"type": "solid", "damage": 0},
        5: {"type": "solid", "damage": 0},
        6: {"type": "solid", "damage": 0},
        7: {"type": "solid", "damage": 0},
        8: {"type": "solid", "damage": 0},
        9: {"type": "solid", "damage": 0},
        10: {"type": "solid", "damage": 0},
        11: {"type": "solid", "damage": 0},
        12: {"type": "passable", "damage": 0},
        13: {"type": "solid", "damage": 0},
        14: {"type": "passable", "damage": 0},
        15: {"type": "passable", "damage": 0},
        16: {"type": "passable", "damage": 0},
        17: {"type": "passable", "damage": 0}
        # 15: "platform",
        # 17: "hazard"
    }

    def __init__(self, pos, tile_id):
        super().__init__()
        self.tile_id = tile_id
        self.collision_type = self.COLLISION_MAP.get(tile_id, {"type": "solid", "damage": 0})
        self.image = self._load_tile_image()
        self.rect = self.image.get_rect(topleft=pos) if self.image else None
    
    def is_solid(self):
        return self.collision_type in ["solid", "platform"]
    
    def handle_collision(self, entity):
        if self.collision["type"] == "hazard":
            Player.take_damage(self.collision["damage"])

    def _load_tile_image(self):
        if self.tile_id in Config.TILE_MAPPING and Config.TILE_MAPPING[self.tile_id]:
            try:
                return pygame.image.load(
                    os.path.join(Config.TILES_PATH, Config.TILE_MAPPING[self.tile_id])
                ).convert_alpha()
            except FileNotFoundError:
                print(f"Missing tile image: {Config.TILE_MAPPING[self.tile_id]}")
        return None