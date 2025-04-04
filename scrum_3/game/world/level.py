import os 
import pygame
from game.world.tile import Tile
from game.entities.player import Player
from game.entities.enemy import Enemy
from config import Config


class Level:
    def __init__(self, filename):
        self.tiles = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self._load_level(filename)
        self.width = len(self.level_data[0]) * Config.TILE_SIZE
        self.height = len(self.level_data) * Config.TILE_SIZE

    def _load_level(self, filename):
        filepath = os.path.join(Config.LEVELS_PATH, filename)
        with open(filepath) as f:
            self.level_data = [line.strip() for line in f]
        
        for y, row in enumerate(self.level_data):
            for x, cell in enumerate(row):
                pos = (x * Config.TILE_SIZE, y * Config.TILE_SIZE)
                if cell == 'X':
                    self.tiles.add(Tile(pos))
                elif cell == 'P':
                    self.player = Player(pos)
                    self.entities.add(self.player)
                elif cell == 'E':
                    self.entities.add(Enemy(pos))