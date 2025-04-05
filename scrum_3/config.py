import os
import pygame
import random


class Config:
    # Window
    WIDTH, HEIGHT = 1280, 720
    FPS = 60
    TILE_SIZE = 128
    
    # Physics
    GRAVITY = 3.2
    PLAYER_SPEED = 20
    JUMP_FORCE = -60
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSETS_PATH = os.path.join(BASE_DIR, 'assets')
    LEVELS_PATH = os.path.join(os.path.dirname(__file__), 'levels')
    TILES_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'textures', 'tiles')
    
    # Colors
    BACKGROUND = (30, 30, 40)
    
    @staticmethod
    def load_image(path):
        return pygame.image.load(os.path.join(Config.ASSETS_PATH, 'textures', path)).convert_alpha()
    
    TILE_MAPPING = {
        -1: None,       
        0: "0.png",
        1: "1.png",
        2: "2.png",
        3: "3.png",
        4: "4.png",
        5: "5.png",
        6: "6.png",
        7: "7.png",
        8: "8.png",
        9: "9.png",
        10: "10.png",
        11: "11.png",
        12: "12.png",
        13: "13.png",
        14: "14.png",
        15: "15.png",
        16: "16.png",  
        17: "17.png"  
    }