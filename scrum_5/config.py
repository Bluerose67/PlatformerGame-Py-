import os

# Game Settings
FPS = 60
WIDTH, HEIGHT = 1280, 720
PLAYER_VEL = 8
GRAVITY = 1
TILE_SIZE = 128
ANIMATION_DELAY = 3
SCALE_FACTOR = 0.5  # Adjust this to control zoom (0.5 = 50% size)
SCALED_TILE = int(TILE_SIZE * SCALE_FACTOR)
BG_SCALE_FACTOR = 0.7  # Adjust this to control background zoom

PLAYER_HEALTH = 3
ENEMY_SPEED = 2
SOUND_VOLUME = 0.5
PLAYER_MAX_HEALTH = 3
INVINCIBILITY_DURATION = 3000  # 3 seconds in milliseconds
ENEMY_DAMAGE_COOLDOWN = 1000  # 1 second between damage


# Path Configuration
ASSETS_DIR = os.path.join("assets")
LEVELS_DIR = os.path.join("levels")

# Tile Properties
SOLID_TILES = {0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 16}
DANGER_TILES = {}

# Calculate level dimensions based on CSV
LEVEL_WIDTH = 30 * TILE_SIZE  # 30 columns in CSV
LEVEL_HEIGHT = 20 * TILE_SIZE  # 20 rows in CSV

BG_LAYERS = [
    {"path": "blue_grass.png", "speed": 0.2},
]

# Lets Add these color constants for menu
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
HIGHLIGHT = (255, 215, 0)  # Gold color for selection

