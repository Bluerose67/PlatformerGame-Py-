import csv
import pygame
import os
from config import Config
from .tile import Tile
from ..entities.player import Player
from ..entities.enemy import Enemy

class Level:
    def __init__(self, csv_file):
        self.tiles = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.player = None
        self.level_data = []
        self._load_csv_level(csv_file)

    def _load_csv_level(self, filename):
        filepath = os.path.join(Config.LEVELS_PATH, filename)
        print(f"Loading level: {filename}")

        
        with open(filepath, 'r') as file:
            csv_reader = csv.reader(file)
            self.level_data = [list(map(int, row)) for row in csv_reader]
            
            # Calculate dimensions
            if self.level_data:
                self.width = len(self.level_data[0]) * Config.TILE_SIZE
                self.height = len(self.level_data) * Config.TILE_SIZE

            for y, row in enumerate(self.level_data):
                for x, tile_id in enumerate(row):
                    self._process_tile(x, y, tile_id)
        print(f"Loaded {len(self.tiles)} tiles")
        print(f"Loaded {len(self.entities)} entities")
        print(f"Level dimensions: {self.width}x{self.height}")

    def _process_tile(self, x, y, tile_id):
        pos = (x * Config.TILE_SIZE, y * Config.TILE_SIZE)
        
        # Debug print
        print(f"Processing tile at ({x},{y}) - ID: {tile_id}")
        
        # Handle player spawn first
        if tile_id == 99:  # Player spawn ID
            print(f"Creating player at {pos}")
            self.player = Player(pos)
            self.entities.add(self.player)
            return
        
        # Handle enemy spawns
        if tile_id == 100:  # Slime
            self.entities.add(Enemy(pos, "slime"))
            return
        if tile_id == 101:  # Worm
            self.entities.add(Enemy(pos, "worm"))
            return
        
        # Handle regular tiles
        if tile_id in Config.TILE_MAPPING:
            print(f"Creating tile ID {tile_id} at {pos}")
            tile = Tile(pos, tile_id)
            if tile.image:
                self.tiles.add(tile)