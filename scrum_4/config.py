import os

# Game Settings
FPS = 60
WIDTH, HEIGHT = 1280, 720
PLAYER_VEL = 6
GRAVITY = 0.8
TILE_SIZE = 128
ANIMATION_DELAY = 3
PLAYER_HEALTH = 3
ENEMY_SPEED = 2
SOUND_VOLUME = 0.5
SCALE_FACTOR = 0.5  # Adjust this to control zoom (0.5 = 50% size)
# Add these background-specific settings
BG_SCALE_FACTOR = 0.7  # Adjust this to control background zoom
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
    
]

# Tile Properties
SOLID_TILES = {0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 16}
DANGER_TILES = {}

# Add these color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
HIGHLIGHT = (255, 215, 0)  # Gold color for selection

# # Add these camera parameters
# CAMERA_SMOOTHING_X = 0.1  # Horizontal follow speed (lower = smoother)
# CAMERA_SMOOTHING_Y = 0.3  # Vertical follow speed (should be faster than X)
# CAMERA_DEADZONE_X = 100   # Horizontal margin before camera moves
# CAMERA_DEADZONE_Y = 50    # Vertical margin before camera moves

# # Camera Settings
# CAMERA_SMOOTHING = 0.1  # Lower = smoother
# PLAYER_SCREEN_X = WIDTH // 2  # Player stays horizontally centered
# PLAYER_SCREEN_Y = HEIGHT // 2  # Vertical center position