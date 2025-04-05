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
        self.level_data = []
        self.width = 0
        self.height = 0
        self._load_csv_level(csv_file)

    def _load_csv_level(self, filename):
        filepath = os.path.join(Config.LEVELS_PATH, filename)
        
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