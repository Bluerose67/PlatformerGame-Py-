import os
import pygame
import random


class Config:
    # Window
    WIDTH, HEIGHT = 1280, 720
    FPS = 60
    TILE_SIZE = 32
    
    # Physics
    GRAVITY = 0.8
    PLAYER_SPEED = 5
    JUMP_FORCE = -15
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSETS_PATH = os.path.join(BASE_DIR, 'assets')
    LEVELS_PATH = os.path.join(BASE_DIR, 'levels')
    
    # Colors
    BACKGROUND = (30, 30, 40)
    
    @staticmethod
    def load_image(path):
        return pygame.image.load(os.path.join(Config.ASSETS_PATH, 'textures', path)).convert_alpha()