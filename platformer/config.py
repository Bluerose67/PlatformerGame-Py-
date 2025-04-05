import os

# Game Settings
FPS = 60
WIDTH, HEIGHT = 1280, 720
PLAYER_VEL = 8
GRAVITY = 0.8
TILE_SIZE = 128
ANIMATION_DELAY = 3
SCALE_FACTOR = 0.5  # Adjust this to control zoom (0.5 = 50% size)
SCALED_TILE = int(TILE_SIZE * SCALE_FACTOR)
# Calculate level dimensions based on CSV
LEVEL_WIDTH = 30 * TILE_SIZE  # 30 columns in CSV
LEVEL_HEIGHT = 20 * TILE_SIZE  # 20 rows in CSV

# Path Configuration
ASSETS_DIR = os.path.join("assets")
LEVELS_DIR = os.path.join("levels")

# Background Settings
BG_LAYERS = [
    {"path": "blue_grass.png", "speed": 0.2},
    {"path": "colored_grass.png", "speed": 0.5}
]

# Tile Properties
SOLID_TILES = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12}
DANGER_TILES = {}